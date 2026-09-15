"""Regression reproductions for the September 15 audit; original tests retained."""
from copy import deepcopy
from dataclasses import asdict,replace
import os,sys,subprocess,json
from pathlib import Path
import pytest
from keensight_scrapling.core import ContractError,canonical
from keensight_scrapling.pipeline import Scanner,ScanConfig
from keensight_scrapling.transport import FixtureTransport,FetchResult
from keensight_scrapling.rules import RulePack
from keensight_scrapling.validation import validate_bundle
from keensight_scrapling.importer import import_donor
from keensight_scrapling.cli import demo

AT='2026-09-14T12:00:00Z';URL='https://example.test/'
HTML='<html><script src="https://assets.calendly.com/w.js"></script><p>Content</p></html>'
def runner(store,pack,transport=None):return Scanner(store,pack,transport or FixtureTransport({}),production=False,clock=lambda:AT)
def evaluate(store,pack,page):return runner(store,pack).evaluate([page],'e',AT)

@pytest.mark.parametrize('field,value',[
 ('observed_at','2026-10-14T12:00:00Z'),('headers',{'x-powered-by':'fabricated'}),
 ('source_id','source:forged'),('complete',False),('mode','RENDERED_DOM'),
 ('subject_id','other'),('source_ttl_seconds',999999999),('status_code',201)])
def test_capture_metadata_is_immutable(store,make_page,field,value):
 p=make_page(HTML)
 with pytest.raises(ContractError):store.body(replace(p.capture,**{field:value}))

@pytest.mark.parametrize('cmd',['EXTRACT_SCRIPT_SRC','MATCH_HOST_SUFFIX'])
def test_failed_producer_cannot_keep_success(store,pack,make_page,cmd):
 b=evaluate(store,pack,make_page(HTML))
 for c in b['commands']:
  if c['command_id']==cmd:c['status']='FAILED'
 with pytest.raises(ContractError):validate_bundle(b)

def test_rule_report_checked(store,pack,make_page):
 b=evaluate(store,pack,make_page(HTML));b['rule_evaluations'][0]['status']='ERROR'
 with pytest.raises(ContractError):validate_bundle(b)

def test_invalid_evaluation_does_not_publish(store,pack,make_page):
 p=make_page(HTML)
 with pytest.raises(ContractError):runner(store,pack).evaluate([p,p],'bad',AT)
 assert store.db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]==0
 assert store.db.execute('SELECT COUNT(*) FROM evaluations').fetchone()[0]==0

def test_publication_fault_rolls_back_all_findings(store,pack,make_page,monkeypatch):
 p=make_page(HTML)
 def fail(*a,**k):raise RuntimeError('injected persistence fault')
 monkeypatch.setattr(store,'harvest',fail)
 with pytest.raises(RuntimeError):evaluate(store,pack,p)
 for table in ('matches','observations','support','evaluations','replay_selection'):
  assert store.db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]==0
 assert store.db.execute('SELECT COUNT(*) FROM captures').fetchone()[0]==1

@pytest.mark.parametrize('rejected',[True,False])
def test_original_selection_survives_replay(store,pack,rejected):
 responses={URL:FetchResult(URL,200,HTML.encode(),{})}
 if rejected:responses={URL+'robots.txt':FetchResult(URL+'robots.txt',200,HTML.encode(),{'content-type':'text/html'})}
 r=runner(store,pack,FixtureTransport(responses));b=r.scan(URL,ScanConfig('t','a','run'));p=r.replay('t','run','replay',AT)
 assert b['claims']==p['claims']
 assert bool(b['claims']) is not rejected

def test_incomplete_surface_not_no_match(store,pack,make_page):
 p=make_page('<html>'+'<script src="https://benign.test/x"></script>'*2000+'<script src="https://assets.calendly.com/x"></script></html>')
 b=evaluate(store,pack,p)
 assert next(c for c in b['commands'] if c['command_id']=='EXTRACT_SCRIPT_SRC')['status']=='PARTIAL'
 assert all(r['status'] not in ['NO_MATCH'] for r in b['rule_evaluations'] if 'script' in r['rule_id'])

