# Iteration 2 — numbered source evidence

Source: the unchanged September 15 repaired package. Line numbers are local source-file line numbers. No remote source was fetched.

## F01 — Identity-binding evidence is outside eligibility/provenance closure

### `canonical/keensight_contracts/validation.py:65–118`

```text
  65:         if artifact['parent_artifact_id']:ids |= self.artifact_lineage(artifact['parent_artifact_id'],seen)
  66:         return ids
  67:     def roots(self,fid,seen=None):
  68:         seen=set() if seen is None else set(seen)
  69:         require(fid not in seen,'PROVENANCE_CYCLE');seen.add(fid)
  70:         f=self.row('facts',fid);e=self.row('evidence',f['evidence_id'])
  71:         roots=set()
  72:         for l in e['locator_ids']:roots |= self.artifact_lineage(self.row('locators',l)['artifact_id'])
  73:         for parent in e['input_fact_ids']:roots |= self.roots(parent,seen)
  74:         # Numerator, denominator, exclusions and retained producer inputs all count.
  75:         for sid in e.get('sample_ids',[]):
  76:             for aid in self.row('samples',sid)['retrieved_artifact_ids']:roots |= self.artifact_lineage(aid)
  77:         if f['execution_id']:
  78:             ex=self.row('executions',f['execution_id'])
  79:             for aid in ex['input_artifact_ids']:roots |= self.artifact_lineage(aid)
  80:             if ex['model_call_id']:
  81:                 call=self.row('model-calls',ex['model_call_id'])
  82:                 for aid in [call['request_artifact_id'],call['response_artifact_id']]:
  83:                     if aid:roots |= self.artifact_lineage(aid)
  84:                 for repair in self.rows['repairs']:
  85:                     if repair['call_id']==call['call_id']:roots |= self.artifact_lineage(repair['output_response_artifact_id'])
  86:         return roots
  87:     def corroborating_artifacts(self,fid,seen=None):
  88:         """Evidence leaves, not model I/O, processing requests, or denominators.
  89: 
  90:         Full provenance still uses roots(). Statistical eligibility still depends
  91:         on the complete sample. Neither is an independence estimate.
  92:         """
  93:         seen=set() if seen is None else set(seen)
  94:         require(fid not in seen,'PROVENANCE_CYCLE');seen.add(fid)
  95:         f=self.row('facts',fid);e=self.row('evidence',f['evidence_id'])
  96:         transcripts={a for c in self.rows['model-calls'] for a in (c['request_artifact_id'],c['response_artifact_id']) if a}
  97:         transcripts|={r['output_response_artifact_id'] for r in self.rows['repairs']}
  98:         out=set()
  99:         for lid in e['locator_ids']:
 100:             aid=self.row('locators',lid)['artifact_id'];visited=set()
 101:             while aid:
 102:                 require(aid not in visited,'ARTIFACT_PROVENANCE_CYCLE');visited.add(aid)
 103:                 artifact=self.row('artifacts',aid)
 104:                 if artifact['parent_artifact_id']: aid=artifact['parent_artifact_id']
 105:                 else:
 106:                     if aid not in transcripts:out.add(aid)
 107:                     break
 108:         for parent in e['input_fact_ids']:out|=self.corroborating_artifacts(parent,seen)
 109:         return out
 110: 
 111:     def ancestry(self,fid,seen=None):
 112:         seen=set() if seen is None else set(seen)
 113:         require(fid not in seen,'PROVENANCE_CYCLE');seen.add(fid)
 114:         f=self.row('facts',fid);e=self.row('evidence',f['evidence_id']);out={fid}
 115:         for parent in e['input_fact_ids']:out |= self.ancestry(parent,seen)
 116:         return out
 117:     def policy_allows(self,pid,purpose,at,production=False,tenant=None):
 118:         p=self.reg('policies',pid)
```

### `canonical/keensight_contracts/validation.py:123–172`

```text
 123:         """Current-use veto; storage of historical/candidate/expired records is allowed."""
 124:         f=self.row('facts',fid)
 125:         if f['state']=='UNKNOWN' or (f['state']=='NOT_FOUND' and not allow_absence):return False
 126:         for replacement in self.rows['facts']:
 127:             if replacement['supersedes_fact_id']==fid and replacement['state']!='UNKNOWN' and instant(replacement['recorded_at'])<=instant(at):
 128:                 if self.usable(replacement['fact_id'],at,purpose=purpose,production=production,allow_absence=True):return False
 129:         for change in self.authorized_changes(at):
 130:             if change['tenant_id']!=f['tenant_id']:continue
 131:             if instant(change['effective_at'])<=instant(at) and change['target_id'] in (fid,f['source_id'],f['binding_id']):return False
 132:         for aid in self.roots(fid):
 133:             a=self.row('artifacts',aid);s=self.reg('sources',a['source_id'])
 134:             if a['status']!='OK' or s['authority']!='ACTIVE':return False
 135:             if a['retention_state']!='RETAINED' or instant(a['retained_until'])<=instant(at):return False
 136:             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
 137:             if a['classification']=='SENSITIVE':return False
 138:             if any(c['target_id']==aid and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 139:         for parent in self.ancestry(fid):
 140:             x=self.row('facts',parent);s=self.reg('sources',x['source_id'])
 141:             if x['state']=='UNKNOWN' or instant(x['observed_at'])>instant(at) or instant(x['expires_at'])<=instant(at):return False
 142:             if s['authority']!='ACTIVE' or (production and s['fixture_only']):return False
 143:             if any(c['target_id'] in (parent,x['source_id'],x['binding_id']) and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 144:             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
 145:             if x['predicate_id']=='technology.footprint' and x['state']=='OBSERVED':
 146:                 fp=self.reg('fingerprints',x['object']['fingerprint_id'])
 147:                 if fp['authority']!='ACTIVE' or (production and fp['fixture_only']):return False
 148:                 if any(c['target_id']==fp['fingerprint_id'] and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 149:             if x['binding_id']:
 150:                 b=self.row('bindings',x['binding_id'])
 151:                 if b['status']!='ACCEPTED' or b['role'] in ['AGENCY','MENTION_ONLY','UNRESOLVED']:return False
 152:             if x['execution_id']:
 153:                 ex=self.row('executions',x['execution_id']);fn=self.reg('functions',ex['function_id'])
 154:                 if ex['status']!='COMPLETE':return False
 155:                 if instant(ex['finished_at'])>instant(x['recorded_at']):return False
 156:                 if fn['authority']!='ACTIVE' or (production and fn['fixture_only']):return False
 157:                 if any(c['target_id']==fn['function_id'] and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 158:                 if ex['model_call_id']:
 159:                     call=self.row('model-calls',ex['model_call_id'])
 160:                     if call['status']!='PARSED' or call['response_artifact_id'] is None:return False
 161:                     repairs=sorted([r for r in self.rows['repairs'] if r['call_id']==call['call_id']],key=lambda r:r['ordinal'])
 162:                     if len(repairs)>call['max_repair_attempts'] or (repairs and repairs[-1]['status']!='VALID'):return False
 163:                     for aid in [call['request_artifact_id'],call['response_artifact_id']]:
 164:                         artifact=self.row('artifacts',aid)
 165:                         if artifact['retention_state']!='RETAINED' or instant(artifact['retained_until'])<=instant(at):return False
 166:         return True
 167:     def evidence_text(self,evidence):
 168:         return '\n'.join(self.locator_text(self.row('locators',lid)) for lid in evidence['locator_ids'])
 169:     def locator_text(self,l):
 170:         a=self.row('artifacts',l['artifact_id'])
 171:         if a['retention_state']!='RETAINED':return ''
 172:         raw=(self.root/a['content_ref']).read_bytes()
```

### `canonical/keensight_contracts/validation.py:297–303`

```text
 297:         stable_order(self.index['artifacts'],[(a['parent_artifact_id'],a['artifact_id']) for a in self.rows['artifacts'] if a['parent_artifact_id']])
 298:         for l in self.rows['locators']:self.row('artifacts',l['artifact_id']);self.locator_text(l)
 299:         for b in self.rows['bindings']:
 300:             sub=self.row('subjects',b['subject_id']);scope=self.row('scopes',b['scope_id'])
 301:             require(sub['tenant_id']==b['tenant_id']==scope['tenant_id'] and scope['subject_id']==sub['subject_id'],'BINDING_SUBJECT_OR_TENANT')
 302:             for aid in b['artifact_ids']:require(self.row('artifacts',aid)['scope_id']==scope['scope_id'],'BINDING_ARTIFACT_SCOPE')
 303:             require(all(self.row('locators',l)['artifact_id'] in b['artifact_ids'] for l in b['evidence_locator_ids']),'BINDING_LOCATOR_OUTSIDE_ARTIFACT')
```

### `canonical/keensight_contracts/completion.py:149–161`

```text
 149:         for parent in self.ancestry(fid):
 150:             p=self.row('facts',parent)
 151:             require(parent in self.available_facts(run),'UNPINNED_ANCESTRAL_FACT')
 152:             e=self.row('evidence',p['evidence_id'])
 153:             require(set(e['sample_ids'])<=set(run['sample_ids']),'UNPINNED_ANCESTRAL_SAMPLE')
 154:             if p['execution_id'] and p['run_id']!=run_id:
 155:                 require(p['execution_id'] in run['imported_execution_ids'],'UNPINNED_ANCESTRAL_EXECUTION')
 156:             if p['binding_id']:
 157:                 require(p['binding_id'] in run['binding_ids'],'UNPINNED_CONSUMED_BINDING')
 158:                 b=self.row('bindings',p['binding_id'])
 159:                 require(instant(b['decided_at'])<=instant(run['sealed_at']),'BINDING_AFTER_SEAL')
 160:         require(self.roots(fid)<=self.available_artifacts(run),'UNPINNED_ANCESTRAL_ARTIFACT')
 161:         return f
```

## F02 — Demoted templates pass the standalone current-use/export boundary

### `canonical/keensight_contracts/completion.py:298–377`

