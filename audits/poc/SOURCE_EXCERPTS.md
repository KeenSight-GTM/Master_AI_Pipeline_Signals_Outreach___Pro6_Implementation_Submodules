# Exact source excerpts — POC standard-usage audit

All paths are relative to the unchanged `baseline/`.

## `collector/src/keensight_scrapling/pipeline.py`

SHA-256: `8aba39ce2fdfbb22695fde9759480be94da43a2dbbabddfd48106798de8919f5`

```text
  51     def scan(self,url: str,config: ScanConfig) -> dict:
  52         seed=normalize_url(url); base=origin(seed)
  53         cfg={**asdict(config),'seed':seed,'release_digest':self.pack.digest,'code_version':'0.2.0'}
  54         self.store.begin_run(config.tenant_id,config.run_id,cfg)
  55         commands=[CommandResult('CATALOG_LOAD','COMPLETE',details={'release_digest':self.pack.digest}),
  56                   CommandResult('NORM_URL','COMPLETE',details={'seed':seed})]
  57         dispositions=[];pages=[];allcaps={}; denied=self.store.cooling_down(config.tenant_id,base,self.clock())
  58         delay=config.min_delay_seconds; last_request=None
  59         # Stored attempts are reused; PENDING means crash uncertainty and is not retried.
  60         def request(target,command,mode='RAW_HTML'):
  61             nonlocal denied,last_request
  62             if origin(target)!=base:
  63                 dispositions.append({'url':target,'status':'SKIPPED_POLICY','reason':'CROSS_ORIGIN'})
  64                 return None
  65             if denied or self.store.cooling_down(config.tenant_id,base,self.clock()):
  66                 denied=True
  67                 dispositions.append({'url':target,'status':'SKIPPED_RATE_LIMIT'})
  68                 commands.append(CommandResult(command,'SKIPPED_POLICY',limitations=['RATE_LIMIT_COOLDOWN']))
  69                 return None
  70             key=identity('request',target,mode)
  71             attempt=self.store.reserve_attempt(config.tenant_id,config.run_id,key,config.max_attempts,{'url':target,'command_id':command,'started_at':self.clock(),'mode':mode})
  72             if not attempt['new']:
  73                 if attempt['status']=='COMPLETE' and 'capture_id' in attempt['payload']:
  74                     cap=next((c for c in self.store.captures(config.tenant_id,config.run_id) if c.capture_id==attempt['payload']['capture_id']),None)
  75                     if cap:
  76                         if cap.status_code==429: denied=True
  77                         allcaps[cap.capture_id]=cap
  78                         commands.append(CommandResult(command,'REUSED',[cap.capture_id],details={'url':target}))
  79                         return cap
  80                 reason='INTERRUPTED_ATTEMPT_NO_BLIND_RETRY' if attempt['status']=='PENDING' else attempt['status']
  81                 dispositions.append({'url':target,'status':reason})
  82                 commands.append(CommandResult(command,reason,details={'url':target}))
  83                 return None
  84             try:
  85                 if not getattr(self.transport,'is_fixture',False):
  86                     if last_request is not None:
  87                         time.sleep(max(0,delay-(time.monotonic()-last_request)))
  88                     last_request=time.monotonic()
```

