from copy import deepcopy
import pytest
from jsonschema.exceptions import ValidationError
from validate_protocol import ROOT,load,validate_pair,validate_payload_pair,digest

def pair():return deepcopy(load(ROOT/'examples/request.json')),deepcopy(load(ROOT/'examples/result.json'))

@pytest.mark.parametrize('mutation',['extra','unknown_operation','wrong_output','no_consumed','duplicate_input','overwrite','past_deadline'])
def test_signature_and_closure_reject(mutation):
 a,b=pair()
 if mutation=='extra':
  r=deepcopy(a['input_refs'][0]);r['record_id']='extra';b['consumed_refs'].append(r)
 elif mutation=='unknown_operation':a['operation']=b['operation']='anything'
 elif mutation=='wrong_output':b['output_refs'][0]['schema_id']='urn:any'
 elif mutation=='no_consumed':b['consumed_refs']=[]
 elif mutation=='duplicate_input':a['input_refs'].append(deepcopy(a['input_refs'][0]))
 elif mutation=='overwrite':b['output_refs'][0]['record_id']=a['input_refs'][0]['record_id']
 else:b['finished_at']='2026-09-15T12:00:00Z'
 b['request_digest']=digest(a)
 with pytest.raises((ValueError,ValidationError)):validate_pair(a,b)

def test_resolved_payloads_match_refs():
 a,b=pair();records=load(ROOT/'examples/fixture_records.json')
 assert validate_payload_pair(a,b,lambda ref:records[ref['record_id']])

def test_corrupt_resolved_payload_rejected():
 a,b=pair();records=deepcopy(load(ROOT/'examples/fixture_records.json'));records['capture:demo']['body']['body_digest']='fabricated'
 with pytest.raises((ValueError,ValidationError)):validate_payload_pair(a,b,lambda ref:records[ref['record_id']])
