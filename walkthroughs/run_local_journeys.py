#!/usr/bin/env python3
"""Offline walkthrough harness. Not the proposed generic ModuleRequest runner.

Writes only beneath --output and executes the shipped local fixture commands.
Every subprocess command, result code, stdout, stderr and assertion is retained.
No network, CRM, actual human approval, enrollment, or sending is implemented.
"""
from __future__ import annotations
import argparse,json,os,pathlib,subprocess,sys,time,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--baseline',type=pathlib.Path,default=ROOT)
 p.add_argument('--output',type=pathlib.Path,required=True)
 p.add_argument('--journey',choices=['all-local','J01','J02','J03','J04','J05','J06','J07','J08'],default='all-local')
 a=p.parse_args();base=a.baseline.resolve();out=a.output.resolve()
 if not (base/'collector/src/keensight_scrapling').is_dir():p.error('Missing unpacked baseline/collector')
 if out==base or out.is_relative_to(base):p.error('Keep walkthrough output outside the audited source')
 out.mkdir(parents=True,exist_ok=True);logs=out/'logs';logs.mkdir(exist_ok=True)
 env={**os.environ,'PYTHONPATH':str(base/'collector/src')+os.pathsep+str(base/'canonical')}
 steps=[];journeys=[]
 def run(label,args,expect=0,cwd=None):
  command=[sys.executable,*map(str,args)];t=time.monotonic()
  r=subprocess.run(command,cwd=cwd or ROOT,env=env,text=True,capture_output=True,timeout=90)
  n=len(steps)+1;prefix=f'{n:02d}-{label}'
  (logs/(prefix+'.stdout.txt')).write_text(r.stdout);(logs/(prefix+'.stderr.txt')).write_text(r.stderr)
  rec={'step':n,'label':label,'command':command,'cwd':str(cwd or ROOT),'returncode':r.returncode,'expected_returncode':expect,'elapsed_seconds':round(time.monotonic()-t,3)};steps.append(rec)
  (out/'invocation-results.json').write_text(json.dumps({'baseline':str(base),'journeys':journeys,'steps':steps,'network_enabled':False},indent=2))
  if r.returncode!=expect:raise RuntimeError(f'{label}: expected exit {expect}, got {r.returncode}: {r.stderr[-1500:]}')
  return r
 demo=out/'demo-store';rules=base/'collector/examples/demo-rules.json'
 def ensure_demo():
  if not (demo/'scan-bundle.json').exists():run('demo-prerequisite',['-m','keensight_scrapling.cli','demo','--output',demo])
 def j01():
  run('command-inventory',['-m','keensight_scrapling.cli','commands'])
  run('demo',['-m','keensight_scrapling.cli','demo','--output',demo])
  b=json.loads((demo/'scan-bundle.json').read_text());assert (len(b['matches']),len(b['observations']),len(b['claims']))==(7,2,1)
  run('demo-check',['-m','keensight_scrapling.cli','check',demo/'scan-bundle.json','--store',demo])
 def j02():
  run('retained-html',['-m','keensight_scrapling.cli','analyze-file','--html',base/'collector/examples/page.html','--url','https://example.test/','--observed-at','2026-09-14T12:00:00Z','--tenant','local','--subject','account:example','--run','retained-example-01','--rules',rules,'--store',out/'imported-store','--output',out/'imported-store/scan-bundle.json'])
  run('retained-check',['-m','keensight_scrapling.cli','check',out/'imported-store/scan-bundle.json','--store',out/'imported-store'])
 def j03():
  ensure_demo();b=json.loads((demo/'scan-bundle.json').read_text());cid=b['observations'][0]['capture_id']
  run('extract',['-m','keensight_scrapling.standalone','extract','--tenant','demo','--capture-id',cid,'--store',demo,'--output',out/'page-evidence.json'])
  run('match',['-m','keensight_scrapling.standalone','match','--page',out/'page-evidence.json','--rules',rules,'--store',demo,'--output',out/'matches.json'])
  run('check-module',['-m','keensight_scrapling.standalone','check','--bundle',demo/'scan-bundle.json','--store',demo,'--output',out/'checked.json'])
  run('resolve',['-m','keensight_scrapling.standalone','resolve','--bundle',demo/'scan-bundle.json','--as-of','2026-09-14T12:00:00Z','--store',demo,'--output',out/'resolved.json'])
  assert json.loads((out/'matches.json').read_text())['matches']
 def j04():
  ensure_demo();before=json.loads((demo/'scan-bundle.json').read_text())
  run('replay',['-m','keensight_scrapling.cli','replay','--store',demo,'--tenant','demo','--capture-run','demo-capture-1','--evaluation-run','walkthrough-replay-01','--as-of','2026-09-14T13:00:00Z','--rules',rules,'--output',out/'replay.json'])
  after=json.loads((out/'replay.json').read_text());assert before['observations']==after['observations']
  run('query-claims',['-m','keensight_scrapling.cli','claims','--store',demo,'--tenant','demo','--rules',rules,'--as-of','2026-09-14T13:00:00Z'])
 def j05():
  ensure_demo()
  run('donor-import',['-m','keensight_scrapling.cli','import-donor','--input',base/'collector/examples/donor-shaped.jsonl','--vendor-map',base/'collector/examples/vendor-map.json','--output',out/'imported-candidates.json','--report',out/'import-report.json'])
  run('candidate-query',['-m','keensight_scrapling.cli','candidates','--store',demo,'--tenant','demo','--min-hosts','1'])
  report=json.loads((out/'import-report.json').read_text());assert report['automatic_approvals']==0
 def j06():
  ensure_demo();b=json.loads((demo/'scan-bundle.json').read_text());b['captures'][0]['headers']['x-audit']='not-in-stored-capture'
  bad=out/'tampered-bundle.json';bad.write_text(json.dumps(b))
  run('expected-integrity-rejection',['-m','keensight_scrapling.standalone','check','--bundle',bad,'--store',demo,'--output',out/'must-not-exist.json'],expect=2)
  run('unchanged-valid-bundle',['-m','keensight_scrapling.standalone','check','--bundle',demo/'scan-bundle.json','--store',demo,'--output',out/'valid-after-rejection.json'])
 def j07():
  run('canonical-generate-check',['generate.py','--check'],cwd=base/'canonical')
  run('canonical-validate',['validate.py'],cwd=base/'canonical')
  run('reference-export',[ROOT/'walkthroughs/reference_preview.py','--canonical',base/'canonical','--output',out/'reference'])
 def j08():
  run('protocol-fixture-check',['validate_protocol.py'],cwd=base/'protocol')
  run('product-design-check',['validate_design.py'],cwd=base/'product-design')
 actions={f'J{i:02d}':fn for i,fn in enumerate([j01,j02,j03,j04,j05,j06,j07,j08],1)}
 for jid,fn in actions.items():
  if a.journey not in ['all-local',jid]:continue
  fn();journeys.append({'id':jid,'status':'PASSED','scope':'OFFLINE_FIXTURE_OR_REFERENCE_ONLY'})
 report={'baseline':str(base),'journeys':journeys,'steps':steps,'network_enabled':False,'send_allowed':False,'all_expected_exit_codes':all(s['returncode']==s['expected_returncode'] for s in steps)}
 (out/'invocation-results.json').write_text(json.dumps(report,indent=2));print(json.dumps({'journeys':len(journeys),'subprocesses':len(steps),'status':'PASS','report':str(out/'invocation-results.json'),'no_live_sources_or_sender_tested':True},indent=2))
if __name__=='__main__':main()
