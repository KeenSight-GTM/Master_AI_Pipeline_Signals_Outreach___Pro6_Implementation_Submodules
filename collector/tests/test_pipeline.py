from pathlib import Path
from copy import deepcopy
import pytest
from keensight_scrapling.cli import demo
from keensight_scrapling.core import ContractError,strict_json
from keensight_scrapling.transport import FixtureTransport,FetchResult
from keensight_scrapling.pipeline import Scanner,ScanConfig
from keensight_scrapling.commands import COMMANDS
from keensight_scrapling.rules import RulePack

ROOT='https://example.test'
WHEN='2026-09-14T12:00:00Z'
HTML=b'<html><script src="https://assets.calendly.com/w.js"></script><p>This is a useful website with several sentences of real copy.</p></html>'

def response(url,body=HTML,code=200,ct='text/html',complete=True,headers=None):
    return FetchResult(url,code,body,headers or {'content-type':ct},complete)

def transport(extra=None):
    rows={ROOT+'/robots.txt':response(ROOT+'/robots.txt',b'User-agent: *\nDisallow: /private',ct='text/plain'),ROOT+'/':response(ROOT+'/')}
    rows.update(extra or {})
    return FixtureTransport(rows)

def runner(store,pack,t):return Scanner(store,pack,t,clock=lambda:WHEN,production=False)

def test_full_demo_deduplicates_and_validates(tmp_path):
    result=demo(tmp_path/'demo')
    assert result['matches']==7 and result['observations']==2 and result['claims']==1
    data=strict_json(Path(result['bundle']).read_text())
    assert len(data['claims'][0]['eligible_match_ids'])==5
    assert data['claims'][0]['evidence_count']==3
    assert set(x['command_id'] for x in data['commands'])==set(COMMANDS)

def test_resume_does_not_refetch(store,pack):
    t=transport();r=runner(store,pack,t);cfg=ScanConfig('t','a','r')
    one=r.scan(ROOT,cfg);calls=len(t.calls);two=r.scan(ROOT,cfg)
    assert len(t.calls)==calls and one['matches']==two['matches'] and one['claims']==two['claims']

def test_budget_counts_404_failures(store,pack):
    t=transport();cfg=ScanConfig('t','a','r',max_attempts=3,probe_paths=True)
    data=runner(store,pack,t).scan(ROOT,cfg)
    assert len(t.calls)==3
    assert any(x['status']=='SKIPPED_BUDGET' for x in data['resource_dispositions'])

def test_failed_robots_prevents_content_fetch(store,pack):
    t=transport({ROOT+'/robots.txt':TimeoutError('offline')})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert t.calls==[ROOT+'/robots.txt'] and not data['observations']
    assert any(x['status']=='FAILED' for x in data['commands'])

def test_robots_html_challenge_fails_closed(store,pack):
    t=transport({ROOT+'/robots.txt':response(ROOT+'/robots.txt',b'<!doctype html><title>challenge</title>')})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert t.calls==[ROOT+'/robots.txt'] and not data['claims']

def test_disallowed_paths_never_fetched(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',HTML.replace(b'</html>',b'<a href="/private">private</a></html>'))})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert ROOT+'/private' not in t.calls
    assert any(x['status']=='SKIPPED_POLICY' for x in data['resource_dispositions'])

def test_429_does_not_invoke_browser(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',b'rate limit',429)})
    class Never:
        def get(self,url):raise AssertionError('must not render a rate-limited URL')
    r=runner(store,pack,t);r.browser=Never()
    data=r.scan(ROOT,ScanConfig('t','a','r',render_empty_shell=True))
    assert not data['matches'] and len(t.calls)==2

def test_redirects_consume_budget_and_are_checked(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',b'',302,headers={'location':ROOT+'/new'}),ROOT+'/new':response(ROOT+'/new')})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r',max_attempts=3))
    assert t.calls==[ROOT+'/robots.txt',ROOT+'/',ROOT+'/new'] and data['matches']

def test_cross_origin_redirect_not_followed(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',b'',302,headers={'location':'http://127.0.0.1/private'})})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert all('127.0.0.1' not in u for u in t.calls) and not data['matches']

def test_cross_origin_canonical_does_not_rebind(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',HTML+b'<link rel="canonical" href="https://other.test/">')})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert all(o['subject_id']=='a' for o in data['observations'])
    assert all('other.test' not in u for u in t.calls)

def test_partial_body_not_interpreted_as_absence(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',HTML,complete=False)})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert not data['observations'] and data['handoff']['absence_facts_emitted'] is False

def test_challenge_not_matched_on_scan_or_replay(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',b'<title>Just a moment</title>'+HTML)})
    r=runner(store,pack,t);one=r.scan(ROOT,ScanConfig('t','a','r'));two=r.replay('t','r','replay','2026-09-14T13:00:00Z')
    assert not one['matches'] and not two['matches']

def test_same_run_changed_pack_fails(store,pack):
    t=transport();runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    raw=deepcopy(pack.raw);raw['release_id']='changed'
    with pytest.raises(ContractError):runner(store,RulePack.compile(raw),t).scan(ROOT,ScanConfig('t','a','r'))

def test_replay_new_rule_preserves_observation_identity(store,pack):
    t=transport();one=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'));calls=len(t.calls)
    raw=deepcopy(pack.raw);row=deepcopy(next(r for r in raw['rules'] if r['id']=='calendly-script-exact'));row['id']='extra';raw['rules'].append(row)
    two=runner(store,RulePack.compile(raw),t).replay('t','r','replay','2026-09-14T13:00:00Z')
    assert len(t.calls)==calls and one['observations']==two['observations']
    assert len(two['matches'])==len(one['matches'])+1

def test_pending_attempt_does_not_silently_repeat(store,pack):
    from dataclasses import asdict
    from keensight_scrapling.core import identity
    cfg=ScanConfig('t','a','r')
    store.begin_run('t','r',{**asdict(cfg),'seed':ROOT+'/','release_digest':pack.digest,'code_version':__import__('keensight_scrapling').__version__})
    store.reserve_attempt('t','r',identity('request',ROOT+'/robots.txt','RAW_HTML'),8,{'started_at':WHEN})
    t=transport();data=runner(store,pack,t).scan(ROOT,cfg)
    assert not t.calls and not data['observations']

def test_negative_priority_does_not_delete_facts(store,pack):
    t=transport({ROOT+'/':response(ROOT+'/',HTML+b'<p>marketing agency</p>')})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert data['priority_score']==0 and data['claims'][0]['status']=='SUPPORTED'

def test_large_robots_delay_is_not_ignored(store,pack):
    t=transport({ROOT+'/robots.txt':response(ROOT+'/robots.txt',b'User-agent: *\nCrawl-delay: 999',ct='text/plain')})
    data=runner(store,pack,t).scan(ROOT,ScanConfig('t','a','r'))
    assert len(t.calls)==1 and not data['observations']
    assert any('ROBOTS_DELAY_EXCEEDS_BATCH_WAIT_POLICY' in x['limitations'] for x in data['commands'])

def test_fixture_only_production_fails_before_fetch(store,pack):
    t=transport()
    with pytest.raises(ContractError):Scanner(store,pack,t)
    assert not t.calls