```text
 123         robots_url=base+'/robots.txt'
 124         rc=request(robots_url,'FETCH_ROBOTS')
 125         rp,maps,reason=robots_policy(robots_url,rc.status_code,self.store.body(rc),rc.complete) if rc else (None,[],'ROBOTS_UNAVAILABLE_FAIL_CLOSED')
 126         if rp is None:
 127             commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=[reason]))
 128             return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
 129         crawl_delay=rp.crawl_delay('KeenSightResearch') or rp.crawl_delay('*') or 0
 130         request_rate=rp.request_rate('KeenSightResearch') or rp.request_rate('*')
 131         delay=max(delay,crawl_delay,(request_rate.seconds/request_rate.requests) if request_rate and request_rate.requests else 0)
 132         if delay>60:
 133             commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=['ROBOTS_DELAY_EXCEEDS_BATCH_WAIT_POLICY']))
 134             return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
 135         queue=deque([(seed,'page',0)])
 136         for u in [*maps,base+'/sitemap.xml']:
 137             try:
 138                 u=normalize_url(u)
 139                 if origin(u)==base: queue.append((u,'sitemap',0))
 140                 else: dispositions.append({'url':u,'status':'SKIPPED_POLICY','reason':'SITEMAP_CROSS_ORIGIN'})
 141             except ValueError:
 142                 dispositions.append({'url':str(u),'status':'INVALID_DISCOVERY_URL'})
 143         if config.probe_paths: queue.extend((base+p,'probe',0) for p in WELL_KNOWN)
 144         seen=set();sitemap_count=0
 145         while queue:
 146             target,kind,depth=queue.popleft()
 147             try: target=normalize_url(target)
 148             except ValueError: continue
 149             if target in seen: continue
 150             seen.add(target)
 151             if denied:
 152                 dispositions.append({'url':target,'status':'SKIPPED_RATE_LIMIT'}); continue
 153             if kind=='sitemap' and (sitemap_count>=config.max_sitemaps or depth>2):
 154                 dispositions.append({'url':target,'status':'SKIPPED_SITEMAP_LIMIT'});continue
 155             if kind!='sitemap' and len(pages)>=config.max_pages:
 156                 dispositions.append({'url':target,'status':'SKIPPED_PAGE_LIMIT'});continue
 157             if origin(target)!=base or not rp.can_fetch('KeenSightResearch',target):
 158                 dispositions.append({'url':target,'status':'SKIPPED_POLICY'});continue
 159             command='FETCH_SITEMAP' if kind=='sitemap' else 'FETCH_WELL_KNOWN' if kind=='probe' else 'FETCH_STATIC'
 160             cap=request(target,command)
 161             if not cap: continue
 162             if 300<=cap.status_code<400:
 163                 redirect=link_url(cap.url,cap.headers.get('location',''))
 164                 if redirect and origin(redirect)==base:
 165                     queue.appendleft((redirect,kind,depth))
 166                 else: dispositions.append({'url':target,'status':'REDIRECT_OUT_OF_SCOPE'})
 167                 continue
 168             if cap.status_code!=200 or not cap.complete:
 169                 dispositions.append({'url':target,'status':'NOT_USABLE','http_status':cap.status_code});continue
 170             body=self.store.body(cap)
 171             if kind=='sitemap':
 172                 sitemap_count+=1
 173                 try:
 174                     discovered,truncated=sitemap_urls(body,target)
 175                     queue.extend((u,t,depth+1 if t=='sitemap' else 0) for t,u in discovered)
 176                     commands[-1].details['declared_url_count']=len(discovered)
 177                     if truncated: commands[-1].limitations.append('SITEMAP_ENTRY_LIMIT')
 178                 except ContractError as exc:
 179                     commands[-1].status='PARTIAL';commands[-1].limitations.append(str(exc))
 180                 continue
 181             ct=cap.headers.get('content-type','').lower()
 182             if not ('html' in ct or (not ct and body.lstrip().lower().startswith((b'<!doctype html',b'<html')))):
 183                 dispositions.append({'url':target,'status':'NON_HTML_ARTIFACT'});continue
 184             # Known access challenges do not become product observations.
 185             prefix=body[:200000].lower()
 186             if any(marker in prefix for marker in (b'<title>just a moment',b'<title>access denied',b'cf-chl-widget')):
 187                 dispositions.append({'url':target,'status':'CHALLENGE_NOT_USABLE'});continue
 188             page=extract(cap,body);pages.append(page)
 189             if config.render_empty_shell and len(pages)<config.max_pages and len(next((s.value for s in page.surfaces if s.kind=='prose'),''))<40:
 190                 rendered=request(target,'FETCH_STEALTH','RENDERED_DOM')
 191                 if rendered and rendered.complete and rendered.status_code==200:
 192                     pages.append(extract(rendered,self.store.body(rendered)))
 193             discovered=template_links([page],seed)
 194             commands.append(CommandResult('DISCOVER_TEMPLATES','COMPLETE',[cap.capture_id],details={'urls':discovered}))
 195             queue.extend((u,'page',0) for u in discovered if u not in seen)
```

