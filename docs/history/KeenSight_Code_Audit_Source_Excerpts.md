# Audited source excerpts

All line numbers below refer to the unchanged extracted input archives. Context is preserved; these excerpts are not patches.

## C01 — Capture metadata is not bound to the stored authoritative record

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/storage.py:122–131`

```python
 122 |     def body(self, cap: Capture) -> bytes:
 123 |         if self.db.execute('SELECT 1 FROM revoked_captures WHERE tenant=? AND capture_id=?',(cap.tenant_id,cap.capture_id)).fetchone():
 124 |             raise ContractError('Capture is revoked')
 125 |         expected=Path('blobs')/identity('tenant',cap.tenant_id)/cap.body_sha256[:2]/cap.body_sha256
 126 |         if str(expected)!=cap.body_path:
 127 |             raise ContractError('Blob path does not match tenant and digest')
 128 |         body=(self.root/expected).read_bytes()
 129 |         if hashlib.sha256(body).hexdigest()!=cap.body_sha256:
 130 |             raise ContractError('Evidence hash mismatch')
 131 |         return body
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/cli.py:69–86`

```python
  69 |         elif args.command=='check':
  70 |             from .validation import validate_bundle
  71 |             data=strict_json(Path(args.bundle).read_text());validate_bundle(data)
  72 |             if args.store:
  73 |                 from .core import Capture
  74 |                 from .extraction import extract
  75 |                 from .core import canonical
  76 |                 store=Store(args.store)
  77 |                 try:
  78 |                     for raw in data['captures']:
  79 |                         cap=Capture(**raw);body=store.body(cap)
  80 |                         present=[s for s in data['surfaces'] if s['capture_id']==cap.capture_id]
  81 |                         if present:
  82 |                             actual=[asdict(s) for s in extract(cap,body).surfaces]
  83 |                             if sorted(map(canonical,present))!=sorted(map(canonical,actual)):
  84 |                                 raise ContractError('Surface extraction does not reproduce from original bytes')
  85 |                 finally:store.close()
  86 |             result={'valid':True,'original_bytes_checked':bool(args.store)}
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/validation.py:23–41`

```python
  23 |     caps={c['capture_id']:Capture(**c) for c in data['captures']}
  24 |     surfaces={s['surface_id']:s for s in data['surfaces']}
  25 |     for cap in caps.values():
  26 |         if instant(cap.observed_at)>instant(data['as_of']): raise ContractError('Future capture input')
  27 |     for s in surfaces.values():
  28 |         if s['capture_id'] not in caps: raise ContractError('Surface capture is missing')
  29 |     matches=[Match(**m) for m in data['matches']]
  30 |     for m in matches:
  31 |         if m.surface_id not in surfaces or surfaces[m.surface_id]['capture_id']!=m.capture_id:
  32 |             raise ContractError('Match does not point to its actual capture/surface')
  33 |         if m.release_digest!=data['release_digest']:
  34 |             raise ContractError('Mixed rule releases in evaluation')
  35 |     pages=[]
  36 |     for cid,cap in caps.items():
  37 |         ss=[Surface(**s) for s in data['surfaces'] if s['capture_id']==cid]
  38 |         if ss: pages.append(PageEvidence(cap,ss,[]))
  39 |     expected_matches,_=match_pages(pack,pages)
  40 |     if sorted(map(canonical,map(record,expected_matches)))!=sorted(map(canonical,data['matches'])):
  41 |         raise ContractError('Matches do not reproduce from pinned rules and surfaces')
```

## C02 — Successful claim output can contradict failed producer diagnostics

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/validation.py:35–52`

```python
  35 |     pages=[]
  36 |     for cid,cap in caps.items():
  37 |         ss=[Surface(**s) for s in data['surfaces'] if s['capture_id']==cid]
  38 |         if ss: pages.append(PageEvidence(cap,ss,[]))
  39 |     expected_matches,_=match_pages(pack,pages)
  40 |     if sorted(map(canonical,map(record,expected_matches)))!=sorted(map(canonical,data['matches'])):
  41 |         raise ContractError('Matches do not reproduce from pinned rules and surfaces')
  42 |     obs=[Observation(**o) for o in data['observations']]
  43 |     expected,links=observation_candidates(caps.values(),matches)
  44 |     if sorted(map(canonical,map(record,expected)))!=sorted(map(canonical,data['observations'])):
  45 |         raise ContractError('Observation target, identity, provenance or value is inconsistent')
  46 |     if sorted(map(canonical,map(record,links)))!=sorted(map(canonical,data['support_links'])):
  47 |         raise ContractError('Missing, duplicate or fabricated support link')
  48 |     views=resolve_claims(obs,matches,links,caps.values(),as_of=data['as_of'])
  49 |     if sorted(map(canonical,map(record,views)))!=sorted(map(canonical,data['claims'])):
  50 |         raise ContractError('Claim view does not recompute from its evidence')
  51 |     if set(c['command_id'] for c in data['commands'])!=set(COMMANDS):
  52 |         raise ContractError('Command manifest must account for all 38 IDs')
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:177–213`

```python
 177 |         commands=list(commands or [])
 178 |         for p in pages: commands.extend(p.commands)
 179 |         caps=captures if captures is not None else [p.capture for p in pages]
 180 |         if any(instant(c.observed_at)>instant(as_of) for c in caps):
 181 |             raise ContractError('Evaluation cutoff precedes an input capture')
 182 |         matches,rule_evaluations=match_pages(self.pack,pages,production=self.production)
 183 |         observations,links=observation_candidates([p.capture for p in pages],matches)
 184 |         if pages:
 185 |             self.store.save_findings(pages[0].capture.tenant_id,matches,observations,links)
 186 |             self.store.harvest(pages[0].capture.tenant_id,pages,matched_surface_ids={m.surface_id for m in matches if m.authority=='APPROVED'})
 187 |         views=resolve_claims(observations,matches,links,[p.capture for p in pages],as_of=as_of)
 188 |         for operator in sorted({r.operator for r in self.pack.rules}):
 189 |             mids=[m.match_id for m in matches if next(r for r in self.pack.rules if r.rule_id==m.rule_id).operator==operator]
 190 |             commands.append(CommandResult(MATCH_COMMAND[operator],'COMPLETE',output_ids=mids))
 191 |         if any(len(r.patterns)>1 for r in self.pack.rules):
 192 |             commands.append(CommandResult('MATCH_OR_GROUP','COMPLETE',details={'semantics':'ANY alternative; all matched branches retained'}))
 193 |         commands.extend([
 194 |             CommandResult('DISCOVER_CANONICAL','COMPLETE',details={'claims':canonical_claims(pages)}),
 195 |             CommandResult('ROLLUP_HOST','COMPLETE',details={'captures':len(pages),'scope':'exact tenant/subject/origin; modes remain separate claim scopes'}),
 196 |             CommandResult('GATE_AND','COMPLETE',details={'qualifications':{r['rule_id']:r.get('qualification') for r in rule_evaluations}}),
 197 |             CommandResult('GATE_SCHEMA','COMPLETE',details={'meaning':'supporting type only; JSONLD subject identity is not assumed'}),
 198 |         ])
 199 |         text='\n'.join(s.value for p in pages for s in p.surfaces if s.kind=='prose').casefold()
 200 |         negatives=[term for term in self.pack.raw.get('negative_terms',[]) if term.casefold() in text]
 201 |         commands.append(CommandResult('GATE_NEGATIVE','COMPLETE',details={'deprioritize':bool(negatives),'terms':negatives,'facts_deleted':False}))
 202 |         supported={v.claim_key for v in views if v.status=='SUPPORTED' and v.predicate=='vendor.present'}
 203 |         score=min(100,10*len(supported)) if not negatives else 0
 204 |         commands.append(CommandResult('SCORE_HOST','COMPLETE',details={'policy':'prototype-unique-supported-presence-v1','score':score,'is_probability':False,'calibrated':False}))
 205 |         commands.append(CommandResult('EMIT','COMPLETE',details={'kind':'ScanBundle','canonical_fact_admission':'NOT_PERFORMED'}))
 206 |         data={'schema_version':'1.0','producer':'keensight-scrapling-ingestion/0.1.0','evaluation_id':evaluation_id,'as_of':as_of,
 207 |               'release_digest':self.pack.digest,'rule_pack':self.pack.raw,'fixture_only':self.pack.fixture_only,'send_allowed':False,
 208 |               'captures':[asdict(c) for c in sorted(caps,key=lambda x:x.capture_id)],
 209 |               'surfaces':[asdict(s) for p in pages for s in p.surfaces],
 210 |               'matches':[asdict(m) for m in matches],'observations':[asdict(o) for o in observations],
 211 |               'support_links':[asdict(x) for x in links],'claims':[asdict(v) for v in views],
 212 |               'rule_evaluations':rule_evaluations,'commands':[asdict(c) for c in complete_command_manifest(commands)],
 213 |               'resource_dispositions':dispositions or [],'priority_score':score,
```

