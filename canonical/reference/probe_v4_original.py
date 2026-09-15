"""Independent boundary counterexamples against an unchanged v4 archive.
Run: python probe_v4.py /path/to/unpacked/keensight-architecture-v4
This is a diagnostic harness, not an implementation of the proposed fixes.
"""
from pathlib import Path
from copy import deepcopy
import json,sys
ROOT=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(ROOT))
from keensight_contracts.validation import Bundle
from keensight_contracts.engine import digest, ContractError, resolve_claim, evaluate_requirements, pointer

def rowadd(b,kind,row,key):
    b.rows[kind].append(row); b.index[kind][row[key]]=row

def unset_run_input(b):b.row('runs','run.demo')['input_fact_ids'].remove('f.tech')
def unknown_without_artifact(b):
    f=b.row('facts','f.tech');f.update(state='UNKNOWN',object=None,reason='POLICY_BLOCKED',binding_id=None)
    b.row('evidence',f['evidence_id']).update(locator_ids=[],input_fact_ids=[])
def model_failed(b):b.row('model-calls','call.fixture').update(status='FAILED',terminal_reason='provider_failure')
def wrong_execution_inputs(b):
    x=b.row('executions','ex.job_llm');x['input_artifact_ids']=['art.home'];x['input_set_hash']=digest({'facts':sorted(x['input_fact_ids']),'artifacts':sorted(x['input_artifact_ids'])})
def remove_denominator_evidence(b):b.row('artifacts','art.product3').update(retention_state='DELETED',content_ref=None)
def add_change(b,tenant,kind,target,replacement=None):
    rowadd(b,'changes',{'change_id':'change.probe','tenant_id':tenant,'kind':kind,'target_id':target,'effective_at':'2026-09-14T19:00:00Z','reason':'audit only','replacement_id':replacement},'change_id')
def add_exposure(b):
    rowadd(b,'exposures',{'exposure_id':'exp.probe','tenant_id':'tenant.demo','package_id':'package.product','business_send_key':'key.probe','provider_message_id':'message.probe','recipient_key':'recipient.probe','accepted_at':'2026-09-14T20:01:00Z','status':'PROVIDER_ACCEPTED'},'exposure_id')
def add_outcome(b):
    rowadd(b,'outcomes',{'event_id':'event.probe','tenant_id':'tenant.demo','provider':'synthetic','provider_event_id':'provider-event.probe','exposure_id':None,'occurred_at':'2026-09-14T20:00:00Z','received_at':'2026-09-14T20:01:00Z','kind':'REPLY','attribution_status':'QUARANTINED','evidence_id':'missing.evidence'},'event_id')
def add_conflict(b):
    f=deepcopy(b.row('facts','f.tech'));f.update(fact_id='f.tech.negative',state='NOT_FOUND',object=None,reason='NOT_DETECTED_IN_SCOPE',evidence_id='ev.tech.negative')
    rowadd(b,'facts',f,'fact_id')
    ev=deepcopy(b.row('evidence','ev.f.tech'));ev.update(evidence_id=f['evidence_id'],coverage_id='coverage.tech')
    rowadd(b,'evidence',ev,'evidence_id')
    c=deepcopy(b.row('coverage','coverage.form'));c.update(coverage_id='coverage.tech',predicate_ids=['technology.footprint'],target={'product_id':'product.calendly'})
    rowadd(b,'coverage',c,'coverage_id')
    b.row('runs','run.demo')['input_fact_ids'].append(f['fact_id'])
    # The conflict is deliberately made visible on the signal, not hidden from its input set.
    b.row('signals','signal.tech')['input_fact_ids'].append(f['fact_id'])
def nonexistent_entrypoint(b): b.reg('functions','signal.required_facts_v1')['entrypoint']='nonexistent.module:not_a_function'
def duplicate_support(b):
    d=deepcopy(b.row('facts','f.tech'));d['fact_id']='f.tech.duplicate'
    rowadd(b,'facts',d,'fact_id');b.row('runs','run.demo')['input_fact_ids'].append(d['fact_id'])
    b.row('signals','signal.tech')['input_fact_ids'].append(d['fact_id'])
    b.reg('signals','TECHNOLOGY_FOOTPRINT')['required_facts'][0]['minimum']=2

