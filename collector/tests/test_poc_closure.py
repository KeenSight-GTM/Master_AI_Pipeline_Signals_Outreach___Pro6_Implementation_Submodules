"""Non-vacuous regressions for the POC/iteration-2 fixes. No network required."""
from dataclasses import asdict
import copy
import gzip
import pytest
from keensight_scrapling.core import ContractError,canonical
from keensight_scrapling.pipeline import Scanner,ScanConfig
from keensight_scrapling.storage import Store
from keensight_scrapling.transport import FixtureTransport,FetchResult
from keensight_scrapling.discovery import sitemap_urls
from keensight_scrapling.validation import validate_bundle
from keensight_scrapling.extraction import extract

URL='https://example.test/'
AT='2026-09-14T12:00:00Z'
BODY=b'<html><script src="https://assets.calendly.com/widget.js"></script></html>'

def response(url,status=200,body=BODY,**headers):
    return FetchResult(url,status,body,{'content-type':'text/html',**headers})

def test_retry_is_explicit_linked_and_bounded(store,pack):
    transport=FixtureTransport({URL+'robots.txt':response(URL+'robots.txt',404,b''),
                               URL:response(URL,429,b'',**{'retry-after':'3600'})})
    clock=[AT]
    runner=Scanner(store,pack,transport,production=False,clock=lambda:clock[0])
    config=ScanConfig('t','a','retry',max_attempts=8)
    runner.scan(URL,config)
    clock[0]='2026-09-14T14:00:00Z'
    # Same inputs are retained by default. No fake active cooldown is reported.
    original=store.db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]
    result=runner.scan(URL,config)
    assert not any(x['status']=='SKIPPED_RATE_LIMIT' for x in result['resource_dispositions'])
    # Explicit GET recovery creates a new linked attempt, never rewrites a 429.
    transport.responses[URL]=response(URL)
    recovered=runner.scan(URL,ScanConfig('t','a','retry',max_attempts=8,retry_failed=True))
    assert any(c['status']=='SUPPORTED' for c in recovered['claims'])
    attempts=[__import__('json').loads(r['payload']) for r in store.db.execute('SELECT payload FROM attempts')]
    retries=[a for a in attempts if a.get('retry_of')]
    assert len(retries)==1 and retries[0]['attempt_ordinal']==2
    assert all(a.get('started_at') and a.get('finished_at') and a.get('command_id') for a in attempts)
    assert any(a.get('http_status')==429 for a in attempts)
    calls=len(transport.calls)
    runner.scan(URL,ScanConfig('t','a','retry',max_attempts=8,retry_failed=True))
    assert len(transport.calls)==calls
    assert len(attempts)<=8

def test_active_cooldown_prevents_even_explicit_retry(store,pack):
    transport=FixtureTransport({URL+'robots.txt':response(URL+'robots.txt',404,b''),
                               URL:response(URL,429,b'',**{'retry-after':'3600'})})
    runner=Scanner(store,pack,transport,production=False,clock=lambda:AT)
    runner.scan(URL,ScanConfig('t','a','rate'))
    calls=len(transport.calls)
    result=runner.scan(URL,ScanConfig('t','a','rate',retry_failed=True))
    assert len(transport.calls)==calls
    assert any(r['status']=='SKIPPED_RATE_LIMIT' for r in result['resource_dispositions'])

@pytest.mark.parametrize('target',[URL+'robots.txt','https://other.test/robots.txt','http://127.0.0.1/robots.txt'])
def test_robots_loop_and_cross_origin_fail_closed(store,pack,target):
    transport=FixtureTransport({URL+'robots.txt':response(URL+'robots.txt',302,b'',location=target)})
    result=Scanner(store,pack,transport,production=False,clock=lambda:AT).scan(URL,ScanConfig('t','a','robots'))
    assert not result['claims']
    assert transport.calls==[URL+'robots.txt']

@pytest.mark.parametrize('body',[gzip.compress(b'x'*200),b'\x1f\x8btruncated'])
def test_gzip_limits_and_invalid_streams_are_explicit(body):
    with pytest.raises(ContractError):sitemap_urls(body,URL,max_decoded_bytes=100)

