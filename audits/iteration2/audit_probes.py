"""Read-only audit against the unpacked September 15 repaired bundle.

Each probe records a missing safety property, not a live exploitation claim.
Run with --output PATH. Set KEENSIGHT_BASELINE to override ./baseline.
No network or remote mutations.
"""
from __future__ import annotations
import argparse, copy, dataclasses, hashlib, importlib.util, json, os, pathlib, subprocess, sys, tempfile, traceback
ROOT = pathlib.Path(__file__).resolve().parent
BASE = pathlib.Path(os.environ.get('KEENSIGHT_BASELINE', str(ROOT.parents[1]))).resolve()
sys.path[:0] = [str(BASE/'collector/src'), str(BASE/'canonical')]
from keensight_scrapling.storage import Store
from keensight_scrapling.pipeline import Scanner, ScanConfig
from keensight_scrapling.rules import RulePack, match_pages
from keensight_scrapling.transport import FixtureTransport, FetchResult
from keensight_scrapling.extraction import extract
from keensight_scrapling.core import canonical, Capture, Match, Observation, SupportLink, ContractError
from keensight_scrapling.claims import observation_candidates
from keensight_scrapling.validation import validate_bundle
from keensight_scrapling.cli import demo
AT='2026-09-14T12:00:00Z'; URL='https://example.test/'
HTML=b'<html><script src="https://assets.calendly.com/w.js"></script><p>Content</p></html>'
PROBES={}
def probe(id):
 def register(fn): PROBES[id]=fn;return fn
 return register

def pack():return RulePack.load(BASE/'collector/examples/demo-rules.json')
def runner(s,p=None,t=None):return Scanner(s,p or pack(),t or FixtureTransport({}),production=False,clock=lambda:AT)
def page(s,body=HTML,run='r',subject='account:a',url=URL,mode='RAW_HTML'):
 s.begin_run('t',run,{'test':'audit','run':run})
 c=s.put_capture(tenant_id='t',subject_id=subject,run_id=run,url=url,observed_at=AT,body=body,headers={'content-type':'text/html'},mode=mode)
 return extract(c,body)
def result(b,**details):return {'violation_present':bool(b),**details}

@probe('R2-C01')
def failed_attempt_loses_request_manifest(tmp):
 with_store=Store(tmp/'store')
 try:
  b=runner(with_store,t=FixtureTransport({URL+'robots.txt':TimeoutError('fixture')})).scan(URL,ScanConfig('t','a','failed'))
  a=dict(with_store.db.execute('SELECT * FROM attempts').fetchone());payload=json.loads(a['payload'])
  return result('started_at' not in payload or 'command_id' not in payload, terminal_payload=payload,bundle_top_keys=sorted(b), persisted_evaluations=with_store.db.execute('SELECT COUNT(*) FROM evaluations').fetchone()[0])
 finally:with_store.close()

@probe('CTRL-REPLAY')
def fresh_rule_replay_cannot_extend_existing_matches(tmp):
 s=Store(tmp/'store')
 try:
  pg=page(s);b=runner(s).evaluate([pg],'original',AT)
  raw=copy.deepcopy(pack().raw);raw['release_id']='new-compatible-release';raw['negative_terms']=['irrelevant-extra-term']
  new=RulePack.compile(raw)
  try:newb=runner(s,p=new).replay('t','r','new-replay',AT);error=None
  except Exception as e:error=f'{type(e).__name__}: {e}'
  return result(error is not None, replay_error=error, old_matches=len(b['matches']))
 finally:s.close()

@probe('R2-C04')
def revoked_evidence_remains_research_candidate(tmp):
 s=Store(tmp/'store')
 try:
  pg=page(s,b'<html><script src="https://unknown-vendor.test/x.js"></script></html>')
  runner(s).evaluate([pg],'e',AT)
  before=s.candidates('t',1);s.revoke('t',pg.capture.capture_id,'delete/restrict fixture')
  after=s.candidates('t',1)
  return result(bool(after) and after==before,candidates_before=before,candidates_after=after)
 finally:s.close()