```text
 198     def evaluate(self,pages,evaluation_id,as_of,commands=None,dispositions=None,captures=None) -> dict:
 199         pages=list(pages)
 200         from .standalone import verify_page
 201         for page in pages:
 202             verify_page(self.store,page)
 203         commands=list(commands or [])
 204         for p in pages: commands.extend(p.commands)
 205         caps=captures if captures is not None else [p.capture for p in pages]
 206         if any(instant(c.observed_at)>instant(as_of) for c in caps):
 207             raise ContractError('Evaluation cutoff precedes an input capture')
 208         matches,rule_evaluations=match_pages(self.pack,pages,production=self.production)
 209         observations,links=observation_candidates([p.capture for p in pages],matches)
 210         views=resolve_claims(observations,matches,links,[p.capture for p in pages],as_of=as_of)
 211         for operator in sorted({r.operator for r in self.pack.rules}):
 212             mids=[m.match_id for m in matches if next(r for r in self.pack.rules if r.rule_id==m.rule_id).operator==operator]
 213             reports=[r for r in rule_evaluations if next(x for x in self.pack.rules if x.rule_id==r['rule_id']).operator==operator]
 214             status='FAILED' if any(r['status']=='ERROR' for r in reports) else 'PARTIAL' if any(r['status']=='PARTIAL' for r in reports) else 'SKIPPED' if not pages else 'COMPLETE'
 215             commands.append(CommandResult(MATCH_COMMAND[operator],status,input_ids=[p.capture.capture_id for p in pages],output_ids=mids))
 216         if any(len(r.patterns)>1 for r in self.pack.rules):
 217             commands.append(CommandResult('MATCH_OR_GROUP','COMPLETE',details={'semantics':'ANY alternative; all matched branches retained'}))
 218         commands.extend([
 219             CommandResult('DISCOVER_CANONICAL','COMPLETE',details={'claims':canonical_claims(pages)}),
 220             CommandResult('ROLLUP_HOST','COMPLETE',details={'captures':len(pages),'scope':'exact tenant/subject/origin; modes remain separate claim scopes'}),
 221             CommandResult('GATE_AND','COMPLETE',details={'qualifications':{r['rule_id']:r.get('qualification') for r in rule_evaluations}}),
 222             CommandResult('GATE_SCHEMA','COMPLETE',details={'meaning':'supporting type only; JSONLD subject identity is not assumed'}),
 223         ])
 224         text='\n'.join(s.value for p in pages for s in p.surfaces if s.kind=='prose').casefold()
 225         negatives=[term for term in self.pack.raw.get('negative_terms',[]) if term.casefold() in text]
 226         commands.append(CommandResult('GATE_NEGATIVE','COMPLETE',details={'deprioritize':bool(negatives),'terms':negatives,'facts_deleted':False}))
 227         supported={v.claim_key for v in views if v.status=='SUPPORTED' and v.predicate=='vendor.present'}
 228         score=min(100,10*len(supported)) if not negatives else 0
 229         commands.append(CommandResult('SCORE_HOST','COMPLETE',details={'policy':'prototype-unique-supported-presence-v1','score':score,'is_probability':False,'calibrated':False}))
 230         commands.append(CommandResult('EMIT','COMPLETE',details={'kind':'ScanBundle','canonical_fact_admission':'NOT_PERFORMED'}))
 231         data={'schema_version':'1.1','producer':'keensight-scrapling-ingestion/0.2.0','evaluation_id':evaluation_id,'as_of':as_of,
 232               'release_digest':self.pack.digest,'rule_pack':self.pack.raw,'fixture_only':self.pack.fixture_only,'send_allowed':False,
 233               'captures':[asdict(c) for c in sorted(caps,key=lambda x:x.capture_id)],
 234               'evaluated_capture_ids':sorted(p.capture.capture_id for p in pages),
 235               'surfaces':[asdict(s) for p in pages for s in p.surfaces],
 236               'matches':[asdict(m) for m in matches],'observations':[asdict(o) for o in observations],
 237               'support_links':[asdict(x) for x in links],'claims':[asdict(v) for v in views],
 238               'rule_evaluations':rule_evaluations,'commands':[asdict(c) for c in complete_command_manifest(commands)],
 239               'resource_dispositions':dispositions or [],'priority_score':score,
 240               'handoff':{'type':'COLLECTOR_OBSERVATIONS','requires_fact_service_admission':True,'absence_facts_emitted':False}}
 241         from .validation import validate_bundle
 242         data=strict_json(canonical(data))
 243         validate_bundle(data)
 244         self.store.publish_evaluation(data,pages,matches,observations,links)
 245         return data
```

## `collector/src/keensight_scrapling/rules.py`

SHA-256: `bb728fe394985196343bed967b439a4d93f29435eed106ae1ef710257104f220`

