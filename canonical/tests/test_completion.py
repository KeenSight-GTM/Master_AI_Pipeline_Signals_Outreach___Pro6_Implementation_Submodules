"""Selected audit fixes A–E, G, H: real guards, not release-hash rejection.

Tests intentionally repin modified registry bytes and remove unrelated handoff
records when probing core semantics. The original v4 probe file is retained too.
"""
from copy import deepcopy
from pathlib import Path
import pytest
from keensight_contracts.engine import ContractError,digest,resolve_claim,claim_key
from keensight_contracts.validation import Bundle
from keensight_contracts.completion import package_hash,export_payload
from keensight_contracts.handoff import LocalPreviewExporter

ROOT=Path(__file__).resolve().parents[1]
AT='2026-09-14T20:00:00Z'

@pytest.fixture
def b():return Bundle(ROOT,check_hashes=False)

def add(b,kind,item,key):
    b.rows[kind].append(item);b.index[kind][item[key]]=item

def rebase(b):
    """Do not let registry hashes or a stale example export mask a semantic test."""
    for run in b.rows['runs']:run['registry_release']=digest(b.registry)
    b.rows['gates'].clear();b.index['gates'].clear()
    b.rows['exports'].clear();b.index['exports'].clear()

def restamp_gate(b):
    for run in b.rows['runs']:run['registry_release']=digest(b.registry)
    for g in b.rows['gates']:g['version_vector']=b.current_version_vector(g['package']['package_id'])

A_CASES=[
 ('failed_run',lambda b:b.row('runs','run.demo').update(status='FAILED'),'FAILED_RUN_HAS_COMPLETE_TARGET'),
 ('failed_producer',lambda b:b.row('executions','ex.job_llm').update(status='FAILED'),'TARGET_WITH_UNFINISHED_EXECUTION'),
 ('abstained_producer',lambda b:b.row('executions','ex.job_llm').update(status='ABSTAINED'),'TARGET_WITH_UNFINISHED_EXECUTION'),
 ('failed_model',lambda b:b.row('model-calls','call.fixture').update(status='FAILED',terminal_reason='provider_error'),'RESOLUTION_POLICY_MISMATCH|FAILED_MODEL_PRODUCER'),
 ('abstained_model',lambda b:b.row('model-calls','call.fixture').update(status='ABSTAINED',terminal_reason='invalid_output'),'RESOLUTION_POLICY_MISMATCH|FAILED_MODEL_PRODUCER'),
 ('producer_finishes_after_output',lambda b:b.row('executions','ex.job_llm').update(finished_at='2026-09-14T17:01:05Z'),'OUTPUT_BEFORE_SUCCESS|RESOLUTION_POLICY_MISMATCH'),
 ('failed_account',lambda b:b.row('runs','run.demo')['target_results'][0].update(status='FAILED',reason='failure'),'COMPLETE_RUN_WITH_FAILED_TARGET'),
]
@pytest.mark.parametrize('name,mut,code',A_CASES,ids=[x[0] for x in A_CASES])
def test_A_completion_rejects(b,name,mut,code):
    rebase(b);mut(b)
    with pytest.raises(ContractError,match=code):b.validate()

@pytest.mark.parametrize('status',['FAILED','ABSTAINED'])
def test_A_failed_producer_not_currently_usable(b,status):
    b.row('executions','ex.job_llm')['status']=status
    assert not b.usable('f.job_statement',AT)
    with pytest.raises(ContractError):b.render(b.row('packages','package.job'))

def test_A_partial_batch_preserves_completed_account(b):
    rebase(b);run=b.row('runs','run.demo');run['status']='PARTIAL'
    next(x for x in run['target_results'] if x['subject_id']=='org.other').update(status='FAILED',reason='policy_denied')
    assert b.validate()['status']=='PASS'
    assert b.render(b.row('packages','package.product')).startswith('I noticed')

def test_A_failed_model_without_response_and_without_output_is_valid(b):
    rebase(b);call=deepcopy(b.row('model-calls','call.fixture'))
    call.update(call_id='call.failure',response_artifact_id=None,status='FAILED',terminal_reason='TIMEOUT')
    add(b,'model-calls',call,'call_id')
    assert b.validate()['status']=='PASS'

def test_A_complete_model_without_response_rejected(b):
    rebase(b);b.row('model-calls','call.fixture')['response_artifact_id']=None
    with pytest.raises(ContractError):b.validate()

