from copy import deepcopy
import pytest
from keensight_scrapling.rules import RulePack,match_pages
from keensight_scrapling.core import ContractError

@pytest.mark.parametrize('url,expected',[
 ('https://assets.calendly.com/a.js',True),('//assets.calendly.com/a.js',True),
 ('https://calendly.com/a.js',True),('https://evilcalendly.com/a.js',False),
 ('https://calendly.com.evil.example/a.js',False),('https://evil.example/calendly.com/a.js',False),
 ('https://evil.example/?x=calendly.com',False),('https://CALENDLY.COM/a.js',True),
])
def test_precise_host_matching(pack,make_page,url,expected):
    p=make_page(f'<script src="{url}"></script>')
    h,_=match_pages(pack,[p]);assert bool(h)==expected

@pytest.mark.parametrize('html',[
 '<footer><script src="https://assets.calendly.com/a.js"></script></footer>',
 '<template><script src="https://assets.calendly.com/a.js"></script></template>',
 '<p><a href="https://calendly.com">A blog mentioning Calendly</a></p>',
 '<!-- <iframe src="https://calendly.com/acme"></iframe> -->',
 '<p>script src="https://assets.calendly.com/a.js"</p>',
])
def test_weak_surfaces_do_not_establish_presence(pack,make_page,html):
    assert match_pages(pack,[make_page(html)])[0]==[]

@pytest.mark.parametrize('mutation',[
 lambda p:p['rules'].append(deepcopy(p['rules'][0])),
 lambda p:p['rules'][0].update(operator='eval'),
 lambda p:p['rules'][0].update(patterns=[]),
 lambda p:p['rules'][0].update(status='active_candidate'),
 lambda p:p['rules'][0].update(confidence=2),
 lambda p:p['rules'][0].update(predicate='unregistered'),
 lambda p:p['rules'][0].update(review=None),
 lambda p:p['rules'][0].update(kinds=['raw_html'],operator='contains'),
 lambda p:p.update(aliases={'a':'b','b':'a'}),
 lambda p:p.update(unexpected=True),
])
def test_invalid_catalog_fails_closed(pack,mutation):
    p=deepcopy(pack.raw);mutation(p)
    with pytest.raises(ContractError):RulePack.compile(p)

@pytest.mark.parametrize('op,kind,pat,field,html',[
 ('contains','raw_html','Example','value','<p>Example</p>'),
 ('equals','meta','Test','value','<meta name="generator" content="Test">'),
 ('regex','prose',r'Ex[a-z]+','value','<p>Example</p>'),
 ('footer_literal','footer','Agency','value','<footer>Agency</footer>'),
 ('image_alt','image','Member','value','<img src="/b" alt="Member">'),
])
def test_operator_handlers(pack,make_page,op,kind,pat,field,html):
    p=deepcopy(pack.raw);r=p['rules'][0];r.update(id='x',predicate='vendor.mentioned',operator=op,kinds=[kind],patterns=[pat],field=field);p['rules']=[r]
    assert len(match_pages(RulePack.compile(p),[make_page(html)])[0])==1

def test_or_keeps_all_branches(pack,make_page):
    p=deepcopy(pack.raw);r=p['rules'][0];r.update(predicate='vendor.mentioned',operator='contains',kinds=['prose'],patterns=['one','two']);p['rules']=[r]
    h,_=match_pages(RulePack.compile(p),[make_page('<p>one two</p>')])
    assert {m.branch for m in h}=={'one','two'}

def test_vertical_guard_does_not_delete_vendor_detection(pack,make_page):
    p=deepcopy(pack.raw)
    for r in p['rules']:r['guard_terms']=['family law']
    h,e=match_pages(RulePack.compile(p),[make_page('<script src="https://assets.calendly.com/w.js"></script>')])
    assert h and all(x['qualification']=='UNQUALIFIED' for x in e)

def test_guards_can_use_second_same_host_page(pack,make_page):
    p=deepcopy(pack.raw)
    for r in p['rules']:r['guard_terms']=['family law']
    pages=[make_page('<script src="https://assets.calendly.com/w.js"></script>'),make_page('<p>family law</p>',url='https://example.test/services')]
    h,e=match_pages(RulePack.compile(p),pages)
    assert h and all(x['qualification']=='QUALIFIED' for x in e)

def test_fixture_pack_rejected_for_production(pack,make_page):
    with pytest.raises(ContractError):match_pages(pack,[make_page()],production=True)

def test_invalid_regex_is_rejected(pack):
    p=deepcopy(pack.raw);p['rules'][0].update(predicate='vendor.mentioned',operator='regex',patterns=['['])
    with pytest.raises(ContractError):RulePack.compile(p)

def test_guards_changing_do_not_change_raw_match_identity(pack,make_page):
    raw=deepcopy(pack.raw)
    for r in raw['rules']:r['guard_terms']=['family law']
    p=RulePack.compile(raw)
    a=make_page('<script src="https://assets.calendly.com/w.js"></script>')
    b=make_page('<p>family law</p>',url='https://example.test/services')
    first,_=match_pages(p,[a]);second,_=match_pages(p,[a,b])
    assert first==second

def test_regex_timeout_does_not_publish_successful_partial_hits(pack,make_page):
    raw=deepcopy(pack.raw);r=raw['rules'][0]
    r.update(predicate='vendor.mentioned',operator='regex',kinds=['prose'],patterns=['a','(a+)+$'])
    raw['rules']=[r]
    hits,evaluations=match_pages(RulePack.compile(raw),[make_page('<p>'+'a'*15000+'!</p>')])
    assert evaluations[0]['status']=='ERROR' and not hits
