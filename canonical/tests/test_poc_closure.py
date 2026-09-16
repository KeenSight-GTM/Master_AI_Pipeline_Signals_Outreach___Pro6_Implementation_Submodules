import copy
from pathlib import Path
import pytest
from keensight_contracts.engine import semantic_value,resolve_claim,evaluate_requirements,ContractError
from keensight_contracts.validation import Bundle
ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('left,right',[(12000,12000.0),(0,-0.0),({'n':[2,0]},{'n':[2.0,0.0]})])
def test_exact_numeric_equivalence(left,right):assert semantic_value(left)==semantic_value(right)

@pytest.mark.parametrize('left,right',[(True,1),(False,0),('12000',12000),(12000,12000.01),({'unit':'usd','value':1},{'unit':'eur','value':1})])
def test_distinct_json_values_are_not_coerced(left,right):assert semantic_value(left)!=semantic_value(right)

def test_usable_does_not_read_unpinned_successors():
    b=Bundle(ROOT);old=b.row('facts','f.tech');later=copy.deepcopy(old)
    later.update(fact_id='f.next',supersedes_fact_id=old['fact_id'],recorded_at='2026-09-14T19:30:00Z')
    b.rows['facts'].append(later);b.index['facts'][later['fact_id']]=later
    at='2026-09-14T20:00:00Z'
    eligible=lambda f,t:b.usable(f['fact_id'],t)
    assert resolve_claim([old],at,eligible)['accepted_fact_ids']==['f.tech']
    assert resolve_claim([old,later],at,eligible)['accepted_fact_ids']==['f.next']
    assert not b.current_claim_eligible('f.tech',at)

def test_minimum_needs_substantive_origin_resolver():
    b=Bundle(ROOT);f=b.row('facts','f.job_statement');req={'required_facts':[{'predicate_id':f['predicate_id'],'state':'OBSERVED','allowed_natures':[f['nature']],'minimum':2}]}
    rows=[f,{**f,'fact_id':'duplicate'}]
    assert evaluate_requirements(req,rows,f['subject_id'],'2026-09-14T20:00:00Z',lambda *a,**kw:True)=='UNRESOLVED'
    same=lambda fid:{('origin','same-job')}
    assert evaluate_requirements(req,rows,f['subject_id'],'2026-09-14T20:00:00Z',lambda *a,**kw:True,substantive_origins=same)=='UNRESOLVED'
    separate=lambda fid:{('origin',fid)}
    assert evaluate_requirements(req,rows,f['subject_id'],'2026-09-14T20:00:00Z',lambda *a,**kw:True,substantive_origins=separate)=='RESOLVED'

def test_supersession_cycle_rejected_before_traversal():
    b=Bundle(ROOT);b.row('facts','f.tech')['supersedes_fact_id']='f.tech'
    with pytest.raises(ContractError,match='SELF_CYCLE'):b.validate()
