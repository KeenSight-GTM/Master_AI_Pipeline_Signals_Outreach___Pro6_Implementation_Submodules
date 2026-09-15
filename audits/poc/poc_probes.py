"""Offline, standard-usage probes over the unchanged supplied implementation.

No network calls, monkeypatches, model calls, schema overrides, or mutations to
application source. Scan tests inject the collector's supported FixtureTransport.
Results distinguish executed defects from capabilities/policies still needed.
"""
from __future__ import annotations
from pathlib import Path
from dataclasses import asdict
from copy import deepcopy
import contextlib
import gzip
import io
import json
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
BASELINE = Path(os.environ.get('KEENSIGHT_BASELINE', str(ROOT.parents[1]))).resolve()
sys.path.insert(0, str(BASELINE / 'collector/src'))
sys.path.insert(0, str(BASELINE / 'canonical'))
from keensight_scrapling.cli import main as cli_main
from keensight_scrapling.core import ContractError
from keensight_scrapling.extraction import extract
from keensight_scrapling.importer import import_donor
from keensight_scrapling.pipeline import Scanner, ScanConfig
from keensight_scrapling.rules import RulePack, match_pages
from keensight_scrapling.storage import Store
from keensight_scrapling.transport import FixtureTransport, FetchResult
from keensight_contracts.validation import Bundle
from keensight_contracts.engine import resolve_claim, claim_key

AT = '2026-09-15T12:00:00Z'
HOST = 'https://shop.example.test'
RULE_PATH = BASELINE / 'collector/examples/demo-rules.json'
RAW = json.loads(RULE_PATH.read_text())
PACK = RulePack.compile(RAW)
HTML = (b'<html><body><script src="https://assets.calendly.com/widget.js"></script>'
        b'<p>Contact our practice to arrange a consultation.</p></body></html>')
QUIET = b'<html><body><p>Welcome to our practice.</p></body></html>'

@contextlib.contextmanager
def temporary_store():
    with tempfile.TemporaryDirectory(prefix='keensight-poc-') as td:
        store = Store(td)
        try:
            yield store
        finally:
            store.close()

def response(url, body=b'', status=200, headers=None):
    return FetchResult(url, status, body, headers if headers is not None else {'content-type':'text/html'})

def website(host=HOST, body=HTML):
    return {host+'/robots.txt': response(host+'/robots.txt', b'User-agent: *\nAllow: /', headers={'content-type':'text/plain'}),
            host+'/':response(host+'/', body)}

def runner(store, transport, pack=PACK, at=AT):
    return Scanner(store, pack, transport, production=False, clock=lambda:at)

def run_fixture(responses, *, seed=HOST, run='run', **configuration):
    with temporary_store() as store:
        transport=FixtureTransport(responses)
        try:
            result=runner(store, transport).scan(seed, ScanConfig('tenant','acct',run,**configuration))
            return {'error':None,'calls':transport.calls,'claim_count':len(result['claims']),
                    'evaluated_urls':[c['url'] for c in result['captures'] if c['capture_id'] in result['evaluated_capture_ids']],
                    'dispositions':result['resource_dispositions'],
                    'fetches':[{k:c[k] for k in ('command_id','status','limitations')} for c in result['commands'] if c['command_id'].startswith('FETCH')]}
        except ContractError as exc:
            return {'error':str(exc),'calls':transport.calls,
                    'committed_observations':store.db.execute('select count(*) from observations').fetchone()[0]}

def multipage():
    # Changing only the logical run ID changes capture hashes, not business inputs.
    results=[]
    for i in range(10):
        rows=website(body=HTML.replace(b'</body>',b'<a href="/contact">Contact</a></body>'))
        rows[HOST+'/contact']=response(HOST+'/contact',HTML)
        results.append({'run_id':f'run-{i}',**run_fixture(rows,run=f'run-{i}')})
    return {'cases':results,'failed_cases':sum(r['error'] is not None for r in results)}

def robots_redirect():
    rows=website()
    rows[HOST+'/robots.txt']=response(HOST+'/robots.txt',status=301,headers={'location':HOST+'/policy/robots.txt'})
    rows[HOST+'/policy/robots.txt']=response(HOST+'/policy/robots.txt',b'User-agent: *\nAllow: /',headers={'content-type':'text/plain'})
    return run_fixture(rows)

def recover_after_rate_limit():
    with temporary_store() as store:
        rows=website(); rows[HOST+'/']=response(HOST+'/',b'Busy',429,{'retry-after':'3600','content-type':'text/plain'})
        transport=FixtureTransport(rows);config=ScanConfig('tenant','acct','run')
        runner(store,transport).scan(HOST,config)
        before=list(transport.calls)
        transport.responses[HOST+'/']=response(HOST+'/',HTML)
        later='2026-09-15T14:00:00Z'
        result=runner(store,transport,at=later).scan(HOST,config)
        return {'cooldown_active':store.cooling_down('tenant',HOST,later),
                'calls_before':before,'calls_after':transport.calls,'new_attempts':len(transport.calls)-len(before),
                'claim_count':len(result['claims']),'dispositions':result['resource_dispositions']}