@probe('R2-C05')
def parser_recovery_silently_drops_deep_evidence(tmp):
 s=Store(tmp/'store')
 try:
  body=b'<html><body>'+b'<div>'*400+HTML+b'</div>'*400+b'</body></html>'
  pg=page(s,body);b=runner(s).evaluate([pg],'e',AT)
  c=next(x for x in b['commands'] if x['command_id']=='EXTRACT_SCRIPT_SRC')
  reports=[r for r in b['rule_evaluations'] if 'script' in r['rule_id']]
  return result(c['status']=='COMPLETE' and not c['output_ids'] and any(r['status']=='NO_MATCH' for r in reports), original_contains_marker=b'assets.calendly.com' in body, extraction=c,reports=reports)
 finally:s.close()

@probe('R2-C06')
def validated_manifest_can_diverge_from_committed_findings(tmp):
 # Test original surviving low-level publication parameter divergence.
 s=Store(tmp/'store')
 try:
  pg=page(s)
  b=runner(s).evaluate([pg],'empty-target',AT)
  matches=[Match(**x) for x in b['matches']];obs=[Observation(**x) for x in b['observations']];links=[SupportLink(**x) for x in b['support_links']]
  # Use a fresh store retaining the same capture, so no previously committed findings.
  second=Store(tmp/'second')
  try:
   page(second)
   # Validator authenticates b, but publication receives zero finding arrays.
   second.publish_evaluation(b,[pg],[],[],[])
   count=second.db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]
   saved=json.loads(second.db.execute('SELECT payload FROM evaluations').fetchone()[0])
   return result(count==0 and len(saved['observations'])>0,manifest_observations=len(saved['observations']),published_observations=count,boundary='Store.publish_evaluation public local-owner API')
  finally:second.close()
 finally:s.close()

@probe('R2-C07')
def input_subject_can_change_inside_analyze_file_run(tmp):
 html=tmp/'page.html';html.write_bytes(HTML);db=tmp/'store'
 env={**os.environ,'PYTHONPATH':str(BASE/'collector/src')}
 commands=[]
 for subject in ['account:a','account:b']:
  args=[sys.executable,'-m','keensight_scrapling.cli','analyze-file','--html',str(html),'--url',URL,'--observed-at',AT,'--tenant','t','--subject',subject,'--run','shared','--rules',str(BASE/'collector/examples/demo-rules.json'),'--store',str(db),'--output',str(tmp/(subject[-1]+'.json'))]
  p=subprocess.run(args,capture_output=True,text=True,env=env);commands.append({'subject':subject,'returncode':p.returncode,'stderr':p.stderr})
 s=Store(db)
 try:
  try:runner(s).replay('t','shared','replay',AT);err=None
  except Exception as e:err=str(e)
  return result(all(x['returncode']==0 for x in commands) and err is not None,commands=commands,replay_error=err,subjects=sorted({c.subject_id for c in s.captures('t','shared')}))
 finally:s.close()

@probe('R2-C08')
def canonical_reference_and_collector_disagree_on_aside(tmp):
 s=Store(tmp/'store')
 try:
  from keensight_contracts.engine import fingerprint_hosts
  from keensight_contracts.validation import Bundle
  b=Bundle(BASE/'canonical',check_hashes=False)
  html='<html><aside><script src="https://assets.calendly.com/w.js"></script></aside></html>'
  pg=page(s,html.encode());out=runner(s).evaluate([pg],'e',AT)
  known=any(v['status']=='SUPPORTED' and v['predicate']=='vendor.present' for v in out['claims'])
  hs=fingerprint_hosts(b.registry['fingerprints'][0],html)
  return result(known and not hs,collector_supported=known,canonical_hosts=sorted(hs))
 finally:s.close()

@probe('R2-C09')
def result_completeness_overreports_failed_acquisition(tmp):
 s=Store(tmp/'store')
 try:
  b=runner(s,t=FixtureTransport({URL+'robots.txt':TimeoutError('fixture')})).scan(URL,ScanConfig('t','a','no-bytes'))
  fields={'tenant_id','subject_id','request_id','run_id'}
  return result(not fields.intersection(b) and not b['captures'] and s.db.execute('SELECT COUNT(*) FROM evaluations').fetchone()[0]==0, identity_fields_present=sorted(fields.intersection(b)),evaluation_id=b['evaluation_id'],capture_count=len(b['captures']),evaluation_records=s.db.execute('SELECT COUNT(*) FROM evaluations').fetchone()[0])
 finally:s.close()