def test_zero_inputs_are_not_evaluated(store,pack):
 b=runner(store,pack,FixtureTransport({URL+'robots.txt':TimeoutError()})).scan(URL,ScanConfig('t','a','r'))
 assert all(r['status']=='NOT_EVALUATED' for r in b['rule_evaluations'])

def test_cooldown_survives_resume(store,pack):
 t=FixtureTransport({URL:FetchResult(URL,429,b'limited',{'retry-after':'3600'})});r=runner(store,pack,t);c=ScanConfig('t','a','r')
 r.scan(URL,c);n=len(t.calls);r.scan(URL,c);assert len(t.calls)==n
 assert store.cooling_down('t',URL.rstrip('/'),AT)

def test_alias_map_is_part_of_semantic_digest(pack):
 a=deepcopy(pack.raw);a['aliases']={'product:calendly':'product:other'}
 # Use the actual authored product key rather than relying on fixture spellings.
 a['aliases']={a['rules'][0]['product_id']:'product:other'}
 new=RulePack.compile(a)
 assert pack.rules[0].digest!=new.rules[0].digest

def test_charset_is_respected(make_page):
 p=make_page('<html><p>Café résumé</p></html>',headers={'content-type':'text/html; charset=utf-8'})
 assert next(s.value for s in p.surfaces if s.kind=='prose')=='Café résumé'

@pytest.mark.parametrize('script_type',['text/plain','application/json','application/ld+json'])
def test_inert_scripts_do_not_create_presence(store,pack,make_page,script_type):
 b=evaluate(store,pack,make_page(HTML.replace('<script ',f'<script type="{script_type}" ')))
 assert not any(x['status']=='SUPPORTED' and x['predicate']=='vendor.present' for x in b['claims'])

def test_malformed_robots_sitemap_is_a_diagnostic(store,pack):
 t=FixtureTransport({URL+'robots.txt':FetchResult(URL+'robots.txt',200,b'User-agent: *\nAllow: /\nSitemap: javascript:bad',{}),URL:FetchResult(URL,200,HTML.encode(),{'content-type':'text/html'})})
 b=runner(store,pack,t).scan(URL,ScanConfig('t','a','r'))
 assert any(d['status']=='INVALID_DISCOVERY_URL' for d in b['resource_dispositions'])

def test_malformed_donor_id_is_quarantined():
 p,r=import_donor([{'id':[],'signal':{}}],{})
 assert r['quarantined_rows']==1

def test_forged_surface_is_not_published(store,pack,make_page):
 p=make_page('<html><p>Clean</p></html>');fake=make_page(HTML,url=URL+'other')
 p.surfaces=fake.surfaces
 with pytest.raises(ContractError):evaluate(store,pack,p)
 assert store.db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]==0

def test_priority_is_recomputed(store,pack,make_page):
 b=evaluate(store,pack,make_page(HTML));b['priority_score']=99
 for c in b['commands']:
  if c['command_id']=='SCORE_HOST':c['details']['score']=99
 with pytest.raises(ContractError):validate_bundle(b)

def test_independent_process_pipeline(tmp_path):
 out=tmp_path/'demo';d=demo(out);b=json.loads((out/'scan-bundle.json').read_text());cid=b['evaluated_capture_ids'][0]
 def run(*args):
  p=subprocess.run([sys.executable,'-m','keensight_scrapling.standalone',*map(str,args)],capture_output=True,text=True,timeout=20,env={**os.environ,'PYTHONPATH':str(Path(__file__).parents[1]/'src')})
  assert p.returncode==0,p.stderr
  assert json.loads(p.stdout)['network_attempts']==0
 page=tmp_path/'page.json';match=tmp_path/'match.json';claims=tmp_path/'claims.json'
 run('extract','--capture-id',cid,'--tenant','demo','--store',out,'--output',page)
 run('match','--page',page,'--rules',Path(__file__).parents[1]/'examples/demo-rules.json','--store',out,'--output',match)
 run('resolve','--bundle',out/'scan-bundle.json','--as-of',AT,'--store',out,'--output',claims)
 assert json.loads(match.read_text())['matches']
 assert json.loads(claims.read_text())['claims']==b['claims']