def gzip_sitemap():
    rows=website(body=QUIET)
    rows[HOST+'/robots.txt']=response(HOST+'/robots.txt', ('User-agent: *\nAllow: /\nSitemap: '+HOST+'/sitemap.xml.gz').encode(),headers={'content-type':'text/plain'})
    xml=('<urlset><url><loc>'+HOST+'/contact</loc></url></urlset>').encode()
    rows[HOST+'/sitemap.xml.gz']=response(HOST+'/sitemap.xml.gz',gzip.compress(xml,mtime=0),headers={'content-type':'application/gzip'})
    rows[HOST+'/contact']=response(HOST+'/contact',HTML)
    return run_fixture(rows)

def sitemap_priority(*,anchor=False):
    body=QUIET.replace(b'</body>',b'<a href="/contact">Contact</a></body>') if anchor else QUIET
    rows=website(body=body)
    paths=['/blog/a','/blog/b','/privacy','/terms','/contact']
    xml=('<urlset>'+''.join('<url><loc>'+HOST+p+'</loc></url>' for p in paths)+'</urlset>').encode()
    rows[HOST+'/sitemap.xml']=response(HOST+'/sitemap.xml',xml,headers={'content-type':'application/xml'})
    for p in paths:rows[HOST+p]=response(HOST+p,HTML if p=='/contact' else QUIET)
    return run_fixture(rows)

def candidate_status():
    rows=[{'id':'imported-calendly','signal':{'value':'calendly','confidence':.99,
            'metadata':{'detector_status':'active_candidate','match':{'scope':['scripts'],
            'operator':'host_equals','patterns':['assets.calendly.com'],'min_matches':1}}}}]
    imported,report=import_donor(rows,{'calendly':'product:calendly'})
    pack=RulePack.compile(imported)
    with temporary_store() as store:
        result=runner(store,FixtureTransport(website()),pack).scan(HOST,ScanConfig('tenant','acct','run'))
        path=store.root/'candidate-rules.json';path.write_text(json.dumps(imported))
        stdout,stderr=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
            rc=cli_main(['claims','--store',str(store.root),'--tenant','tenant','--as-of',AT,'--rules',str(path)])
        query=json.loads(stdout.getvalue())
        return {'automatic_approvals':report['automatic_approvals'],'query_exit':rc,
                'bundle_states':[x['status'] for x in result['claims']],
                'query_states':[x['status'] for x in query],
                'candidate_support_retained':all(x['supporting_match_ids'] for x in query),
                'eligible_support_counts':[len(x['eligible_match_ids']) for x in query]}

def resolved_candidate_queue():
    with temporary_store() as store:
        empty=deepcopy(RAW);empty['rules']=[]
        transport=FixtureTransport(website())
        runner(store,transport,RulePack.compile(empty)).scan(HOST,ScanConfig('tenant','acct','run'))
        before=store.candidates('tenant',1)
        result=runner(store,transport,PACK).replay('tenant','run','replay',AT)
        after=store.candidates('tenant',1)
        return {'before':before,'after':after,'approved_claims':sum(c['status']=='SUPPORTED' for c in result['claims'])}

def multi_account_query():
    with temporary_store() as store:
        for who in ['account:A','account:B']:
            host='https://'+who[-1].lower()+'.example.test'
            runner(store,FixtureTransport(website(host))).scan(host,ScanConfig('tenant',who,who))
        stdout,stderr=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
            rc=cli_main(['claims','--store',str(store.root),'--tenant','tenant','--as-of',AT,'--rules',str(RULE_PATH)])
        records=json.loads(stdout.getvalue())
        return {'exit':rc,'rows':len(records),'keys':sorted(records[0]),
                'distinct_claim_keys':len({r['claim_key'] for r in records}),
                'returned_subject_ids':[r.get('subject_id') for r in records],
                'subjects_remain_in_storage':[json.loads(r[0])['subject_id'] for r in store.db.execute('select payload from observations order by id')]}

def numeric_resolution(*,value=12000.0):
    bundle=Bundle(BASELINE/'canonical')
    first=deepcopy(bundle.row('facts','f.traffic'));second=deepcopy(first)
    second['fact_id']='f.traffic-other-serialization';second['object']['value']=value
    for fact in [first,second]:
        bundle.shape(fact,'Fact')
        bundle.shape(fact['object'],bundle.reg('predicates',fact['predicate_id'])['value_schema'])
    return {'schema_valid':True,'same_claim_identity':claim_key(first)==claim_key(second),
            'values':[first['object']['value'],second['object']['value']],
            'resolution':resolve_claim([first,second],'2026-09-15T12:00:00Z',lambda f,t:True)}