```text
 298: 
 299:     def validate_package_dependencies(self,p,*,require_completion=True):
 300:         run=self.row('runs',p['run_id']);profile=self.reg('profiles',run['profile_id'])
 301:         require(p['tenant_id']==run['tenant_id']==self.row('subjects',p['subject_id'])['tenant_id'],'PACKAGE_OWNER')
 302:         require(profile['product_boundary'] in ['PREVIEW','REVIEWED_HANDOFF'],'KNOWLEDGE_PROFILE_CANNOT_PUBLISH_COPY')
 303:         require(p['template_id'] in profile['template_ids'],'TEMPLATE_NOT_ENABLED')
 304:         at=p['approved_at'] or run['as_of']
 305:         if require_completion:self.target_completed(run['run_id'],p['subject_id'],at)
 306:         for sid in p['signal_ids']:
 307:             s=self.row('signals',sid)
 308:             require(s['run_id']==run['run_id'] and s['tenant_id']==p['tenant_id'] and s['subject_id']==p['subject_id'] and s['status']=='RESOLVED','PACKAGE_SIGNAL_ELIGIBILITY')
 309:             require(s['signal_type_id'] in profile['signal_ids'],'SIGNAL_NOT_ENABLED')
 310:             require(instant(s['evaluated_at'])<=instant(at),'PACKAGE_BEFORE_SIGNAL')
 311:             for fid in s['input_fact_ids']:
 312:                 self.assert_consumed(fid,run['run_id'],s['evaluated_at'])
 313:                 require(self.decision_eligible(fid,at,run_id=run['run_id'],allow_absence=True),'PACKAGE_SIGNAL_INPUT_INELIGIBLE')
 314:         for cid in p['context_ids']:
 315:             c=self.row('contexts',cid)
 316:             require(c['status']=='ELIGIBLE' and c['run_id']==run['run_id'] and c['tenant_id']==p['tenant_id'] and c['account_subject_id']==p['subject_id'],'ABSTAINED_OR_FOREIGN_CONTEXT')
 317:             self.validate_context(c)
 318:             for fid in [c['link_fact_id']]+c['context_fact_ids']:
 319:                 require(self.decision_eligible(fid,at,run_id=run['run_id']),'CURRENT_CONTEXT_INELIGIBLE')
 320:         for clause in p['clauses']:
 321:             for fid in clause['fact_ids']:
 322:                 self.assert_consumed(fid,run['run_id'],at)
 323:                 require(self.decision_eligible(fid,at,run_id=run['run_id'],purpose='OUTREACH',allow_absence=True),'CLAIM_NOT_RESOLVED_FOR_COPY')
 324: 
 325:     def validate_review(self,r,*,verify_support=True):
 326:         self.require_actor(r['reviewer_id'],r['tenant_id'],'REVIEW_PACKAGE')
 327:         p=self.row('packages',r['package']['package_id'])
 328:         require(r['tenant_id']==p['tenant_id'] and r['package']['revision']==p['revision'] and r['package']['content_hash']==package_hash(p),'REVIEW_REVISION_HASH')
 329:         if r['action']=='APPROVE':
 330:             require(p['review_id']==r['review_id'] and p['approved_at']==r['decided_at'],'PACKAGE_REVIEW_BACKLINK')
 331:             require(r['policy_version']==self.row('runs',p['run_id'])['approval_policy_version'],'REVIEW_POLICY_PIN')
 332:             if verify_support:
 333:                 self.validate_package_dependencies(p)
 334:                 require(self.render(p)==p['rendered_text'],'REVIEW_UNSUPPORTED_COPY')
 335: 
 336:     def gate_reasons(self,g,at=None):
 337:         at=at or g['evaluated_at'];p=self.row('packages',g['package']['package_id']);reasons=[]
 338:         try:
 339:             self.validate_package_dependencies({**p,'approved_at':at})
 340:             for cl in p['clauses']:
 341:                 for fid in cl['fact_ids']:
 342:                     require(self.current_claim_eligible(fid,at,purpose='EXPORT',allow_absence=True),'EXPORT_EVIDENCE_INELIGIBLE')
 343:             for rid in p['signal_ids']:
 344:                 for fid in self.row('signals',rid)['input_fact_ids']:
 345:                     require(self.current_claim_eligible(fid,at,allow_absence=True),'SIGNAL_EVIDENCE_INELIGIBLE')
 346:             for cid in p['context_ids']:
 347:                 ctx=self.row('contexts',cid)
 348:                 for fid in [ctx['link_fact_id']]+ctx['context_fact_ids']:
 349:                     require(self.current_claim_eligible(fid,at),'CONTEXT_CURRENT_CONFLICT')
 350:         except ContractError:reasons.append('INELIGIBLE_CURRENT_SUPPORT')
 351:         for r in self.rows['restrictions']:
 352:             if (r['tenant_id']==p['tenant_id'] and r['subject_id']==p['subject_id'] and
 353:                 (r['recipient_key'] is None or r['recipient_key']==g['recipient_key']) and
 354:                 instant(r['effective_at'])<=instant(at) and (r['released_at'] is None or instant(at)<instant(r['released_at']))):
 355:                 reasons.append(r['kind'])
 356:         return sorted(set(reasons))
 357: 
 358:     def validate_gate(self,g,at=None):
 359:         self.require_actor(g['actor_id'],g['tenant_id'],'USE_GATE')
 360:         p=self.row('packages',g['package']['package_id']);dest=self.reg('destinations',g['destination_id']);review=self.row('reviews',g['review_id'])
 361:         profile=self.reg('profiles',self.row('runs',p['run_id'])['profile_id'])
 362:         require(profile['export_enabled'] and profile['product_boundary']=='REVIEWED_HANDOFF','EXPORT_DISABLED')
 363:         require(p['tenant_id']==g['tenant_id']==dest['tenant_id']==review['tenant_id'] and dest['enabled'],'GATE_OWNER_OR_DESTINATION')
 364:         require(g['package']==review['package'] and g['package']['content_hash']==package_hash(p),'GATE_CONTENT_HASH')
 365:         require(review['action']=='APPROVE' and p['review_id']==review['review_id'],'UNAPPROVED_GATE')
 366:         self.validate_review(review,verify_support=False)
 367:         require(instant(review['decided_at'])<=instant(g['evaluated_at'])<instant(g['valid_until'])<=instant(g['evaluated_at'])+timedelta(minutes=5),'GATE_CHRONOLOGY')
 368:         require((g['purpose']=='CONTACT_EXPORT')==(dest['kind']=='CONTACT_HANDOFF'),'DESTINATION_PURPOSE')
 369:         require(g['recipient_key'] is not None if g['purpose']=='CONTACT_EXPORT' else g['recipient_key'] is None,'GATE_RECIPIENT_REQUIRED_OR_UNEXPECTED')
 370:         require(g['version_vector']==self.current_version_vector(p['package_id']),'STALE_USE_GATE')
 371:         now=at or g['evaluated_at']
 372:         require(instant(g['evaluated_at'])<=instant(now)<instant(g['valid_until']),'EXPIRED_USE_GATE')
 373:         reasons=self.gate_reasons(g,now)
 374:         require(g['decision']==('BLOCK' if reasons else 'ALLOW') and g['reasons']==reasons,'USE_GATE_DECISION_MISMATCH')
 375: 
 376:     def validate_export(self,x):
 377:         self.require_actor(x['actor_id'],x['tenant_id'],'EXPORT')
```

### `canonical/keensight_contracts/handoff.py:19–43`

```text
  19: class LocalPreviewExporter:
  20:     def __init__(self,bundle,output_directory: Path):
  21:         self.bundle=bundle
  22:         self.directory=Path(output_directory).resolve()
  23: 
  24:     def export(self,gate_id: str,*,principal_id: str,at: str,idempotency_key: str) -> LocalExportResult:
  25:         b=self.bundle;gate=b.row('gates',gate_id);pkg=b.row('packages',gate['package']['package_id'])
  26:         b.require_actor(principal_id,gate['tenant_id'],'EXPORT')
  27:         require(b.row('runs',pkg['run_id'])['mode']=='DESIGN_TEST','LIVE_EXPORT_NOT_IMPLEMENTED')
  28:         destination=b.reg('destinations',gate['destination_id'])
  29:         require(destination['kind']=='LOCAL_PREVIEW' and destination['fixture_only'],'REMOTE_EXPORT_NOT_IMPLEMENTED')
  30:         b.validate_gate(gate,at);require(gate['decision']=='ALLOW','EXPORT_GATE_BLOCKED')
  31:         data=export_payload(pkg,destination,gate['recipient_key'])
  32:         key=digest({'tenant':gate['tenant_id'],'destination':destination['destination_id'],'idempotency_key':idempotency_key}).split(':')[1]
  33:         self.directory.mkdir(parents=True,exist_ok=True)
  34:         path=self.directory/(key+'.json')
  35:         # O_EXCL prevents an accidental overwrite or a second payload for a key.
  36:         # Recovery of incomplete local writes remains fail-closed, not silent resend.
  37:         try:fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  38:         except FileExistsError:
  39:             require(path.is_file() and not path.is_symlink() and path.read_bytes()==data,'IDEMPOTENCY_PAYLOAD_CONFLICT')
  40:             return LocalExportResult(str(path),digest(data),True)
  41:         with os.fdopen(fd,'wb') as f:
  42:             f.write(data);f.flush();os.fsync(f.fileno())
  43:         return LocalExportResult(str(path),digest(data),False)
```

### `canonical/keensight_contracts/validation.py:408–422`

```text
 408:         for p in self.rows['packages']:
 409:             self.row('subjects',p['subject_id']);run=self.row('runs',p['run_id']);t=self.reg('templates',p['template_id'])
 410:             require(p['tenant_id']==run['tenant_id'],'PACKAGE_TENANT')
 411:             for sid in p['signal_ids']:
 412:                 s=self.row('signals',sid);require(s['subject_id']==p['subject_id'] and s['status']=='RESOLVED','PACKAGE_SIGNAL_ELIGIBILITY')
 413:             for cid in p['context_ids']:require(self.row('contexts',cid)['account_subject_id']==p['subject_id'],'PACKAGE_CONTEXT_TARGET')
 414:             if p['status'] in ['APPROVED','DESIGN_TEST_APPROVED']:
 415:                 require(p['approved_at'] is not None and t['authority']=='ACTIVE','MISSING_APPROVAL')
 416:                 require(p['status']!='APPROVED' or run['mode']=='PRODUCTION','FIXTURE_IS_NOT_PRODUCTION')
 417:                 require(all(instant(self.row('facts',fid)['recorded_at'])<=instant(p['approved_at']) for clause in p['clauses'] for rootfid in clause['fact_ids'] for fid in self.ancestry(rootfid)),'APPROVAL_PRECEDES_EVIDENCE')
 418:                 require(p['rendered_text']==self.render(p),'UNSUPPORTED_RENDERED_COPY')
 419:                 # Mature offers are contracted, but deliberately fail closed until a renderer exists.
 420:                 require(t['mode']=='OBSERVATION_QUESTION','MATURITY_OFFER_NOT_IMPLEMENTED')
 421:                 require(p['maturity_fact_id'] is None,'UNNECESSARY_MATURITY_DEPENDENCY')
 422:         for change in self.rows['changes']:self.validate_change(change)
```

## F03 — Publication validates one payload and can persist a different argument set

### `collector/src/keensight_scrapling/storage.py:211–258`