@probe('R2-C10')
def command_contradictory_duplicate_is_accepted(tmp):
 s=Store(tmp/'store')
 try:
  b=runner(s).evaluate([page(s)],'e',AT)
  c=copy.deepcopy(next(c for c in b['commands'] if c['command_id']=='MATCH_HOST_SUFFIX'))
  c['status']='FAILED';c['output_ids']=[];c['limitations']=['INJECTED_FAILURE'];b['commands'].append(c)
  try:validate_bundle(b);err=None
  except Exception as e:err=str(e)
  return result(err is None,error=err,command_outcomes=[c['status'] for c in b['commands'] if c['command_id']=='MATCH_HOST_SUFFIX'])
 finally:s.close()

@probe('CTRL-CAPTURE')
def changed_metadata_rejected(tmp):
 s=Store(tmp/'store')
 try:
  pg=page(s)
  try:s.body(dataclasses.replace(pg.capture,headers={'x-powered-by':'forged'}));blocked=False
  except ContractError:blocked=True
  return result(not blocked,control_passed=blocked)
 finally:s.close()

@probe('CTRL-PUBLICATION')
def duplicate_input_rejected_without_writes(tmp):
 s=Store(tmp/'store')
 try:
  pg=page(s)
  try:runner(s).evaluate([pg,pg],'e',AT);blocked=False
  except ContractError:blocked=True
  count=s.db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]
  return result(not(blocked and count==0),control_passed=blocked and count==0,observations=count)
 finally:s.close()

# Canonical and protocol probes follow below.

def canonical_bundle():
 from keensight_contracts.validation import Bundle
 return Bundle(BASE/'canonical',check_hashes=False)

def addrow(b,family,obj):
 key={'artifacts':'artifact_id','locators':'locator_id','facts':'fact_id','executions':'execution_id','changes':'change_id','repairs':'attempt_id'}[family]
 b.rows[family].append(obj);b.index[family][obj[key]]=obj

def full(b):
 try:return {'passed':True,'value':b.validate()}
 except Exception as e:return {'passed':False,'error':f'{type(e).__name__}: {e}'}

def refresh(b,drop_exports=True):
 from keensight_contracts.engine import digest
 for r in b.rows['runs']:r['registry_release']=digest(b.registry)
 for g in b.rows['gates']:g['version_vector']=b.current_version_vector(g['package']['package_id'])
 if drop_exports:b.rows['exports'].clear();b.index['exports'].clear()

@probe('R2-A01')
def binding_evidence_not_in_fact_lineage(tmp):
 b=canonical_bundle()
 art=copy.deepcopy(b.row('artifacts','art.home'))
 art.update(artifact_id='art.binding-only',retention_state='DELETED',content_ref=None)
 addrow(b,'artifacts',art)
 loc=copy.deepcopy(b.row('locators','loc.art.home'));loc.update(locator_id='loc.binding-only',artifact_id=art['artifact_id'])
 addrow(b,'locators',loc)
 bind=b.row('bindings','bind.art.home');bind['artifact_ids']=[art['artifact_id']];bind['evidence_locator_ids']=[loc['locator_id']]
 refresh(b)
 usable=b.current_claim_eligible('f.tech','2026-09-14T20:00:10Z',purpose='EXPORT')
 check=full(b)
 return result(usable and check['passed'], binding_uses_deleted_artifact=True,binding_artifact_in_fact_roots=art['artifact_id'] in b.roots('f.tech'),current_eligible=usable,full_validation=check)

@probe('R2-A02')
def template_demotion_does_not_block_export_gate(tmp):
 from keensight_contracts.handoff import LocalPreviewExporter
 b=canonical_bundle();pkg=b.row('packages','package.product');t=b.reg('templates',pkg['template_id']);t['authority']='CANDIDATE';refresh(b)
 g=b.rows['gates'][0]
 try:
  r=LocalPreviewExporter(b,tmp/'export').export(g['gate_id'],principal_id='actor.fixture',at=g['evaluated_at'],idempotency_key='demoted-template')
  exported=True;error=None
 except Exception as e:exported=False;error=str(e)
 return result(exported,template_authority=t['authority'],exported=exported,error=error,full_validation=full(b),boundary='Current-use gate and local exporter, not full bundle admission')