def alias_redirect():
    rows=website();target='https://www.shop.example.test/'
    rows[HOST+'/']=response(HOST+'/',status=301,headers={'location':target})
    rows[target]=response(target,HTML)
    return run_fixture(rows)

def footer_policy():
    rows=website(body=HTML.replace(b'<script',b'<footer><script').replace(b'</script>',b'</script></footer>'))
    return run_fixture(rows)

def multi_page_import():
    with tempfile.TemporaryDirectory(prefix='keensight-poc-import-') as td:
        root=Path(td);(root/'page.html').write_bytes(HTML)
        args=['analyze-file','--html',str(root/'page.html'),'--url',HOST+'/', '--observed-at',AT,
              '--tenant','tenant','--subject','acct','--run','run','--rules',str(RULE_PATH),
              '--store',str(root/'store'),'--output',str(root/'bundle.json')]
        out,err=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
            first=cli_main(args);args[args.index('--url')+1]=HOST+'/contact';second=cli_main(args)
        return {'exits':[first,second],'stderr':err.getvalue()}

def same_origin_page_redirect():
    rows=website();rows[HOST+'/']=response(HOST+'/',status=302,headers={'location':HOST+'/welcome'})
    rows[HOST+'/welcome']=response(HOST+'/welcome',HTML)
    return run_fixture(rows,max_attempts=3)

def unchanged_replay_support():
    with temporary_store() as store:
        transport=FixtureTransport(website());runner(store,transport).scan(HOST,ScanConfig('tenant','acct','run'))
        before=store.stored_claims('tenant',as_of=AT)[0]
        changed=deepcopy(RAW);changed['release_id']='added-unrelated-rule'
        extra=deepcopy(changed['rules'][0]);extra['id']='another-product';extra['patterns']=['unrelated.invalid'];changed['rules'].append(extra)
        updated=RulePack.compile(changed);calls=len(transport.calls)
        runner(store,transport,updated).replay('tenant','run','replay',AT)
        after=store.stored_claims('tenant',as_of=AT)[0]
        return {'observations_before':len(before.observation_ids),'observations_after':len(after.observation_ids),
                'evidence_before':before.evidence_count,'evidence_after':after.evidence_count,
                'matches_before':len(before.supporting_match_ids),'matches_after':len(after.supporting_match_ids),
                'source_groups_after':after.source_group_count,'confidence':after.confidence,
                'additional_network':len(transport.calls)-calls}

PROBES = [
 ('POC-01','BUG',multipage),
 ('POC-02','CAPABILITY_GAP',robots_redirect),
 ('POC-03','RECOVERY_GAP',recover_after_rate_limit),
 ('POC-04','CAPABILITY_GAP',gzip_sitemap),
 ('POC-05','PLANNING_GAP',sitemap_priority),
 ('POC-06','READ_MODEL_INCONSISTENCY',candidate_status),
 ('POC-07','RESEARCH_PROJECTION_STALE',resolved_candidate_queue),
 ('POC-08','READ_MODEL_GAP',multi_account_query),
 ('POC-09','REFERENCE_COMPARATOR_BUG',numeric_resolution),
 ('POLICY-01','EXISTING_SAFETY_POLICY',alias_redirect),
 ('POLICY-02','EXISTING_ATTRIBUTION_POLICY',footer_policy),
 ('SCOPE-01','EXISTING_SINGLE_SNAPSHOT_SCOPE',multi_page_import),
 ('CONTROL-01','PASSING_CONTROL',same_origin_page_redirect),
 ('CONTROL-02','PASSING_CONTROL',lambda:sitemap_priority(anchor=True)),
 ('CONTROL-03','PASSING_CONTROL',lambda:numeric_resolution(value=12000)),
 ('CONTROL-04','PASSING_CONTROL',lambda:numeric_resolution(value=13000)),
 ('CONTROL-05','PASSING_CONTROL',unchanged_replay_support),
]

def main():
    results=[]
    for ident,classification,probe in PROBES:
        try:result=probe(); error=None
        except Exception as exc:result=None;error=f'{type(exc).__name__}: {exc}'
        results.append({'id':ident,'classification':classification,'result':result,'probe_error':error})
        print(f'{ident}: {"executed" if error is None else error}',flush=True)
    dest=ROOT/'reports/poc-probe-results.json';dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(results,indent=2)+'\n')
    return int(any(r['probe_error'] for r in results))

if __name__=='__main__':raise SystemExit(main())
