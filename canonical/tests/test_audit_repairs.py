"""Concrete reference-boundary repairs, not live provider integration."""
from copy import deepcopy
from pathlib import Path
import pytest
from keensight_contracts.validation import Bundle
from keensight_contracts.engine import ContractError,digest,matches_fingerprint
ROOT=Path(__file__).parents[1]
@pytest.fixture
def b():return Bundle(ROOT,check_hashes=False)
def refresh(b):
 b.rows['gates'].clear();b.index['gates'].clear();b.rows['exports'].clear();b.index['exports'].clear()
 for r in b.rows['runs']:r['registry_release']=digest(b.registry)

def test_model_provenance_is_not_corroboration(b):
 assert {'art.request','art.response','art.job'}<=b.roots('f.job_statement')
 assert b.corroborating_artifacts('f.job_statement')=={'art.job'}
 s=next(s for s in b.rows['signals'] if s['input_fact_ids']==['f.job_statement'])
 b.reg('signals',s['signal_type_id'])['required_facts'][0]['minimum']=3;refresh(b)
 with pytest.raises(ContractError,match='SIGNAL_REQUIREMENT'):b.validate()

def test_new_conflict_blocks_current_gate(b):
 f=deepcopy(b.row('facts','f.tech'));f.update(fact_id='f.conflict',recorded_at='2026-09-14T20:00:05Z');f['object']['version']='different'
 b.rows['facts'].append(f);b.index['facts'][f['fact_id']]=f
 g=b.rows['gates'][0];g['version_vector']=b.current_version_vector('package.product')
 assert 'INELIGIBLE_CURRENT_SUPPORT' in b.gate_reasons(g)
 with pytest.raises(ContractError):b.validate_gate(g)

def test_future_conflict_is_not_yet_known_to_gate(b):
 f=deepcopy(b.row('facts','f.tech'));f.update(fact_id='f.future',recorded_at='2099-01-01T00:00:00Z');f['object']['version']='different'
 b.rows['facts'].append(f);b.index['facts'][f['fact_id']]=f
 assert b.current_claim_eligible('f.tech','2026-09-14T20:00:00Z')

def produced_response(b):
 art=b.row('artifacts','art.response');art['captured_at']='2026-09-14T17:00:30Z'
 for a in b.rows['attempts']:
  if 'art.response' in a['artifact_ids']:a['finished_at']='2026-09-14T17:00:31Z'
 run=b.row('runs','run.ingest');run['input_artifact_ids'].remove('art.response');run['produced_artifact_ids'].append('art.response')
 b.row('executions','ex.job_llm')['output_artifact_ids'].append('art.response')
 refresh(b)

def test_genuine_generated_response_is_not_external_input(b):
 produced_response(b);assert b.validate()['status']=='PASS'

@pytest.mark.parametrize('mutation',['undeclared','early','late','self_input'])
def test_generated_artifact_contract_rejects_invalid_closure(b,mutation):
 produced_response(b);ex=b.row('executions','ex.job_llm')
 if mutation=='undeclared':ex['output_artifact_ids']=[]
 elif mutation=='early':b.row('artifacts','art.response')['captured_at']='2026-09-14T16:00:00Z'
 elif mutation=='late':b.row('artifacts','art.response')['captured_at']='2026-09-14T18:00:00Z'
 else:ex['input_artifact_ids'].append('art.response')
 with pytest.raises(ContractError):b.validate()

def change(**kw):
 c=dict(change_id='change.test',tenant_id='tenant.demo',kind='RETRACTION',target_id='f.tech',replacement_id=None,
        effective_at='2026-09-14T19:00:00Z',recorded_at='2026-09-14T19:00:00Z',reason='fixture',actor_id='actor.fixture',target_type='facts')
 c.update(kw);return c

def test_authorized_retraction_takes_effect(b):
 c=change();b.validate_change(c);b.rows['changes'].append(c)
 assert not b.usable('f.tech','2026-09-14T20:00:00Z')

@pytest.mark.parametrize('mut',[{'tenant_id':'tenant.foreign'},{'actor_id':'missing'}, {'target_type':'bindings'}, {'replacement_id':'missing'},{'recorded_at':'2026-09-14T18:00:00Z'}])
def test_unauthorized_changes_cannot_deny_another_claim(b,mut):
 c=change(**mut)
 with pytest.raises(ContractError):b.validate_change(c)
 b.rows['changes'].append(c)
 assert b.usable('f.tech','2026-09-14T20:00:00Z')

def test_authorized_future_retraction_not_visible_yet(b):
 c=change(recorded_at='2026-09-15T00:00:00Z');b.rows['changes'].append(c)
 assert b.usable('f.tech','2026-09-14T20:00:00Z')

def test_matched_fact_requires_actual_capture(b):
 b.row('facts','f.tech')['object']['matched_value']='not-evidenced.example';refresh(b)
 with pytest.raises(ContractError,match='FINGERPRINT_NOT_SUPPORTED'):b.validate()

@pytest.mark.parametrize('wrapper',['template','noscript','footer','aside'])
def test_reference_fingerprint_rejects_inert_and_attribution_areas(b,wrapper):
 assert not matches_fingerprint(b.registry['fingerprints'][0],f'<{wrapper}><script src="https://assets.calendly.com/a.js"></script></{wrapper}>')

def test_reference_fingerprint_rejects_inert_script_type(b):
 assert not matches_fingerprint(b.registry['fingerprints'][0],'<script type="text/plain" src="https://assets.calendly.com/a.js"></script>')