@probe('R2-A03')
def produced_artifact_rejected_by_second_layer(tmp):
 from keensight_contracts.engine import digest
 b=canonical_bundle();art=b.row('artifacts','art.response');art['captured_at']='2026-09-14T17:00:30Z'
 for a in b.rows['attempts']:
  if 'art.response' in a['artifact_ids']:a['finished_at']='2026-09-14T17:00:31Z'
 run=b.row('runs','run.ingest');run['input_artifact_ids'].remove('art.response');run['produced_artifact_ids'].append('art.response')
 producer=b.row('executions','ex.job_llm');producer['output_artifact_ids'].append('art.response')
 # A declared successful later no-output operation consumes the already completed model response.
 ex=copy.deepcopy(b.row('executions','ex.classify.product1'))
 ex.update(execution_id='ex.consume.response',subject_id='org.acme',input_artifact_ids=['art.response'],input_fact_ids=[],input_sample_ids=[],output_fact_ids=[],output_artifact_ids=[],started_at='2026-09-14T17:01:01Z',finished_at='2026-09-14T17:01:05Z')
 ex['input_set_hash']=digest({'facts':[],'artifacts':['art.response']});ex['sample_set_hash']=digest([])
 addrow(b,'executions',ex);refresh(b)
 try:b.validate_completion();first=True;first_err=None
 except Exception as e:first=False;first_err=str(e)
 f=full(b)
 return result(first and not f['passed'] and 'ARTIFACT_OUTSIDE_RUN' in f.get('error',''),completion_layer_passed=first,completion_error=first_err,full_validation=f)

@probe('R2-A04')
def supersession_cycle_raises_uncontrolled_recursion(tmp):
 b=canonical_bundle();b.row('facts','f.tech')['supersedes_fact_id']='f.tech'
 check=full(b)
 return result('RecursionError' in check.get('error',''),full_validation=check)

@probe('R2-A05')
def effective_date_has_no_current_use_effect(tmp):
 b=canonical_bundle();b.row('facts','f.tech')['effective_at']='2026-10-14T12:00:00Z';refresh(b)
 eligible=b.current_claim_eligible('f.tech','2026-09-14T20:00:10Z',purpose='EXPORT')
 check=full(b)
 return result(eligible and check['passed'],effective_at=b.row('facts','f.tech')['effective_at'],gate_time='2026-09-14T20:00:10Z',current_eligible=eligible,full_validation=check,classification='Temporal semantics gap: declared effective time is ignored')

@probe('R2-A06')
def historical_result_changes_under_later_supersession(tmp):
 from keensight_contracts.engine import resolve_claim
 b=canonical_bundle();f=copy.deepcopy(b.row('facts','f.tech'))
 f.update(fact_id='f.later',recorded_at='2026-09-14T19:30:00Z',supersedes_fact_id='f.tech');f['object']['version']='later-version'
 addrow(b,'facts',f)
 run=b.row('runs','run.demo')
 # New observation was recorded after the old sealed input cutoff but before as_of.
 available=[b.row('facts',i) for i in b.available_facts(run) if i=='f.tech']
 r=resolve_claim(available,run['as_of'],lambda x,t:b.usable(x['fact_id'],t))
 return result(r['status']=='UNKNOWN',old_fact_pinned='f.tech' in b.available_facts(run),replacement_pinned='f.later' in b.available_facts(run),replacement_recorded_at=f['recorded_at'],old_cutoff=run['knowledge_cutoff'],historical_resolution=r)

@probe('CTRL-BINDING')
def successor_can_inherit_retracted_ancestor(tmp):
 # Verify whether binding status change itself remains enforced (a negative control).
 b=canonical_bundle();b.row('bindings','bind.art.home')['status']='UNRESOLVED'
 eligible=b.current_claim_eligible('f.tech','2026-09-14T20:00:10Z')
 return result(eligible,control_passed=not eligible)