```text
 211:     def publish_evaluation(self, data, pages, matches, observations, links):
 212:         """Publish only a validated evaluation; every projection write rolls back together.
 213: 
 214:         Physical capture bytes/attempt diagnostics already retained are intentionally
 215:         outside this publication transaction. A commit is a local owner boundary,
 216:         not a substitute for hosted authentication.
 217:         """
 218:         from .validation import validate_bundle
 219:         validate_bundle(data)
 220:         caps = [Capture(**c) for c in data['captures']]
 221:         for cap in caps:
 222:             self.body(cap)
 223:         tenants = {c.tenant_id for c in caps}
 224:         if len(tenants) > 1:
 225:             raise ContractError('Cross-tenant evaluation')
 226:         if not tenants:
 227:             return
 228:         tenant = next(iter(tenants))
 229:         key = identity('evaluation', data['evaluation_id'], data['release_digest'],
 230:                        data['as_of'], data['evaluated_capture_ids'])
 231:         # Transport diagnostics can legitimately differ on resume. Only immutable
 232:         # semantic output is stored as the publication identity.
 233:         payload = canonical({k:data[k] for k in ('evaluation_id','as_of','release_digest',
 234:                             'evaluated_capture_ids','matches','observations','support_links','claims')})
 235:         with self.db:
 236:             old = self.db.execute('SELECT payload FROM evaluations WHERE tenant=? AND evaluation_key=?',
 237:                                   (tenant,key)).fetchone()
 238:             if old and old['payload'] != payload:
 239:                 raise ContractError('Evaluation identity reused with different semantic output')
 240:             self.db.execute('INSERT OR IGNORE INTO evaluations VALUES(?,?,?)',(tenant,key,payload))
 241:             self.save_findings(tenant,matches,observations,links,transaction_owned=True)
 242:             self.harvest(tenant,pages,matched_surface_ids={m.surface_id for m in matches if m.authority=='APPROVED'},
 243:                          transaction_owned=True)
 244:             selected=set(data['evaluated_capture_ids'])
 245:             for cap in caps:
 246:                 eligible=int(cap.capture_id in selected)
 247:                 previous=self.db.execute('SELECT eligible FROM replay_selection WHERE tenant=? AND capture_id=?',
 248:                                          (tenant,cap.capture_id)).fetchone()
 249:                 if previous and previous['eligible']!=eligible:
 250:                     raise ContractError('Capture eligibility cannot be silently reinterpreted; create a new explicit policy evaluation')
 251:                 self.db.execute('INSERT OR IGNORE INTO replay_selection VALUES(?,?,?)',(tenant,cap.capture_id,eligible))
 252: 
 253:     def replay_eligible(self, cap):
 254:         row=self.db.execute('SELECT eligible FROM replay_selection WHERE tenant=? AND capture_id=?',
 255:                             (cap.tenant_id,cap.capture_id)).fetchone()
 256:         if row is None:
 257:             raise ContractError('No successful original selection manifest; recapture or explicitly import evidence')
 258:         return bool(row['eligible'])
```

### `collector/src/keensight_scrapling/pipeline.py:231–246`

```text
 231:         data={'schema_version':'1.1','producer':'keensight-scrapling-ingestion/0.2.0','evaluation_id':evaluation_id,'as_of':as_of,
 232:               'release_digest':self.pack.digest,'rule_pack':self.pack.raw,'fixture_only':self.pack.fixture_only,'send_allowed':False,
 233:               'captures':[asdict(c) for c in sorted(caps,key=lambda x:x.capture_id)],
 234:               'evaluated_capture_ids':sorted(p.capture.capture_id for p in pages),
 235:               'surfaces':[asdict(s) for p in pages for s in p.surfaces],
 236:               'matches':[asdict(m) for m in matches],'observations':[asdict(o) for o in observations],
 237:               'support_links':[asdict(x) for x in links],'claims':[asdict(v) for v in views],
 238:               'rule_evaluations':rule_evaluations,'commands':[asdict(c) for c in complete_command_manifest(commands)],
 239:               'resource_dispositions':dispositions or [],'priority_score':score,
 240:               'handoff':{'type':'COLLECTOR_OBSERVATIONS','requires_fact_service_admission':True,'absence_facts_emitted':False}}
 241:         from .validation import validate_bundle
 242:         data=strict_json(canonical(data))
 243:         validate_bundle(data)
 244:         self.store.publish_evaluation(data,pages,matches,observations,links)
 245:         return data
 246: 
```

## F04 — Later supersession leaks into an earlier sealed evaluation

### `canonical/keensight_contracts/validation.py:123–144`

```text
 123:         """Current-use veto; storage of historical/candidate/expired records is allowed."""
 124:         f=self.row('facts',fid)
 125:         if f['state']=='UNKNOWN' or (f['state']=='NOT_FOUND' and not allow_absence):return False
 126:         for replacement in self.rows['facts']:
 127:             if replacement['supersedes_fact_id']==fid and replacement['state']!='UNKNOWN' and instant(replacement['recorded_at'])<=instant(at):
 128:                 if self.usable(replacement['fact_id'],at,purpose=purpose,production=production,allow_absence=True):return False
 129:         for change in self.authorized_changes(at):
 130:             if change['tenant_id']!=f['tenant_id']:continue
 131:             if instant(change['effective_at'])<=instant(at) and change['target_id'] in (fid,f['source_id'],f['binding_id']):return False
 132:         for aid in self.roots(fid):
 133:             a=self.row('artifacts',aid);s=self.reg('sources',a['source_id'])
 134:             if a['status']!='OK' or s['authority']!='ACTIVE':return False
 135:             if a['retention_state']!='RETAINED' or instant(a['retained_until'])<=instant(at):return False
 136:             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
 137:             if a['classification']=='SENSITIVE':return False
 138:             if any(c['target_id']==aid and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 139:         for parent in self.ancestry(fid):
 140:             x=self.row('facts',parent);s=self.reg('sources',x['source_id'])
 141:             if x['state']=='UNKNOWN' or instant(x['observed_at'])>instant(at) or instant(x['expires_at'])<=instant(at):return False
 142:             if s['authority']!='ACTIVE' or (production and s['fixture_only']):return False
 143:             if any(c['target_id'] in (parent,x['source_id'],x['binding_id']) and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 144:             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
```

### `canonical/keensight_contracts/completion.py:170–199`

```text
 170:     def decision_eligible(self,fid,at,*,run_id,purpose='INTERNAL_RESEARCH',allow_absence=False,production=False):
 171:         """Resolve the whole available claim group, not a cherry-picked signal list."""
 172:         f=self.assert_consumed(fid,run_id)
 173:         if not self.usable(fid,at,purpose=purpose,allow_absence=allow_absence,production=production):return False
 174:         run=self.row('runs',run_id)
 175:         # A conflict cannot be laundered through a derived observation.
 176:         for parent in self.ancestry(fid):
 177:             target=self.row('facts',parent)
 178:             fs=[self.row('facts',i) for i in self.available_facts(run) if claim_key(self.row('facts',i))==claim_key(target)]
 179:             got=resolve_claim(fs,at,lambda x,t:self.usable(x['fact_id'],t,purpose=purpose,production=production,allow_absence=True))
 180:             if got['status']!='KNOWN' or parent not in got['accepted_fact_ids']:return False
 181:         return True
 182: 
 183:     def validate_resolution_closure(self,run):
 184:         groups=defaultdict(list)
 185:         for fid in self.available_facts(run):groups[claim_key(self.row('facts',fid))].append(fid)
 186:         covered={}
 187:         for rid in run['resolution_ids']:
 188:             r=self.row('resolutions',rid)
 189:             require(r['run_id']==run['run_id'] and r['tenant_id']==run['tenant_id'],'RESOLUTION_RUN')
 190:             fs=[self.row('facts',i) for i in r['observation_ids']]
 191:             require(bool(fs),'EMPTY_RESOLUTION');key=claim_key(fs[0])
 192:             require(key not in covered,'DUPLICATE_RESOLUTION_FOR_CLAIM')
 193:             require(set(r['observation_ids'])==set(groups.get(key,[])),'INCOMPLETE_CLAIM_RESOLUTION')
 194:             require(r['as_of']==run['as_of'],'RESOLUTION_LOGICAL_TIME')
 195:             require(all(instant(f['recorded_at'])<=instant(r['resolved_at']) for f in fs),'RESOLUTION_BEFORE_INPUT')
 196:             got=resolve_claim(fs,run['as_of'],lambda f,t:self.usable(f['fact_id'],t,allow_absence=True))
 197:             require(got['status']==r['status'] and got['accepted_fact_ids']==sorted(r['accepted_fact_ids']),'RESOLUTION_POLICY_MISMATCH')
 198:             covered[key]=rid
 199:         require(set(covered)==set(groups),'MISSING_CLAIM_RESOLUTION')
```

### `canonical/keensight_contracts/engine.py:86–98`

```text
  86: def resolve_claim(facts: list[dict],as_of: str,eligible) -> dict:
  87:     """Conservative reference: unknowns do not erase known facts; ties abstain.
  88: 
  89:     Explicit supersession removes only named prior observations. Different reports
  90:     remain a conflict unless a separately approved resolution policy decides it.
  91:     """
  92:     require(bool(facts),'EMPTY_CLAIM')
  93:     require(len({claim_key(f) for f in facts})==1,'MIXED_CLAIM_IDENTITIES')
  94:     removed={f['supersedes_fact_id'] for f in facts if f['supersedes_fact_id'] and f['state']!='UNKNOWN' and eligible(f,as_of)}
  95:     candidates=[f for f in facts if f['fact_id'] not in removed and f['state']!='UNKNOWN' and eligible(f,as_of)]
  96:     values={canonical((f['state'],f['object'])) for f in candidates}
  97:     return {'status':'UNKNOWN' if not values else ('KNOWN' if len(values)==1 else 'CONFLICT'),
  98:             'accepted_fact_ids':sorted(f['fact_id'] for f in candidates) if len(values)==1 else []}
```

## F05 — Generated-artifact handoff is accepted by one validator and rejected by another

### `canonical/keensight_contracts/completion.py:425–458`

```text
 425:             generated={aid for ex in self.rows['executions'] if ex['run_id']==run['run_id'] for aid in ex['output_artifact_ids']}
 426:             require(generated==set(run['produced_artifact_ids']) and not generated&set(run['input_artifact_ids']),'RUN_ARTIFACT_OUTPUT_CLOSURE')
 427:             declared=[aid for ex in self.rows['executions'] if ex['run_id']==run['run_id'] for aid in ex['output_artifact_ids']]
 428:             require(len(declared)==len(set(declared)),'MULTIPLE_ARTIFACT_PRODUCERS')
 429:             for aid in run['input_artifact_ids']:
 430:                 require(instant(self.row('artifacts',aid)['captured_at'])<=instant(run['knowledge_cutoff']),'ARTIFACT_AFTER_CUTOFF')
 431:             for sid in run['sample_ids']:
 432:                 sample=self.row('samples',sid)
 433:                 require(sample['tenant_id']==run['tenant_id'] and instant(sample['created_at'])<=instant(run['sealed_at']),'SAMPLE_SEAL')
 434:                 require(set(sample['retrieved_artifact_ids'])<=set(run['input_artifact_ids']),'SAMPLE_UNPINNED_RECORDS')
 435:         for ex in self.rows['executions']:
 436:             run=self.row('runs',ex['run_id']);fn=self.reg('functions',ex['function_id']);profile=self.reg('profiles',run['profile_id'])
 437:             require(ex['function_id'] in profile['execute_function_ids'],'EXECUTED_FUNCTION_NOT_ENABLED')
 438:             require(instant(run['sealed_at'])<=instant(ex['started_at']),'EXECUTION_BEFORE_SEAL')
 439:             if ex['status']!='COMPLETE':require(not ex['output_fact_ids'] and ex['terminal_reason'] is not None,'FAILED_PRODUCER_OUTPUT')
 440:             else:require(ex['terminal_reason'] is None,'SUCCESS_WITH_FAILURE_REASON')
 441:             require(not set(ex['input_artifact_ids'])&set(ex['output_artifact_ids']),'SELF_CONSUMED_ARTIFACT')
 442:             for aid in ex['input_artifact_ids']:
 443:                 require(aid in self.available_artifacts(run),'UNPINNED_EXECUTION_ARTIFACT')
 444:                 if aid in run['produced_artifact_ids']:
 445:                     producer=next(p for p in self.rows['executions'] if p['run_id']==run['run_id'] and aid in p['output_artifact_ids'])
 446:                     require(producer['status']=='COMPLETE' and instant(producer['finished_at'])<=instant(ex['started_at']),'UNFINISHED_ARTIFACT_PRODUCER')
 447:             allowed_generated=set()
 448:             if ex['model_call_id']:
 449:                 model=self.row('model-calls',ex['model_call_id'])
 450:                 allowed_generated={x for x in [model['request_artifact_id'],model['response_artifact_id']] if x}
 451:                 allowed_generated|={r['output_response_artifact_id'] for r in self.rows['repairs'] if r['call_id']==model['call_id']}
 452:             require(set(ex['output_artifact_ids'])<=allowed_generated,'UNSUPPORTED_ARTIFACT_PRODUCER_KIND')
 453:             for aid in ex['output_artifact_ids']:
 454:                 artifact=self.row('artifacts',aid)
 455:                 require(artifact['tenant_id']==ex['tenant_id'] and ex['status']=='COMPLETE','GENERATED_ARTIFACT_OWNER_OR_PRODUCER')
 456:                 require(instant(ex['started_at'])<=instant(artifact['captured_at'])<=instant(ex['finished_at']),'GENERATED_ARTIFACT_TIME')
 457:             for fid in ex['input_fact_ids']:self.assert_consumed(fid,run['run_id'],ex['started_at'])
 458:             samples=[self.row('samples',i) for i in ex['input_sample_ids']]
```

