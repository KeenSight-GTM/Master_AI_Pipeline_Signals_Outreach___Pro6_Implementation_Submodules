from __future__ import annotations

import hashlib
import os
import sqlite3
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Iterable
from .core import Capture, Match, Observation, SupportLink, ContractError, canonical, strict_json, identity, instant


class Store:
    """Single-machine SQLite + private content store. Not a hosted auth service."""
    def __init__(self, directory: str | Path):
        self.root=Path(directory)
        self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
        self.db=sqlite3.connect(self.root/'scanner.sqlite3',timeout=30)
        self.db.row_factory=sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS runs(tenant TEXT NOT NULL, run_id TEXT NOT NULL, config_hash TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(tenant,run_id));
        CREATE TABLE IF NOT EXISTS attempts(tenant TEXT NOT NULL, run_id TEXT NOT NULL, request_key TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL,
          PRIMARY KEY(tenant,run_id,request_key), FOREIGN KEY(tenant,run_id) REFERENCES runs(tenant,run_id));
        CREATE TABLE IF NOT EXISTS captures(tenant TEXT NOT NULL,id TEXT NOT NULL,run_id TEXT NOT NULL,payload TEXT NOT NULL,
          PRIMARY KEY(tenant,id),FOREIGN KEY(tenant,run_id) REFERENCES runs(tenant,run_id));
        CREATE TABLE IF NOT EXISTS matches(tenant TEXT NOT NULL,id TEXT NOT NULL,capture_id TEXT NOT NULL,payload TEXT NOT NULL,
          PRIMARY KEY(tenant,id),FOREIGN KEY(tenant,capture_id) REFERENCES captures(tenant,id));
        CREATE TABLE IF NOT EXISTS observations(tenant TEXT NOT NULL,id TEXT NOT NULL,capture_id TEXT NOT NULL,claim_key TEXT NOT NULL,payload TEXT NOT NULL,
          PRIMARY KEY(tenant,id),FOREIGN KEY(tenant,capture_id) REFERENCES captures(tenant,id));
        CREATE TABLE IF NOT EXISTS support(tenant TEXT NOT NULL,observation_id TEXT NOT NULL,match_id TEXT NOT NULL,
          PRIMARY KEY(tenant,observation_id,match_id),FOREIGN KEY(tenant,observation_id) REFERENCES observations(tenant,id),FOREIGN KEY(tenant,match_id) REFERENCES matches(tenant,id));
        CREATE TABLE IF NOT EXISTS revoked_captures(tenant TEXT NOT NULL,capture_id TEXT NOT NULL,reason TEXT NOT NULL,
          PRIMARY KEY(tenant,capture_id),FOREIGN KEY(tenant,capture_id) REFERENCES captures(tenant,id));
        CREATE TABLE IF NOT EXISTS feature_occurrences(tenant TEXT NOT NULL,feature_id TEXT NOT NULL,origin TEXT NOT NULL,capture_id TEXT NOT NULL,value TEXT NOT NULL,
          PRIMARY KEY(tenant,feature_id,origin,capture_id),FOREIGN KEY(tenant,capture_id) REFERENCES captures(tenant,id));
        ''')
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS evaluations(
          tenant TEXT NOT NULL, evaluation_key TEXT NOT NULL, payload TEXT NOT NULL,
          PRIMARY KEY(tenant,evaluation_key));
        CREATE TABLE IF NOT EXISTS replay_selection(
          tenant TEXT NOT NULL, capture_id TEXT NOT NULL, eligible INTEGER NOT NULL,
          PRIMARY KEY(tenant,capture_id),
          FOREIGN KEY(tenant,capture_id) REFERENCES captures(tenant,id));
        CREATE TABLE IF NOT EXISTS cooldowns(
          tenant TEXT NOT NULL, origin TEXT NOT NULL, until_utc TEXT NOT NULL,
          PRIMARY KEY(tenant,origin));
        """)
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS feature_states(
          tenant TEXT NOT NULL, feature_id TEXT NOT NULL, capture_id TEXT NOT NULL,
          release_digest TEXT NOT NULL, matched INTEGER NOT NULL,
          PRIMARY KEY(tenant,feature_id,capture_id,release_digest));
        CREATE TABLE IF NOT EXISTS capture_releases(
          tenant TEXT NOT NULL,capture_id TEXT NOT NULL,release_digest TEXT NOT NULL,
          PRIMARY KEY(tenant,capture_id));
        """)
        self.db.commit()
        try: os.chmod(self.root/'scanner.sqlite3',0o600)
        except OSError: pass

    def close(self):
        self.db.close()

    def begin_run(self, tenant: str, run_id: str, config: dict):
        if not tenant or not run_id:
            raise ContractError('Tenant and run ID are required')
        config={k:v for k,v in config.items() if k!='retry_failed'}
        payload=canonical(config); digest=identity('runconfig',config)
        with self.db:
            row=self.db.execute('SELECT config_hash FROM runs WHERE tenant=? AND run_id=?',(tenant,run_id)).fetchone()
            if row and row['config_hash']!=digest:
                raise ContractError('Run ID reuse with changed configuration or release; use a new run or replay')
            self.db.execute('INSERT OR IGNORE INTO runs VALUES(?,?,?,?)',(tenant,run_id,digest,payload))

    def reserve_attempt(self, tenant: str, run_id: str, request_key: str, budget: int,
                        payload: dict, *, retry_failed: bool=False, retry_limit: int=1) -> dict:
        """Reserve GET attempts atomically. Retries retain and link the original.

        PENDING means uncertain process interruption and is never retried here.
        This operation does not authorize retries of sends or non-idempotent APIs.
        """
        self.db.execute('BEGIN IMMEDIATE')
        try:
            original=request_key; retry_of=None; ordinal=0
            while True:
                row=self.db.execute('SELECT status,payload FROM attempts WHERE tenant=? AND run_id=? AND request_key=?',
                                    (tenant,run_id,request_key)).fetchone()
                if not row: break
                previous=strict_json(row['payload'])
                retryable=row['status']=='FAILED' or previous.get('http_status') in {429,500,502,503,504}
                if not retry_failed or not retryable or ordinal>=retry_limit:
                    self.db.commit()
                    return {'new':False,'status':row['status'],'payload':previous,'request_key':request_key}
                retry_of=request_key; ordinal+=1
                request_key=identity('retry',original,ordinal)
            count=self.db.execute('SELECT COUNT(*) FROM attempts WHERE tenant=? AND run_id=?',(tenant,run_id)).fetchone()[0]
            if count>=budget:
                self.db.commit(); return {'new':False,'status':'SKIPPED_BUDGET','payload':{},'request_key':request_key}
            payload={**payload,'request_key':request_key,'retry_of':retry_of,'attempt_ordinal':ordinal+1}
            self.db.execute('INSERT INTO attempts VALUES(?,?,?,?,?)',(tenant,run_id,request_key,'PENDING',canonical(payload)))
            self.db.commit()
            return {'new':True,'status':'PENDING','payload':payload,'request_key':request_key}
        except Exception:
            self.db.rollback(); raise

    def finish_attempt(self, tenant: str, run_id: str, key: str, status: str, payload: dict):
        if status not in {'COMPLETE','FAILED'}:
            raise ContractError('Invalid terminal attempt status')
        with self.db:
            row=self.db.execute('SELECT status,payload FROM attempts WHERE tenant=? AND run_id=? AND request_key=?',
                                (tenant,run_id,key)).fetchone()
            if not row: raise ContractError('Attempt was not reserved')
            original=strict_json(row['payload'])
            immutable={'url','command_id','mode','started_at','request_key','retry_of','attempt_ordinal'}
            if any(k in original and k in payload and original[k]!=payload[k] for k in immutable):
                raise ContractError('Attempt request metadata cannot be rewritten')
            combined={**original,**payload}
            if combined.get('started_at') and combined.get('finished_at'):
                if instant(combined['finished_at'])<instant(combined['started_at']):
                    raise ContractError('Attempt finished before it started')
            if row['status']!='PENDING':
                if row['status']!=status or row['payload']!=canonical(combined):
                    raise ContractError('Terminal attempt cannot be rewritten')
                return
            self.db.execute('UPDATE attempts SET status=?,payload=? WHERE tenant=? AND run_id=? AND request_key=?',
                            (status,canonical(combined),tenant,run_id,key))

    def put_capture(self, *, tenant_id: str,subject_id: str,run_id: str,url: str,observed_at: str,body: bytes,
                    headers: dict[str,str],status_code: int=200,mode: str='RAW_HTML',complete: bool=True,limitations=(),source_ttl_seconds=2592000,source_id='source:public-website') -> Capture:
        instant(observed_at)
        if mode not in {'RAW_HTML','RENDERED_DOM'} or not subject_id:
            raise ContractError('Invalid capture mode or subject')
        existing=self.db.execute('SELECT payload FROM captures WHERE tenant=? AND run_id=? LIMIT 1',
                                 (tenant_id,run_id)).fetchone()
        if existing and strict_json(existing['payload'])['subject_id']!=subject_id:
            raise ContractError('Capture run cannot change subject identity')
        digest=hashlib.sha256(body).hexdigest()
        # Content dedup is tenant-scoped; capture identity is not a content hash.
        relative=Path('blobs')/identity('tenant',tenant_id)/digest[:2]/digest
        dest=self.root/relative; dest.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        if dest.exists():
            if hashlib.sha256(dest.read_bytes()).hexdigest()!=digest:
                raise ContractError('Corrupt existing blob')
        else:
            fd,tmp=tempfile.mkstemp(dir=dest.parent)
            try:
                with os.fdopen(fd,'wb') as stream:
                    stream.write(body); stream.flush(); os.fsync(stream.fileno())
                os.replace(tmp,dest)
            finally:
                if os.path.exists(tmp): os.unlink(tmp)
        cid=identity('capture',tenant_id,subject_id,run_id,url,observed_at,mode)
        cap=Capture(cid,tenant_id,subject_id,run_id,url,observed_at,mode,status_code,digest,str(relative),headers,complete,
                    source_id=source_id,limitations=tuple(limitations),source_ttl_seconds=source_ttl_seconds)
        with self.db:
            self._immutable('captures',tenant_id,cid,asdict(cap),('run_id',),(run_id,))
        return cap

    def _immutable(self, table: str, tenant: str, key: str, payload: dict, extra_names=(),extra_values=()):
        # Table and column names are internal constants, never user input.
        assert table in {'captures','matches','observations'}
        serialized=canonical(payload)
        row=self.db.execute(f'SELECT payload FROM {table} WHERE tenant=? AND id=?',(tenant,key)).fetchone()
        if row and row['payload']!=serialized:
            raise ContractError(f'{table}: same identity with different content')
        columns=['tenant','id',*extra_names,'payload']
        self.db.execute(f'INSERT OR IGNORE INTO {table} ({",".join(columns)}) VALUES ({",".join("?" for _ in columns)})',
                        (tenant,key,*extra_values,serialized))

    def body(self, cap: Capture) -> bytes:
        row = self.db.execute('SELECT payload FROM captures WHERE tenant=? AND id=?',
                              (cap.tenant_id, cap.capture_id)).fetchone()
        if row is None or row['payload'] != canonical(asdict(cap)):
            raise ContractError('Capture metadata differs from its authoritative stored record')
        if self.db.execute('SELECT 1 FROM revoked_captures WHERE tenant=? AND capture_id=?',(cap.tenant_id,cap.capture_id)).fetchone():
            raise ContractError('Capture is revoked')
        expected=Path('blobs')/identity('tenant',cap.tenant_id)/cap.body_sha256[:2]/cap.body_sha256
        if str(expected)!=cap.body_path:
            raise ContractError('Blob path does not match tenant and digest')
        body=(self.root/expected).read_bytes()
        if hashlib.sha256(body).hexdigest()!=cap.body_sha256:
            raise ContractError('Evidence hash mismatch')
        return body

    def save_findings(self, tenant: str, matches: list[Match], observations: list[Observation], links: list[SupportLink], *, transaction_owned=False):
        from .claims import resolve_claims
        capids={m.capture_id for m in matches}|{o.capture_id for o in observations}
        caps=[]
        for cid in capids:
            row=self.db.execute('SELECT payload FROM captures WHERE tenant=? AND id=?',(tenant,cid)).fetchone()
            if not row: raise ContractError('Unknown or cross-tenant capture')
            caps.append(Capture(**strict_json(row['payload'])))
        if any(o.tenant_id!=tenant for o in observations): raise ContractError('Cross-tenant observation')
        if observations:
            resolve_claims(observations,matches,links,caps,as_of=max(o.observed_at for o in observations))
        from contextlib import nullcontext
        with (nullcontext() if transaction_owned else self.db):
            for m in matches: self._immutable('matches',tenant,m.match_id,asdict(m),('capture_id',),(m.capture_id,))
            for o in observations: self._immutable('observations',tenant,o.observation_id,asdict(o),('capture_id','claim_key'),(o.capture_id,o.claim_key))
            for link in links:
                self.db.execute('INSERT OR IGNORE INTO support VALUES(?,?,?)',(tenant,link.observation_id,link.match_id))

    def captures(self,tenant: str, run_id: str | None=None) -> list[Capture]:
        query='SELECT payload FROM captures WHERE tenant=?'; params=[tenant]
        if run_id is not None: query+=' AND run_id=?'; params.append(run_id)
        return [Capture(**strict_json(r['payload'])) for r in self.db.execute(query+' ORDER BY id',params)]

    def revoke(self,tenant: str,capture_id: str,reason: str):
        # Local owner operation only; no claim of solving hosted ChangeRecord F.
        if not reason: raise ContractError('Revocation reason required')
        with self.db: self.db.execute('INSERT OR REPLACE INTO revoked_captures VALUES(?,?,?)',(tenant,capture_id,reason))

    def stored_claims(self,tenant: str,*,as_of: str,allowed_rule_digests: set[str] | None=None,subject_id: str | None=None):
        from .claims import resolve_claims
        def allrows(table): return [strict_json(r['payload']) for r in self.db.execute(f'SELECT payload FROM {table} WHERE tenant=?',(tenant,))]
        obs=[Observation(**x) for x in allrows('observations')]
        matches=[Match(**x) for x in allrows('matches')]
        links=[SupportLink(r['observation_id'],r['match_id']) for r in self.db.execute('SELECT * FROM support WHERE tenant=?',(tenant,))]
        revoked={r[0] for r in self.db.execute('SELECT capture_id FROM revoked_captures WHERE tenant=?',(tenant,))}
        views=resolve_claims(obs,matches,links,self.captures(tenant),as_of=as_of,allowed_rule_digests=allowed_rule_digests,revoked_capture_ids=revoked)
        return [v for v in views if subject_id is None or v.subject_id==subject_id]

    def harvest(self,tenant: str,pages,*,matched_surface_ids: set[str], transaction_owned=False,release_digest: str | None=None):
        from .urls import origin
        from urllib.parse import urlsplit
        from contextlib import nullcontext
        with (nullcontext() if transaction_owned else self.db):
            for page in pages:
                for s in page.surfaces:
                    if release_digest is None and s.surface_id in matched_surface_ids: continue
                    if s.kind in {'script_url','iframe_url','link_url'}:
                        normalized=(urlsplit(s.value).hostname or '').lower()
                        kind=s.kind+':host'
                    elif s.kind=='cookie_name': normalized=s.value; kind=s.kind
                    else: continue
                    if not normalized: continue
                    feature=identity('feature',kind,normalized)
                    self.db.execute('INSERT OR IGNORE INTO feature_occurrences VALUES(?,?,?,?,?)',
                        (tenant,feature,origin(page.capture.url),page.capture.capture_id,canonical({'kind':kind,'value':normalized})))
                    if release_digest is not None:
                        self.db.execute('''INSERT INTO feature_states VALUES(?,?,?,?,?)
                          ON CONFLICT(tenant,feature_id,capture_id,release_digest)
                          DO UPDATE SET matched=MAX(feature_states.matched,excluded.matched)''',
                          (tenant,feature,page.capture.capture_id,release_digest,int(s.surface_id in matched_surface_ids)))
                if release_digest is not None:
                    self.db.execute('INSERT OR REPLACE INTO capture_releases VALUES(?,?,?)',
                                    (tenant,page.capture.capture_id,release_digest))

    def candidates(self,tenant: str,min_hosts: int=3,*,release_digest: str | None=None,
                   include_resolved: bool=False,as_of: str | None=None):
        """Current queue from retained eligible captures; historical counts stay explicit.

        With no release argument use the latest evaluated release for each capture.
        Supplying an unevaluated release does not inherit another release's approval.
        """
        if isinstance(min_hosts,bool) or min_hosts<1: raise ContractError('min_hosts must be positive')
        from .core import utcnow,expires_at
        checked_at=as_of or utcnow();at=instant(checked_at); groups={}
        rows=self.db.execute("""SELECT f.*,c.payload,rc.capture_id AS revoked,fs.matched,
                 COALESCE(?,cr.release_digest) AS evaluated_release
          FROM feature_occurrences f JOIN captures c ON c.tenant=f.tenant AND c.id=f.capture_id
          LEFT JOIN revoked_captures rc ON rc.tenant=f.tenant AND rc.capture_id=f.capture_id
          LEFT JOIN capture_releases cr ON cr.tenant=f.tenant AND cr.capture_id=f.capture_id
          LEFT JOIN feature_states fs ON fs.tenant=f.tenant AND fs.feature_id=f.feature_id
            AND fs.capture_id=f.capture_id AND fs.release_digest=COALESCE(?,cr.release_digest)
          WHERE f.tenant=?""",(release_digest,release_digest,tenant))
        for row in rows:
            item=groups.setdefault(row['feature_id'],{'feature_id':row['feature_id'],'value':row['value'],
                    'history':set(),'origins':set(),'captures':set(),'unknown':set()})
            item['history'].add(row['capture_id']);cap=Capture(**strict_json(row['payload']))
            eligible=(not row['revoked'] and cap.complete and cap.status_code==200 and
                      instant(cap.observed_at)<=at<instant(expires_at(cap.observed_at,cap.source_ttl_seconds)))
            if not eligible:continue
            item['origins'].add(row['origin']);item['captures'].add(row['capture_id'])
            if not row['matched']:item['unknown'].add(row['origin'])
        output=[]
        for item in groups.values():
            status='UNRESOLVED' if item['unknown'] else 'RESOLVED' if item['captures'] else 'HISTORICAL'
            if len(item['unknown'])>=min_hosts or (include_resolved and status!='UNRESOLVED'):
                output.append({'feature_id':item['feature_id'],'value':item['value'],'status':status,
                  'observed_origin_count':len(item['origins']),'capture_count':len(item['captures']),
                  'unresolved_origin_count':len(item['unknown']),'historical_capture_count':len(item['history']),
                  'release_digest':release_digest,'as_of':checked_at})
        return sorted(output,key=lambda r:(-r['observed_origin_count'],r['feature_id']))

    def publish_evaluation(self, data, *_legacy_findings):
        """Publish exactly the verified bundle, never a second findings collection.

        Legacy positional collections are ignored for compatibility, not trusted.
        The store reconstructs extraction from original bytes. This is a local owner
        boundary, not hosted authentication. Capture/attempt diagnostics survive failure.
        """
        from .validation import validate_bundle
        from .extraction import extract
        from .standalone import verify_page
        from .core import Surface,PageEvidence,CommandResult
        validate_bundle(data)
        tenant=data['tenant_id'];run=data['capture_run_id']
        if not self.db.execute('SELECT 1 FROM runs WHERE tenant=? AND run_id=?',(tenant,run)).fetchone():
            raise ContractError('Evaluation has no authorized local run')
        caps=[Capture(**c) for c in data['captures']];pages=[]
        for cap in caps:
            self.body(cap)
            if cap.capture_id in data['evaluated_capture_ids']:
                page=PageEvidence(cap,[Surface(**s) for s in data['surfaces'] if s['capture_id']==cap.capture_id],
                    [CommandResult(**c) for c in data['commands'] if c['command_id'].startswith('EXTRACT_') and c['input_ids']==[cap.capture_id]])
                verify_page(self,page);pages.append(page)
        matches=[Match(**x) for x in data['matches']]
        observations=[Observation(**x) for x in data['observations']]
        links=[SupportLink(**x) for x in data['support_links']]
        key=identity('evaluation',run,data['subject_id'],data['evaluation_id'],data['release_digest'],
                     data['as_of'],data['evaluated_capture_ids'])
        payload=canonical({k:data[k] for k in ('tenant_id','subject_id','capture_run_id','evaluation_id','as_of',
                        'release_digest','evaluated_capture_ids','matches','observations','support_links','claims')})
        with self.db:
            old=self.db.execute('SELECT payload FROM evaluations WHERE tenant=? AND evaluation_key=?',(tenant,key)).fetchone()
            if old and old['payload']!=payload:
                raise ContractError('Evaluation identity reused with different semantic output')
            self.db.execute('INSERT OR IGNORE INTO evaluations VALUES(?,?,?)',(tenant,key,payload))
            self.save_findings(tenant,matches,observations,links,transaction_owned=True)
            self.harvest(tenant,pages,matched_surface_ids={m.surface_id for m in matches if m.authority=='APPROVED'},
                         transaction_owned=True,release_digest=data['release_digest'])
            selected=set(data['evaluated_capture_ids'])
            for cap in caps:
                eligible=int(cap.capture_id in selected)
                previous=self.db.execute('SELECT eligible FROM replay_selection WHERE tenant=? AND capture_id=?',(tenant,cap.capture_id)).fetchone()
                if previous and previous['eligible']!=eligible:
                    raise ContractError('Capture eligibility cannot be silently reinterpreted; create a new explicit policy evaluation')
                self.db.execute('INSERT OR IGNORE INTO replay_selection VALUES(?,?,?)',(tenant,cap.capture_id,eligible))

    def replay_eligible(self, cap):
        row=self.db.execute('SELECT eligible FROM replay_selection WHERE tenant=? AND capture_id=?',
                            (cap.tenant_id,cap.capture_id)).fetchone()
        if row is None:
            raise ContractError('No successful original selection manifest; recapture or explicitly import evidence')
        return bool(row['eligible'])

    def set_cooldown(self,tenant,origin,until):
        instant(until)
        with self.db:
            row=self.db.execute('SELECT until_utc FROM cooldowns WHERE tenant=? AND origin=?',(tenant,origin)).fetchone()
            if row and instant(row['until_utc'])>instant(until):return
            self.db.execute('INSERT OR REPLACE INTO cooldowns VALUES(?,?,?)',(tenant,origin,until))

    def cooling_down(self,tenant,origin,at):
        row=self.db.execute('SELECT until_utc FROM cooldowns WHERE tenant=? AND origin=?',(tenant,origin)).fetchone()
        return bool(row and instant(at)<instant(row['until_utc']))