B_CASES=[
 ('missing_fact_pin',lambda b:b.row('runs','run.demo')['input_fact_ids'].remove('f.tech'),'UNPINNED_CONSUMED_FACT|INCOMPLETE_CLAIM_RESOLUTION'),
 ('missing_binding_pin',lambda b:b.row('runs','run.demo').update(binding_ids=[]),'UNPINNED_CONSUMED_BINDING'),
 ('missing_artifact_pin',lambda b:b.row('runs','run.demo')['input_artifact_ids'].remove('art.home'),'UNPINNED_ANCESTRAL_ARTIFACT'),
 ('missing_imported_producer',lambda b:b.row('runs','run.demo')['imported_execution_ids'].remove('ex.job_llm'),'UNPINNED_IMPORTED_EXECUTION'),
 ('missing_sample_pin',lambda b:b.row('runs','run.demo').update(sample_ids=[]),'UNPINNED_ANCESTRAL_SAMPLE'),
 ('missing_output_declaration',lambda b:b.row('runs','run.demo')['produced_fact_ids'].remove('f.prior.product'),'RUN_OUTPUT_CLOSURE'),
 ('future_input',lambda b:b.row('runs','run.demo').update(knowledge_cutoff='2026-09-14T16:00:00Z'),'INPUT_AFTER_KNOWLEDGE_CUTOFF'),
 ('different_model_inputs',lambda b:b.row('model-calls','call.fixture').update(input_artifact_ids=['art.home']),'MODEL_EXECUTION_INPUT_MISMATCH'),
 ('output_not_in_producer_list',lambda b:b.row('executions','ex.job_llm').update(output_fact_ids=[]),'RUN_OUTPUT_CLOSURE'),
 ('missing_resolution_pin',lambda b:b.row('runs','run.demo').update(resolution_ids=[]),'MISSING_CLAIM_RESOLUTION'),
 ('sample_record_not_pinned',lambda b:b.row('runs','run.demo')['input_artifact_ids'].remove('art.product3'),'UNPINNED_ANCESTRAL_ARTIFACT'),
]
@pytest.mark.parametrize('name,mut,code',B_CASES,ids=[x[0] for x in B_CASES])
def test_B_dependency_closure(b,name,mut,code):
    rebase(b);mut(b)
    with pytest.raises(ContractError,match=code):b.validate()

def test_B_wrong_producer_raw_input_despite_recomputed_hash(b):
    rebase(b);ex=b.row('executions','ex.job_llm');ex['input_artifact_ids']=['art.home']
    ex['input_set_hash']=digest({'facts':[],'artifacts':['art.home']})
    b.row('model-calls','call.fixture')['input_artifact_ids']=['art.home']
    with pytest.raises(ContractError,match='OUTPUT_RAW_INPUT_MISMATCH'):b.validate()

def test_B_sample_bytes_not_just_sample_id_are_pinned(b):
    rebase(b);b.row('samples','sample.product')['limitations'].append('New selection after execution')
    with pytest.raises(ContractError,match='SAMPLE_INPUT_HASH'):b.validate()

def conflict(b,fid='f.tech'):
    original=b.row('facts',fid);f=deepcopy(original);f['fact_id']=fid+'.conflict'
    if fid=='f.tech':f['object']['version']='conflicting-reported-version'
    else:f['object']['text']='Another incompatible review text'
    add(b,'facts',f,'fact_id')
    for run in b.rows['runs']:
        if fid in run['input_fact_ids']:run['input_fact_ids'].append(f['fact_id'])
    return f

def test_C_conflict_blocks_render_even_when_signal_hides_the_conflict(b):
    conflict(b)
    assert b.row('signals','signal.tech')['input_fact_ids']==['f.tech']
    assert not b.decision_eligible('f.tech',AT,run_id='run.demo')
    with pytest.raises(ContractError,match='PACKAGE_SIGNAL_INPUT_INELIGIBLE|CLAIM_NOT_RESOLVED_FOR_COPY'):b.render(b.row('packages','package.product'))

def test_C_recorded_resolution_cannot_omit_conflict(b):
    rebase(b);conflict(b)
    with pytest.raises(ContractError,match='INCOMPLETE_CLAIM_RESOLUTION'):b.validate()

def test_C_derived_prior_cannot_launder_input_conflict(b):
    conflict(b,'f.product1')
    assert not b.decision_eligible('f.prior.product',AT,run_id='run.demo')
    with pytest.raises(ContractError):b.validate_context(b.row('contexts','context.product'))