```text
 139 def match_pages(pack: RulePack, pages: list[PageEvidence], *, production: bool = False) -> tuple[list[Match],list[dict]]:
 140     """Retain EVERY rule/surface/alternative hit. Deduplicate claims later."""
 141     if production and pack.fixture_only:
 142         raise ContractError("Fixture-only pack is not eligible for production matching")
 143     matches, evaluations = [], []
 144     # Never pool different subjects, tenants, or origins into the host index.
 145     from .urls import origin
 146     keys = {(p.capture.tenant_id,p.capture.subject_id,origin(p.capture.url)) for p in pages}
 147     if len(keys)>1:
 148         raise ContractError('Cross-subject/tenant/origin host rollup forbidden')
 149     prose = '\n'.join(s.value for p in pages for s in p.surfaces if s.kind in {'prose','header_nav'})
 150     types = {t for p in pages for s in p.surfaces if s.kind=='jsonld' and not s.attributes.get('parse_error') for t in s.attributes.get('types',[])}
 151     for rule in pack.rules:
 152         if rule.status=='DISABLED':
 153             evaluations.append({'rule_id':rule.rule_id,'status':'DISABLED','match_ids':[]})
 154             continue
 155         qualification = 'QUALIFIED' if all(x.casefold() in prose.casefold() for x in rule.guard_terms) and (not rule.schema_types or bool(types.intersection(rule.schema_types))) else 'UNQUALIFIED'
 156         found, errors, limited = [], [], []
 157         start = len(matches)
 158         for page in pages:
 159             command_states={c.command_id:c.status for c in page.commands}
 160             needed={KIND_COMMAND[k] for k in rule.kinds}
 161             if not page.capture.complete or any(command_states.get(c)!='COMPLETE' for c in needed):
 162                 limited.append(page.capture.capture_id)
 163             for s in page.surfaces:
 164                 if s.kind not in rule.kinds or (rule.selector and not s.locator.startswith(rule.selector)):
 165                     continue
 166                 if rule.predicate=='vendor.present' and s.context in {'FOOTER','NOSCRIPT','INERT_TEMPLATE','INERT_SCRIPT'}:
 167                     continue
 168                 if rule.predicate=='vendor.present' and s.kind=='link_url' and 'stylesheet' not in s.attributes.get('rel','').split():
 169                     continue
 170                 value = s.value if rule.field=='value' else str(s.attributes.get(rule.field,''))
 171                 for pattern in rule.patterns:
 172                     try:
 173                         if rule.operator in {'host_suffix','host_equals'}:
 174                             hit = host_match(value,pattern,exact=rule.operator=='host_equals')
 175                         elif rule.operator=='equals': hit = value.casefold()==pattern.casefold()
 176                         elif rule.operator=='regex': hit = bool(regex.search(pattern,value[:131072],timeout=0.025))
 177                         elif rule.operator=='image_alt': hit = pattern.casefold() in str(s.attributes.get('alt','')).casefold()
 178                         else: hit = pattern.casefold() in value.casefold()
 179                     except TimeoutError:
 180                         errors.append({'capture_id':page.capture.capture_id,'reason':'REGEX_TIMEOUT'})
 181                         continue
 182                     if hit:
 183                         authority = 'APPROVED' if rule.status=='APPROVED' else 'CANDIDATE'
 184                         mid = identity('match',rule.digest,pack.digest,page.capture.capture_id,s.surface_id,pattern)
 185                         matches.append(Match(mid,rule.rule_id,rule.digest,pack.digest,authority,page.capture.capture_id,s.surface_id,pattern,rule.predicate,rule.product_id,True,identity('evidence',page.capture.capture_id,s.locator),identity('rule_evidence',rule.digest,page.capture.capture_id,s.surface_id,pattern),rule.confidence))
 186                         found.append(mid)
 187         if errors:
 188             matches = matches[:start]
 189             found = []
 190         evaluations.append({'rule_id':rule.rule_id,'status':'ERROR' if errors else 'NOT_EVALUATED' if not pages else 'PARTIAL' if limited else 'MATCH' if found else 'NO_MATCH',
 191                             'match_ids':found,'errors':errors,'incomplete_capture_ids':sorted(set(limited)), 'qualification':qualification,
 192                             'absence_fact_emitted':False})
 193     # Identical alternate patterns cannot create duplicate link rows.
 194     unique = {m.match_id:m for m in matches}
 195     return sorted(unique.values(),key=lambda x:x.match_id),evaluations
```

## `collector/src/keensight_scrapling/validation.py`

SHA-256: `de115d25207d9a9fa850389f4286935781aa3407641b757027e905a055719311`

```text
  36     if not set(selected)<=set(caps):
  37         raise ContractError('Unknown evaluated capture')
  38     if any(s['capture_id'] not in selected for s in data['surfaces']):
  39         raise ContractError('Surface from capture excluded by acquisition disposition')
  40     from .extraction import EXTRACTORS
  41     pages=[]
  42     for cid in selected:
  43         cap=caps[cid]
  44         ss=[Surface(**s) for s in data['surfaces'] if s['capture_id']==cid]
  45         cmds=[CommandResult(**c) for c in data['commands'] if c['command_id'] in EXTRACTORS and c['input_ids']==[cid]]
  46         if len(cmds)!=len(EXTRACTORS) or {c.command_id for c in cmds}!=set(EXTRACTORS):
  47             raise ContractError('Missing or duplicate per-capture extraction execution')
  48         for command in cmds:
  49             produced=[s.surface_id for s in ss if s.command_id==command.command_id]
  50             if sorted(command.output_ids)!=sorted(produced):
  51                 raise ContractError('Extraction output linkage mismatch')
  52             if produced and command.status not in {'COMPLETE','PARTIAL'}:
  53                 raise ContractError('Failed extraction cannot publish surfaces')
  54         pages.append(PageEvidence(cap,ss,cmds))
  55     expected_matches,expected_reports=match_pages(pack,pages)
  56     if sorted(map(canonical,map(record,expected_matches)))!=sorted(map(canonical,data['matches'])):
  57         raise ContractError('Matches do not reproduce from pinned rules and surfaces')
  58     if canonical(expected_reports)!=canonical(data['rule_evaluations']):
  59         raise ContractError('Rule execution outcomes do not reproduce')
  60     from .rules import MATCH_COMMAND
  61     for operator in {r.operator for r in pack.rules}:
  62         cid=MATCH_COMMAND[operator]
  63         command_rows=[c for c in data['commands'] if c['command_id']==cid]
  64         reports=[r for r in expected_reports if next(x for x in pack.rules if x.rule_id==r['rule_id']).operator==operator]
  65         expected_status='FAILED' if any(r['status']=='ERROR' for r in reports) else 'PARTIAL' if any(r['status']=='PARTIAL' for r in reports) else 'SKIPPED' if not pages else 'COMPLETE'
  66         mids=sorted(m.match_id for m in matches if next(r for r in pack.rules if r.rule_id==m.rule_id).operator==operator)
```

