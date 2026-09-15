from __future__ import annotations
import copy
import pytest
from jsonschema.exceptions import ValidationError
from validate_protocol import ROOT, load, validators, validate_pair, validate_pack, digest


def pair():
    return copy.deepcopy(load(ROOT/'examples/request.json')), copy.deepcopy(load(ROOT/'examples/result.json'))


def test_pack():
    assert validate_pack()['module_definitions']==30


def test_success():
    validate_pair(*pair())


@pytest.mark.parametrize('status', ['FAILED','SKIPPED','CANCELLED'])
def test_non_success_forbids_positive_output(status):
    a,b=pair(); b['execution_status']=status
    with pytest.raises(ValidationError): validate_pair(a,b)


@pytest.mark.parametrize('field,value', [('trace_id','0'*32),('span_id','0'*16),('trace_id','Z'*32),('span_id','short')])
def test_trace_format(field,value):
    a,b=pair(); a['trace'][field]=value
    with pytest.raises(ValidationError): validators()['ModuleRequest'].validate(a)


@pytest.mark.parametrize('field', ['request_id','execution_id','operation','module_id'])
def test_result_pair_binding(field):
    a,b=pair(); b[field]='CTL-01' if field=='module_id' else 'different'
    with pytest.raises((ValueError,ValidationError)): validate_pair(a,b)


def test_context_mismatch():
    a,b=pair(); b['context']['tenant_id']='other'
    with pytest.raises(ValueError): validate_pair(a,b)


def test_digest_mismatch():
    a,b=pair(); b['request_digest']='sha256:'+'b'*64
    with pytest.raises(ValueError): validate_pair(a,b)


def test_chronology():
    a,b=pair(); b['finished_at']='2026-09-14T11:00:00Z'
    with pytest.raises(ValueError): validate_pair(a,b)


def test_cross_tenant_input():
    a,b=pair(); b['consumed_refs'][0]['tenant_id']='other'
    with pytest.raises(ValueError): validate_pair(a,b)


def test_mutated_reference():
    a,b=pair(); b['consumed_refs'][0]['content_digest']='sha256:'+'a'*64
    with pytest.raises(ValueError): validate_pair(a,b)


@pytest.mark.parametrize('field', ['unexpected','raw_provider_response','access_token'])
def test_closed_envelope(field):
    a,b=pair(); a[field]='data'
    with pytest.raises(ValidationError): validators()['ModuleRequest'].validate(a)


def test_invalid_timestamp():
    a,b=pair(); a['deadline_at']='2026-02-31T12:00:00Z'
    with pytest.raises(ValidationError): validators()['ModuleRequest'].validate(a)


def test_missing_evaluation_asof():
    a,b=pair(); a['context']['as_of']=None
    with pytest.raises(ValidationError): validators()['ModuleRequest'].validate(a)


def test_capture_can_precede_sealing():
    a,b=pair(); a['context']['mode']='CAPTURE';a['context']['as_of']=None;a['context']['knowledge_cutoff']=None
    validators()['ModuleRequest'].validate(a)


def test_unknown_money_is_not_zero():
    a,b=pair(); b['usage']['cost_status']='UNKNOWN'; b['usage']['cost_amount']='0'
    with pytest.raises(ValidationError): validators()['ModuleResult'].validate(b)


def test_known_money_requires_currency():
    a,b=pair(); b['usage']['cost_status']='KNOWN'; b['usage']['cost_amount']='0.004';b['usage']['currency']=None
    with pytest.raises(ValidationError): validators()['ModuleResult'].validate(b)


def test_fractional_request_counter():
    a,b=pair(); b['usage']['network_attempts']=0.5
    with pytest.raises(ValidationError): validators()['ModuleResult'].validate(b)


def test_nonbootstrap_needs_lock():
    a,b=pair();a['release_lock_ref']=None;b['request_digest']=digest(a)
    with pytest.raises(ValueError): validate_pair(a,b)


def test_no_recursion_on_reuse():
    a,b=pair();b['reused_execution_id']=b['execution_id']
    with pytest.raises(ValueError): validate_pair(a,b)


def test_legacy_business_status_not_execution_status():
    a,b=pair();b['execution_status']='RESOLVED'
    with pytest.raises(ValidationError): validators()['ModuleResult'].validate(b)


def test_controlled_failure_keeps_diagnostic_record():
    a,b=pair();b['execution_status']='FAILED';b['output_refs']=[]
    b['diagnostic_record_refs']=[a['input_refs'][0]]
    b['diagnostics']=[dict(diagnostic_id='diag:1',code='NETWORK.TIMEOUT',severity='ERROR',message='No response obtained.',record_refs=[],field_path=None,cause_execution_id=None,suggested_action='RETRY_AFTER_POLICY',restricted_details_ref=None)]
    validate_pair(a,b)


def test_unregistered_diagnostic_code():
    a,b=pair()
    b['diagnostics']=[dict(diagnostic_id='diag:1',code='MADEUP.ERROR',severity='ERROR',message='No.',record_refs=[],field_path=None,cause_execution_id=None,suggested_action='NONE',restricted_details_ref=None)]
    with pytest.raises(ValueError): validate_pair(a,b)


def test_suggestion_is_not_freeform_code():
    a,b=pair()
    b['diagnostics']=[dict(diagnostic_id='diag:1',code='NETWORK.TIMEOUT',severity='ERROR',message='No.',record_refs=[],field_path=None,cause_execution_id=None,suggested_action='EXECUTE_ARBITRARY_CODE',restricted_details_ref=None)]
    with pytest.raises(ValidationError): validate_pair(a,b)