def test_C_distinct_vendors_remain_eligible(b):
    assert b.decision_eligible('f.vendor1',AT,run_id='run.demo')
    assert b.decision_eligible('f.vendor2',AT,run_id='run.demo')

def test_C_unknown_does_not_override_usable_positive(b):
    f=deepcopy(b.row('facts','f.tech'));f.update(fact_id='unknown.sameclaim',state='UNKNOWN',object=None,reason='NOT_CHECKED')
    add(b,'facts',f,'fact_id');b.row('runs','run.demo')['input_fact_ids'].append(f['fact_id'])
    assert b.decision_eligible('f.tech',AT,run_id='run.demo')

@pytest.mark.parametrize('stance,sentiment', [('NEGATED','POSITIVE'),('ASKED','NEGATIVE'),('QUOTED','NEGATIVE'),('UNCERTAIN','NEGATIVE'),('EXPERIENCED','POSITIVE'),('EXPERIENCED','NEUTRAL')])
def test_D_nonpain_not_counted_as_pain(b,stance,sentiment):
    b.row('facts','f.classify.product1')['object'].update(stance=stance,sentiment=sentiment)
    with pytest.raises(ContractError,match='INVALID_PAIN_SUPPORT'):b.validate_prior(b.row('facts','f.prior.product'))

@pytest.mark.parametrize('field,value',[('retention_state','DELETED'),('retained_until','2026-09-14T19:00:00Z')])
def test_D_denominator_only_evidence_blocks_reuse(b,field,value):
    b.row('artifacts','art.product3')[field]=value
    assert 'art.product3' in b.roots('f.prior.product')
    assert not b.usable('f.prior.product',AT)
    with pytest.raises(ContractError):b.validate_context(b.row('contexts','context.product'))

def test_D_abstained_context_is_not_decision_input(b):
    rebase(b);b.row('contexts','context.product')['status']='ABSTAINED'
    with pytest.raises(ContractError,match='ABSTAINED_OR_FOREIGN_CONTEXT'):b.validate()

def test_D_unknown_denominator_is_not_negative_label(b):
    b.validate_prior(b.row('facts','f.prior.product'))
    value=b.row('facts','f.prior.product')['object']
    assert value['support_count']==2 and value['eligible_count']==3
    assert value['classified_eligible_count']==2 and value['unclassified_count']==1
    assert value['denominator_definition']=='ELIGIBLE_RETRIEVED_RECORDS_INCLUDING_UNCLASSIFIED'

def test_D_neutral_workflow_mentions_have_a_different_policy(b):
    prior=b.row('facts','f.prior.industry');b.validate_prior(prior)
    assert prior['object']['support_policy_id']=='support.workflow_mention'
    assert b.reg('support-policies',prior['object']['support_policy_id'])['meaning']=='WORKFLOW_MENTION'

def test_D_missing_record_decision_rejected(b):
    b.row('samples','sample.product')['record_decisions'].pop()
    with pytest.raises(ContractError,match='INCOMPLETE_SAMPLE_DECISIONS'):b.validate_prior(b.row('facts','f.prior.product'))

def test_D_unclassified_cannot_be_treated_as_measured_no_theme(b):
    b.row('samples','sample.product')['record_decisions'][-1].update(status='NO_THEME',reason=None)
    with pytest.raises(ContractError,match='DECISION_WITHOUT_CLASSIFICATION'):b.validate_prior(b.row('facts','f.prior.product'))

def test_D_support_locator_must_belong_to_counted_record(b):
    b.row('facts','f.classify.product1')['object']['support_locator_ids']=['loc.art.product2']
    with pytest.raises(ContractError,match='CLASSIFICATION_SUPPORT_LOCATOR_TARGET'):b.validate_prior(b.row('facts','f.prior.product'))

