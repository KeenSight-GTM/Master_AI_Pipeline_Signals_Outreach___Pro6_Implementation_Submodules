from __future__ import annotations

from dataclasses import dataclass,asdict
from collections import deque
import time
import math
from urllib.parse import urlsplit
from .core import ContractError,DependencyUnavailable,CommandResult,identity,utcnow,instant,canonical,strict_json
from .urls import normalize_url,origin,link_url
from .transport import Transport,FetchResult,ScraplingBrowserTransport
from .storage import Store
from .rules import RulePack,match_pages,MATCH_COMMAND
from .extraction import extract
from .claims import observation_candidates,resolve_claims
from .discovery import robots_policy,sitemap_urls,template_links,canonical_claims,WELL_KNOWN
from .commands import complete_command_manifest


@dataclass(frozen=True)
class ScanConfig:
    tenant_id: str
    subject_id: str
    run_id: str
    max_attempts: int=8
    max_pages: int=5
    max_sitemaps: int=2
    max_body_bytes: int=2_000_000
    probe_paths: bool=False
    render_empty_shell: bool=False
    source_ttl_seconds: int=2592000
    min_delay_seconds: float=1.0

    def __post_init__(self):
        if not self.tenant_id or not self.subject_id or not self.run_id:
            raise ContractError('Explicit tenant, subject and run ID required')
        if isinstance(self.min_delay_seconds,bool) or not isinstance(self.min_delay_seconds,(int,float)) or not math.isfinite(self.min_delay_seconds) or not 0<=self.min_delay_seconds<=60:
            raise ContractError('min_delay_seconds must be finite and between zero and 60')
        for name in ('max_attempts','max_pages','max_sitemaps','max_body_bytes','source_ttl_seconds'):
            value=getattr(self,name)
            if isinstance(value,bool) or not isinstance(value,int) or value<1:
                raise ContractError(f'{name} must be positive integer')


