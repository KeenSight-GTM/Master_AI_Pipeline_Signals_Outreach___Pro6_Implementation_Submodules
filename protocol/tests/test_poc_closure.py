import copy
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import validate_protocol as p

def pair():return p.load(p.ROOT/'examples/request.json'),p.load(p.ROOT/'examples/result.json')

def test_late_failure_can_record_actual_finish():
    req,res=pair();res.update(execution_status='FAILED',output_refs=[],finished_at='2026-09-14T12:02:01Z')
    res['diagnostics']=[{'diagnostic_id':'deadline:1','code':'MODULE.DEADLINE_EXCEEDED','severity':'ERROR','message':'Timed out; terminal diagnostic finalized after deadline.','record_refs':[],'field_path':None,'cause_execution_id':None,'suggested_action':'NONE','restricted_details_ref':None}]
    p.validate_pair(req,res)

def test_late_success_cannot_publish():
    req,res=pair();res['finished_at']='2026-09-14T12:02:01Z'
    with pytest.raises(ValueError,match='beyond deadline'):p.validate_pair(req,res)

@pytest.mark.parametrize('mode,network',[('CAPTURE',0),('EVALUATE',1),('REPLAY',1)])
def test_mode_and_effect_signature(mode,network):
    req,res=pair();req['context']['mode']=mode;res['context']['mode']=mode
    res['request_digest']=p.digest(req);res['usage']['network_attempts']=network
    with pytest.raises(ValueError):p.validate_pair(req,res)