### `canonical/keensight_contracts/validation.py:340–356`

```text
 340:             fn=self.reg('functions',ex['function_id']);run=self.row('runs',ex['run_id']);self.shape(ex['parameters'],fn['parameter_schema'])
 341:             require(ex['function_version']==fn['version'],'FUNCTION_VERSION_MISMATCH')
 342:             require(ex['tenant_id']==run['tenant_id']==self.row('subjects',ex['subject_id'])['tenant_id'],'EXECUTION_TENANT')
 343:             require(instant(ex['started_at'])<=instant(ex['finished_at']),'EXECUTION_TIME')
 344:             require(ex['input_set_hash']==digest({'facts':sorted(ex['input_fact_ids']),'artifacts':sorted(ex['input_artifact_ids'])}),'EXECUTION_INPUT_HASH')
 345:             for fid in ex['input_fact_ids']:
 346:                 f=self.row('facts',fid);require(f['predicate_id'] in fn['input_predicates'],'UNDECLARED_FUNCTION_INPUT')
 347:                 require(f['tenant_id']==ex['tenant_id'],'EXECUTION_INPUT_TENANT')
 348:                 require(instant(f['recorded_at'])<=instant(ex['started_at']),'UNRECORDED_EXECUTION_INPUT')
 349:                 require(f['subject_id']==ex['subject_id'],'UNDECLARED_CROSS_SUBJECT_DERIVATION')
 350:                 require(fid in run['input_fact_ids'] or (f['run_id']==run['run_id'] and f['execution_id'] is not None),'INPUT_OUTSIDE_RUN')
 351:                 if f['execution_id']:
 352:                     pex=self.row('executions',f['execution_id']);require(instant(pex['finished_at'])<=instant(ex['started_at']),'FORWARD_EXECUTION_DEPENDENCY')
 353:             for aid in ex['input_artifact_ids']:require(aid in run['input_artifact_ids'],'ARTIFACT_OUTSIDE_RUN')
 354:             for fid in ex['output_fact_ids']:
 355:                 f=self.row('facts',fid);require(f['execution_id']==ex['execution_id'] and f['subject_id']==ex['subject_id'],'EXECUTION_OUTPUT_LINK')
 356:                 require(f['predicate_id'] in fn['output_predicates'],'UNDECLARED_FUNCTION_OUTPUT')
```

## F06 — HTML recovery can silently truncate the parse while reporting complete detection

### `collector/src/keensight_scrapling/extraction.py:54–67`

```text
  54:     for encoding_source,encoding in choices:
  55:         try: codecs.lookup(encoding); source=body.decode(encoding,errors='replace'); break
  56:         except (LookupError,UnicodeError): continue
  57:     parser = html.HTMLParser(encoding='utf-8',no_network=True, recover=True, huge_tree=False, remove_comments=False)
  58:     try:
  59:         root = html.document_fromstring(source.encode('utf-8') or b'<html></html>', parser=parser)
  60:     except (etree.ParserError, ValueError) as exc:
  61:         return PageEvidence(capture, [], [CommandResult(x, 'FAILED', [capture.capture_id], limitations=[type(exc).__name__]) for x in EXTRACTORS])
  62:     tree = root.getroottree()
  63:     base = capture.url
  64:     for el in root.xpath('//base[@href]')[:1]:
  65:         base = link_url(capture.url, el.get('href')) or capture.url
  66:     results = {c: CommandResult(c, 'COMPLETE', [capture.capture_id]) for c in EXTRACTORS}
  67:     counts = {c: 0 for c in EXTRACTORS}
```

### `collector/src/keensight_scrapling/extraction.py:96–110`

```text
  96:     # Keep node-local attributes so one node cannot lend evidence to another.
  97:     for el in root.iter():
  98:         if not isinstance(el.tag, str):
  99:             continue
 100:         tag = el.tag.lower()
 101:         path = tree.getpath(el)
 102:         attrs = dict(el.attrib)
 103:         if tag == 'script':
 104:             if el.get('src'):
 105:                 value = link_url(base, el.get('src'))
 106:                 if value:
 107:                     add('EXTRACT_SCRIPT_SRC', 'script_url', el, value, locator=path+'/@src', attrs={'type': el.get('type','')})
 108:             elif el.get('type', '').lower() != 'application/ld+json':
 109:                 add('EXTRACT_SCRIPT_INLINE', 'inline_script', el, el.text or '', attrs={'type': el.get('type', '')})
 110:         if tag in {'iframe', 'embed', 'object'}:
```

### `collector/src/keensight_scrapling/rules.py:158–191`

```text
 158:         for page in pages:
 159:             command_states={c.command_id:c.status for c in page.commands}
 160:             needed={KIND_COMMAND[k] for k in rule.kinds}
 161:             if not page.capture.complete or any(command_states.get(c)!='COMPLETE' for c in needed):
 162:                 limited.append(page.capture.capture_id)
 163:             for s in page.surfaces:
 164:                 if s.kind not in rule.kinds or (rule.selector and not s.locator.startswith(rule.selector)):
 165:                     continue
 166:                 if rule.predicate=='vendor.present' and s.context in {'FOOTER','NOSCRIPT','INERT_TEMPLATE','INERT_SCRIPT'}:
 167:                     continue
 168:                 if rule.predicate=='vendor.present' and s.kind=='link_url' and 'stylesheet' not in s.attributes.get('rel','').split():
 169:                     continue
 170:                 value = s.value if rule.field=='value' else str(s.attributes.get(rule.field,''))
 171:                 for pattern in rule.patterns:
 172:                     try:
 173:                         if rule.operator in {'host_suffix','host_equals'}:
 174:                             hit = host_match(value,pattern,exact=rule.operator=='host_equals')
 175:                         elif rule.operator=='equals': hit = value.casefold()==pattern.casefold()
 176:                         elif rule.operator=='regex': hit = bool(regex.search(pattern,value[:131072],timeout=0.025))
 177:                         elif rule.operator=='image_alt': hit = pattern.casefold() in str(s.attributes.get('alt','')).casefold()
 178:                         else: hit = pattern.casefold() in value.casefold()
 179:                     except TimeoutError:
 180:                         errors.append({'capture_id':page.capture.capture_id,'reason':'REGEX_TIMEOUT'})
 181:                         continue
 182:                     if hit:
 183:                         authority = 'APPROVED' if rule.status=='APPROVED' else 'CANDIDATE'
 184:                         mid = identity('match',rule.digest,pack.digest,page.capture.capture_id,s.surface_id,pattern)
 185:                         matches.append(Match(mid,rule.rule_id,rule.digest,pack.digest,authority,page.capture.capture_id,s.surface_id,pattern,rule.predicate,rule.product_id,True,identity('evidence',page.capture.capture_id,s.locator),identity('rule_evidence',rule.digest,page.capture.capture_id,s.surface_id,pattern),rule.confidence))
 186:                         found.append(mid)
 187:         if errors:
 188:             matches = matches[:start]
 189:             found = []
 190:         evaluations.append({'rule_id':rule.rule_id,'status':'ERROR' if errors else 'NOT_EVALUATED' if not pages else 'PARTIAL' if limited else 'MATCH' if found else 'NO_MATCH',
 191:                             'match_ids':found,'errors':errors,'incomplete_capture_ids':sorted(set(limited)), 'qualification':qualification,
```

## F07 — A self-superseding fact raises RecursionError before semantic rejection

### `canonical/keensight_contracts/validation.py:123–130`

```text
 123:         """Current-use veto; storage of historical/candidate/expired records is allowed."""
 124:         f=self.row('facts',fid)
 125:         if f['state']=='UNKNOWN' or (f['state']=='NOT_FOUND' and not allow_absence):return False
 126:         for replacement in self.rows['facts']:
 127:             if replacement['supersedes_fact_id']==fid and replacement['state']!='UNKNOWN' and instant(replacement['recorded_at'])<=instant(at):
 128:                 if self.usable(replacement['fact_id'],at,purpose=purpose,production=production,allow_absence=True):return False
 129:         for change in self.authorized_changes(at):
 130:             if change['tenant_id']!=f['tenant_id']:continue
```

### `canonical/keensight_contracts/validation.py:485–489`

```text
 485:         if f['supersedes_fact_id']:
 486:             prior=self.row('facts',f['supersedes_fact_id'])
 487:             require(claim_key(prior)==claim_key(f) and prior['source_id']==f['source_id'],'WRONG_SUPERSESSION_KEY')
 488:             require(instant(prior['recorded_at'])<instant(f['recorded_at']),'INVALID_SUPERSESSION_ORDER')
 489:             require(f['state']!='UNKNOWN' or prior['state']=='UNKNOWN','UNKNOWN_CANNOT_SUPERSEDE_KNOWN')
```

### `canonical/keensight_contracts/completion.py:183–199`