## `collector/src/keensight_scrapling/discovery.py`

SHA-256: `19b817c6196367c9c2c9e0e4a90d437d1b833d85b5e684228f0c2e275f468b88`

```text
   1 from __future__ import annotations
   2 
   3 from urllib.parse import urlsplit
   4 from urllib.robotparser import RobotFileParser
   5 from defusedxml.ElementTree import fromstring
   6 from .core import ContractError
   7 from .urls import normalize_url,origin,link_url
   8 
   9 TEMPLATES=('contact','about','services','locations','booking','schedule','careers','jobs','shop','products','patient-portal','client-portal','pricing','integrations')
  10 WELL_KNOWN=('/llms.txt','/contact','/about','/careers','/book','/locations')
  11 
  12 
  13 def robots_policy(url: str,code: int,body: bytes,complete: bool) -> tuple[RobotFileParser | None,list[str],str]:
  14     parser=RobotFileParser(url)
  15     if code in {404,410}:
  16         parser.parse([]); return parser,[],'NO_ROBOTS_FILE'
  17     if code!=200 or not complete or body.lstrip().lower().startswith((b'<html',b'<!doctype html')):
  18         return None,[],'ROBOTS_UNAVAILABLE_FAIL_CLOSED'
  19     parser.parse(body.decode('utf-8',errors='replace').splitlines())
  20     return parser,parser.site_maps() or [],'ROBOTS_PARSED'
  21 
  22 
  23 def sitemap_urls(body: bytes,base: str,*,max_entries: int=5000) -> tuple[list[tuple[str,str]],bool]:
  24     try: root=fromstring(body)
  25     except Exception as exc: raise ContractError('Invalid or unsafe sitemap XML') from exc
  26     name=root.tag.rsplit('}',1)[-1]
  27     if name not in {'urlset','sitemapindex'}: raise ContractError('Not a sitemap/urlset')
  28     values=[]
  29     for el in root.iter():
  30         if el.tag.rsplit('}',1)[-1]!='loc' or not el.text: continue
  31         url=link_url(base,el.text)
  32         if url and origin(url)==origin(base):
  33             values.append(('sitemap' if name=='sitemapindex' else 'page',url))
  34     distinct=list(dict.fromkeys(values))
  35     return distinct[:max_entries],len(distinct)>max_entries
  36 
  37 
  38 def template_links(pages,seed: str) -> list[str]:
  39     urls={s.value for page in pages for s in page.surfaces if s.kind=='anchor_url' and origin(s.value)==origin(seed)}
  40     def rank(url):
  41         path=urlsplit(url).path.lower()
  42         return next((i for i,x in enumerate(TEMPLATES) if x in path),len(TEMPLATES)),url
  43     return sorted(urls,key=rank)
  44 
  45 
  46 def canonical_claims(pages):
  47     return [{'capture_id':p.capture.capture_id,'url':s.value,'same_origin':origin(s.value)==origin(p.capture.url),'subject_rebound':False}
  48             for p in pages for s in p.surfaces if s.kind=='link_url' and 'canonical' in s.attributes.get('rel','').split()]
```

## `collector/src/keensight_scrapling/storage.py`

SHA-256: `15322ecdfff153682f5dd23f73e5cc53e6762d54c4f9047301b2bc509d8d2103`

```text
  69     def reserve_attempt(self, tenant: str, run_id: str, request_key: str, budget: int, payload: dict) -> dict:
  70         self.db.execute('BEGIN IMMEDIATE')
  71         try:
  72             row=self.db.execute('SELECT status,payload FROM attempts WHERE tenant=? AND run_id=? AND request_key=?',(tenant,run_id,request_key)).fetchone()
  73             if row:
  74                 self.db.commit()
  75                 return {'new':False,'status':row['status'],'payload':strict_json(row['payload'])}
  76             count=self.db.execute('SELECT COUNT(*) FROM attempts WHERE tenant=? AND run_id=?',(tenant,run_id)).fetchone()[0]
  77             if count>=budget:
  78                 self.db.commit(); return {'new':False,'status':'SKIPPED_BUDGET','payload':{}}
  79             self.db.execute('INSERT INTO attempts VALUES(?,?,?,?,?)',(tenant,run_id,request_key,'PENDING',canonical(payload)))
  80             self.db.commit()
  81             return {'new':True,'status':'PENDING','payload':payload}
  82         except Exception:
  83             self.db.rollback(); raise
```