def test_gzip_and_plain_xml_produce_identical_ranked_urls():
    body=b'<urlset><url><loc>https://example.test/blog/a</loc></url><url><loc>https://example.test/contact</loc></url></urlset>'
    assert sitemap_urls(body,URL)==sitemap_urls(gzip.compress(body),URL)
    assert sitemap_urls(body,URL)[0][0][1].endswith('/contact')

def test_parser_depth_loss_is_partial_not_absence(make_page,store,pack):
    page=make_page('<html>'+('<div>'*400)+BODY.decode()+('</div>'*400)+'</html>')
    report=next(c for c in page.commands if c.command_id=='EXTRACT_SCRIPT_SRC')
    assert report.status=='PARTIAL' and 'PARSER_RECOVERY_LOSS' in report.limitations
    result=Scanner(store,pack,FixtureTransport({}),production=False).evaluate([page],'e',AT)
    assert not any(r['status']=='NO_MATCH' for r in result['rule_evaluations'] if 'script' in r['rule_id'])

def test_one_authoritative_publication_input(make_page,store,pack):
    page=make_page(BODY.decode())
    b=Scanner(store,pack,FixtureTransport({}),production=False).evaluate([page],'e',AT)
    store.publish_evaluation(b,[page],[],[],[])  # legacy lists cannot change payload
    assert store.db.execute('SELECT COUNT(*) FROM observations').fetchone()[0]==len(b['observations'])
    assert store.db.execute('SELECT COUNT(*) FROM support').fetchone()[0]==len(b['support_links'])

def test_zero_capture_evaluation_is_identified_and_persisted(store,pack):
    b=Scanner(store,pack,FixtureTransport({URL+'robots.txt':TimeoutError('fixture')}),production=False,clock=lambda:AT).scan(URL,ScanConfig('t','a','failed'))
    assert (b['tenant_id'],b['subject_id'],b['capture_run_id'])==('t','a','failed')
    assert b['captures']==[] and b['observations']==[]
    assert store.db.execute('SELECT COUNT(*) FROM evaluations').fetchone()[0]==1

def test_duplicate_terminal_invocation_rejected(make_page,store,pack):
    b=Scanner(store,pack,FixtureTransport({}),production=False).evaluate([make_page(BODY.decode())],'e',AT)
    c=copy.deepcopy(next(c for c in b['commands'] if c['command_id']=='MATCH_HOST_SUFFIX'))
    c['status']='FAILED';c['output_ids']=[];b['commands'].append(c)
    with pytest.raises(ContractError,match='Duplicate command invocation'):validate_bundle(b)

def test_research_view_is_release_and_revocation_aware(make_page,store,pack):
    from keensight_scrapling.rules import RulePack
    page=make_page(BODY.decode());raw=copy.deepcopy(pack.raw);raw['rules']=[]
    unknown=RulePack.compile(raw)
    Scanner(store,unknown,FixtureTransport({}),production=False).evaluate([page],'unknown',AT)
    assert store.candidates('t',1,as_of=AT)
    Scanner(store,pack,FixtureTransport({}),production=False).replay('t','r','known',AT)
    assert not store.candidates('t',1,as_of=AT)
    assert store.candidates('t',1,release_digest=unknown.digest,as_of=AT)
    assert all(x['status']=='RESOLVED' for x in store.candidates('t',1,include_resolved=True,as_of=AT))
    store.revoke('t',page.capture.capture_id,'fixture restriction')
    assert not store.candidates('t',1,as_of=AT)
    assert all(x['status']=='HISTORICAL' and x['capture_count']==0 for x in store.candidates('t',1,include_resolved=True,as_of=AT))

def test_claim_filter_keeps_identity_and_scope(make_page,store,pack):
    runner=Scanner(store,pack,FixtureTransport({}),production=False)
    for subject,run in [('account:a','a'),('account:b','b')]:
        runner.evaluate([make_page(BODY.decode(),subject=subject,run=run)],run,AT)
    rows=store.stored_claims('t',as_of=AT,subject_id='account:a')
    assert rows and all(v.subject_id=='account:a' and v.tenant_id=='t' and v.scope_id and v.origins and v.observed_at for v in rows)
    assert store.stored_claims('other',as_of=AT)==[]