```text
 183:     def validate_resolution_closure(self,run):
 184:         groups=defaultdict(list)
 185:         for fid in self.available_facts(run):groups[claim_key(self.row('facts',fid))].append(fid)
 186:         covered={}
 187:         for rid in run['resolution_ids']:
 188:             r=self.row('resolutions',rid)
 189:             require(r['run_id']==run['run_id'] and r['tenant_id']==run['tenant_id'],'RESOLUTION_RUN')
 190:             fs=[self.row('facts',i) for i in r['observation_ids']]
 191:             require(bool(fs),'EMPTY_RESOLUTION');key=claim_key(fs[0])
 192:             require(key not in covered,'DUPLICATE_RESOLUTION_FOR_CLAIM')
 193:             require(set(r['observation_ids'])==set(groups.get(key,[])),'INCOMPLETE_CLAIM_RESOLUTION')
 194:             require(r['as_of']==run['as_of'],'RESOLUTION_LOGICAL_TIME')
 195:             require(all(instant(f['recorded_at'])<=instant(r['resolved_at']) for f in fs),'RESOLUTION_BEFORE_INPUT')
 196:             got=resolve_claim(fs,run['as_of'],lambda f,t:self.usable(f['fact_id'],t,allow_absence=True))
 197:             require(got['status']==r['status'] and got['accepted_fact_ids']==sorted(r['accepted_fact_ids']),'RESOLUTION_POLICY_MISMATCH')
 198:             covered[key]=rid
 199:         require(set(covered)==set(groups),'MISSING_CLAIM_RESOLUTION')
```

## F08 — Requirement minimum means fact count in the helper but origin count in validation

### `canonical/keensight_contracts/engine.py:143–150`

```text
 143: def evaluate_requirements(definition: dict,facts: list[dict],subject_id: str,as_of: str,eligible) -> str:
 144:     """Reference AND rule; unknowns/failed checks yield UNRESOLVED, not absence."""
 145:     for req in definition['required_facts']:
 146:         matching=[f for f in facts if f['subject_id']==subject_id and f['predicate_id']==req['predicate_id'] and
 147:                   f['state']==req['state'] and f['nature'] in req['allowed_natures'] and eligible(f['fact_id'],as_of,allow_absence=req['state']=='NOT_FOUND')]
 148:         if len(matching)<req['minimum']:return 'UNRESOLVED'
 149:     return 'RESOLVED'
 150: 
```

### `canonical/keensight_contracts/validation.py:399–407`

```text
 399:             for fid in s['input_fact_ids']:
 400:                 f=self.row('facts',fid);require(f['subject_id']==s['subject_id'] and f['tenant_id']==s['tenant_id'],'CROSS_ACCOUNT_SIGNAL')
 401:             for cid in s['context_ids']:
 402:                 c=self.row('contexts',cid);require(definition['context_allowed'] and c['account_subject_id']==s['subject_id'],'UNDECLARED_SIGNAL_CONTEXT')
 403:             if s['status']=='RESOLVED':
 404:                 for req in definition['required_facts']:
 405:                     good=[self.row('facts',fid) for fid in s['input_fact_ids'] if self.row('facts',fid)['predicate_id']==req['predicate_id'] and self.row('facts',fid)['state']==req['state'] and self.row('facts',fid)['nature'] in req['allowed_natures'] and self.decision_eligible(fid,run['as_of'],run_id=run['run_id'],allow_absence=req['state']=='NOT_FOUND')]
 406:                     origins=distinct_origins(self.row('artifacts',a) for f in good for a in self.corroborating_artifacts(f['fact_id']))
 407:                     require(len(origins)>=req['minimum'],'SIGNAL_REQUIREMENT_UNSATISFIED')
```

## F09 — Retained-file import does not pin subject identity in run configuration

### `collector/src/keensight_scrapling/cli.py:103–114`

```text
 103:                 elif args.command=='candidates':result=store.candidates(args.tenant,args.min_hosts)
 104:                 elif args.command=='claims':
 105:                     pack=RulePack.load(args.rules)
 106:                     result=[asdict(c) for c in store.stored_claims(args.tenant,as_of=args.as_of,allowed_rule_digests={r.digest for r in pack.rules if r.status=='APPROVED'})]
 107:                 elif args.command=='replay':
 108:                     pack=RulePack.load(args.rules)
 109:                     # Replay never invokes this deliberately unusable transport.
 110:                     runner=Scanner(store,pack,FixtureTransport({}),production=not pack.fixture_only)
 111:                     result=runner.replay(args.tenant,args.capture_run,args.evaluation_run,args.as_of)
 112:                     write_json(args.output,result);result={'bundle':args.output,'claims':len(result['claims'])}
 113:                 else:
 114:                     # Missing dependencies are a CLI error, not a successful empty scan.
```

### `collector/src/keensight_scrapling/storage.py:59–67`

```text
  59:     def begin_run(self, tenant: str, run_id: str, config: dict):
  60:         if not tenant or not run_id:
  61:             raise ContractError('Tenant and run ID are required')
  62:         payload=canonical(config); digest=identity('runconfig',config)
  63:         with self.db:
  64:             row=self.db.execute('SELECT config_hash FROM runs WHERE tenant=? AND run_id=?',(tenant,run_id)).fetchone()
  65:             if row and row['config_hash']!=digest:
  66:                 raise ContractError('Run ID reuse with changed configuration or release; use a new run or replay')
  67:             self.db.execute('INSERT OR IGNORE INTO runs VALUES(?,?,?,?)',(tenant,run_id,digest,payload))
```

### `collector/src/keensight_scrapling/pipeline.py:248–256`

```text
 248:         caps=self.store.captures(tenant,capture_run_id)
 249:         if not caps: raise ContractError('Unknown capture run')
 250:         pages=[]
 251:         for c in caps:
 252:             if not self.store.replay_eligible(c): continue
 253:             body=self.store.body(c)
 254:             if any(marker in body[:200000].lower() for marker in (b'<title>just a moment',b'<title>access denied',b'cf-chl-widget')): continue
 255:             pages.append(extract(c,body))
 256:         return self.evaluate(pages,evaluation_id,as_of,[CommandResult('CATALOG_LOAD','COMPLETE',details={'release_digest':self.pack.digest,'mode':'REPLAY'})],captures=caps)
```

## F10 — Current candidate discovery counts unlabelled revoked evidence

### `collector/src/keensight_scrapling/storage.py:164–215`

```text
 164:             for link in links:
 165:                 self.db.execute('INSERT OR IGNORE INTO support VALUES(?,?,?)',(tenant,link.observation_id,link.match_id))
 166: 
 167:     def captures(self,tenant: str, run_id: str | None=None) -> list[Capture]:
 168:         query='SELECT payload FROM captures WHERE tenant=?'; params=[tenant]
 169:         if run_id is not None: query+=' AND run_id=?'; params.append(run_id)
 170:         return [Capture(**strict_json(r['payload'])) for r in self.db.execute(query+' ORDER BY id',params)]
 171: 
 172:     def revoke(self,tenant: str,capture_id: str,reason: str):
 173:         # Local owner operation only; no claim of solving hosted ChangeRecord F.
 174:         if not reason: raise ContractError('Revocation reason required')
 175:         with self.db: self.db.execute('INSERT OR REPLACE INTO revoked_captures VALUES(?,?,?)',(tenant,capture_id,reason))
 176: 
 177:     def stored_claims(self,tenant: str,*,as_of: str,allowed_rule_digests: set[str] | None=None):
 178:         from .claims import resolve_claims
 179:         def allrows(table): return [strict_json(r['payload']) for r in self.db.execute(f'SELECT payload FROM {table} WHERE tenant=?',(tenant,))]
 180:         obs=[Observation(**x) for x in allrows('observations')]
 181:         matches=[Match(**x) for x in allrows('matches')]
 182:         links=[SupportLink(r['observation_id'],r['match_id']) for r in self.db.execute('SELECT * FROM support WHERE tenant=?',(tenant,))]
 183:         revoked={r[0] for r in self.db.execute('SELECT capture_id FROM revoked_captures WHERE tenant=?',(tenant,))}
 184:         return resolve_claims(obs,matches,links,self.captures(tenant),as_of=as_of,allowed_rule_digests=allowed_rule_digests,revoked_capture_ids=revoked)
 185: 
 186:     def harvest(self,tenant: str,pages,*,matched_surface_ids: set[str], transaction_owned=False):
 187:         from .urls import origin
 188:         from urllib.parse import urlsplit
 189:         from contextlib import nullcontext
 190:         with (nullcontext() if transaction_owned else self.db):
 191:             for page in pages:
 192:                 for s in page.surfaces:
 193:                     if s.surface_id in matched_surface_ids: continue
 194:                     if s.kind in {'script_url','iframe_url','link_url'}:
 195:                         normalized=(urlsplit(s.value).hostname or '').lower()
 196:                         kind=s.kind+':host'
 197:                     elif s.kind=='cookie_name': normalized=s.value; kind=s.kind
 198:                     else: continue
 199:                     if not normalized: continue
 200:                     feature=identity('feature',kind,normalized)
 201:                     self.db.execute('INSERT OR IGNORE INTO feature_occurrences VALUES(?,?,?,?,?)',
 202:                         (tenant,feature,origin(page.capture.url),page.capture.capture_id,canonical({'kind':kind,'value':normalized})))
 203: 
 204:     def candidates(self,tenant: str,min_hosts: int=3):
 205:         if min_hosts<1: raise ContractError('min_hosts must be positive')
 206:         return [dict(row) for row in self.db.execute('''SELECT feature_id,value,COUNT(DISTINCT origin) AS observed_origin_count,
 207:           COUNT(DISTINCT capture_id) AS capture_count FROM feature_occurrences WHERE tenant=? GROUP BY feature_id,value
 208:           HAVING COUNT(DISTINCT origin)>=? ORDER BY observed_origin_count DESC,feature_id''',(tenant,min_hosts))]
 209: 
 210: 
 211:     def publish_evaluation(self, data, pages, matches, observations, links):
 212:         """Publish only a validated evaluation; every projection write rolls back together.
 213: 
 214:         Physical capture bytes/attempt diagnostics already retained are intentionally
 215:         outside this publication transaction. A commit is a local owner boundary,
```

## F11 — Contradictory duplicate command outcomes are accepted

### `collector/src/keensight_scrapling/pipeline.py:211–218`

```text
 211:         for operator in sorted({r.operator for r in self.pack.rules}):
 212:             mids=[m.match_id for m in matches if next(r for r in self.pack.rules if r.rule_id==m.rule_id).operator==operator]
 213:             reports=[r for r in rule_evaluations if next(x for x in self.pack.rules if x.rule_id==r['rule_id']).operator==operator]
 214:             status='FAILED' if any(r['status']=='ERROR' for r in reports) else 'PARTIAL' if any(r['status']=='PARTIAL' for r in reports) else 'SKIPPED' if not pages else 'COMPLETE'
 215:             commands.append(CommandResult(MATCH_COMMAND[operator],status,input_ids=[p.capture.capture_id for p in pages],output_ids=mids))
 216:         if any(len(r.patterns)>1 for r in self.pack.rules):
 217:             commands.append(CommandResult('MATCH_OR_GROUP','COMPLETE',details={'semantics':'ANY alternative; all matched branches retained'}))
 218:         commands.extend([
```

### `collector/src/keensight_scrapling/validation.py:60–72`