@probe('R2-A08')
def conflicting_minimum_semantics(tmp):
 from keensight_contracts.engine import evaluate_requirements
 b=canonical_bundle();s=next(x for x in b.rows['signals'] if x['input_fact_ids']==['f.job_statement'])
 d=b.reg('signals',s['signal_type_id']);d['required_facts'][0]['minimum']=2
 duplicate=copy.deepcopy(b.row('facts','f.job_statement'));duplicate['fact_id']='f.job.copy'
 old=b.row('facts','f.job_statement')
 verdict=evaluate_requirements(d,[old,duplicate],'org.acme','2026-09-14T20:00:00Z',lambda *a,**k:True)
 origins=b.corroborating_artifacts(old['fact_id'])
 return result(verdict=='RESOLVED' and len(origins)==1,helper_verdict=verdict,distinct_substantive_origins=len(origins),full_validator_rule='Counts distinct substantive artifact origins, not fact rows')

@probe('CTRL-AUTH')
def foreign_change_rejected(tmp):
 b=canonical_bundle()
 c=dict(change_id='foreign',tenant_id='tenant.foreign',kind='RETRACTION',target_id='f.tech',target_type='facts',replacement_id=None,effective_at='2026-09-14T19:00:00Z',recorded_at='2026-09-14T19:00:00Z',actor_id='actor.fixture',reason='control')
 try:b.validate_change(c);blocked=False
 except Exception:blocked=True
 b.rows['changes'].append(c)
 eligible=b.usable('f.tech','2026-09-14T20:00:00Z')
 return result(not(blocked and eligible),control_passed=blocked and eligible)

def protocol():
 spec=importlib.util.spec_from_file_location('review_protocol',BASE/'protocol/validate_protocol.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 return m,json.loads((BASE/'protocol/examples/request.json').read_text()),json.loads((BASE/'protocol/examples/result.json').read_text())

@probe('R2-P01')
def late_timeout_result_is_rejected(tmp):
 p,req,res=protocol();res['execution_status']='FAILED';res['output_refs']=[];res['finished_at']='2026-09-14T12:02:01Z'
 res['usage']['duration_ms']=60000
 res['diagnostics']=[{'diagnostic_id':'timeout','code':'NETWORK.TIMEOUT','severity':'ERROR','message':'fixture operation timed out','record_refs':[],'field_path':None,'cause_execution_id':None,'suggested_action':'RETRY_AFTER_POLICY','restricted_details_ref':None}]
 # A real timeout finalizes after deadline; no positive outputs published.
 try:p.validate_pair(req,res);error=None
 except Exception as e:error=str(e)
 return result(error is not None and 'beyond deadline' in error,checker_error=error,result_status=res['execution_status'],finished_at=res['finished_at'],deadline_at=req['deadline_at'])

@probe('R2-P02')
def mode_and_usage_not_constrained_by_operation(tmp):
 p,req,res=protocol();req['context']['mode']='CAPTURE';res['context']['mode']='CAPTURE'
 # Existing match parameters forbid network; request/result report network use.
 res['usage']['network_attempts']=5
 res['request_digest']=p.digest(req)
 records=json.loads((BASE/'protocol/examples/fixture_records.json').read_text())
 try:p.validate_payload_pair(req,res,lambda ref:records[ref['record_id']]);error=None
 except Exception as e:error=str(e)
 return result(error is None,checker_error=error,mode=req['context']['mode'],reported_network_attempts=res['usage']['network_attempts'])

@probe('CTRL-PROTOCOL')
def unpinned_record_is_rejected(tmp):
 p,req,res=protocol();ref=copy.deepcopy(res['consumed_refs'][0]);ref['record_id']='not-declared';res['consumed_refs'].append(ref)
 try:p.validate_pair(req,res);blocked=False
 except Exception:blocked=True
 return result(not blocked,control_passed=blocked)

def run_selected(output,selected=None):
 records=[]
 for id,fn in PROBES.items():
  if selected and id not in selected:continue
  with tempfile.TemporaryDirectory(prefix='ks-r2-') as td:
   try:record={'id':id,'probe':fn.__name__,**fn(pathlib.Path(td))}
   except Exception as exc:record={'id':id,'probe':fn.__name__,'probe_error':f'{type(exc).__name__}: {exc}','traceback':traceback.format_exc()}
  records.append(record);print(id,record.get('violation_present',record.get('probe_error')),flush=True)
 pathlib.Path(output).write_text(json.dumps({'baseline':str(BASE),'probes':records},indent=2))
 return records


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--select',nargs='*');a=p.parse_args();run_selected(a.output,a.select)