## C03 — Failed evaluation can publish supported findings to SQLite

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:177–213`

```python
 177 |         commands=list(commands or [])
 178 |         for p in pages: commands.extend(p.commands)
 179 |         caps=captures if captures is not None else [p.capture for p in pages]
 180 |         if any(instant(c.observed_at)>instant(as_of) for c in caps):
 181 |             raise ContractError('Evaluation cutoff precedes an input capture')
 182 |         matches,rule_evaluations=match_pages(self.pack,pages,production=self.production)
 183 |         observations,links=observation_candidates([p.capture for p in pages],matches)
 184 |         if pages:
 185 |             self.store.save_findings(pages[0].capture.tenant_id,matches,observations,links)
 186 |             self.store.harvest(pages[0].capture.tenant_id,pages,matched_surface_ids={m.surface_id for m in matches if m.authority=='APPROVED'})
 187 |         views=resolve_claims(observations,matches,links,[p.capture for p in pages],as_of=as_of)
 188 |         for operator in sorted({r.operator for r in self.pack.rules}):
 189 |             mids=[m.match_id for m in matches if next(r for r in self.pack.rules if r.rule_id==m.rule_id).operator==operator]
 190 |             commands.append(CommandResult(MATCH_COMMAND[operator],'COMPLETE',output_ids=mids))
 191 |         if any(len(r.patterns)>1 for r in self.pack.rules):
 192 |             commands.append(CommandResult('MATCH_OR_GROUP','COMPLETE',details={'semantics':'ANY alternative; all matched branches retained'}))
 193 |         commands.extend([
 194 |             CommandResult('DISCOVER_CANONICAL','COMPLETE',details={'claims':canonical_claims(pages)}),
 195 |             CommandResult('ROLLUP_HOST','COMPLETE',details={'captures':len(pages),'scope':'exact tenant/subject/origin; modes remain separate claim scopes'}),
 196 |             CommandResult('GATE_AND','COMPLETE',details={'qualifications':{r['rule_id']:r.get('qualification') for r in rule_evaluations}}),
 197 |             CommandResult('GATE_SCHEMA','COMPLETE',details={'meaning':'supporting type only; JSONLD subject identity is not assumed'}),
 198 |         ])
 199 |         text='\n'.join(s.value for p in pages for s in p.surfaces if s.kind=='prose').casefold()
 200 |         negatives=[term for term in self.pack.raw.get('negative_terms',[]) if term.casefold() in text]
 201 |         commands.append(CommandResult('GATE_NEGATIVE','COMPLETE',details={'deprioritize':bool(negatives),'terms':negatives,'facts_deleted':False}))
 202 |         supported={v.claim_key for v in views if v.status=='SUPPORTED' and v.predicate=='vendor.present'}
 203 |         score=min(100,10*len(supported)) if not negatives else 0
 204 |         commands.append(CommandResult('SCORE_HOST','COMPLETE',details={'policy':'prototype-unique-supported-presence-v1','score':score,'is_probability':False,'calibrated':False}))
 205 |         commands.append(CommandResult('EMIT','COMPLETE',details={'kind':'ScanBundle','canonical_fact_admission':'NOT_PERFORMED'}))
 206 |         data={'schema_version':'1.0','producer':'keensight-scrapling-ingestion/0.1.0','evaluation_id':evaluation_id,'as_of':as_of,
 207 |               'release_digest':self.pack.digest,'rule_pack':self.pack.raw,'fixture_only':self.pack.fixture_only,'send_allowed':False,
 208 |               'captures':[asdict(c) for c in sorted(caps,key=lambda x:x.capture_id)],
 209 |               'surfaces':[asdict(s) for p in pages for s in p.surfaces],
 210 |               'matches':[asdict(m) for m in matches],'observations':[asdict(o) for o in observations],
 211 |               'support_links':[asdict(x) for x in links],'claims':[asdict(v) for v in views],
 212 |               'rule_evaluations':rule_evaluations,'commands':[asdict(c) for c in complete_command_manifest(commands)],
 213 |               'resource_dispositions':dispositions or [],'priority_score':score,
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/storage.py:133–148`

```python
 133 |     def save_findings(self, tenant: str, matches: list[Match], observations: list[Observation], links: list[SupportLink]):
 134 |         from .claims import resolve_claims
 135 |         capids={m.capture_id for m in matches}|{o.capture_id for o in observations}
 136 |         caps=[]
 137 |         for cid in capids:
 138 |             row=self.db.execute('SELECT payload FROM captures WHERE tenant=? AND id=?',(tenant,cid)).fetchone()
 139 |             if not row: raise ContractError('Unknown or cross-tenant capture')
 140 |             caps.append(Capture(**strict_json(row['payload'])))
 141 |         if any(o.tenant_id!=tenant for o in observations): raise ContractError('Cross-tenant observation')
 142 |         if observations:
 143 |             resolve_claims(observations,matches,links,caps,as_of=max(o.observed_at for o in observations))
 144 |         with self.db:
 145 |             for m in matches: self._immutable('matches',tenant,m.match_id,asdict(m),('capture_id',),(m.capture_id,))
 146 |             for o in observations: self._immutable('observations',tenant,o.observation_id,asdict(o),('capture_id','claim_key'),(o.capture_id,o.claim_key))
 147 |             for link in links:
 148 |                 self.db.execute('INSERT OR IGNORE INTO support VALUES(?,?,?)',(tenant,link.observation_id,link.match_id))
```

## C04 — Replay does not preserve live capture eligibility

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:104–170`

```python
 104 |                 commands.append(CommandResult(command,'FAILED',limitations=[reason],details=payload))
 105 |                 dispositions.append({'url':target,'status':'FAILED','reason':reason})
 106 |                 return None
 107 |         robots_url=base+'/robots.txt'
 108 |         rc=request(robots_url,'FETCH_ROBOTS')
 109 |         rp,maps,reason=robots_policy(robots_url,rc.status_code,self.store.body(rc),rc.complete) if rc else (None,[],'ROBOTS_UNAVAILABLE_FAIL_CLOSED')
 110 |         if rp is None:
 111 |             commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=[reason]))
 112 |             return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
 113 |         crawl_delay=rp.crawl_delay('KeenSightResearch') or rp.crawl_delay('*') or 0
 114 |         request_rate=rp.request_rate('KeenSightResearch') or rp.request_rate('*')
 115 |         delay=max(delay,crawl_delay,(request_rate.seconds/request_rate.requests) if request_rate and request_rate.requests else 0)
 116 |         if delay>60:
 117 |             commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=['ROBOTS_DELAY_EXCEEDS_BATCH_WAIT_POLICY']))
 118 |             return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
 119 |         queue=deque([(seed,'page',0)])
 120 |         queue.extend((u,'sitemap',0) for u in [*maps,base+'/sitemap.xml'] if origin(u)==base)
 121 |         if config.probe_paths: queue.extend((base+p,'probe',0) for p in WELL_KNOWN)
 122 |         seen=set();sitemap_count=0
 123 |         while queue:
 124 |             target,kind,depth=queue.popleft()
 125 |             try: target=normalize_url(target)
 126 |             except ValueError: continue
 127 |             if target in seen: continue
 128 |             seen.add(target)
 129 |             if denied:
 130 |                 dispositions.append({'url':target,'status':'SKIPPED_RATE_LIMIT'}); continue
 131 |             if kind=='sitemap' and (sitemap_count>=config.max_sitemaps or depth>2):
 132 |                 dispositions.append({'url':target,'status':'SKIPPED_SITEMAP_LIMIT'});continue
 133 |             if kind!='sitemap' and len(pages)>=config.max_pages:
 134 |                 dispositions.append({'url':target,'status':'SKIPPED_PAGE_LIMIT'});continue
 135 |             if origin(target)!=base or not rp.can_fetch('KeenSightResearch',target):
 136 |                 dispositions.append({'url':target,'status':'SKIPPED_POLICY'});continue
 137 |             command='FETCH_SITEMAP' if kind=='sitemap' else 'FETCH_WELL_KNOWN' if kind=='probe' else 'FETCH_STATIC'
 138 |             cap=request(target,command)
 139 |             if not cap: continue
 140 |             if 300<=cap.status_code<400:
 141 |                 redirect=link_url(cap.url,cap.headers.get('location',''))
 142 |                 if redirect and origin(redirect)==base:
 143 |                     queue.appendleft((redirect,kind,depth))
 144 |                 else: dispositions.append({'url':target,'status':'REDIRECT_OUT_OF_SCOPE'})
 145 |                 continue
 146 |             if cap.status_code!=200 or not cap.complete:
 147 |                 dispositions.append({'url':target,'status':'NOT_USABLE','http_status':cap.status_code});continue
 148 |             body=self.store.body(cap)
 149 |             if kind=='sitemap':
 150 |                 sitemap_count+=1
 151 |                 try:
 152 |                     discovered,truncated=sitemap_urls(body,target)
 153 |                     queue.extend((u,t,depth+1 if t=='sitemap' else 0) for t,u in discovered)
 154 |                     commands[-1].details['declared_url_count']=len(discovered)
 155 |                     if truncated: commands[-1].limitations.append('SITEMAP_ENTRY_LIMIT')
 156 |                 except ContractError as exc:
 157 |                     commands[-1].status='PARTIAL';commands[-1].limitations.append(str(exc))
 158 |                 continue
 159 |             ct=cap.headers.get('content-type','').lower()
 160 |             if not ('html' in ct or (not ct and body.lstrip().lower().startswith((b'<!doctype html',b'<html')))):
 161 |                 dispositions.append({'url':target,'status':'NON_HTML_ARTIFACT'});continue
 162 |             # Known access challenges do not become product observations.
 163 |             prefix=body[:200000].lower()
 164 |             if any(marker in prefix for marker in (b'<title>just a moment',b'<title>access denied',b'cf-chl-widget')):
 165 |                 dispositions.append({'url':target,'status':'CHALLENGE_NOT_USABLE'});continue
 166 |             page=extract(cap,body);pages.append(page)
 167 |             if config.render_empty_shell and len(pages)<config.max_pages and len(next((s.value for s in page.surfaces if s.kind=='prose'),''))<40:
 168 |                 rendered=request(target,'FETCH_STEALTH','RENDERED_DOM')
 169 |                 if rendered and rendered.complete and rendered.status_code==200:
 170 |                     pages.append(extract(rendered,self.store.body(rendered)))
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:215–229`

```python
 215 |         from .validation import validate_bundle
 216 |         data=strict_json(canonical(data))
 217 |         validate_bundle(data)
 218 |         return data
 219 | 
 220 |     def replay(self,tenant: str,capture_run_id: str,evaluation_id: str,as_of: str) -> dict:
 221 |         caps=self.store.captures(tenant,capture_run_id)
 222 |         if not caps: raise ContractError('Unknown capture run')
 223 |         pages=[]
 224 |         for c in caps:
 225 |             if c.status_code!=200 or not c.complete or 'html' not in c.headers.get('content-type','').lower(): continue
 226 |             body=self.store.body(c)
 227 |             if any(marker in body[:200000].lower() for marker in (b'<title>just a moment',b'<title>access denied',b'cf-chl-widget')): continue
 228 |             pages.append(extract(c,body))
 229 |         return self.evaluate(pages,evaluation_id,as_of,[CommandResult('CATALOG_LOAD','COMPLETE',details={'release_digest':self.pack.digest,'mode':'REPLAY'})],captures=caps)
```

## C05 — Incomplete or absent extraction is reported as ordinary NO_MATCH

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:55–75`

```python
  55 |     def add(command, kind, node, value, *, attrs=None, locator=None, context=None):
  56 |         if value is None:
  57 |             return
  58 |         result = results[command]
  59 |         if counts[command] >= max_items:
  60 |             result.status = 'PARTIAL'
  61 |             if 'ITEM_LIMIT' not in result.limitations:
  62 |                 result.limitations.append('ITEM_LIMIT')
  63 |             return
  64 |         value = str(value)
  65 |         if len(value) > max_text:
  66 |             value = value[:max_text]
  67 |             result.status = 'PARTIAL'
  68 |             if 'TEXT_LIMIT' not in result.limitations:
  69 |                 result.limitations.append('TEXT_LIMIT')
  70 |         loc = locator or (tree.getpath(node) if node is not None else kind)
  71 |         s = Surface(identity('surface', capture.capture_id, command, kind, loc, value, attrs or {}),
  72 |                     capture.capture_id, command, kind, loc, value,
  73 |                     context or (region(node) if node is not None else 'PAGE'), attrs or {})
  74 |         surfaces.append(s)
  75 |         counts[command] += 1
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:149–180`

```python
 149 |         for page in pages:
 150 |             if not page.capture.complete:
 151 |                 limited.append(page.capture.capture_id)
 152 |             for s in page.surfaces:
 153 |                 if s.kind not in rule.kinds or (rule.selector and not s.locator.startswith(rule.selector)):
 154 |                     continue
 155 |                 if rule.predicate=='vendor.present' and s.context in {'FOOTER','NOSCRIPT','INERT_TEMPLATE'}:
 156 |                     continue
 157 |                 if rule.predicate=='vendor.present' and s.kind=='link_url' and 'stylesheet' not in s.attributes.get('rel','').split():
 158 |                     continue
 159 |                 value = s.value if rule.field=='value' else str(s.attributes.get(rule.field,''))
 160 |                 for pattern in rule.patterns:
 161 |                     try:
 162 |                         if rule.operator in {'host_suffix','host_equals'}:
 163 |                             hit = host_match(value,pattern,exact=rule.operator=='host_equals')
 164 |                         elif rule.operator=='equals': hit = value.casefold()==pattern.casefold()
 165 |                         elif rule.operator=='regex': hit = bool(regex.search(pattern,value[:131072],timeout=0.025))
 166 |                         elif rule.operator=='image_alt': hit = pattern.casefold() in str(s.attributes.get('alt','')).casefold()
 167 |                         else: hit = pattern.casefold() in value.casefold()
 168 |                     except TimeoutError:
 169 |                         errors.append({'capture_id':page.capture.capture_id,'reason':'REGEX_TIMEOUT'})
 170 |                         continue
 171 |                     if hit:
 172 |                         authority = 'APPROVED' if rule.status=='APPROVED' else 'CANDIDATE'
 173 |                         mid = identity('match',rule.digest,pack.digest,page.capture.capture_id,s.surface_id,pattern)
 174 |                         matches.append(Match(mid,rule.rule_id,rule.digest,pack.digest,authority,page.capture.capture_id,s.surface_id,pattern,rule.predicate,rule.product_id,True,identity('evidence',page.capture.capture_id,s.locator),identity('rule_evidence',rule.digest,page.capture.capture_id,s.surface_id,pattern),rule.confidence))
 175 |                         found.append(mid)
 176 |         if errors:
 177 |             matches = matches[:start]
 178 |             found = []
 179 |         evaluations.append({'rule_id':rule.rule_id,'status':'ERROR' if errors else 'PARTIAL' if limited else 'MATCH' if found else 'NO_MATCH',
 180 |                             'match_ids':found,'errors':errors,'incomplete_capture_ids':sorted(set(limited)), 'qualification':qualification,
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:177–213`

```python
 177 |         commands=list(commands or [])
 178 |         for p in pages: commands.extend(p.commands)
 179 |         caps=captures if captures is not None else [p.capture for p in pages]
 180 |         if any(instant(c.observed_at)>instant(as_of) for c in caps):
 181 |             raise ContractError('Evaluation cutoff precedes an input capture')
 182 |         matches,rule_evaluations=match_pages(self.pack,pages,production=self.production)
 183 |         observations,links=observation_candidates([p.capture for p in pages],matches)
 184 |         if pages:
 185 |             self.store.save_findings(pages[0].capture.tenant_id,matches,observations,links)
 186 |             self.store.harvest(pages[0].capture.tenant_id,pages,matched_surface_ids={m.surface_id for m in matches if m.authority=='APPROVED'})
 187 |         views=resolve_claims(observations,matches,links,[p.capture for p in pages],as_of=as_of)
 188 |         for operator in sorted({r.operator for r in self.pack.rules}):
 189 |             mids=[m.match_id for m in matches if next(r for r in self.pack.rules if r.rule_id==m.rule_id).operator==operator]
 190 |             commands.append(CommandResult(MATCH_COMMAND[operator],'COMPLETE',output_ids=mids))
 191 |         if any(len(r.patterns)>1 for r in self.pack.rules):
 192 |             commands.append(CommandResult('MATCH_OR_GROUP','COMPLETE',details={'semantics':'ANY alternative; all matched branches retained'}))
 193 |         commands.extend([
 194 |             CommandResult('DISCOVER_CANONICAL','COMPLETE',details={'claims':canonical_claims(pages)}),
 195 |             CommandResult('ROLLUP_HOST','COMPLETE',details={'captures':len(pages),'scope':'exact tenant/subject/origin; modes remain separate claim scopes'}),
 196 |             CommandResult('GATE_AND','COMPLETE',details={'qualifications':{r['rule_id']:r.get('qualification') for r in rule_evaluations}}),
 197 |             CommandResult('GATE_SCHEMA','COMPLETE',details={'meaning':'supporting type only; JSONLD subject identity is not assumed'}),
 198 |         ])
 199 |         text='\n'.join(s.value for p in pages for s in p.surfaces if s.kind=='prose').casefold()
 200 |         negatives=[term for term in self.pack.raw.get('negative_terms',[]) if term.casefold() in text]
 201 |         commands.append(CommandResult('GATE_NEGATIVE','COMPLETE',details={'deprioritize':bool(negatives),'terms':negatives,'facts_deleted':False}))
 202 |         supported={v.claim_key for v in views if v.status=='SUPPORTED' and v.predicate=='vendor.present'}
 203 |         score=min(100,10*len(supported)) if not negatives else 0
 204 |         commands.append(CommandResult('SCORE_HOST','COMPLETE',details={'policy':'prototype-unique-supported-presence-v1','score':score,'is_probability':False,'calibrated':False}))
 205 |         commands.append(CommandResult('EMIT','COMPLETE',details={'kind':'ScanBundle','canonical_fact_admission':'NOT_PERFORMED'}))
 206 |         data={'schema_version':'1.0','producer':'keensight-scrapling-ingestion/0.1.0','evaluation_id':evaluation_id,'as_of':as_of,
 207 |               'release_digest':self.pack.digest,'rule_pack':self.pack.raw,'fixture_only':self.pack.fixture_only,'send_allowed':False,
 208 |               'captures':[asdict(c) for c in sorted(caps,key=lambda x:x.capture_id)],
 209 |               'surfaces':[asdict(s) for p in pages for s in p.surfaces],
 210 |               'matches':[asdict(m) for m in matches],'observations':[asdict(o) for o in observations],
 211 |               'support_links':[asdict(x) for x in links],'claims':[asdict(v) for v in views],
 212 |               'rule_evaluations':rule_evaluations,'commands':[asdict(c) for c in complete_command_manifest(commands)],
 213 |               'resource_dispositions':dispositions or [],'priority_score':score,
```

## C06 — Resume forgets rate-limit state

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:46–96`

```python
  46 |         if production and pack.fixture_only:
  47 |             raise ContractError('Fixture-only rules are forbidden in production before capture')
  48 |         self.store=store;self.pack=pack;self.transport=transport
  49 |         self.browser=browser or ScraplingBrowserTransport();self.clock=clock;self.production=production
  50 | 
  51 |     def scan(self,url: str,config: ScanConfig) -> dict:
  52 |         seed=normalize_url(url); base=origin(seed)
  53 |         cfg={**asdict(config),'seed':seed,'release_digest':self.pack.digest,'code_version':'0.1.0'}
  54 |         self.store.begin_run(config.tenant_id,config.run_id,cfg)
  55 |         commands=[CommandResult('CATALOG_LOAD','COMPLETE',details={'release_digest':self.pack.digest}),
  56 |                   CommandResult('NORM_URL','COMPLETE',details={'seed':seed})]
  57 |         dispositions=[];pages=[];allcaps={}; denied=False
  58 |         delay=config.min_delay_seconds; last_request=None
  59 |         # Stored attempts are reused; PENDING means crash uncertainty and is not retried.
  60 |         def request(target,command,mode='RAW_HTML'):
  61 |             nonlocal denied,last_request
  62 |             if origin(target)!=base:
  63 |                 dispositions.append({'url':target,'status':'SKIPPED_POLICY','reason':'CROSS_ORIGIN'})
  64 |                 return None
  65 |             key=identity('request',target,mode)
  66 |             attempt=self.store.reserve_attempt(config.tenant_id,config.run_id,key,config.max_attempts,{'url':target,'command_id':command,'started_at':self.clock(),'mode':mode})
  67 |             if not attempt['new']:
  68 |                 if attempt['status']=='COMPLETE' and 'capture_id' in attempt['payload']:
  69 |                     cap=next((c for c in self.store.captures(config.tenant_id,config.run_id) if c.capture_id==attempt['payload']['capture_id']),None)
  70 |                     if cap:
  71 |                         allcaps[cap.capture_id]=cap
  72 |                         commands.append(CommandResult(command,'REUSED',[cap.capture_id],details={'url':target}))
  73 |                         return cap
  74 |                 reason='INTERRUPTED_ATTEMPT_NO_BLIND_RETRY' if attempt['status']=='PENDING' else attempt['status']
  75 |                 dispositions.append({'url':target,'status':reason})
  76 |                 commands.append(CommandResult(command,reason,details={'url':target}))
  77 |                 return None
  78 |             try:
  79 |                 if not getattr(self.transport,'is_fixture',False):
  80 |                     if last_request is not None:
  81 |                         time.sleep(max(0,delay-(time.monotonic()-last_request)))
  82 |                     last_request=time.monotonic()
  83 |                 reply=(self.browser if mode=='RENDERED_DOM' else self.transport).get(target)
  84 |                 if normalize_url(reply.url)!=target:
  85 |                     raise ContractError('Unrecorded redirect from transport')
  86 |                 data=reply.body[:config.max_body_bytes]
  87 |                 complete=reply.complete and len(reply.body)<=config.max_body_bytes
  88 |                 limitations=list(reply.limitations)
  89 |                 if not complete: limitations.append('CAPTURE_INCOMPLETE')
  90 |                 cap=self.store.put_capture(tenant_id=config.tenant_id,subject_id=config.subject_id,run_id=config.run_id,
  91 |                                           url=target,observed_at=self.clock(),body=data,headers=reply.headers,status_code=reply.status_code,
  92 |                                           mode=mode,complete=complete,limitations=limitations,source_ttl_seconds=config.source_ttl_seconds,
  93 |                                           source_id='source:synthetic-fixture' if getattr(self.transport,'is_fixture',False) else 'source:public-website')
  94 |                 allcaps[cap.capture_id]=cap
  95 |                 payload={'url':target,'capture_id':cap.capture_id,'http_status':cap.status_code,'mode':mode,'finished_at':self.clock()}
  96 |                 self.store.finish_attempt(config.tenant_id,config.run_id,key,'COMPLETE',payload)
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:119–144`

```python
 119 |         queue=deque([(seed,'page',0)])
 120 |         queue.extend((u,'sitemap',0) for u in [*maps,base+'/sitemap.xml'] if origin(u)==base)
 121 |         if config.probe_paths: queue.extend((base+p,'probe',0) for p in WELL_KNOWN)
 122 |         seen=set();sitemap_count=0
 123 |         while queue:
 124 |             target,kind,depth=queue.popleft()
 125 |             try: target=normalize_url(target)
 126 |             except ValueError: continue
 127 |             if target in seen: continue
 128 |             seen.add(target)
 129 |             if denied:
 130 |                 dispositions.append({'url':target,'status':'SKIPPED_RATE_LIMIT'}); continue
 131 |             if kind=='sitemap' and (sitemap_count>=config.max_sitemaps or depth>2):
 132 |                 dispositions.append({'url':target,'status':'SKIPPED_SITEMAP_LIMIT'});continue
 133 |             if kind!='sitemap' and len(pages)>=config.max_pages:
 134 |                 dispositions.append({'url':target,'status':'SKIPPED_PAGE_LIMIT'});continue
 135 |             if origin(target)!=base or not rp.can_fetch('KeenSightResearch',target):
 136 |                 dispositions.append({'url':target,'status':'SKIPPED_POLICY'});continue
 137 |             command='FETCH_SITEMAP' if kind=='sitemap' else 'FETCH_WELL_KNOWN' if kind=='probe' else 'FETCH_STATIC'
 138 |             cap=request(target,command)
 139 |             if not cap: continue
 140 |             if 300<=cap.status_code<400:
 141 |                 redirect=link_url(cap.url,cap.headers.get('location',''))
 142 |                 if redirect and origin(redirect)==base:
 143 |                     queue.appendleft((redirect,kind,depth))
 144 |                 else: dispositions.append({'url':target,'status':'REDIRECT_OUT_OF_SCOPE'})
```

## C07 — Rule authorization digest excludes product-alias semantics

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:50–72`

```python
  50 |         if not isinstance(data, dict) or set(data) - {'schema_version','release_id','fixture_only','aliases','rules','negative_terms'}:
  51 |             raise ContractError('Unknown rule-pack fields')
  52 |         if data.get('schema_version') != '1.0' or not isinstance(data.get('release_id'), str) or not data['release_id']:
  53 |             raise ContractError('Invalid rule pack version or release ID')
  54 |         if not isinstance(data.get('fixture_only'), bool) or not isinstance(data.get('rules'), list):
  55 |             raise ContractError('Pack must explicitly declare fixture_only and rules')
  56 |         aliases = data.get('aliases', {})
  57 |         if not isinstance(aliases, dict) or any(not isinstance(k,str) or not isinstance(v,str) or not k or not v for k,v in aliases.items()):
  58 |             raise ContractError('Alias map must contain nonempty strings')
  59 |         def canonical_product(product):
  60 |             visited = set()
  61 |             while product in aliases:
  62 |                 if product in visited:
  63 |                     raise ContractError('Alias cycle')
  64 |                 visited.add(product)
  65 |                 product = aliases[product]
  66 |             return product
  67 |         for key in aliases:
  68 |             canonical_product(key)
  69 |         negative = data.get('negative_terms', [])
  70 |         if not isinstance(negative,list) or any(not isinstance(x,str) or not x for x in negative):
  71 |             raise ContractError('Invalid negative terms')
  72 |         ids, rules = set(), []
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:115–131`

```python
 115 |             if confidence is not None and (isinstance(confidence,bool) or not isinstance(confidence,(int,float)) or not 0 <= confidence <= 1):
 116 |                 raise ContractError('Invalid authored confidence')
 117 |             for prop in ('guard_terms','schema_types'):
 118 |                 if not isinstance(row.get(prop,[]),list) or any(not isinstance(x,str) or not x for x in row.get(prop,[])):
 119 |                     raise ContractError('Malformed guard')
 120 |             selector = row.get('selector')
 121 |             if selector is not None and (not isinstance(selector,str) or not selector or len(selector)>512):
 122 |                 raise ContractError('selector is a bounded literal XPath prefix, never executable code')
 123 |             rules.append(Rule(rid,identity('rule',row),status,pred,canonical_product(product),tuple(kinds),op,tuple(pats),f,selector,tuple(row.get('guard_terms',[])),tuple(row.get('schema_types',[])),confidence,row.get('source',{})))
 124 |         # Rule iteration order must not change evidence identities or the release hash.
 125 |         normalized = dict(data)
 126 |         normalized['rules'] = sorted(data['rules'],key=lambda r:r['id'])
 127 |         return cls(data['release_id'],identity('release',normalized),data['fixture_only'],sorted(rules,key=lambda r:r.rule_id),normalized)
 128 | 
 129 | 
 130 | def match_pages(pack: RulePack, pages: list[PageEvidence], *, production: bool = False) -> tuple[list[Match],list[dict]]:
 131 |     """Retain EVERY rule/surface/alternative hit. Deduplicate claims later."""
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/claims.py:57–86`

```python
  57 |         links[o.observation_id].add(m.match_id)
  58 |     groups = defaultdict(list)
  59 |     for o in obsmap.values():
  60 |         cap = caps.get(o.capture_id)
  61 |         if cap is None or (cap.tenant_id,cap.subject_id)!=(o.tenant_id,o.subject_id):
  62 |             raise ContractError('Observation has a missing or cross-account capture')
  63 |         if instant(o.observed_at) > now:
  64 |             continue
  65 |         groups[o.claim_key].append(o)
  66 |     views=[]
  67 |     for key, rows in sorted(groups.items()):
  68 |         eligible, all_matches, usable_rows, shadow = set(),set(),[],False
  69 |         for o in rows:
  70 |             mids = links[o.observation_id]
  71 |             all_matches.update(mids)
  72 |             cap = caps[o.capture_id]
  73 |             usable = (o.state=='OBSERVED' and cap.complete and o.capture_id not in revoked and instant(o.expires_at)>now)
  74 |             active = {mid for mid in mids if (allowed_rule_digests is None or matchmap[mid].rule_digest in allowed_rule_digests)}
  75 |             good = {mid for mid in active if matchmap[mid].authority=='APPROVED'} if usable else set()
  76 |             shadow |= bool(usable and active-good)
  77 |             if good:
  78 |                 eligible.update(good)
  79 |                 usable_rows.append(o)
  80 |         values = {canonical(o.object_value):o.object_value for o in usable_rows}
  81 |         status = 'CONFLICT' if len(values)>1 else 'SUPPORTED' if values else 'CANDIDATE' if shadow else 'UNKNOWN'
  82 |         views.append(ClaimView(key,rows[0].predicate,rows[0].target,status,next(iter(values.values())) if len(values)==1 else None,
  83 |                                sorted(o.observation_id for o in rows),sorted(all_matches),sorted(eligible),
  84 |                                sorted({matchmap[m].rule_id for m in all_matches}),len({o.capture_id for o in usable_rows}),
  85 |                                len({o.source_group for o in usable_rows}),len({matchmap[m].evidence_key for m in eligible})))
  86 |     return views
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/cli.py:102–109`

```python
 102 |                 elif args.command=='candidates':result=store.candidates(args.tenant,args.min_hosts)
 103 |                 elif args.command=='claims':
 104 |                     pack=RulePack.load(args.rules)
 105 |                     result=[asdict(c) for c in store.stored_claims(args.tenant,as_of=args.as_of,allowed_rule_digests={r.digest for r in pack.rules if r.status=='APPROVED'})]
 106 |                 elif args.command=='replay':
 107 |                     pack=RulePack.load(args.rules)
 108 |                     # Replay never invokes this deliberately unusable transport.
 109 |                     runner=Scanner(store,pack,FixtureTransport({}),production=not pack.fixture_only)
```

## C08 — HTTP character encoding is ignored by extraction

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:36–44`

```python
  36 | def extract(capture: Capture, body: bytes, *, max_items: int = 2000, max_text: int = 131072) -> PageEvidence:
  37 |     """Parse retained bytes deterministically. No network or adaptive selectors.
  38 | 
  39 |     lxml is an explicit parser backend, NOT a fallback HTTP client. Acquisition
  40 |     uses Scrapling. Static prose is not claimed to be computed browser visibility.
  41 |     """
  42 |     parser = html.HTMLParser(no_network=True, recover=True, huge_tree=False, remove_comments=False)
  43 |     try:
  44 |         root = html.document_fromstring(body or b'<html></html>', parser=parser)
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:78–84`

```python
  78 |     encoding = root.getroottree().docinfo.encoding or 'utf-8'
  79 |     try:
  80 |         source = body.decode(encoding, errors='replace')
  81 |     except LookupError:
  82 |         source = body.decode('utf-8', errors='replace')
  83 |     add('EXTRACT_RAW_HTML', 'raw_html', None, source, locator='retained-body:decoded', attrs={'encoding': encoding})
  84 |     results['EXTRACT_RAW_HTML'].details['original_body_sha256'] = capture.body_sha256
```

## C09 — Inert script contexts are not consistently modeled

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:93–99`

```python
  93 |         if tag == 'script':
  94 |             if el.get('src'):
  95 |                 value = link_url(base, el.get('src'))
  96 |                 if value:
  97 |                     add('EXTRACT_SCRIPT_SRC', 'script_url', el, value, locator=path+'/@src')
  98 |             elif el.get('type', '').lower() != 'application/ld+json':
  99 |                 add('EXTRACT_SCRIPT_INLINE', 'inline_script', el, el.text or '', attrs={'type': el.get('type', '')})
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:152–157`

```python
 152 |             for s in page.surfaces:
 153 |                 if s.kind not in rule.kinds or (rule.selector and not s.locator.startswith(rule.selector)):
 154 |                     continue
 155 |                 if rule.predicate=='vendor.present' and s.context in {'FOOTER','NOSCRIPT','INERT_TEMPLATE'}:
 156 |                     continue
 157 |                 if rule.predicate=='vendor.present' and s.kind=='link_url' and 'stylesheet' not in s.attributes.get('rel','').split():
```

### `architecture/keensight-architecture-v4.1/keensight_contracts/engine.py:110–139`

```python
 110 |         supported |= distinct_origins(artifacts[a] for a in matched)
 111 |     require(supported<=eligible,'SUPPORT_OUTSIDE_SAMPLE')
 112 |     unknown=distinct_origins(artifacts[d['artifact_id']] for d in decisions if d['status']=='UNCLASSIFIED')
 113 |     return {'support_count':len(supported),'eligible_count':len(eligible),'sample_share':len(supported)/len(eligible),'population_claim':False,
 114 |         'support_policy_id':sample['support_policy_id'],'classified_eligible_count':len(eligible-unknown),
 115 |         'unclassified_count':len(unknown),'denominator_definition':'ELIGIBLE_RETRIEVED_RECORDS_INCLUDING_UNCLASSIFIED'}
 116 | 
 117 | def matches_fingerprint(definition: dict,html: str) -> bool:
 118 |     """Narrow HTML fixture matcher; not a 2,500-signature library or live browser."""
 119 |     from html.parser import HTMLParser
 120 |     from urllib.parse import urlsplit
 121 |     require(definition['operator']=='SCRIPT_HOST','MATCHER_NOT_IMPLEMENTED')
 122 |     class Parser(HTMLParser):
 123 |         def __init__(self):super().__init__();self.stack=[];self.hit=False
 124 |         def handle_starttag(self,tag,attrs):
 125 |             if tag=='script' and not any(x in ['footer','aside'] for x in self.stack):
 126 |                 src=dict(attrs).get('src','')
 127 |                 try:host=(urlsplit('https:'+src if src.startswith('//') else src).hostname or '').lower().rstrip('.')
 128 |                 except ValueError:host=''
 129 |                 domain=definition['match_value'].lower().rstrip('.')
 130 |                 if host==domain or host.endswith('.'+domain):self.hit=True
 131 |             if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(tag)
 132 |         def handle_endtag(self,tag):
 133 |             if tag in self.stack:
 134 |                 while self.stack:
 135 |                     if self.stack.pop()==tag:break
 136 |     p=Parser();p.feed(html);p.close();return p.hit
 137 | 
 138 | 
 139 | def evaluate_requirements(definition: dict,facts: list[dict],subject_id: str,as_of: str,eligible) -> str:
```

## C10 — Malformed source inputs escape local quarantine/diagnostics

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:104–119`

```python
 104 |                 commands.append(CommandResult(command,'FAILED',limitations=[reason],details=payload))
 105 |                 dispositions.append({'url':target,'status':'FAILED','reason':reason})
 106 |                 return None
 107 |         robots_url=base+'/robots.txt'
 108 |         rc=request(robots_url,'FETCH_ROBOTS')
 109 |         rp,maps,reason=robots_policy(robots_url,rc.status_code,self.store.body(rc),rc.complete) if rc else (None,[],'ROBOTS_UNAVAILABLE_FAIL_CLOSED')
 110 |         if rp is None:
 111 |             commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=[reason]))
 112 |             return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
 113 |         crawl_delay=rp.crawl_delay('KeenSightResearch') or rp.crawl_delay('*') or 0
 114 |         request_rate=rp.request_rate('KeenSightResearch') or rp.request_rate('*')
 115 |         delay=max(delay,crawl_delay,(request_rate.seconds/request_rate.requests) if request_rate and request_rate.requests else 0)
 116 |         if delay>60:
 117 |             commands.append(CommandResult('FETCH_STATIC','SKIPPED_POLICY',limitations=['ROBOTS_DELAY_EXCEEDS_BATCH_WAIT_POLICY']))
 118 |             return self.evaluate([],config.run_id,self.clock(),commands,dispositions,list(allcaps.values()))
 119 |         queue=deque([(seed,'page',0)])
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/importer.py:38–47`

```python
  38 |     if not isinstance(vendor_map,dict) or any(not isinstance(k,str) or not isinstance(v,str) or not v for k,v in vendor_map.items()):
  39 |         raise ContractError('Explicit vendor mapping required')
  40 |     counts=Counter(row.get('id') for row in rows)
  41 |     imported=[];dispositions=[]
  42 |     for index,row in enumerate(rows):
  43 |         rid=row.get('id'); reason=None
  44 |         sig=row.get('signal',{}); meta=sig.get('metadata',{}) if isinstance(sig,dict) else {}
  45 |         match=meta.get('match',{}) if isinstance(meta,dict) else {}
  46 |         try:
  47 |             if not isinstance(rid,str) or not rid or counts[rid]>1: raise ContractError('MISSING_OR_DUPLICATE_ID')
```

## C11 — Priority and diagnostic reports are not reproducibly validated

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:197–213`

```python
 197 |             CommandResult('GATE_SCHEMA','COMPLETE',details={'meaning':'supporting type only; JSONLD subject identity is not assumed'}),
 198 |         ])
 199 |         text='\n'.join(s.value for p in pages for s in p.surfaces if s.kind=='prose').casefold()
 200 |         negatives=[term for term in self.pack.raw.get('negative_terms',[]) if term.casefold() in text]
 201 |         commands.append(CommandResult('GATE_NEGATIVE','COMPLETE',details={'deprioritize':bool(negatives),'terms':negatives,'facts_deleted':False}))
 202 |         supported={v.claim_key for v in views if v.status=='SUPPORTED' and v.predicate=='vendor.present'}
 203 |         score=min(100,10*len(supported)) if not negatives else 0
 204 |         commands.append(CommandResult('SCORE_HOST','COMPLETE',details={'policy':'prototype-unique-supported-presence-v1','score':score,'is_probability':False,'calibrated':False}))
 205 |         commands.append(CommandResult('EMIT','COMPLETE',details={'kind':'ScanBundle','canonical_fact_admission':'NOT_PERFORMED'}))
 206 |         data={'schema_version':'1.0','producer':'keensight-scrapling-ingestion/0.1.0','evaluation_id':evaluation_id,'as_of':as_of,
 207 |               'release_digest':self.pack.digest,'rule_pack':self.pack.raw,'fixture_only':self.pack.fixture_only,'send_allowed':False,
 208 |               'captures':[asdict(c) for c in sorted(caps,key=lambda x:x.capture_id)],
 209 |               'surfaces':[asdict(s) for p in pages for s in p.surfaces],
 210 |               'matches':[asdict(m) for m in matches],'observations':[asdict(o) for o in observations],
 211 |               'support_links':[asdict(x) for x in links],'claims':[asdict(v) for v in views],
 212 |               'rule_evaluations':rule_evaluations,'commands':[asdict(c) for c in complete_command_manifest(commands)],
 213 |               'resource_dispositions':dispositions or [],'priority_score':score,
```

### `collector/keensight-scrapling-ingestion/src/keensight_scrapling/validation.py:39–52`

```python
  39 |     expected_matches,_=match_pages(pack,pages)
  40 |     if sorted(map(canonical,map(record,expected_matches)))!=sorted(map(canonical,data['matches'])):
  41 |         raise ContractError('Matches do not reproduce from pinned rules and surfaces')
  42 |     obs=[Observation(**o) for o in data['observations']]
  43 |     expected,links=observation_candidates(caps.values(),matches)
  44 |     if sorted(map(canonical,map(record,expected)))!=sorted(map(canonical,data['observations'])):
  45 |         raise ContractError('Observation target, identity, provenance or value is inconsistent')
  46 |     if sorted(map(canonical,map(record,links)))!=sorted(map(canonical,data['support_links'])):
  47 |         raise ContractError('Missing, duplicate or fabricated support link')
  48 |     views=resolve_claims(obs,matches,links,caps.values(),as_of=data['as_of'])
  49 |     if sorted(map(canonical,map(record,views)))!=sorted(map(canonical,data['claims'])):
  50 |         raise ContractError('Claim view does not recompute from its evidence')
  51 |     if set(c['command_id'] for c in data['commands'])!=set(COMMANDS):
  52 |         raise ContractError('Command manifest must account for all 38 IDs')
```

## A01 — Model transcripts inflate corroboration counts

### `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:65–86`

```python
  65 |         if artifact['parent_artifact_id']:ids |= self.artifact_lineage(artifact['parent_artifact_id'],seen)
  66 |         return ids
  67 |     def roots(self,fid,seen=None):
  68 |         seen=set() if seen is None else set(seen)
  69 |         require(fid not in seen,'PROVENANCE_CYCLE');seen.add(fid)
  70 |         f=self.row('facts',fid);e=self.row('evidence',f['evidence_id'])
  71 |         roots=set()
  72 |         for l in e['locator_ids']:roots |= self.artifact_lineage(self.row('locators',l)['artifact_id'])
  73 |         for parent in e['input_fact_ids']:roots |= self.roots(parent,seen)
  74 |         # Numerator, denominator, exclusions and retained producer inputs all count.
  75 |         for sid in e.get('sample_ids',[]):
  76 |             for aid in self.row('samples',sid)['retrieved_artifact_ids']:roots |= self.artifact_lineage(aid)
  77 |         if f['execution_id']:
  78 |             ex=self.row('executions',f['execution_id'])
  79 |             for aid in ex['input_artifact_ids']:roots |= self.artifact_lineage(aid)
  80 |             if ex['model_call_id']:
  81 |                 call=self.row('model-calls',ex['model_call_id'])
  82 |                 for aid in [call['request_artifact_id'],call['response_artifact_id']]:
  83 |                     if aid:roots |= self.artifact_lineage(aid)
  84 |                 for repair in self.rows['repairs']:
  85 |                     if repair['call_id']==call['call_id']:roots |= self.artifact_lineage(repair['output_response_artifact_id'])
  86 |         return roots
```

### `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:367–382`

```python
 367 |         for s in self.rows['signals']:
 368 |             definition=self.reg('signals',s['signal_type_id']);run=self.row('runs',s['run_id'])
 369 |             require(s['tenant_id']==run['tenant_id'],'SIGNAL_TENANT')
 370 |             if s['status']=='RESOLVED':require(s['reason'] is None and bool(s['input_fact_ids']),'RESOLVED_SIGNAL_INVALID')
 371 |             if s['status']=='UNRESOLVED':require(s['reason'] in ['THIN_DATA','CONFLICT','POLICY'],'UNRESOLVED_REASON')
 372 |             if s['status']=='SUPPRESSED':require(s['reason']=='DNC','SUPPRESSION_REASON')
 373 |             if s['status']=='CANDIDATE':require(s['reason']=='CANDIDATE_SOURCE','CANDIDATE_REASON')
 374 |             for fid in s['input_fact_ids']:
 375 |                 f=self.row('facts',fid);require(f['subject_id']==s['subject_id'] and f['tenant_id']==s['tenant_id'],'CROSS_ACCOUNT_SIGNAL')
 376 |             for cid in s['context_ids']:
 377 |                 c=self.row('contexts',cid);require(definition['context_allowed'] and c['account_subject_id']==s['subject_id'],'UNDECLARED_SIGNAL_CONTEXT')
 378 |             if s['status']=='RESOLVED':
 379 |                 for req in definition['required_facts']:
 380 |                     good=[self.row('facts',fid) for fid in s['input_fact_ids'] if self.row('facts',fid)['predicate_id']==req['predicate_id'] and self.row('facts',fid)['state']==req['state'] and self.row('facts',fid)['nature'] in req['allowed_natures'] and self.decision_eligible(fid,run['as_of'],run_id=run['run_id'],allow_absence=req['state']=='NOT_FOUND')]
 381 |                     origins=distinct_origins(self.row('artifacts',a) for f in good for a in self.roots(f['fact_id']))
 382 |                     require(len(origins)>=req['minimum'],'SIGNAL_REQUIREMENT_UNSATISFIED')
```

## A02 — A refreshed current-use gate ignores newly admitted conflicts

### `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:117–127`

```python
 117 |     def decision_eligible(self,fid,at,*,run_id,purpose='INTERNAL_RESEARCH',allow_absence=False,production=False):
 118 |         """Resolve the whole available claim group, not a cherry-picked signal list."""
 119 |         f=self.assert_consumed(fid,run_id)
 120 |         if not self.usable(fid,at,purpose=purpose,allow_absence=allow_absence,production=production):return False
 121 |         run=self.row('runs',run_id)
 122 |         # A conflict cannot be laundered through a derived observation.
 123 |         for parent in self.ancestry(fid):
 124 |             target=self.row('facts',parent)
 125 |             fs=[self.row('facts',i) for i in self.available_facts(run) if claim_key(self.row('facts',i))==claim_key(target)]
 126 |             got=resolve_claim(fs,at,lambda x,t:self.usable(x['fact_id'],t,purpose=purpose,production=production,allow_absence=True))
 127 |             if got['status']!='KNOWN' or parent not in got['accepted_fact_ids']:return False
```

### `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:240–244`

```python
 240 |     def current_version_vector(self,package_id):
 241 |         # Conservative whole-bundle vector; excludes decisions/receipts to avoid self-reference.
 242 |         families=['facts','artifacts','evidence','bindings','resolutions','samples','executions','model-calls','changes','restrictions','contexts','signals','runs','reviews']
 243 |         return digest({'registry':self.registry,'package':package_hash(self.row('packages',package_id)),
 244 |                        'state':{k:self.rows[k] for k in families}})
```

### `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:246–320`

```python
 246 |     def validate_package_dependencies(self,p,*,require_completion=True):
 247 |         run=self.row('runs',p['run_id']);profile=self.reg('profiles',run['profile_id'])
 248 |         require(p['tenant_id']==run['tenant_id']==self.row('subjects',p['subject_id'])['tenant_id'],'PACKAGE_OWNER')
 249 |         require(profile['product_boundary'] in ['PREVIEW','REVIEWED_HANDOFF'],'KNOWLEDGE_PROFILE_CANNOT_PUBLISH_COPY')
 250 |         require(p['template_id'] in profile['template_ids'],'TEMPLATE_NOT_ENABLED')
 251 |         at=p['approved_at'] or run['as_of']
 252 |         if require_completion:self.target_completed(run['run_id'],p['subject_id'],at)
 253 |         for sid in p['signal_ids']:
 254 |             s=self.row('signals',sid)
 255 |             require(s['run_id']==run['run_id'] and s['tenant_id']==p['tenant_id'] and s['subject_id']==p['subject_id'] and s['status']=='RESOLVED','PACKAGE_SIGNAL_ELIGIBILITY')
 256 |             require(s['signal_type_id'] in profile['signal_ids'],'SIGNAL_NOT_ENABLED')
 257 |             require(instant(s['evaluated_at'])<=instant(at),'PACKAGE_BEFORE_SIGNAL')
 258 |             for fid in s['input_fact_ids']:
 259 |                 self.assert_consumed(fid,run['run_id'],s['evaluated_at'])
 260 |                 require(self.decision_eligible(fid,at,run_id=run['run_id'],allow_absence=True),'PACKAGE_SIGNAL_INPUT_INELIGIBLE')
 261 |         for cid in p['context_ids']:
 262 |             c=self.row('contexts',cid)
 263 |             require(c['status']=='ELIGIBLE' and c['run_id']==run['run_id'] and c['tenant_id']==p['tenant_id'] and c['account_subject_id']==p['subject_id'],'ABSTAINED_OR_FOREIGN_CONTEXT')
 264 |             self.validate_context(c)
 265 |             for fid in [c['link_fact_id']]+c['context_fact_ids']:
 266 |                 require(self.decision_eligible(fid,at,run_id=run['run_id']),'CURRENT_CONTEXT_INELIGIBLE')
 267 |         for clause in p['clauses']:
 268 |             for fid in clause['fact_ids']:
 269 |                 self.assert_consumed(fid,run['run_id'],at)
 270 |                 require(self.decision_eligible(fid,at,run_id=run['run_id'],purpose='OUTREACH',allow_absence=True),'CLAIM_NOT_RESOLVED_FOR_COPY')
 271 | 
 272 |     def validate_review(self,r,*,verify_support=True):
 273 |         self.require_actor(r['reviewer_id'],r['tenant_id'],'REVIEW_PACKAGE')
 274 |         p=self.row('packages',r['package']['package_id'])
 275 |         require(r['tenant_id']==p['tenant_id'] and r['package']['revision']==p['revision'] and r['package']['content_hash']==package_hash(p),'REVIEW_REVISION_HASH')
 276 |         if r['action']=='APPROVE':
 277 |             require(p['review_id']==r['review_id'] and p['approved_at']==r['decided_at'],'PACKAGE_REVIEW_BACKLINK')
 278 |             require(r['policy_version']==self.row('runs',p['run_id'])['approval_policy_version'],'REVIEW_POLICY_PIN')
 279 |             if verify_support:
 280 |                 self.validate_package_dependencies(p)
 281 |                 require(self.render(p)==p['rendered_text'],'REVIEW_UNSUPPORTED_COPY')
 282 | 
 283 |     def gate_reasons(self,g,at=None):
 284 |         at=at or g['evaluated_at'];p=self.row('packages',g['package']['package_id']);reasons=[]
 285 |         try:
 286 |             self.validate_package_dependencies({**p,'approved_at':at})
 287 |             for cl in p['clauses']:
 288 |                 for fid in cl['fact_ids']:
 289 |                     require(self.usable(fid,at,purpose='EXPORT',allow_absence=True),'EXPORT_EVIDENCE_INELIGIBLE')
 290 |             for rid in p['signal_ids']:
 291 |                 for fid in self.row('signals',rid)['input_fact_ids']:
 292 |                     require(self.usable(fid,at,allow_absence=True),'SIGNAL_EVIDENCE_INELIGIBLE')
 293 |         except ContractError:reasons.append('INELIGIBLE_CURRENT_SUPPORT')
 294 |         for r in self.rows['restrictions']:
 295 |             if (r['tenant_id']==p['tenant_id'] and r['subject_id']==p['subject_id'] and
 296 |                 (r['recipient_key'] is None or r['recipient_key']==g['recipient_key']) and
 297 |                 instant(r['effective_at'])<=instant(at) and (r['released_at'] is None or instant(at)<instant(r['released_at']))):
 298 |                 reasons.append(r['kind'])
 299 |         return sorted(set(reasons))
 300 | 
 301 |     def validate_gate(self,g,at=None):
 302 |         self.require_actor(g['actor_id'],g['tenant_id'],'USE_GATE')
 303 |         p=self.row('packages',g['package']['package_id']);dest=self.reg('destinations',g['destination_id']);review=self.row('reviews',g['review_id'])
 304 |         profile=self.reg('profiles',self.row('runs',p['run_id'])['profile_id'])
 305 |         require(profile['export_enabled'] and profile['product_boundary']=='REVIEWED_HANDOFF','EXPORT_DISABLED')
 306 |         require(p['tenant_id']==g['tenant_id']==dest['tenant_id']==review['tenant_id'] and dest['enabled'],'GATE_OWNER_OR_DESTINATION')
 307 |         require(g['package']==review['package'] and g['package']['content_hash']==package_hash(p),'GATE_CONTENT_HASH')
 308 |         require(review['action']=='APPROVE' and p['review_id']==review['review_id'],'UNAPPROVED_GATE')
 309 |         self.validate_review(review,verify_support=False)
 310 |         require(instant(review['decided_at'])<=instant(g['evaluated_at'])<instant(g['valid_until'])<=instant(g['evaluated_at'])+timedelta(minutes=5),'GATE_CHRONOLOGY')
 311 |         require((g['purpose']=='CONTACT_EXPORT')==(dest['kind']=='CONTACT_HANDOFF'),'DESTINATION_PURPOSE')
 312 |         require(g['recipient_key'] is not None if g['purpose']=='CONTACT_EXPORT' else g['recipient_key'] is None,'GATE_RECIPIENT_REQUIRED_OR_UNEXPECTED')
 313 |         require(g['version_vector']==self.current_version_vector(p['package_id']),'STALE_USE_GATE')
 314 |         now=at or g['evaluated_at']
 315 |         require(instant(g['evaluated_at'])<=instant(now)<instant(g['valid_until']),'EXPIRED_USE_GATE')
 316 |         reasons=self.gate_reasons(g,now)
 317 |         require(g['decision']==('BLOCK' if reasons else 'ALLOW') and g['reasons']==reasons,'USE_GATE_DECISION_MISMATCH')
 318 | 
 319 |     def validate_export(self,x):
 320 |         self.require_actor(x['actor_id'],x['tenant_id'],'EXPORT')
```

## A03 — In-run model artifacts cannot satisfy the frozen-input contract

### `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:368–397`

```python
 368 |             for aid in run['input_artifact_ids']:
 369 |                 require(instant(self.row('artifacts',aid)['captured_at'])<=instant(run['knowledge_cutoff']),'ARTIFACT_AFTER_CUTOFF')
 370 |             for sid in run['sample_ids']:
 371 |                 sample=self.row('samples',sid)
 372 |                 require(sample['tenant_id']==run['tenant_id'] and instant(sample['created_at'])<=instant(run['sealed_at']),'SAMPLE_SEAL')
 373 |                 require(set(sample['retrieved_artifact_ids'])<=set(run['input_artifact_ids']),'SAMPLE_UNPINNED_RECORDS')
 374 |         for ex in self.rows['executions']:
 375 |             run=self.row('runs',ex['run_id']);fn=self.reg('functions',ex['function_id']);profile=self.reg('profiles',run['profile_id'])
 376 |             require(ex['function_id'] in profile['execute_function_ids'],'EXECUTED_FUNCTION_NOT_ENABLED')
 377 |             require(instant(run['sealed_at'])<=instant(ex['started_at']),'EXECUTION_BEFORE_SEAL')
 378 |             if ex['status']!='COMPLETE':require(not ex['output_fact_ids'] and ex['terminal_reason'] is not None,'FAILED_PRODUCER_OUTPUT')
 379 |             else:require(ex['terminal_reason'] is None,'SUCCESS_WITH_FAILURE_REASON')
 380 |             for fid in ex['input_fact_ids']:self.assert_consumed(fid,run['run_id'],ex['started_at'])
 381 |             samples=[self.row('samples',i) for i in ex['input_sample_ids']]
 382 |             require(set(ex['input_sample_ids'])<=set(run['sample_ids']),'UNPINNED_EXECUTION_SAMPLE')
 383 |             require(ex['sample_set_hash']==digest(samples),'SAMPLE_INPUT_HASH')
 384 |             sample_artifacts={a for s in samples for a in s['retrieved_artifact_ids']}
 385 |             require(sample_artifacts<=set(ex['input_artifact_ids']),'MISSING_DENOMINATOR_EXECUTION_INPUT')
 386 |             for sid in ex['input_sample_ids']:
 387 |                 sample=self.row('samples',sid)
 388 |                 cls={f for d in sample['record_decisions'] for f in d['classification_fact_ids']}
 389 |                 require(cls<=set(ex['input_fact_ids']),'UNPINNED_SAMPLE_CLASSIFICATION')
 390 |             if ex['model_call_id']:
 391 |                 call=self.row('model-calls',ex['model_call_id'])
 392 |                 require(call['tenant_id']==ex['tenant_id'] and set(call['input_artifact_ids'])==set(ex['input_artifact_ids']),'MODEL_EXECUTION_INPUT_MISMATCH')
 393 |                 if ex['status']=='COMPLETE':require(call['status']=='PARSED' and call['response_artifact_id'] is not None,'FAILED_MODEL_PRODUCER')
 394 |                 for aid in [call['request_artifact_id'],call['response_artifact_id']]:
 395 |                     if aid:
 396 |                         require(aid in run['input_artifact_ids'],'UNPINNED_MODEL_IO')
 397 |                         require(instant(self.row('artifacts',aid)['captured_at'])<=instant(ex['finished_at']),'MODEL_IO_AFTER_EXECUTION')
```

### `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:328–332`

```python
 328 |             for aid in ex['input_artifact_ids']:require(aid in run['input_artifact_ids'],'ARTIFACT_OUTSIDE_RUN')
 329 |             for fid in ex['output_fact_ids']:
 330 |                 f=self.row('facts',fid);require(f['execution_id']==ex['execution_id'] and f['subject_id']==ex['subject_id'],'EXECUTION_OUTPUT_LINK')
 331 |                 require(f['predicate_id'] in fn['output_predicates'],'UNDECLARED_FUNCTION_OUTPUT')
 332 |             if fn['processor']=='LLM':require(ex['model_call_id'] is not None,'UNJOURNALED_MODEL_CALL');self.row('model-calls',ex['model_call_id'])
```

## A04 — ChangeRecord authorization remains open (previously deferred F)

### `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:93–119`

```python
  93 |     def policy_allows(self,pid,purpose,at,production=False,tenant=None):
  94 |         p=self.reg('policies',pid)
  95 |         if tenant is not None and tenant not in p['tenant_ids']:return False
  96 |         if any(c['kind']=='POLICY_REVOCATION' and c['target_id']==pid and instant(c['effective_at'])<=instant(at) for c in self.rows['changes']):return False
  97 |         return p['review_status']=='APPROVED' and purpose in p['purposes'] and instant(p['reviewed_at'])<=instant(at)<instant(p['valid_until']) and (not production or not p['fixture_only'])
  98 |     def usable(self,fid,at,*,purpose='INTERNAL_RESEARCH',production=False,allow_absence=False):
  99 |         """Current-use veto; storage of historical/candidate/expired records is allowed."""
 100 |         f=self.row('facts',fid)
 101 |         if f['state']=='UNKNOWN' or (f['state']=='NOT_FOUND' and not allow_absence):return False
 102 |         for replacement in self.rows['facts']:
 103 |             if replacement['supersedes_fact_id']==fid and replacement['state']!='UNKNOWN' and instant(replacement['recorded_at'])<=instant(at):
 104 |                 if self.usable(replacement['fact_id'],at,purpose=purpose,production=production,allow_absence=True):return False
 105 |         for change in self.rows['changes']:
 106 |             if instant(change['effective_at'])<=instant(at) and change['target_id'] in (fid,f['source_id'],f['binding_id']):return False
 107 |         for aid in self.roots(fid):
 108 |             a=self.row('artifacts',aid);s=self.reg('sources',a['source_id'])
 109 |             if a['status']!='OK' or s['authority']!='ACTIVE':return False
 110 |             if a['retention_state']!='RETAINED' or instant(a['retained_until'])<=instant(at):return False
 111 |             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
 112 |             if a['classification']=='SENSITIVE':return False
 113 |             if any(c['target_id']==aid and instant(c['effective_at'])<=instant(at) for c in self.rows['changes']):return False
 114 |         for parent in self.ancestry(fid):
 115 |             x=self.row('facts',parent);s=self.reg('sources',x['source_id'])
 116 |             if x['state']=='UNKNOWN' or instant(x['observed_at'])>instant(at) or instant(x['expires_at'])<=instant(at):return False
 117 |             if s['authority']!='ACTIVE' or (production and s['fixture_only']):return False
 118 |             if any(c['target_id'] in (parent,x['source_id'],x['binding_id']) and instant(c['effective_at'])<=instant(at) for c in self.rows['changes']):return False
 119 |             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
```

## A05 — Canonical fingerprint facts are not re-derived from their actual evidence

### `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:214–221`

```python
 214 |         for fp in self.registry['fingerprints']:
 215 |             product=self.row('subjects',fp['product_subject_id']);require(product['kind']=='SOFTWARE_PRODUCT','FINGERPRINT_PRODUCT_KIND')
 216 |             self.reg('predicates',fp['emits'])
 217 |             if fp['implementation_status']=='REFERENCE_IMPLEMENTED':
 218 |                 for paths,expected in [(fp['positive_fixtures'],True),(fp['negative_fixtures'],False)]:
 219 |                     for path in paths:
 220 |                         p=(self.root/path).resolve();require(p.is_relative_to(self.root.resolve()) and p.is_file(),'FINGERPRINT_FIXTURE_PATH')
 221 |                         require(matches_fingerprint(fp,p.read_text())==expected,'FINGERPRINT_FIXTURE_RESULT')
```

### `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:496–520`

```python
 496 |                 ids=value if isinstance(value,list) else [value]
 497 |                 typ=rr.get('target_type','SUBJECT');kind={'SUBJECT':'subjects','FACT':'facts','ARTIFACT':'artifacts','LOCATOR':'locators'}[typ]
 498 |                 for sid in ids:
 499 |                     target=self.row(kind,sid)
 500 |                     tenant=target.get('tenant_id') if typ!='LOCATOR' else self.row('artifacts',target['artifact_id'])['tenant_id']
 501 |                     require(tenant==f['tenant_id'],'OBJECT_REFERENCE_TENANT')
 502 |                     if typ=='SUBJECT':require(target['kind'] in rr['subject_kinds'],'OBJECT_SUBJECT_REFERENCE')
 503 |                     if typ=='FACT':require(sid in e['input_fact_ids'],'OBJECT_FACT_REFERENCE_NOT_IN_LINEAGE')
 504 |                     if typ=='LOCATOR':require(target['artifact_id'] in self.roots(f['fact_id']),'LOCATOR_OUTSIDE_LINEAGE')
 505 |             o=f['object']
 506 |             if isinstance(o,dict):
 507 |                 for field in set(o)&set(f['target']):require(o[field]==f['target'][field],'TARGET_VALUE_MISMATCH:'+field)
 508 |                 for lo,hi in [('minimum_minor','maximum_minor'),('minimum','maximum')]:
 509 |                     if lo in o and hi in o and o[lo] is not None and o[hi] is not None:require(o[lo]<=o[hi],'REVERSED_RANGE')
 510 |                 if 'statement_id' in o:
 511 |                     self.reg('taxonomy',o['topic_id'])
 512 |                     require(e['directness']=='RAW' and o['text'] in self.evidence_text(e),'UNSUPPORTED_QUOTED_STATEMENT')
 513 |                 if 'theme_id' in o:self.reg('taxonomy',o['theme_id'])
 514 |                 if f['predicate_id']=='job.salary':require(o['minimum_minor'] is not None or o['maximum_minor'] is not None,'EMPTY_SALARY')
 515 |                 if f['predicate_id']=='review.record' and o['rating'] is not None:require(o['rating_scale_max'] is not None and 0<=o['rating']<=o['rating_scale_max'],'RATING_OUT_OF_RANGE')
 516 |                 if f['predicate_id']=='technology.footprint':
 517 |                     fp=self.reg('fingerprints',o['fingerprint_id']);require(fp['product_subject_id']==o['product_id'] and fp['emits']==f['predicate_id'] and fp['capture_mode']==scope['capture_mode'],'FINGERPRINT_OUTPUT_MISMATCH')
 518 |                 if f['predicate_id'].endswith('.measurement'):self.validate_measurement(f)
 519 |                 if f['predicate_id'] in ['event.authorized_attendance','phone.call_event','phone.routing_verified','phone.recording_verified','integration.connection.verified','ops.automation.verified','ops.sales.verified']:
 520 |                     require(scope['kind']=='AUTHORIZED_SYSTEM','PRIVATE_OPERATIONS_REQUIRE_AUTHORIZED_SCOPE')
```

## P01 — The proposed common protocol is structural, not an enforcing runtime interface

### `protocol/keensight-module-design/validate_protocol.py:58–114`

```python
  58 | def validate_pair(request: dict[str, Any], result: dict[str, Any]) -> None:
  59 |     vs = validators()
  60 |     vs["ModuleRequest"].validate(request)
  61 |     vs["ModuleResult"].validate(result)
  62 |     for key in ("request_id", "execution_id", "module_id", "operation", "context", "trace"):
  63 |         if request[key] != result[key]:
  64 |             raise ValueError(f"Request/result mismatch at {key}")
  65 |     if result["request_digest"] != digest(request):
  66 |         raise ValueError("Request digest mismatch")
  67 |     if datetime.fromisoformat(result["finished_at"]) < datetime.fromisoformat(result["started_at"]):
  68 |         raise ValueError("Result finished before it started")
  69 |     if result["reused_execution_id"] == result["execution_id"]:
  70 |         raise ValueError("Execution cannot reuse itself")
  71 |     if request["module_id"] != "CTL-01" and request["release_lock_ref"] is None:
  72 |         raise ValueError("Non-bootstrap operation requires a release lock")
  73 |     mids = {m["module_id"] for m in load(ROOT / "modules.json")["modules"]}
  74 |     if request["module_id"] not in mids:
  75 |         raise ValueError("Unregistered module")
  76 |     context = request["context"]
  77 |     if context["as_of"] and context["knowledge_cutoff"]:
  78 |         # These timestamps have different meanings: either may be earlier.
  79 |         # Do not invent an ordering relation between valid time and recorded time.
  80 |         pass
  81 |     allowed_codes = load(ROOT / "error_codes.json")["codes"]
  82 |     if any(d["code"] not in allowed_codes for d in result["diagnostics"]):
  83 |         raise ValueError("Unregistered diagnostic code")
  84 |     all_refs = request["input_refs"] + result["consumed_refs"] + result["output_refs"] + result["diagnostic_record_refs"]
  85 |     for key in ("release_lock_ref", "parameters_ref", "budget_reservation_ref"):
  86 |         if request[key] is not None:
  87 |             all_refs.append(request[key])
  88 |     if context["subject_ref"] is not None:
  89 |         all_refs.append(context["subject_ref"])
  90 |     for d in result["diagnostics"]:
  91 |         all_refs += d["record_refs"]
  92 |         if d["restricted_details_ref"] is not None:
  93 |             all_refs.append(d["restricted_details_ref"])
  94 |     seen: dict[str, dict[str, Any]] = {}
  95 |     for ref in all_refs:
  96 |         # This draft uses tenant-scoped references, including aliases for shared
  97 |         # releases. It does not implement cross-tenant authorization.
  98 |         if ref["tenant_id"] != context["tenant_id"]:
  99 |             raise ValueError("Cross-tenant reference")
 100 |         previous = seen.get(ref["record_id"])
 101 |         if previous is not None and previous != ref:
 102 |             raise ValueError("Immutable reference has conflicting metadata/digest")
 103 |         seen[ref["record_id"]] = ref
 104 | 
 105 | 
 106 | def validate_pack() -> dict[str, Any]:
 107 |     vs = validators()
 108 |     cat = load(ROOT / "modules.json")
 109 |     modules = cat["modules"]
 110 |     ids = [m["module_id"] for m in modules]
 111 |     if len(ids) != len(set(ids)) or len(ids) != cat["module_count"]:
 112 |         raise ValueError("Module IDs/count do not agree")
 113 |     for m in modules:
 114 |         for key in ("input_contracts", "output_contracts", "submodules"):
```