```text
  60:     from .rules import MATCH_COMMAND
  61:     for operator in {r.operator for r in pack.rules}:
  62:         cid=MATCH_COMMAND[operator]
  63:         command_rows=[c for c in data['commands'] if c['command_id']==cid]
  64:         reports=[r for r in expected_reports if next(x for x in pack.rules if x.rule_id==r['rule_id']).operator==operator]
  65:         expected_status='FAILED' if any(r['status']=='ERROR' for r in reports) else 'PARTIAL' if any(r['status']=='PARTIAL' for r in reports) else 'SKIPPED' if not pages else 'COMPLETE'
  66:         mids=sorted(m.match_id for m in matches if next(r for r in pack.rules if r.rule_id==m.rule_id).operator==operator)
  67:         if not any(c['status']==expected_status and sorted(c['output_ids'])==mids and sorted(c['input_ids'])==sorted(selected) for c in command_rows):
  68:             raise ContractError('Matcher command contradicts executable result')
  69:     obs=[Observation(**o) for o in data['observations']]
  70:     expected,links=observation_candidates(caps.values(),matches)
  71:     if sorted(map(canonical,map(record,expected)))!=sorted(map(canonical,data['observations'])):
  72:         raise ContractError('Observation target, identity, provenance or value is inconsistent')
```

### `collector/src/keensight_scrapling/core.py:100–111`

```text
 100: class CommandResult:
 101:     command_id: str
 102:     status: str
 103:     input_ids: list[str] = field(default_factory=list)
 104:     output_ids: list[str] = field(default_factory=list)
 105:     limitations: list[str] = field(default_factory=list)
 106:     details: dict[str, Any] = field(default_factory=dict)
 107: 
 108: 
 109: @dataclass
 110: class PageEvidence:
 111:     capture: Capture
```

## F12 — No-byte failures lose invocation details and have no persisted evaluation manifest

### `collector/src/keensight_scrapling/pipeline.py:46–60`

```text
  46:         if production and pack.fixture_only:
  47:             raise ContractError('Fixture-only rules are forbidden in production before capture')
  48:         self.store=store;self.pack=pack;self.transport=transport
  49:         self.browser=browser or ScraplingBrowserTransport();self.clock=clock;self.production=production
  50: 
  51:     def scan(self,url: str,config: ScanConfig) -> dict:
  52:         seed=normalize_url(url); base=origin(seed)
  53:         cfg={**asdict(config),'seed':seed,'release_digest':self.pack.digest,'code_version':'0.2.0'}
  54:         self.store.begin_run(config.tenant_id,config.run_id,cfg)
  55:         commands=[CommandResult('CATALOG_LOAD','COMPLETE',details={'release_digest':self.pack.digest}),
  56:                   CommandResult('NORM_URL','COMPLETE',details={'seed':seed})]
  57:         dispositions=[];pages=[];allcaps={}; denied=self.store.cooling_down(config.tenant_id,base,self.clock())
  58:         delay=config.min_delay_seconds; last_request=None
  59:         # Stored attempts are reused; PENDING means crash uncertainty and is not retried.
  60:         def request(target,command,mode='RAW_HTML'):
```

### `collector/src/keensight_scrapling/pipeline.py:76–126`

```text
  76:                         if cap.status_code==429: denied=True
  77:                         allcaps[cap.capture_id]=cap
  78:                         commands.append(CommandResult(command,'REUSED',[cap.capture_id],details={'url':target}))
  79:                         return cap
  80:                 reason='INTERRUPTED_ATTEMPT_NO_BLIND_RETRY' if attempt['status']=='PENDING' else attempt['status']
  81:                 dispositions.append({'url':target,'status':reason})
  82:                 commands.append(CommandResult(command,reason,details={'url':target}))
  83:                 return None
  84:             try:
  85:                 if not getattr(self.transport,'is_fixture',False):
  86:                     if last_request is not None:
  87:                         time.sleep(max(0,delay-(time.monotonic()-last_request)))
  88:                     last_request=time.monotonic()
  89:                 reply=(self.browser if mode=='RENDERED_DOM' else self.transport).get(target)
  90:                 if normalize_url(reply.url)!=target:
  91:                     raise ContractError('Unrecorded redirect from transport')
  92:                 data=reply.body[:config.max_body_bytes]
  93:                 complete=reply.complete and len(reply.body)<=config.max_body_bytes
  94:                 limitations=list(reply.limitations)
  95:                 if not complete: limitations.append('CAPTURE_INCOMPLETE')
  96:                 cap=self.store.put_capture(tenant_id=config.tenant_id,subject_id=config.subject_id,run_id=config.run_id,
  97:                                           url=target,observed_at=self.clock(),body=data,headers=reply.headers,status_code=reply.status_code,
  98:                                           mode=mode,complete=complete,limitations=limitations,source_ttl_seconds=config.source_ttl_seconds,
  99:                                           source_id='source:synthetic-fixture' if getattr(self.transport,'is_fixture',False) else 'source:public-website')
 100:                 allcaps[cap.capture_id]=cap
 101:                 payload={'url':target,'capture_id':cap.capture_id,'http_status':cap.status_code,'mode':mode,'finished_at':self.clock()}
 102:                 self.store.finish_attempt(config.tenant_id,config.run_id,key,'COMPLETE',payload)
 103:                 commands.append(CommandResult(command,'COMPLETE' if complete else 'PARTIAL',output_ids=[cap.capture_id],details=payload))
 104:                 if cap.status_code==429:
 105:                     denied=True
 106:                     from datetime import timedelta, timezone
 107:                     from email.utils import parsedate_to_datetime
 108:                     retry=cap.headers.get('retry-after','').strip()
 109:                     try:
 110:                         until=(instant(self.clock())+timedelta(seconds=max(1,int(retry)))).isoformat().replace('+00:00','Z')
 111:                     except (ValueError,OverflowError):
 112:                         try: until=parsedate_to_datetime(retry).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
 113:                         except (ValueError,TypeError,OverflowError): until=(instant(self.clock())+timedelta(hours=1)).isoformat().replace('+00:00','Z')
 114:                     self.store.set_cooldown(config.tenant_id,base,until)
 115:                 return cap
 116:             except Exception as exc:
 117:                 reason=type(exc).__name__
 118:                 payload={'url':target,'reason':reason,'message':str(exc)[:300],'finished_at':self.clock()}
 119:                 self.store.finish_attempt(config.tenant_id,config.run_id,key,'FAILED',payload)
 120:                 commands.append(CommandResult(command,'FAILED',limitations=[reason],details=payload))
 121:                 dispositions.append({'url':target,'status':'FAILED','reason':reason})
 122:                 return None
 123:         robots_url=base+'/robots.txt'
 124:         rc=request(robots_url,'FETCH_ROBOTS')
 125:         rp,maps,reason=robots_policy(robots_url,rc.status_code,self.store.body(rc),rc.complete) if rc else (None,[],'ROBOTS_UNAVAILABLE_FAIL_CLOSED')
 126:         if rp is None:
```

### `collector/src/keensight_scrapling/storage.py:69–94`

```text
  69:     def reserve_attempt(self, tenant: str, run_id: str, request_key: str, budget: int, payload: dict) -> dict:
  70:         self.db.execute('BEGIN IMMEDIATE')
  71:         try:
  72:             row=self.db.execute('SELECT status,payload FROM attempts WHERE tenant=? AND run_id=? AND request_key=?',(tenant,run_id,request_key)).fetchone()
  73:             if row:
  74:                 self.db.commit()
  75:                 return {'new':False,'status':row['status'],'payload':strict_json(row['payload'])}
  76:             count=self.db.execute('SELECT COUNT(*) FROM attempts WHERE tenant=? AND run_id=?',(tenant,run_id)).fetchone()[0]
  77:             if count>=budget:
  78:                 self.db.commit(); return {'new':False,'status':'SKIPPED_BUDGET','payload':{}}
  79:             self.db.execute('INSERT INTO attempts VALUES(?,?,?,?,?)',(tenant,run_id,request_key,'PENDING',canonical(payload)))
  80:             self.db.commit()
  81:             return {'new':True,'status':'PENDING','payload':payload}
  82:         except Exception:
  83:             self.db.rollback(); raise
  84: 
  85:     def finish_attempt(self, tenant: str, run_id: str, key: str, status: str, payload: dict):
  86:         with self.db:
  87:             row=self.db.execute('SELECT status,payload FROM attempts WHERE tenant=? AND run_id=? AND request_key=?',(tenant,run_id,key)).fetchone()
  88:             if not row:
  89:                 raise ContractError('Attempt was not reserved')
  90:             if row['status']!='PENDING':
  91:                 if row['status']!=status or row['payload']!=canonical(payload):
  92:                     raise ContractError('Terminal attempt cannot be rewritten')
  93:                 return
  94:             self.db.execute('UPDATE attempts SET status=?,payload=? WHERE tenant=? AND run_id=? AND request_key=?',(status,canonical(payload),tenant,run_id,key))
```

### `collector/src/keensight_scrapling/storage.py:214–236`

```text
 214:         Physical capture bytes/attempt diagnostics already retained are intentionally
 215:         outside this publication transaction. A commit is a local owner boundary,
 216:         not a substitute for hosted authentication.
 217:         """
 218:         from .validation import validate_bundle
 219:         validate_bundle(data)
 220:         caps = [Capture(**c) for c in data['captures']]
 221:         for cap in caps:
 222:             self.body(cap)
 223:         tenants = {c.tenant_id for c in caps}
 224:         if len(tenants) > 1:
 225:             raise ContractError('Cross-tenant evaluation')
 226:         if not tenants:
 227:             return
 228:         tenant = next(iter(tenants))
 229:         key = identity('evaluation', data['evaluation_id'], data['release_digest'],
 230:                        data['as_of'], data['evaluated_capture_ids'])
 231:         # Transport diagnostics can legitimately differ on resume. Only immutable
 232:         # semantic output is stored as the publication identity.
 233:         payload = canonical({k:data[k] for k in ('evaluation_id','as_of','release_digest',
 234:                             'evaluated_capture_ids','matches','observations','support_links','claims')})
 235:         with self.db:
 236:             old = self.db.execute('SELECT payload FROM evaluations WHERE tenant=? AND evaluation_key=?',
```

## F13 — Protocol rejects an honest timeout failure reported after its deadline

### `protocol/validate_protocol.py:92–151`

