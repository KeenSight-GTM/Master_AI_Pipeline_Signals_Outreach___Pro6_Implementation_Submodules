"""Exercise the shipped canonical fixtures, NOT collector-to-fact admission."""
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--canonical',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.canonical.resolve()))
from keensight_contracts.validation import Bundle
from keensight_contracts.handoff import LocalPreviewExporter
b=Bundle(a.canonical.resolve());validated=b.validate()
g=b.rows['gates'][0];exporter=LocalPreviewExporter(b,a.output/'exports')
first=exporter.export(g['gate_id'],principal_id='actor.fixture',at=g['evaluated_at'],idempotency_key='journey-fixture-preview')
second=exporter.export(g['gate_id'],principal_id='actor.fixture',at=g['evaluated_at'],idempotency_key='journey-fixture-preview')
assert second.reused and Path(first.path).read_bytes()==Path(second.path).read_bytes()
result={'kind':'REFERENCE_FIXTURE_WALKTHROUGH','canonical_validation':validated,'export_path':first.path,'payload_hash':first.payload_hash,'second_call_reused':second.reused,'send_allowed':False,'network_attempts':0,'as_of':g['evaluated_at'],'fixture_actor_not_authentication':True,'collector_to_canonical_bridge_exercised':False}
a.output.mkdir(parents=True,exist_ok=True);(a.output/'reference-preview.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