```text
 177     def stored_claims(self,tenant: str,*,as_of: str,allowed_rule_digests: set[str] | None=None):
 178         from .claims import resolve_claims
 179         def allrows(table): return [strict_json(r['payload']) for r in self.db.execute(f'SELECT payload FROM {table} WHERE tenant=?',(tenant,))]
 180         obs=[Observation(**x) for x in allrows('observations')]
 181         matches=[Match(**x) for x in allrows('matches')]
 182         links=[SupportLink(r['observation_id'],r['match_id']) for r in self.db.execute('SELECT * FROM support WHERE tenant=?',(tenant,))]
 183         revoked={r[0] for r in self.db.execute('SELECT capture_id FROM revoked_captures WHERE tenant=?',(tenant,))}
 184         return resolve_claims(obs,matches,links,self.captures(tenant),as_of=as_of,allowed_rule_digests=allowed_rule_digests,revoked_capture_ids=revoked)
 185 
 186     def harvest(self,tenant: str,pages,*,matched_surface_ids: set[str], transaction_owned=False):
 187         from .urls import origin
 188         from urllib.parse import urlsplit
 189         from contextlib import nullcontext
 190         with (nullcontext() if transaction_owned else self.db):
 191             for page in pages:
 192                 for s in page.surfaces:
 193                     if s.surface_id in matched_surface_ids: continue
 194                     if s.kind in {'script_url','iframe_url','link_url'}:
 195                         normalized=(urlsplit(s.value).hostname or '').lower()
 196                         kind=s.kind+':host'
 197                     elif s.kind=='cookie_name': normalized=s.value; kind=s.kind
 198                     else: continue
 199                     if not normalized: continue
 200                     feature=identity('feature',kind,normalized)
 201                     self.db.execute('INSERT OR IGNORE INTO feature_occurrences VALUES(?,?,?,?,?)',
 202                         (tenant,feature,origin(page.capture.url),page.capture.capture_id,canonical({'kind':kind,'value':normalized})))
 203 
 204     def candidates(self,tenant: str,min_hosts: int=3):
 205         if min_hosts<1: raise ContractError('min_hosts must be positive')
 206         return [dict(row) for row in self.db.execute('''SELECT feature_id,value,COUNT(DISTINCT origin) AS observed_origin_count,
 207           COUNT(DISTINCT capture_id) AS capture_count FROM feature_occurrences WHERE tenant=? GROUP BY feature_id,value
 208           HAVING COUNT(DISTINCT origin)>=? ORDER BY observed_origin_count DESC,feature_id''',(tenant,min_hosts))]
 209 
 210 
 211     def publish_evaluation(self, data, pages, matches, observations, links):
 212         """Publish only a validated evaluation; every projection write rolls back together.
 213 
 214         Physical capture bytes/attempt diagnostics already retained are intentionally
 215         outside this publication transaction. A commit is a local owner boundary,
 216         not a substitute for hosted authentication.
 217         """
 218         from .validation import validate_bundle
 219         validate_bundle(data)
 220         caps = [Capture(**c) for c in data['captures']]
 221         for cap in caps:
 222             self.body(cap)
 223         tenants = {c.tenant_id for c in caps}
 224         if len(tenants) > 1:
 225             raise ContractError('Cross-tenant evaluation')
 226         if not tenants:
 227             return
 228         tenant = next(iter(tenants))
 229         key = identity('evaluation', data['evaluation_id'], data['release_digest'],
 230                        data['as_of'], data['evaluated_capture_ids'])
 231         # Transport diagnostics can legitimately differ on resume. Only immutable
 232         # semantic output is stored as the publication identity.
 233         payload = canonical({k:data[k] for k in ('evaluation_id','as_of','release_digest',
 234                             'evaluated_capture_ids','matches','observations','support_links','claims')})
 235         with self.db:
 236             old = self.db.execute('SELECT payload FROM evaluations WHERE tenant=? AND evaluation_key=?',
 237                                   (tenant,key)).fetchone()
 238             if old and old['payload'] != payload:
 239                 raise ContractError('Evaluation identity reused with different semantic output')
 240             self.db.execute('INSERT OR IGNORE INTO evaluations VALUES(?,?,?)',(tenant,key,payload))
 241             self.save_findings(tenant,matches,observations,links,transaction_owned=True)
 242             self.harvest(tenant,pages,matched_surface_ids={m.surface_id for m in matches if m.authority=='APPROVED'},
 243                          transaction_owned=True)
 244             selected=set(data['evaluated_capture_ids'])
 245             for cap in caps:
 246                 eligible=int(cap.capture_id in selected)
 247                 previous=self.db.execute('SELECT eligible FROM replay_selection WHERE tenant=? AND capture_id=?',
 248                                          (tenant,cap.capture_id)).fetchone()
 249                 if previous and previous['eligible']!=eligible:
 250                     raise ContractError('Capture eligibility cannot be silently reinterpreted; create a new explicit policy evaluation')
```

## `collector/src/keensight_scrapling/claims.py`

SHA-256: `045725bbecf7a5ea6fd80254a1f582102bd2b2d3f2002a2d45075da492b6f943`