```text
  92:           'CaptureInput':{'body_digest':{'type':'string','minLength':1},'observed_at':{'type':'string','format':'date-time'}},
  93:           'FingerprintParameters':{'allow_network':{'const':False},'policy':{'const':'approved-only'}},
  94:           'ReleaseLock':{'collector':{'type':'string'},'domain_contracts':{'type':'string'},'rule_release':{'type':'string'}},
  95:           'MatchEvaluation':{'evidence_points':{'type':'integer','minimum':0},'matches':{'type':'integer','minimum':0},'verdict':{'enum':['MATCH','NO_MATCH','UNKNOWN']}},
  96:         }
  97:         if expected not in bodies:raise ValueError('No installed domain payload validator')
  98:         body_schema={'type':'object','properties':bodies[expected],'required':list(bodies[expected]),'additionalProperties':False}
  99:         Draft7Validator(body_schema,format_checker=FormatChecker()).validate(payload['body'])
 100:     return True
 101: 
 102: def validate_pair(request: dict[str, Any], result: dict[str, Any]) -> None:
 103:     vs = validators()
 104:     vs["ModuleRequest"].validate(request)
 105:     vs["ModuleResult"].validate(result)
 106:     for key in ("request_id", "execution_id", "module_id", "operation", "context", "trace"):
 107:         if request[key] != result[key]:
 108:             raise ValueError(f"Request/result mismatch at {key}")
 109:     if result["request_digest"] != digest(request):
 110:         raise ValueError("Request digest mismatch")
 111:     if datetime.fromisoformat(result["finished_at"]) < datetime.fromisoformat(result["started_at"]):
 112:         raise ValueError("Result finished before it started")
 113:     if result["reused_execution_id"] == result["execution_id"]:
 114:         raise ValueError("Execution cannot reuse itself")
 115:     if request["module_id"] != "CTL-01" and request["release_lock_ref"] is None:
 116:         raise ValueError("Non-bootstrap operation requires a release lock")
 117:     mids = {m["module_id"] for m in load(ROOT / "modules.json")["modules"]}
 118:     if request["module_id"] not in mids:
 119:         raise ValueError("Unregistered module")
 120:     signature=OPERATION_SIGNATURES.get((request['module_id'],request['operation']))
 121:     if signature is None:raise ValueError('Unregistered operation implementation/signature')
 122:     if len(request['input_refs'])<signature['min_inputs'] or any(ref_type(r) not in signature['inputs'] for r in request['input_refs']):
 123:         raise ValueError('Operation input schema/version mismatch')
 124:     if request['parameters_ref'] is None or ref_type(request['parameters_ref'])!=signature['parameters']:
 125:         raise ValueError('Operation parameters schema/version mismatch')
 126:     if request['release_lock_ref'] is None or ref_type(request['release_lock_ref'])!=signature['release']:
 127:         raise ValueError('Operation release schema/version mismatch')
 128:     declared=request['input_refs']+[request[k] for k in ('release_lock_ref','parameters_ref','budget_reservation_ref') if request[k] is not None]
 129:     allowed={r['record_id']:r for r in declared}
 130:     if len(allowed)!=len(declared):raise ValueError('Duplicate declared input reference')
 131:     consumed=result['consumed_refs']
 132:     if len({r['record_id'] for r in consumed})!=len(consumed):raise ValueError('Duplicate consumed reference')
 133:     if any(allowed.get(r['record_id'])!=r for r in consumed):raise ValueError('Consumed record not declared by exact reference')
 134:     if result['execution_status']=='SUCCEEDED':
 135:         if {r['record_id'] for r in consumed}!=set(allowed):raise ValueError('Successful operation did not report required inputs')
 136:         if len(result['output_refs'])<signature['min_outputs']:raise ValueError('Successful operation omitted output')
 137:     if any(ref_type(r) not in signature['outputs'] for r in result['output_refs']):raise ValueError('Operation output schema/version mismatch')
 138:     if len({r['record_id'] for r in result['output_refs']})!=len(result['output_refs']):raise ValueError('Duplicate output reference')
 139:     if any(r['record_id'] in allowed for r in result['output_refs']):raise ValueError('Output overwrites an immutable input')
 140:     if datetime.fromisoformat(result['finished_at'])>datetime.fromisoformat(request['deadline_at']):raise ValueError('Operation finished beyond deadline')
 141:     context = request["context"]
 142:     if context["as_of"] and context["knowledge_cutoff"]:
 143:         # These timestamps have different meanings: either may be earlier.
 144:         # Do not invent an ordering relation between valid time and recorded time.
 145:         pass
 146:     allowed_codes = load(ROOT / "error_codes.json")["codes"]
 147:     if any(d["code"] not in allowed_codes for d in result["diagnostics"]):
 148:         raise ValueError("Unregistered diagnostic code")
 149:     all_refs = request["input_refs"] + result["consumed_refs"] + result["output_refs"] + result["diagnostic_record_refs"]
 150:     for key in ("release_lock_ref", "parameters_ref", "budget_reservation_ref"):
 151:         if request[key] is not None:
```

## F14 — Collector and canonical matcher disagree on aside-region semantics

### `collector/src/keensight_scrapling/extraction.py:23–35`

```text
  23: def region(node) -> str:
  24:     tags = {str(n.tag).lower() for n in [node, *node.iterancestors()]}
  25:     if str(node.tag).lower()=='script' and node.get('type','').strip().lower() not in {'','module','text/javascript','application/javascript','application/ecmascript','text/ecmascript'}:
  26:         return 'INERT_SCRIPT'
  27:     if 'template' in tags:
  28:         return 'INERT_TEMPLATE'
  29:     if 'noscript' in tags:
  30:         return 'NOSCRIPT'
  31:     if 'footer' in tags:
  32:         return 'FOOTER'
  33:     if tags & {'header', 'nav'}:
  34:         return 'HEADER_NAV'
  35:     return 'PAGE'
```

### `collector/src/keensight_scrapling/rules.py:163–169`

```text
 163:             for s in page.surfaces:
 164:                 if s.kind not in rule.kinds or (rule.selector and not s.locator.startswith(rule.selector)):
 165:                     continue
 166:                 if rule.predicate=='vendor.present' and s.context in {'FOOTER','NOSCRIPT','INERT_TEMPLATE','INERT_SCRIPT'}:
 167:                     continue
 168:                 if rule.predicate=='vendor.present' and s.kind=='link_url' and 'stylesheet' not in s.attributes.get('rel','').split():
 169:                     continue
```

### `canonical/keensight_contracts/engine.py:117–138`

```text
 117: def fingerprint_hosts(definition: dict,html: str) -> set[str]:
 118:     """Narrow HTML fixture matcher; not a 2,500-signature library or live browser."""
 119:     from html.parser import HTMLParser
 120:     from urllib.parse import urlsplit
 121:     require(definition['operator']=='SCRIPT_HOST','MATCHER_NOT_IMPLEMENTED')
 122:     class Parser(HTMLParser):
 123:         def __init__(self):super().__init__();self.stack=[];self.hits=set()
 124:         def handle_starttag(self,tag,attrs):
 125:             if tag=='script' and dict(attrs).get('type','').strip().lower() in ('','module','text/javascript','application/javascript','application/ecmascript','text/ecmascript') and not any(x in ['footer','aside','template','noscript'] for x in self.stack):
 126:                 src=dict(attrs).get('src','')
 127:                 try:host=(urlsplit('https:'+src if src.startswith('//') else src).hostname or '').lower().rstrip('.')
 128:                 except ValueError:host=''
 129:                 domain=definition['match_value'].lower().rstrip('.')
 130:                 if host==domain or host.endswith('.'+domain):self.hits.add(host)
 131:             if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(tag)
 132:         def handle_endtag(self,tag):
 133:             if tag in self.stack:
 134:                 while self.stack:
 135:                     if self.stack.pop()==tag:break
 136:     p=Parser();p.feed(html);p.close();return p.hits
 137: 
 138: 
```

## F15 — The protocol fixture does not constrain mode/effects against operation parameters

### `protocol/validate_protocol.py:51–131`

```text
  51:     return {
  52:         s["$id"].rsplit(":", 1)[-1]: Draft7Validator(s, registry=registry,
  53:                                                     format_checker=FormatChecker())
  54:         for s in schemas
  55:     }
  56: 
  57: 
  58: # Installed operation signatures are trusted application configuration, never
  59: # arbitrary entrypoint names from a request. Only the delivered fixture adapter
  60: # is registered here. Other proposed operations deliberately fail closed.
  61: OPERATION_SIGNATURES = {
  62:     ('FP-01','match'): {
  63:         'inputs': {('urn:keensight:protocol-fixture:CaptureInput','example-only')},
  64:         'parameters': ('urn:keensight:protocol-fixture:FingerprintParameters','example-only'),
  65:         'release': ('urn:keensight:protocol-fixture:ReleaseLock','example-only'),
  66:         'outputs': {('urn:keensight:protocol-fixture:MatchEvaluation','example-only')},
  67:         'min_inputs': 1,'min_outputs': 1,
  68:     }
  69: }
  70: 
  71: def ref_type(ref):return (ref['schema_id'],ref['schema_version'])
  72: 
  73: def validate_payload_pair(request, result, resolve):
  74:     """Resolve all referenced bytes through a trusted local record resolver.
  75: 
  76:     This is an admission/verification helper, not a process sandbox or an auth
  77:     server. `resolve` must enforce tenant isolation and immutable storage.
  78:     """
  79:     validate_pair(request,result)
  80:     refs=request['input_refs']+result['consumed_refs']+result['output_refs']+result['diagnostic_record_refs']
  81:     refs += [request[k] for k in ('parameters_ref','release_lock_ref') if request[k]]
  82:     for ref in refs:
  83:         payload=resolve(ref)
  84:         if digest(payload)!=ref['content_digest']:raise ValueError('Resolved record digest mismatch')
  85:         expected=ref['schema_id'].rsplit(':',1)[-1]
  86:         # This delivered operation is explicitly fixture-only, not a shortcut
  87:         # accepting arbitrary production records in the generic envelope.
  88:         if set(payload)!={'body','fixture_only','type'} or payload['fixture_only'] is not True or payload['type']!=expected:
  89:             raise ValueError('Resolved record violates registered fixture contract')
  90:         if not isinstance(payload['body'],dict):raise ValueError('Invalid fixture body')
  91:         bodies={
  92:           'CaptureInput':{'body_digest':{'type':'string','minLength':1},'observed_at':{'type':'string','format':'date-time'}},
  93:           'FingerprintParameters':{'allow_network':{'const':False},'policy':{'const':'approved-only'}},
  94:           'ReleaseLock':{'collector':{'type':'string'},'domain_contracts':{'type':'string'},'rule_release':{'type':'string'}},
  95:           'MatchEvaluation':{'evidence_points':{'type':'integer','minimum':0},'matches':{'type':'integer','minimum':0},'verdict':{'enum':['MATCH','NO_MATCH','UNKNOWN']}},
  96:         }
  97:         if expected not in bodies:raise ValueError('No installed domain payload validator')
  98:         body_schema={'type':'object','properties':bodies[expected],'required':list(bodies[expected]),'additionalProperties':False}
  99:         Draft7Validator(body_schema,format_checker=FormatChecker()).validate(payload['body'])
 100:     return True
 101: 
 102: def validate_pair(request: dict[str, Any], result: dict[str, Any]) -> None:
 103:     vs = validators()
 104:     vs["ModuleRequest"].validate(request)
 105:     vs["ModuleResult"].validate(result)
 106:     for key in ("request_id", "execution_id", "module_id", "operation", "context", "trace"):
 107:         if request[key] != result[key]:
 108:             raise ValueError(f"Request/result mismatch at {key}")
 109:     if result["request_digest"] != digest(request):
 110:         raise ValueError("Request digest mismatch")
 111:     if datetime.fromisoformat(result["finished_at"]) < datetime.fromisoformat(result["started_at"]):
 112:         raise ValueError("Result finished before it started")
 113:     if result["reused_execution_id"] == result["execution_id"]:
 114:         raise ValueError("Execution cannot reuse itself")
 115:     if request["module_id"] != "CTL-01" and request["release_lock_ref"] is None:
 116:         raise ValueError("Non-bootstrap operation requires a release lock")
 117:     mids = {m["module_id"] for m in load(ROOT / "modules.json")["modules"]}
 118:     if request["module_id"] not in mids:
 119:         raise ValueError("Unregistered module")
 120:     signature=OPERATION_SIGNATURES.get((request['module_id'],request['operation']))
 121:     if signature is None:raise ValueError('Unregistered operation implementation/signature')
 122:     if len(request['input_refs'])<signature['min_inputs'] or any(ref_type(r) not in signature['inputs'] for r in request['input_refs']):
 123:         raise ValueError('Operation input schema/version mismatch')
 124:     if request['parameters_ref'] is None or ref_type(request['parameters_ref'])!=signature['parameters']:
 125:         raise ValueError('Operation parameters schema/version mismatch')
 126:     if request['release_lock_ref'] is None or ref_type(request['release_lock_ref'])!=signature['release']:
 127:         raise ValueError('Operation release schema/version mismatch')
 128:     declared=request['input_refs']+[request[k] for k in ('release_lock_ref','parameters_ref','budget_reservation_ref') if request[k] is not None]
 129:     allowed={r['record_id']:r for r in declared}
 130:     if len(allowed)!=len(declared):raise ValueError('Duplicate declared input reference')
 131:     consumed=result['consumed_refs']
```