CASES=[
 ('failed_run_approved_preview','invalid_allowed',lambda b:b.row('runs','run.demo').update(status='FAILED'),'run.demo status FAILED, approved packages unchanged'),
 ('failed_execution_publishes_observed_fact','invalid_allowed',lambda b:b.row('executions','ex.job_llm').update(status='FAILED'),'ex.job_llm FAILED; f.job_statement remains OBSERVED and approved'),
 ('failed_model_publishes_observed_fact','invalid_allowed',model_failed,'call.fixture FAILED with terminal reason; approved job package unchanged'),
 ('fact_recorded_before_execution_finished','invalid_allowed',lambda b:b.row('executions','ex.job_llm').update(finished_at='2026-09-14T22:00:00Z'),'execution finishes after output recording and package approval'),
 ('signal_input_not_pinned','invalid_allowed',unset_run_input,'remove f.tech from run input facts; signal still consumes it'),
 ('bindings_not_pinned','invalid_allowed',lambda b:b.row('runs','run.demo').update(binding_ids=[]),'remove all pinned bindings; retained facts and packages still consume them'),
 ('execution_and_fact_raw_inputs_disagree','invalid_allowed',wrong_execution_inputs,'ex.job_llm pins homepage instead of job artifact; input hash recomputed'),
 ('model_and_execution_inputs_disagree','invalid_allowed',lambda b:b.row('model-calls','call.fixture').update(input_artifact_ids=['art.home']),'model call pins homepage, execution pins job'),
 ('unimplemented_entrypoint_accepted','invalid_allowed',nonexistent_entrypoint,'enabled function points to nonexistent callable; registry pin recomputed'),
 ('disabled_signals_and_templates_consumed','invalid_allowed',lambda b:b.reg('profiles','profile.broad_research').update(signal_ids=[],template_ids=[]),'profile enables no signals/templates but examples remain approved'),
 ('abstained_context_used','invalid_allowed',lambda b:b.row('contexts','context.product').update(status='ABSTAINED'),'signal and package still reference context.product'),
 ('conflict_does_not_block_signal_or_copy','invalid_allowed',add_conflict,'positive and explicit covered NOT_FOUND observations coexist on same claim and signal'),
 ('duplicate_origin_counts_twice','ambiguous_minimum_semantics',duplicate_support,'same artifact/evidence under two fact IDs satisfies minimum=2'),
 ('negated_positive_theme_counts_as_pain','invalid_allowed',lambda b:b.row('facts','f.classify.product1')['object'].update(stance='NEGATED',sentiment='POSITIVE'),'supporting classification becomes positive/negated, support_count remains 2'),
 ('denominator_deleted_prior_still_eligible','invalid_allowed',remove_denominator_evidence,'delete eligible denominator-only product3 artifact; prior still used'),
 ('coverage_predates_capture','invalid_allowed',lambda b:b.row('coverage','coverage.form').update(checked_at='2026-09-13T00:00:00Z'),'coverage checked before raw capture'),
 ('unknown_detector_release_for_absence','invalid_allowed',lambda b:b.row('coverage','coverage.form').update(detector_release='sha256:'+'0'*64),'unresolved detector release hash'),
 ('foreign_tenant_change_targets_fact','invalid_allowed',lambda b:add_change(b,'tenant.other','RETRACTION','f.vendor1'),'other-tenant change retracts tenant.demo f.vendor1'),
 ('dangling_change_replacement','invalid_allowed',lambda b:add_change(b,'tenant.demo','RETRACTION','f.vendor1','missing.replacement'),'replacement_id nonexistent'),
 ('exposure_from_design_preview','reserved_future_contract',add_exposure,'provider accepted exposure references send_allowed=false design-test package'),
 ('outcome_missing_evidence','reserved_future_contract',add_outcome,'outcome cites missing EvidenceSet'),
 ('unknown_without_captured_artifact','legitimate_path_blocked',unknown_without_artifact,'policy blocked before any bytes captured; no evidence fabricated'),
 ('negative_array_pointer','helper_conformance',lambda b:None,'JSON pointer /-1 should not address last array element'),
 ('late_record_visible_historically','helper_temporal_semantics',lambda b:b.row('facts','f.tech').update(recorded_at='2026-09-15T00:00:00Z'),'usable(f.tech, 2026-09-14T20:00Z) with next-day record'),
 ('invalid_timestamp_control','rejection_control',lambda b:b.row('facts','f.tech').update(recorded_at='2026-99-99T00:00:00Z'),'malformed timestamp'),
 ('cross_account_copy_control','rejection_control',lambda b:b.row('packages','package.product')['clauses'][0].update(fact_ids=['f.product1']),'product review cited as account footprint'),
 ('incomplete_coverage_control','rejection_control',lambda b:b.row('coverage','coverage.form').update(status='INCOMPLETE'),'NOT_FOUND uses incomplete coverage'),
 ('expired_copy_control','rejection_control',lambda b:b.row('facts','f.tech').update(expires_at='2026-09-14T19:00:00Z'),'source expired before approval'),
]
results=[]
for name,category,mut,detail in CASES:
    b=Bundle(ROOT,check_hashes=False)
    try:
        mut(b)
        for run in b.rows['runs']:run['registry_release']=digest(b.registry)
        extra={}
        boundary='Bundle.validate'
        if name=='negative_array_pointer':
            boundary='engine.pointer';extra['value']=pointer(['first','last'],'/-1')
        elif name=='late_record_visible_historically':
            boundary='Bundle.usable';extra['usable']=b.usable('f.tech','2026-09-14T20:00:00Z')
        else:
            b.validate()
            if name=='conflict_does_not_block_signal_or_copy':
                fs=[b.row('facts',i) for i in ['f.tech','f.tech.negative']]
                extra['resolution']=resolve_claim(fs,'2026-09-14T20:00:00Z',lambda f,t:b.usable(f['fact_id'],t,allow_absence=True))
                extra['rendered']=b.render(b.row('packages','package.product'))
            if name=='denominator_deleted_prior_still_eligible':extra['usable']=b.usable('f.prior.product','2026-09-14T20:00:00Z')
            if name=='foreign_tenant_change_targets_fact':extra['usable']=b.usable('f.vendor1','2026-09-14T20:00:00Z')
        r={'case':name,'category':category,'boundary':boundary,'result':'ACCEPTED','detail':detail,**extra}
    except Exception as e:
        r={'case':name,'category':category,'result':'REJECTED','error':type(e).__name__+':'+str(e),'detail':detail}
    results.append(r)
    print(name+': '+r['result']+(' '+r.get('error','')))
    if r['result']=='ACCEPTED' and extra:print('  ',extra)
out=Path(__file__).parent/'counterexamples.json';out.write_text(json.dumps(results,indent=2)+'\n')
print('RESULT_FILE',out)