```text
  42     independent corroboration. No noisy-OR, vote counting, maximum confidence,
  43     or candidate-to-approved promotion is performed.
  44     """
  45     now = instant(as_of)
  46     obsmap = {o.observation_id:o for o in observations}
  47     matchmap = {m.match_id:m for m in matches}
  48     caps = {c.capture_id:c for c in captures}
  49     links = defaultdict(set)
  50     revoked = revoked_capture_ids or set()
  51     for link in support:
  52         if link.observation_id not in obsmap or link.match_id not in matchmap:
  53             raise ContractError('Dangling support link')
  54         o, m = obsmap[link.observation_id],matchmap[link.match_id]
  55         if (o.capture_id,o.predicate,o.target.get('product_id'),o.object_value) != (m.capture_id,m.predicate,m.product_id,m.object_value):
  56             raise ContractError('Support from a different capture, target, predicate, or value')
  57         links[o.observation_id].add(m.match_id)
  58     groups = defaultdict(list)
  59     for o in obsmap.values():
  60         cap = caps.get(o.capture_id)
  61         if cap is None or (cap.tenant_id,cap.subject_id)!=(o.tenant_id,o.subject_id):
  62             raise ContractError('Observation has a missing or cross-account capture')
  63         if instant(o.observed_at) > now:
  64             continue
  65         groups[o.claim_key].append(o)
  66     views=[]
  67     for key, rows in sorted(groups.items()):
  68         eligible, all_matches, usable_rows, shadow = set(),set(),[],False
  69         for o in rows:
  70             mids = links[o.observation_id]
  71             all_matches.update(mids)
  72             cap = caps[o.capture_id]
  73             usable = (o.state=='OBSERVED' and cap.complete and o.capture_id not in revoked and instant(o.expires_at)>now)
  74             active = {mid for mid in mids if (allowed_rule_digests is None or matchmap[mid].rule_digest in allowed_rule_digests)}
  75             good = {mid for mid in active if matchmap[mid].authority=='APPROVED'} if usable else set()
  76             shadow |= bool(usable and active-good)
  77             if good:
```

## `collector/src/keensight_scrapling/core.py`

SHA-256: `bf0089ed8ce49ab590d94ecd94482fa75a05432b595c638ebe241d17d9bbe33f`

```text
 139     subject_id: str
 140     predicate: str
 141     target: dict[str, str]
 142     scope_id: str
 143     nature: str
 144     state: str
 145     object_value: Any
 146     capture_id: str
 147     source_id: str
 148     source_group: str
 149     observed_at: str
 150     expires_at: str
 151 
 152 
 153 @dataclass(frozen=True)
 154 class SupportLink:
 155     observation_id: str
 156     match_id: str
 157 
 158 
 159 @dataclass
 160 class ClaimView:
 161     claim_key: str
 162     predicate: str
 163     target: dict[str, str]
```

## `collector/src/keensight_scrapling/cli.py`

SHA-256: `d5aa220fe2f860245bdff88be8fcd2a2d4cbd5922454f84913946e903b3c3685`

```text
  48 def main(argv=None):
  49     p=argparse.ArgumentParser(description='Scrapling collector: retain matches, deduplicate claims, never inflate confidence.')
  50     sub=p.add_subparsers(dest='command',required=True)
  51     d=sub.add_parser('demo');d.add_argument('--output',default='./demo-output')
  52     c=sub.add_parser('commands')
  53     s=sub.add_parser('scan');s.add_argument('url');s.add_argument('--rules',required=True);s.add_argument('--store',required=True)
  54     for arg in ('tenant','subject','run'):s.add_argument('--'+arg,required=True)
  55     s.add_argument('--output',required=True);s.add_argument('--max-attempts',type=int,default=8);s.add_argument('--max-pages',type=int,default=5)
  56     s.add_argument('--probes',action='store_true')
  57     r=sub.add_parser('replay');r.add_argument('--store',required=True);r.add_argument('--rules',required=True);r.add_argument('--tenant',required=True)
  58     r.add_argument('--capture-run',required=True);r.add_argument('--evaluation-run',required=True);r.add_argument('--as-of',required=True);r.add_argument('--output',required=True)
  59     q=sub.add_parser('claims');q.add_argument('--store',required=True);q.add_argument('--tenant',required=True);q.add_argument('--as-of',required=True);q.add_argument('--rules',required=True)
  60     q=sub.add_parser('candidates');q.add_argument('--store',required=True);q.add_argument('--tenant',required=True);q.add_argument('--min-hosts',type=int,default=3)
  61     i=sub.add_parser('import-donor');i.add_argument('--input',required=True);i.add_argument('--vendor-map',required=True);i.add_argument('--output',required=True);i.add_argument('--report',required=True)
  62     a=sub.add_parser('analyze-file');a.add_argument('--html',required=True);a.add_argument('--url',required=True);a.add_argument('--observed-at',required=True)
  63     for arg in ('tenant','subject','run','rules','store','output'):a.add_argument('--'+arg,required=True)
  64     v=sub.add_parser('check');v.add_argument('bundle');v.add_argument('--store')
  65     args=p.parse_args(argv)
  66     try:
```