E_CASES=[
 ('coverage_before_capture',lambda b:b.row('coverage','coverage.form').update(checked_at='2026-09-13T00:00:00Z'),'COVERAGE_PRECEDES_DETECTOR'),
 ('unknown_detector_hash',lambda b:b.row('coverage','coverage.form').update(detector_release='sha256:'+'0'*64),'UNRESOLVED_DETECTOR_RELEASE'),
 ('failed_detector',lambda b:b.row('executions','ex.detect.form').update(status='FAILED'),'FAILED_DETECTOR_COVERAGE'),
 ('wrong_capture_modality',lambda b:b.row('scopes','scope.home').update(capture_mode='RENDERED_DOM'),'DETECTOR_CAPTURE_MODE'),
 ('missing_capture_attempt',lambda b:b.row('coverage','coverage.form').update(attempt_ids=['missing']),'DANGLING_attempts'),
 ('unfinished_pagination',lambda b:b.row('attempts','attempt.art.home').update(pagination='INCOMPLETE'),'INCOMPLETE_SUCCESS'),
 ('truncated_attempt',lambda b:b.row('attempts','attempt.art.home').update(truncated=True),'INCOMPLETE_SUCCESS'),
 ('wrong_detector_target',lambda b:b.row('executions','ex.detect.form')['parameters'].update(target={'form_key':'different'}),'DETECTOR_TARGET_MISMATCH'),
 ('detector_before_capture',lambda b:b.row('executions','ex.detect.form').update(started_at='2026-09-14T15:59:00Z'),'DETECTOR_BEFORE_CAPTURE_FINISH'),
]
@pytest.mark.parametrize('name,mut,code',E_CASES,ids=[x[0] for x in E_CASES])
def test_E_absence_requires_execution(b,name,mut,code):
    mut(b)
    with pytest.raises(ContractError,match=code):b.validate_coverage_execution(b.row('coverage','coverage.form'))

def test_E_raw_form_detector_ignores_comments_but_checks_actual_forms():
    from keensight_contracts.completion import form_detector
    assert not form_detector('<!-- <form action="/submit"></form> -->')
    assert form_detector('<form action="/submit"></form>')

def test_G_no_bytes_unknown_is_real_and_not_business_evidence(b):
    a=b.row('attempts','attempt.denied');assert a['artifact_ids']==[] and a['requests_made']==0
    b.validate_fact(b.row('facts','f.unknown'))
    assert not b.usable('f.unknown',AT)
    assert b.validate()['status']=='PASS'

@pytest.mark.parametrize('state,obj,reason',[('OBSERVED',{'product_id':'product.crm'},None),('NOT_FOUND',None,'NOT_DETECTED_IN_SCOPE')])
def test_G_diagnostic_attempt_cannot_prove_fact_or_absence(b,state,obj,reason):
    f=b.row('facts','f.unknown');f.update(state=state,object=obj,reason=reason)
    with pytest.raises(ContractError,match='ATTEMPT_CANNOT_PROVE_BUSINESS_FACT'):b.validate_fact(f)

def test_G_unresolved_target_can_fail_without_fabricated_subject(b):
    intake=deepcopy(b.row('intakes','intake.fixture'));target={'resource_uri':'https://fixture.example.test/unresolved','subject_id':None}
    intake.update(intake_id='intake.unresolved',targets=[target],idempotency_key='unresolved')
    intake['request_hash']=digest({'profile_id':intake['profile_id'],'purpose':intake['purpose'],'targets':intake['targets']})
    add(b,'intakes',intake,'intake_id')
    a=deepcopy(b.row('attempts','attempt.denied'));a.update(attempt_id='attempt.unresolved',intake_id=intake['intake_id'],target=target,scope_id=None,operation_key='unresolved')
    a['request_hash']=digest({'target':target,'source_id':a['source_id'],'operation_key':a['operation_key']})
    b.validate_attempt(a)

def test_G_empty_success_requires_an_actual_response(b):
    a=deepcopy(b.row('attempts','attempt.denied'));a.update(status='EMPTY_RESULT',terminal_reason='NO_RESULTS')
    with pytest.raises(ContractError,match='SUCCESS_WITHOUT_RESPONSE'):b.validate_attempt(a)

H_CASES=[
 ('disabled_signal',lambda b:b.reg('profiles','profile.broad_research')['signal_ids'].remove('TECHNOLOGY_FOOTPRINT'),'SIGNAL_NOT_ENABLED'),
 ('disabled_template',lambda b:b.reg('profiles','profile.broad_research')['template_ids'].remove('template.observed_product'),'TEMPLATE_NOT_ENABLED'),
 ('nonexistent_entrypoint',lambda b:b.reg('functions','signal.required_facts_v1').update(entrypoint='missing.module:nope'),'ENTRYPOINT_NOT_ALLOWLISTED'),
 ('missing_review',lambda b:b.row('packages','package.product').update(review_id=None),'APPROVAL_WITHOUT_REVIEW|PACKAGE_REVIEW_BACKLINK'),
 ('wrong_review_revision',lambda b:b.row('reviews','review.package.product')['package'].update(revision=2),'REVIEW_REVISION_HASH'),
 ('wrong_review_actor',lambda b:b.row('reviews','review.package.product').update(reviewer_id='missing.actor'),'DANGLING_actors'),
]
@pytest.mark.parametrize('name,mut,code',H_CASES,ids=[x[0] for x in H_CASES])
def test_H_handoff_chain(b,name,mut,code):
    rebase(b);mut(b)
    for run in b.rows['runs']:run['registry_release']=digest(b.registry)
    with pytest.raises(ContractError,match=code):b.validate()

