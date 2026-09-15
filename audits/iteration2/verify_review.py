#!/usr/bin/env python3
"""Validate review indexes/evidence without claiming that its failing repairs are implemented."""
from pathlib import Path
import json, re, subprocess, sys, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent

def read(name):return json.loads((R/name).read_text())
def main():
    checks=[]
    def check(ok,label):
        if not ok:raise AssertionError(label)
        checks.append(label)
    findings=read('findings.json');features=read('feature-map.json');journeys=read('user-journeys.json')
    modules=read('baseline/product-design/module_catalog.json')['modules']
    mids={m['module_id'] for m in modules};fids={f['feature_id'] for f in features};jids={j['journey_id'] for j in journeys};issue_ids={f['id'] for f in findings}
    check(len(mids)==39,'39 original module IDs retained')
    check(len(features)==len(fids)==36,'36 unique feature cards')
    check(jids=={f'J{i:02d}' for i in range(1,20)},'19 unique journey cards')
    check(len(findings)==len(issue_ids)==16,'15 code findings and one policy question')
    check(sum(x['classification']=='POLICY_DECISION_REQUIRED' for x in findings)==1,'Temporal policy remains separately classified')
    check(all(not x['patched_in_this_review'] for x in findings),'Findings do not claim patched runtime')
    check(set().union(*(set(f['modules']) for f in features))==mids,'Feature map covers exactly all original modules')
    for f in features:
        check(set(f['journeys'])<=jids,f"{f['feature_id']} journey references resolve")
    for f in findings:
        check(set(f['modules'])<=mids and set(f['journeys'])<=jids,f"{f['id']} ownership and journeys resolve")
        for path,start,end in f['source_ranges']:
            p=R/'baseline'/path
            check(p.is_file() and 1<=start<=end<=len(p.read_text().splitlines()),f"{f['id']} source range {path}:{start}-{end}")
    stages=read('baseline/docs/stage_cards.json')
    text=(R/'UPDATED_STAGE_WALKTHROUGHS.md').read_text()
    check(len(stages)==27 and all('F'+s['step'] in text for s in stages),'All 27 original stage IDs appear in revised walkthroughs')
    bindings=read('baseline/product-design/reference/command_bindings.json')['commands']
    check(len(bindings)==len({b['command_id'] for b in bindings})==38 and all(b['module_id'] in mids for b in bindings),'38 collector command bindings retained')
    probes=read('reports/probe-results.json')['probes'];pids={p['id'] for p in probes}
    check(len(probes)==len(pids)==23 and not any('probe_error' in p for p in probes),'23 probes executed without probe harness errors')
    check(sum(bool(p['violation_present']) for p in probes)==17,'16 safety counterexamples plus one temporal question reproduced')
    check(sum(p['id'].startswith('CTRL-') and not p['violation_present'] for p in probes)==6,'Six prior safety controls remain effective')
    check(set().union(*(set(f['probe_ids']) for f in findings))=={p['id'] for p in probes if not p['id'].startswith('CTRL-')},'Each non-control probe maps to a reported finding')
    xml=ET.parse(R/'reports/required-behaviour.xml').getroot();suites=list(xml.iter('testsuite'))
    check(sum(int(s.attrib.get('tests',0)) for s in suites)==22 and sum(int(s.attrib.get('failures',0)) for s in suites)==16 and sum(int(s.attrib.get('errors',0)) for s in suites)==0,'Required-behavior suite: 16 failures, 6 passes, no runner errors')
    smoke=read('reports/journey-smoke/invocation-results.json')
    check({j['id'] for j in smoke['journeys']}=={f'J{i:02d}' for i in range(1,9)},'J01–J08 executed')
    check(len(smoke['steps'])==20 and all(s['returncode']==s['expected_returncode'] for s in smoke['steps']),'20 subprocess invocations match expected exit codes')
    check(smoke['network_enabled'] is False and smoke['send_allowed'] is False,'Smoke report claims neither live networking nor sending')
    r=subprocess.run([sys.executable,str(R/'baseline/verify_integrity.py')],cwd=R/'baseline',capture_output=True,text=True,check=True)
    check('PASS 438 packaged files' in r.stdout,'All 438 original integrity-manifest files unchanged')
    report={'status':'PASS','purpose':'Review index and evidence consistency, not production readiness','checks':checks,'counts':{'original_modules':39,'feature_cards':36,'journeys':19,'stage_cards':27,'code_findings':15,'temporal_policy_questions':1,'probes':23,'safety_failures':16,'passing_controls':6,'smoke_journeys':8,'smoke_invocations':20},'baseline_modified':False,'runtime_fixes_in_this_review':False}
    (R/'reports/review-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','review_consistency_checks':len(checks),'counts':report['counts'],'not_a_production_signoff':True},indent=2))
if __name__=='__main__':main()