```text
 100                     cap=store.put_capture(tenant_id=args.tenant,subject_id=args.subject,run_id=args.run,url=url,observed_at=args.observed_at,body=body,headers={'content-type':'text/html'},source_id='source:user-provided-snapshot')
 101                     bundle=Scanner(store,pack,FixtureTransport({}),production=not pack.fixture_only).evaluate([extract(cap,body)],args.run,args.observed_at)
 102                     write_json(args.output,bundle);result={'bundle':args.output,'claims':len(bundle['claims']),'network_requests':0,'timestamp_is_user_supplied':True}
 103                 elif args.command=='candidates':result=store.candidates(args.tenant,args.min_hosts)
 104                 elif args.command=='claims':
 105                     pack=RulePack.load(args.rules)
 106                     result=[asdict(c) for c in store.stored_claims(args.tenant,as_of=args.as_of,allowed_rule_digests={r.digest for r in pack.rules if r.status=='APPROVED'})]
 107                 elif args.command=='replay':
 108                     pack=RulePack.load(args.rules)
 109                     # Replay never invokes this deliberately unusable transport.
 110                     runner=Scanner(store,pack,FixtureTransport({}),production=not pack.fixture_only)
 111                     result=runner.replay(args.tenant,args.capture_run,args.evaluation_run,args.as_of)
 112                     write_json(args.output,result);result={'bundle':args.output,'claims':len(result['claims'])}
 113                 else:
 114                     # Missing dependencies are a CLI error, not a successful empty scan.
 115                     try:
 116                         from scrapling.fetchers import FetcherSession
 117                     except ImportError as exc:
 118                         raise DependencyUnavailable('Scrapling live extra missing; pip install -e ".[live]"') from exc
 119                     pack=RulePack.load(args.rules)
 120                     if pack.fixture_only:raise ContractError('Fixture-only release cannot be used for a live scan')
 121                     url=normalize_url(args.url)
 122                     transport=ScraplingTransport(NetworkPolicy((origin(url),)))
 123                     config=ScanConfig(args.tenant,args.subject,args.run,max_attempts=args.max_attempts,max_pages=args.max_pages,probe_paths=args.probes)
 124                     bundle=Scanner(store,pack,transport).scan(url,config)
 125                     write_json(args.output,bundle)
 126                     result={'bundle':args.output,'claims':len(bundle['claims']),'send_allowed':False}
 127             finally:store.close()
 128         print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
 129         return 0
```

## `canonical/keensight_contracts/engine.py`

SHA-256: `961348d78234df4952125dc7806a41e43cc6e5d8080fc50c126aa44cfd1f0d0c`

```text
  24     return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=invalid)
  25 
  26 def canonical(value: Any) -> bytes:
  27     # Python reference format, not an assertion of RFC 8785/cross-language hashing.
  28     return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
  29 
  30 def digest(value: Any) -> str:
  31     return 'sha256:'+sha256(value if isinstance(value,bytes) else canonical(value)).hexdigest()
  32 
  33 def instant(value: str) -> datetime:
  34     require(value.endswith('Z'),'TIMESTAMP_MUST_BE_UTC')
  35     return datetime.fromisoformat(value[:-1]+'+00:00')
  36 
  37 def claim_key(fact: dict) -> tuple:
  38     """Nature is part of the claim channel; source identity remains on observations.
  39 
  40     Reports never silently overwrite direct observations. Measurement targets include
  41     provider/method/dimensions; PERIOD windows distinguish distinct measurements.
  42     """
  43     return (fact['tenant_id'],fact['subject_id'],fact['predicate_id'],fact['nature'],
  44             fact['scope_id'],canonical(fact['target']).decode(),canonical(fact['window']).decode())
```

```text
  86 def resolve_claim(facts: list[dict],as_of: str,eligible) -> dict:
  87     """Conservative reference: unknowns do not erase known facts; ties abstain.
  88 
  89     Explicit supersession removes only named prior observations. Different reports
  90     remain a conflict unless a separately approved resolution policy decides it.
  91     """
  92     require(bool(facts),'EMPTY_CLAIM')
  93     require(len({claim_key(f) for f in facts})==1,'MIXED_CLAIM_IDENTITIES')
  94     removed={f['supersedes_fact_id'] for f in facts if f['supersedes_fact_id'] and f['state']!='UNKNOWN' and eligible(f,as_of)}
  95     candidates=[f for f in facts if f['fact_id'] not in removed and f['state']!='UNKNOWN' and eligible(f,as_of)]
  96     values={canonical((f['state'],f['object'])) for f in candidates}
  97     return {'status':'UNKNOWN' if not values else ('KNOWN' if len(values)==1 else 'CONFLICT'),
  98             'accepted_fact_ids':sorted(f['fact_id'] for f in candidates) if len(values)==1 else []}
```