def test_H_local_export_is_exact_no_send_and_idempotent(b,tmp_path):
    exporter=LocalPreviewExporter(b,tmp_path)
    first=exporter.export('gate.fixture',principal_id='actor.fixture',at='2026-09-14T20:00:30Z',idempotency_key='op1')
    second=exporter.export('gate.fixture',principal_id='actor.fixture',at='2026-09-14T20:00:30Z',idempotency_key='op1')
    assert not first.reused and second.reused and not first.send_allowed and first.path==second.path
    data=Path(first.path).read_text();assert 'Reporting requires' not in data and 'send_allowed":false' in data

def test_H_idempotency_refuses_different_payload(b,tmp_path):
    exporter=LocalPreviewExporter(b,tmp_path)
    r=exporter.export('gate.fixture',principal_id='actor.fixture',at='2026-09-14T20:00:30Z',idempotency_key='op1')
    Path(r.path).write_text('interrupted or conflicting bytes')
    with pytest.raises(ContractError,match='IDEMPOTENCY_PAYLOAD_CONFLICT'):
        exporter.export('gate.fixture',principal_id='actor.fixture',at='2026-09-14T20:00:30Z',idempotency_key='op1')

def test_H_expired_gate_cannot_export(b,tmp_path):
    with pytest.raises(ContractError,match='EXPIRED_USE_GATE'):
        LocalPreviewExporter(b,tmp_path).export('gate.fixture',principal_id='actor.fixture',at='2026-09-14T20:06:00Z',idempotency_key='later')

def test_H_changed_source_state_requires_new_gate(b):
    b.row('artifacts','art.product3')['retention_state']='DELETED'
    with pytest.raises(ContractError):b.validate_gate(b.row('gates','gate.fixture'))

def test_H_DNC_has_no_implicit_fact_TTL(b):
    r={'restriction_id':'restriction.dnc','tenant_id':'tenant.demo','subject_id':'org.acme','recipient_key':None,'kind':'DNC',
       'actor_id':'actor.fixture','effective_at':'2026-09-01T00:00:00Z','released_at':None,'released_by':None,'reason':'Opt out'}
    add(b,'restrictions',r,'restriction_id');g=b.row('gates','gate.fixture')
    assert 'DNC' in b.gate_reasons(g,'2026-09-14T20:00:30Z')
    assert 'DNC' in b.gate_reasons(g,'2027-09-14T20:00:30Z')
    restamp_gate(b)
    with pytest.raises(ContractError,match='USE_GATE_DECISION_MISMATCH'):b.validate_gate(g)
    g.update(decision='BLOCK',reasons=['DNC']);b.validate_gate(g)
    with pytest.raises(ContractError,match='EXPORT_GATE_BLOCKED'):b.validate_export(b.row('exports','export.fixture'))

def test_H_recipient_is_required_for_contact_specific_handoff(b):
    d=b.reg('destinations','destination.fixture');d['kind']='CONTACT_HANDOFF'
    g=b.row('gates','gate.fixture');g['purpose']='CONTACT_EXPORT';restamp_gate(b)
    with pytest.raises(ContractError,match='GATE_RECIPIENT_REQUIRED_OR_UNEXPECTED'):b.validate_gate(g)

def test_H_review_is_not_permission_to_send(b):
    ex={'exposure_id':'exposure.fake','tenant_id':'tenant.demo','package_id':'package.product','business_send_key':'key','provider_message_id':'fake',
        'recipient_key':'recipient','accepted_at':'2026-09-14T20:00:30Z','status':'PROVIDER_ACCEPTED'}
    add(b,'exposures',ex,'exposure_id')
    with pytest.raises(ContractError,match='DELIVERY_DISABLED'):b.validate_handoffs()

def test_H_unknown_export_result_has_no_confirmation(b):
    x=deepcopy(b.row('exports','export.fixture'));x.update(status='UNKNOWN',external_reference=None,payload_ref=None,completed_at=None)
    b.validate_export(x)
    x['external_reference']='pretend-confirmed'
    with pytest.raises(ContractError,match='UNCERTAIN_EXPORT_AS_CONFIRMED'):b.validate_export(x)