class Scanner:
    def __init__(self,store: Store,pack: RulePack,transport: Transport,*,browser=None,clock=utcnow,production=True):
        if production and pack.fixture_only:
            raise ContractError('Fixture-only rules are forbidden in production before capture')
        self.store=store;self.pack=pack;self.transport=transport
        self.browser=browser or ScraplingBrowserTransport();self.clock=clock;self.production=production

    def scan(self,url: str,config: ScanConfig) -> dict:
        seed=normalize_url(url); base=origin(seed)
        cfg={**asdict(config),'seed':seed,'release_digest':self.pack.digest,'code_version':'0.2.0'}
        self.store.begin_run(config.tenant_id,config.run_id,cfg)
        commands=[CommandResult('CATALOG_LOAD','COMPLETE',details={'release_digest':self.pack.digest}),
                  CommandResult('NORM_URL','COMPLETE',details={'seed':seed})]
        dispositions=[];pages=[];allcaps={}; denied=self.store.cooling_down(config.tenant_id,base,self.clock())
        delay=config.min_delay_seconds; last_request=None
        # Stored attempts are reused; PENDING means crash uncertainty and is not retried.
        def request(target,command,mode='RAW_HTML'):
            nonlocal denied,last_request
            if origin(target)!=base:
                dispositions.append({'url':target,'status':'SKIPPED_POLICY','reason':'CROSS_ORIGIN'})
                return None
            if denied or self.store.cooling_down(config.tenant_id,base,self.clock()):
                denied=True
                dispositions.append({'url':target,'status':'SKIPPED_RATE_LIMIT'})
                commands.append(CommandResult(command,'SKIPPED_POLICY',limitations=['RATE_LIMIT_COOLDOWN']))
                return None
            key=identity('request',target,mode)
            attempt=self.store.reserve_attempt(config.tenant_id,config.run_id,key,config.max_attempts,{'url':target,'command_id':command,'started_at':self.clock(),'mode':mode})
            if not attempt['new']:
                if attempt['status']=='COMPLETE' and 'capture_id' in attempt['payload']:
                    cap=next((c for c in self.store.captures(config.tenant_id,config.run_id) if c.capture_id==attempt['payload']['capture_id']),None)
                    if cap:
                        if cap.status_code==429: denied=True
                        allcaps[cap.capture_id]=cap
                        commands.append(CommandResult(command,'REUSED',[cap.capture_id],details={'url':target}))
                        return cap
                reason='INTERRUPTED_ATTEMPT_NO_BLIND_RETRY' if attempt['status']=='PENDING' else attempt['status']
                dispositions.append({'url':target,'status':reason})
                commands.append(CommandResult(command,reason,details={'url':target}))
                return None
            try:
                if not getattr(self.transport,'is_fixture',False):
                    if last_request is not None:
                        time.sleep(max(0,delay-(time.monotonic()-last_request)))
                    last_request=time.monotonic()
                reply=(self.browser if mode=='RENDERED_DOM' else self.transport).get(target)
                if normalize_url(reply.url)!=target:
                    raise ContractError('Unrecorded redirect from transport')
                data=reply.body[:config.max_body_bytes]
                complete=reply.complete and len(reply.body)<=config.max_body_bytes
                limitations=list(reply.limitations)
                if not complete: limitations.append('CAPTURE_INCOMPLETE')
                cap=self.store.put_capture(tenant_id=config.tenant_id,subject_id=config.subject_id,run_id=config.run_id,
                                          url=target,observed_at=self.clock(),body=data,headers=reply.headers,status_code=reply.status_code,
                                          mode=mode,complete=complete,limitations=limitations,source_ttl_seconds=config.source_ttl_seconds,
                                          source_id='source:synthetic-fixture' if getattr(self.transport,'is_fixture',False) else 'source:public-website')
                allcaps[cap.capture_id]=cap
                payload={'url':target,'capture_id':cap.capture_id,'http_status':cap.status_code,'mode':mode,'finished_at':self.clock()}
                self.store.finish_attempt(config.tenant_id,config.run_id,key,'COMPLETE',payload)
                commands.append(CommandResult(command,'COMPLETE' if complete else 'PARTIAL',output_ids=[cap.capture_id],details=payload))
                if cap.status_code==429:
                    denied=True
                    from datetime import timedelta, timezone
                    from email.utils import parsedate_to_datetime
                    retry=cap.headers.get('retry-after','').strip()
                    try:
                        until=(instant(self.clock())+timedelta(seconds=max(1,int(retry)))).isoformat().replace('+00:00','Z')
                    except (ValueError,OverflowError):
                        try: until=parsedate_to_datetime(retry).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
                        except (ValueError,TypeError,OverflowError): until=(instant(self.clock())+timedelta(hours=1)).isoformat().replace('+00:00','Z')
                    self.store.set_cooldown(config.tenant_id,base,until)
                return cap
            except Exception as exc:
                reason=type(exc).__name__
                payload={'url':target,'reason':reason,'message':str(exc)[:300],'finished_at':self.clock()}
                self.store.finish_attempt(config.tenant_id,config.run_id,key,'FAILED',payload)
                commands.append(CommandResult(command,'FAILED',limitations=[reason],details=payload))
                dispositions.append({'url':target,'status':'FAILED','reason':reason})
                return None
        robots_url=base+'/robots.txt'
        rc=request(robots_url,'FETCH_ROBOTS')
        rp,maps,reason=robots_policy(robots_url,rc.status_code,self.store.body(rc),rc.complete) if rc else (None,[],'ROBOTS_UNAVAILABLE_FAIL_CLOSED')
        if rp is None:
            commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=[reason]))
            return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
        crawl_delay=rp.crawl_delay('KeenSightResearch') or rp.crawl_delay('*') or 0
        request_rate=rp.request_rate('KeenSightResearch') or rp.request_rate('*')
        delay=max(delay,crawl_delay,(request_rate.seconds/request_rate.requests) if request_rate and request_rate.requests else 0)
        if delay>60:
            commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=['ROBOTS_DELAY_EXCEEDS_BATCH_WAIT_POLICY']))
            return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
        queue=deque([(seed,'page',0)])
        for u in [*maps,base+'/sitemap.xml']:
            try:
                u=normalize_url(u)
                if origin(u)==base: queue.append((u,'sitemap',0))
                else: dispositions.append({'url':u,'status':'SKIPPED_POLICY','reason':'SITEMAP_CROSS_ORIGIN'})
            except ValueError:
                dispositions.append({'url':str(u),'status':'INVALID_DISCOVERY_URL'})
        if config.probe_paths: queue.extend((base+p,'probe',0) for p in WELL_KNOWN)
        seen=set();sitemap_count=0
        while queue:
            target,kind,depth=queue.popleft()
            try: target=normalize_url(target)
            except ValueError: continue
            if target in seen: continue
            seen.add(target)
            if denied:
                dispositions.append({'url':target,'status':'SKIPPED_RATE_LIMIT'}); continue
            if kind=='sitemap' and (sitemap_count>=config.max_sitemaps or depth>2):
                dispositions.append({'url':target,'status':'SKIPPED_SITEMAP_LIMIT'});continue
            if kind!='sitemap' and len(pages)>=config.max_pages:
                dispositions.append({'url':target,'status':'SKIPPED_PAGE_LIMIT'});continue
            if origin(target)!=base or not rp.can_fetch('KeenSightResearch',target):
                dispositions.append({'url':target,'status':'SKIPPED_POLICY'});continue
            command='FETCH_SITEMAP' if kind=='sitemap' else 'FETCH_WELL_KNOWN' if kind=='probe' else 'FETCH_STATIC'
            cap=request(target,command)
            if not cap: continue
            if 300<=cap.status_code<400:
                redirect=link_url(cap.url,cap.headers.get('location',''))
                if redirect and origin(redirect)==base:
                    queue.appendleft((redirect,kind,depth))
                else: dispositions.append({'url':target,'status':'REDIRECT_OUT_OF_SCOPE'})
                continue
            if cap.status_code!=200 or not cap.complete:
                dispositions.append({'url':target,'status':'NOT_USABLE','http_status':cap.status_code});continue
            body=self.store.body(cap)
            if kind=='sitemap':
                sitemap_count+=1
                try:
                    discovered,truncated=sitemap_urls(body,target)
                    queue.extend((u,t,depth+1 if t=='sitemap' else 0) for t,u in discovered)
                    commands[-1].details['declared_url_count']=len(discovered)
                    if truncated: commands[-1].limitations.append('SITEMAP_ENTRY_LIMIT')
                except ContractError as exc:
                    commands[-1].status='PARTIAL';commands[-1].limitations.append(str(exc))
                continue
            ct=cap.headers.get('content-type','').lower()
            if not ('html' in ct or (not ct and body.lstrip().lower().startswith((b'<!doctype html',b'<html')))):
                dispositions.append({'url':target,'status':'NON_HTML_ARTIFACT'});continue
            # Known access challenges do not become product observations.
            prefix=body[:200000].lower()
            if any(marker in prefix for marker in (b'<title>just a moment',b'<title>access denied',b'cf-chl-widget')):
                dispositions.append({'url':target,'status':'CHALLENGE_NOT_USABLE'});continue
            page=extract(cap,body);pages.append(page)
            if config.render_empty_shell and len(pages)<config.max_pages and len(next((s.value for s in page.surfaces if s.kind=='prose'),''))<40:
                rendered=request(target,'FETCH_STEALTH','RENDERED_DOM')
                if rendered and rendered.complete and rendered.status_code==200:
                    pages.append(extract(rendered,self.store.body(rendered)))
            discovered=template_links([page],seed)
            commands.append(CommandResult('DISCOVER_TEMPLATES','COMPLETE',[cap.capture_id],details={'urls':discovered}))
            queue.extend((u,'page',0) for u in discovered if u not in seen)
        return self.evaluate(pages,config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))

    def evaluate(self,pages,evaluation_id,as_of,commands=None,dispositions=None,captures=None) -> dict:
        pages=list(pages)
        from .standalone import verify_page
        for page in pages:
            verify_page(self.store,page)
        commands=list(commands or [])
        for p in pages: commands.extend(p.commands)
        caps=captures if captures is not None else [p.capture for p in pages]
        if any(instant(c.observed_at)>instant(as_of) for c in caps):
            raise ContractError('Evaluation cutoff precedes an input capture')
        matches,rule_evaluations=match_pages(self.pack,pages,production=self.production)
        observations,links=observation_candidates([p.capture for p in pages],matches)
        views=resolve_claims(observations,matches,links,[p.capture for p in pages],as_of=as_of)
        for operator in sorted({r.operator for r in self.pack.rules}):
            mids=[m.match_id for m in matches if next(r for r in self.pack.rules if r.rule_id==m.rule_id).operator==operator]
            reports=[r for r in rule_evaluations if next(x for x in self.pack.rules if x.rule_id==r['rule_id']).operator==operator]
            status='FAILED' if any(r['status']=='ERROR' for r in reports) else 'PARTIAL' if any(r['status']=='PARTIAL' for r in reports) else 'SKIPPED' if not pages else 'COMPLETE'
            commands.append(CommandResult(MATCH_COMMAND[operator],status,input_ids=[p.capture.capture_id for p in pages],output_ids=mids))
        if any(len(r.patterns)>1 for r in self.pack.rules):
            commands.append(CommandResult('MATCH_OR_GROUP','COMPLETE',details={'semantics':'ANY alternative; all matched branches retained'}))
        commands.extend([
            CommandResult('DISCOVER_CANONICAL','COMPLETE',details={'claims':canonical_claims(pages)}),
            CommandResult('ROLLUP_HOST','COMPLETE',details={'captures':len(pages),'scope':'exact tenant/subject/origin; modes remain separate claim scopes'}),
            CommandResult('GATE_AND','COMPLETE',details={'qualifications':{r['rule_id']:r.get('qualification') for r in rule_evaluations}}),
            CommandResult('GATE_SCHEMA','COMPLETE',details={'meaning':'supporting type only; JSONLD subject identity is not assumed'}),
        ])
        text='\n'.join(s.value for p in pages for s in p.surfaces if s.kind=='prose').casefold()
        negatives=[term for term in self.pack.raw.get('negative_terms',[]) if term.casefold() in text]
        commands.append(CommandResult('GATE_NEGATIVE','COMPLETE',details={'deprioritize':bool(negatives),'terms':negatives,'facts_deleted':False}))
        supported={v.claim_key for v in views if v.status=='SUPPORTED' and v.predicate=='vendor.present'}
        score=min(100,10*len(supported)) if not negatives else 0
        commands.append(CommandResult('SCORE_HOST','COMPLETE',details={'policy':'prototype-unique-supported-presence-v1','score':score,'is_probability':False,'calibrated':False}))
        commands.append(CommandResult('EMIT','COMPLETE',details={'kind':'ScanBundle','canonical_fact_admission':'NOT_PERFORMED'}))
        data={'schema_version':'1.1','producer':'keensight-scrapling-ingestion/0.2.0','evaluation_id':evaluation_id,'as_of':as_of,
              'release_digest':self.pack.digest,'rule_pack':self.pack.raw,'fixture_only':self.pack.fixture_only,'send_allowed':False,
              'captures':[asdict(c) for c in sorted(caps,key=lambda x:x.capture_id)],
              'evaluated_capture_ids':sorted(p.capture.capture_id for p in pages),
              'surfaces':[asdict(s) for p in pages for s in p.surfaces],
              'matches':[asdict(m) for m in matches],'observations':[asdict(o) for o in observations],
              'support_links':[asdict(x) for x in links],'claims':[asdict(v) for v in views],
              'rule_evaluations':rule_evaluations,'commands':[asdict(c) for c in complete_command_manifest(commands)],
              'resource_dispositions':dispositions or [],'priority_score':score,
              'handoff':{'type':'COLLECTOR_OBSERVATIONS','requires_fact_service_admission':True,'absence_facts_emitted':False}}
        from .validation import validate_bundle
        data=strict_json(canonical(data))
        validate_bundle(data)
        self.store.publish_evaluation(data,pages,matches,observations,links)
        return data

    def replay(self,tenant: str,capture_run_id: str,evaluation_id: str,as_of: str) -> dict:
        caps=self.store.captures(tenant,capture_run_id)
        if not caps: raise ContractError('Unknown capture run')
        pages=[]
        for c in caps:
            if not self.store.replay_eligible(c): continue
            body=self.store.body(c)
            if any(marker in body[:200000].lower() for marker in (b'<title>just a moment',b'<title>access denied',b'cf-chl-widget')): continue
            pages.append(extract(c,body))
        return self.evaluate(pages,evaluation_id,as_of,[CommandResult('CATALOG_LOAD','COMPLETE',details={'release_digest':self.pack.digest,'mode':'REPLAY'})],captures=caps)