## F16 — effective_at is stored but its decision semantics are undefined/unused

### `canonical/keensight_contracts/engine.py:37–44`

```text
  37: def claim_key(fact: dict) -> tuple:
  38:     """Nature is part of the claim channel; source identity remains on observations.
  39: 
  40:     Reports never silently overwrite direct observations. Measurement targets include
  41:     provider/method/dimensions; PERIOD windows distinguish distinct measurements.
  42:     """
  43:     return (fact['tenant_id'],fact['subject_id'],fact['predicate_id'],fact['nature'],
  44:             fact['scope_id'],canonical(fact['target']).decode(),canonical(fact['window']).decode())
```

### `canonical/keensight_contracts/validation.py:123–171`

```text
 123:         """Current-use veto; storage of historical/candidate/expired records is allowed."""
 124:         f=self.row('facts',fid)
 125:         if f['state']=='UNKNOWN' or (f['state']=='NOT_FOUND' and not allow_absence):return False
 126:         for replacement in self.rows['facts']:
 127:             if replacement['supersedes_fact_id']==fid and replacement['state']!='UNKNOWN' and instant(replacement['recorded_at'])<=instant(at):
 128:                 if self.usable(replacement['fact_id'],at,purpose=purpose,production=production,allow_absence=True):return False
 129:         for change in self.authorized_changes(at):
 130:             if change['tenant_id']!=f['tenant_id']:continue
 131:             if instant(change['effective_at'])<=instant(at) and change['target_id'] in (fid,f['source_id'],f['binding_id']):return False
 132:         for aid in self.roots(fid):
 133:             a=self.row('artifacts',aid);s=self.reg('sources',a['source_id'])
 134:             if a['status']!='OK' or s['authority']!='ACTIVE':return False
 135:             if a['retention_state']!='RETAINED' or instant(a['retained_until'])<=instant(at):return False
 136:             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
 137:             if a['classification']=='SENSITIVE':return False
 138:             if any(c['target_id']==aid and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 139:         for parent in self.ancestry(fid):
 140:             x=self.row('facts',parent);s=self.reg('sources',x['source_id'])
 141:             if x['state']=='UNKNOWN' or instant(x['observed_at'])>instant(at) or instant(x['expires_at'])<=instant(at):return False
 142:             if s['authority']!='ACTIVE' or (production and s['fixture_only']):return False
 143:             if any(c['target_id'] in (parent,x['source_id'],x['binding_id']) and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 144:             if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
 145:             if x['predicate_id']=='technology.footprint' and x['state']=='OBSERVED':
 146:                 fp=self.reg('fingerprints',x['object']['fingerprint_id'])
 147:                 if fp['authority']!='ACTIVE' or (production and fp['fixture_only']):return False
 148:                 if any(c['target_id']==fp['fingerprint_id'] and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 149:             if x['binding_id']:
 150:                 b=self.row('bindings',x['binding_id'])
 151:                 if b['status']!='ACCEPTED' or b['role'] in ['AGENCY','MENTION_ONLY','UNRESOLVED']:return False
 152:             if x['execution_id']:
 153:                 ex=self.row('executions',x['execution_id']);fn=self.reg('functions',ex['function_id'])
 154:                 if ex['status']!='COMPLETE':return False
 155:                 if instant(ex['finished_at'])>instant(x['recorded_at']):return False
 156:                 if fn['authority']!='ACTIVE' or (production and fn['fixture_only']):return False
 157:                 if any(c['target_id']==fn['function_id'] and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
 158:                 if ex['model_call_id']:
 159:                     call=self.row('model-calls',ex['model_call_id'])
 160:                     if call['status']!='PARSED' or call['response_artifact_id'] is None:return False
 161:                     repairs=sorted([r for r in self.rows['repairs'] if r['call_id']==call['call_id']],key=lambda r:r['ordinal'])
 162:                     if len(repairs)>call['max_repair_attempts'] or (repairs and repairs[-1]['status']!='VALID'):return False
 163:                     for aid in [call['request_artifact_id'],call['response_artifact_id']]:
 164:                         artifact=self.row('artifacts',aid)
 165:                         if artifact['retention_state']!='RETAINED' or instant(artifact['retained_until'])<=instant(at):return False
 166:         return True
 167:     def evidence_text(self,evidence):
 168:         return '\n'.join(self.locator_text(self.row('locators',lid)) for lid in evidence['locator_ids'])
 169:     def locator_text(self,l):
 170:         a=self.row('artifacts',l['artifact_id'])
 171:         if a['retention_state']!='RETAINED':return ''
```

### `canonical/keensight_contracts/validation.py:452–493`

```text
 452:     def validate_fact(self,f):
 453:         p=self.reg('predicates',f['predicate_id']);s=self.reg('sources',f['source_id']);scope=self.row('scopes',f['scope_id']);sub=self.row('subjects',f['subject_id']);run=self.row('runs',f['run_id']);e=self.row('evidence',f['evidence_id'])
 454:         # A no-byte failure records our own attempt metadata, not derivative vendor content.
 455:         rights_sources=set() if e['attempt_id'] and f['state']=='UNKNOWN' else {f['source_id']}|{self.row('artifacts',aid)['source_id'] for aid in self.roots(f['fact_id'])}
 456:         for source_id in rights_sources:
 457:             pol=self.reg('policies',self.reg('sources',source_id)['policy_id'])
 458:             require(self.policy_allows(pol['policy_id'],'DERIVE',f['recorded_at'],tenant=f['tenant_id']),'DERIVATION_RIGHTS_DENIED')
 459:             require(instant(f['expires_at'])<=instant(f['recorded_at'])+timedelta(seconds=pol['max_derived_retention_seconds']),'DERIVED_RETENTION_EXCEEDED')
 460:         require(f['tenant_id']==scope['tenant_id']==sub['tenant_id']==run['tenant_id']==e['tenant_id'],'FACT_TENANT')
 461:         require(scope['subject_id']==f['subject_id'] and sub['kind'] in p['subject_kinds'],'FACT_SUBJECT_SCOPE')
 462:         require(f['predicate_id'] in s['emits'],'SOURCE_CANNOT_EMIT');require(f['nature'] in p['allowed_natures'] and f['nature'] in s['allowed_natures'],'UNSUPPORTED_EPISTEMIC_KIND')
 463:         self.shape(f['target'],p['target_schema'])
 464:         require(instant(f['observed_at'])<=instant(f['recorded_at']) and instant(f['observed_at'])<=instant(run['as_of']),'FACT_TIME')
 465:         require(f['execution_id']==e['execution_id'],'FACT_EXECUTION_EVIDENCE_MISMATCH')
 466:         if e['attempt_id']:
 467:             a=self.row('attempts',e['attempt_id']);self.validate_attempt(a)
 468:             require(f['state']=='UNKNOWN' and f['object'] is None and e['directness']=='DIAGNOSTIC','ATTEMPT_CANNOT_PROVE_BUSINESS_FACT')
 469:             require(a['target']['subject_id']==f['subject_id'] and a['source_id']==f['source_id'] and a['scope_id']==f['scope_id'],'UNKNOWN_ATTEMPT_TARGET')
 470:             require(f['observed_at']==a['finished_at'] and instant(a['finished_at'])<=instant(f['recorded_at']),'UNKNOWN_BEFORE_FAILURE')
 471:             require(f['reason']=={'POLICY_DENIED':'POLICY_BLOCKED','TIMEOUT':'FETCH_FAILED','FAILED':'FETCH_FAILED','BUDGET_DENIED':'NOT_CHECKED','CANCELLED':'NOT_CHECKED','PARTIAL':'INSUFFICIENT_EVIDENCE'}.get(a['status']),'UNKNOWN_FAILURE_REASON')
 472:         if f['execution_id']:
 473:             ex=self.row('executions',f['execution_id']);fn=self.reg('functions',ex['function_id'])
 474:             require(ex['status']=='COMPLETE' and instant(ex['finished_at'])<=instant(f['recorded_at']),'FAILED_OR_UNFINISHED_PRODUCER')
 475:             if ex['model_call_id']:require(self.row('model-calls',ex['model_call_id'])['status']=='PARSED','FAILED_MODEL_PRODUCER')
 476:             require(f['fact_id'] in ex['output_fact_ids'],'FACT_OUTPUT_BACKLINK');require(set(e['input_fact_ids'])==set(ex['input_fact_ids']),'PROVENANCE_INPUT_SET_MISMATCH')
 477:             processor=fn['processor']
 478:         else:processor='HUMAN_REVIEW' if s['acquisition_method']=='HUMAN_UPLOAD' else 'DETERMINISTIC'
 479:         require(processor in p['allowed_processors'],'UNSUPPORTED_PROCESSOR')
 480:         if f['nature'] in ['INFERENCE','DERIVED_MEASUREMENT']:require(f['execution_id'] is not None,'MISSING_DERIVATION')
 481:         if f['confidence'] and f['confidence']['meaning']=='CALIBRATED_PRECISION':
 482:             require(f['confidence']['calibration_id'] is not None,'UNCITED_CALIBRATION')
 483:             cal=self.row('calibrations',f['confidence']['calibration_id'])
 484:             require(f['confidence']['value']==cal['measured_precision'],'CALIBRATION_VALUE_MISMATCH')
 485:         if f['supersedes_fact_id']:
 486:             prior=self.row('facts',f['supersedes_fact_id'])
 487:             require(claim_key(prior)==claim_key(f) and prior['source_id']==f['source_id'],'WRONG_SUPERSESSION_KEY')
 488:             require(instant(prior['recorded_at'])<instant(f['recorded_at']),'INVALID_SUPERSESSION_ORDER')
 489:             require(f['state']!='UNKNOWN' or prior['state']=='UNKNOWN','UNKNOWN_CANNOT_SUPERSEDE_KNOWN')
 490:         if f['state']=='OBSERVED':self.shape(f['object'],p['value_schema'])
 491:         require((p['temporal_mode']=='PERIOD')==(f['window'] is not None),'MISSING_OR_UNEXPECTED_PERIOD')
 492:         if f['window']:require(instant(f['window']['start'])<instant(f['window']['end'])<=instant(run['as_of']),'INVALID_MEASUREMENT_WINDOW')
 493:         if f['state']!='UNKNOWN' and e['directness']=='RAW':
```