def test_H_actor_permission_not_taken_from_package(b):
    b.reg('actors','actor.fixture')['permissions'].remove('REVIEW_PACKAGE')
    with pytest.raises(ContractError,match='ACTOR_NOT_AUTHORIZED'):b.validate_review(b.row('reviews','review.package.product'))

def test_H_export_payload_cannot_add_internal_priors(b):
    x=deepcopy(b.row('exports','export.fixture'));x['payload_hash']=digest(b'unsafe case-study or internal pain claim')
    with pytest.raises(ContractError,match='EXPORT_PAYLOAD_HASH'):b.validate_export(x)


def test_B_direct_signal_consumer_rejects_unpinned_input(b):
    b.row('runs','run.demo')['input_fact_ids'].remove('f.tech')
    with pytest.raises(ContractError,match='UNPINNED_CONSUMED_FACT'):
        b.assert_consumed('f.tech','run.demo')


def test_C_duplicate_upstream_origin_does_not_meet_minimum(b):
    rebase(b);f=deepcopy(b.row('facts','f.tech'));f['fact_id']='f.tech.duplicate'
    add(b,'facts',f,'fact_id')
    for run in b.rows['runs']:
        run['input_fact_ids'].append(f['fact_id'])
        for rid in run['resolution_ids']:
            r=b.row('resolutions',rid)
            if 'f.tech' in r['observation_ids']:
                r['observation_ids'].append(f['fact_id']);r['accepted_fact_ids'].append(f['fact_id'])
    b.row('signals','signal.tech')['input_fact_ids'].append(f['fact_id'])
    b.reg('signals','TECHNOLOGY_FOOTPRINT')['required_facts'][0]['minimum']=2
    rebase(b)
    with pytest.raises(ContractError,match='SIGNAL_REQUIREMENT_UNSATISFIED'):b.validate()


def test_G_diagnostic_metadata_does_not_require_deriving_provider_content(b):
    b.reg('policies','policy.blocked')['purposes']=[]
    b.validate_fact(b.row('facts','f.unknown'))
    assert not b.usable('f.unknown',AT)


def test_H_live_capture_must_be_enabled_even_when_source_rights_allow(b):
    a=deepcopy(b.row('attempts','attempt.art.home'));a['execution_mode']='LIVE_CAPTURE'
    with pytest.raises(ContractError,match='CAPTURE_SOURCE_NOT_ENABLED'):b.validate_attempt(a)


def test_H_blocked_gate_can_record_revocation_after_valid_historical_review(b):
    b.row('artifacts','art.product3')['retention_state']='DELETED'
    g=b.row('gates','gate.fixture');g.update(decision='BLOCK',reasons=['INELIGIBLE_CURRENT_SUPPORT'])
    restamp_gate(b)
    b.validate_gate(g)
    with pytest.raises(ContractError,match='EXPORT_GATE_BLOCKED'):b.validate_export(b.row('exports','export.fixture'))


def test_A_model_io_is_in_full_provenance_and_rights_checks(b):
    assert {'art.request','art.response','art.job'}<=b.roots('f.job_statement')
    b.reg('sources','source.model')['authority']='CANDIDATE'
    assert not b.usable('f.job_statement',AT)


def test_ledger_all_52_ids_and_predicate_references(b):
    import json
    rows=json.loads((ROOT/'docs/LEDGER_MAP.json').read_text())
    assert [r['id'] for r in rows]==list(range(1,53))
    for row in rows:
        for pid in row['predicate_ids']:assert b.reg('predicates',pid)
        assert row['live_provider_integration_added'] is False


def test_new_record_families_preserve_full_v4_catalog(b):
    assert len(b.registry['predicates'])==213
    assert len(b.registry['metrics'])==89
    assert {'case_study.report','case_study.outcome_report','legal.filing_record','registry.financing_filing','repository.activity_observed'}<=set(b.rindex['predicates'])


def test_scenario_cannot_be_labeled_verified_loss(b):
    scenario={'scenario_id':'s','tenant_id':'tenant.demo','subject_id':'org.acme','observed_input_fact_ids':[],
        'assumptions':[{'name':'missed_calls','value':10,'unit':'calls','basis':'Illustrative only'}],'formula_version':'1.0.0',
        'currency':'USD','lower_minor':0,'upper_minor':10000,'time_period':'month','limitations':['No measured loss'],
        'verified_loss':True,'implementation_status':'DESIGN_ONLY'}
    with pytest.raises(ContractError):b.shape(scenario,'ScenarioEstimate')
