from copy import deepcopy
from dataclasses import replace
import pytest
from keensight_scrapling.core import ContractError,canonical
from keensight_scrapling.rules import RulePack,match_pages
from keensight_scrapling.claims import observation_candidates,resolve_claims

HTML='<html><script src="https://assets.calendly.com/widget.js"></script><iframe src="https://calendly.com/demo"></iframe></html>'
NOW='2026-09-14T13:00:00Z'

def records(pack,pages):
    hits,_=match_pages(pack,pages)
    obs,links=observation_candidates([p.capture for p in pages],hits)
    return hits,obs,links

def test_same_capture_one_observation_all_four_rule_hits(make_page,pack):
    page=make_page(HTML)
    hits,obs,links=records(pack,[page])
    assert len(hits)==4 and len(obs)==1 and len(links)==4
    view=resolve_claims(obs,hits,links,[page.capture],as_of=NOW)[0]
    assert view.status=='SUPPORTED' and len(view.eligible_match_ids)==3
    assert view.source_group_count==1 and view.confidence is None

def test_alias_is_same_claim(make_page,pack):
    hits,obs,links=records(pack,[make_page(HTML)])
    assert {o.target['product_id'] for o in obs}=={'product:calendly'}

def test_two_pages_two_observations_one_claim_one_source(make_page,pack):
    pages=[make_page(HTML),make_page(HTML,url='https://example.test/contact')]
    hits,obs,links=records(pack,pages)
    views=resolve_claims(obs,hits,links,[p.capture for p in pages],as_of=NOW)
    assert len(obs)==2 and len(views)==1
    assert views[0].capture_count==2 and views[0].source_group_count==1

def test_future_scan_retained_without_adding_corroboration(make_page,pack):
    p1=make_page(HTML)
    p2=make_page(HTML,run='r2',when='2026-09-15T12:00:00Z')
    hits,obs,links=records(pack,[p1,p2])
    old=resolve_claims(obs,hits,links,[p1.capture,p2.capture],as_of=NOW)
    new=resolve_claims(obs,hits,links,[p1.capture,p2.capture],as_of='2026-09-15T13:00:00Z')
    assert old[0].capture_count==1 and new[0].capture_count==2
    assert new[0].source_group_count==1

def test_new_detector_adds_support_not_observation(make_page,pack):
    page=make_page(HTML)
    h1,o1,l1=records(pack,[page])
    raw=deepcopy(pack.raw);extra=deepcopy(raw['rules'][0]);extra['id']='new-overlapping-rule';raw['rules'].append(extra)
    h2,o2,l2=records(RulePack.compile(raw),[page])
    assert o1==o2 and len(h2)==len(h1)+1

def test_retry_is_idempotent_in_database(make_page,pack,store):
    page=make_page(HTML);h,o,l=records(pack,[page])
    for _ in range(3):store.save_findings('t',h,o,l)
    assert store.db.execute('SELECT count(*) FROM observations').fetchone()[0]==1
    assert store.db.execute('SELECT count(*) FROM matches').fetchone()[0]==4
    assert store.db.execute('SELECT count(*) FROM support').fetchone()[0]==4

def test_confidence_never_inflates(make_page,pack):
    raw=deepcopy(pack.raw)
    for i in range(30):
        row=deepcopy(raw['rules'][0]);row['id']=f'overlap-{i}';raw['rules'].append(row)
    page=make_page(HTML);h,o,l=records(RulePack.compile(raw),[page])
    v=resolve_claims(o,h,l,[page.capture],as_of=NOW)[0]
    assert v.confidence is None and v.source_group_count==1 and len(o)==1

def test_candidates_cannot_strengthen_approved_support(make_page,pack):
    raw=deepcopy(pack.raw)
    for r in raw['rules']:r['status']='CANDIDATE'
    page=make_page(HTML);h,o,l=records(RulePack.compile(raw),[page])
    v=resolve_claims(o,h,l,[page.capture],as_of=NOW)[0]
    assert v.status=='CANDIDATE' and not v.eligible_match_ids

def test_approved_support_removal_does_not_upgrade_candidates(make_page,pack):
    page=make_page(HTML);h,o,l=records(pack,[page])
    allowed={r.digest for r in pack.rules if r.status=='CANDIDATE'}
    v=resolve_claims(o,h,l,[page.capture],as_of=NOW,allowed_rule_digests=allowed)[0]
    assert v.status=='CANDIDATE'

def test_reprocessing_does_not_extend_ttl(make_page,pack):
    page=make_page(HTML,ttl=60);h,o,l=records(pack,[page])
    assert o[0].expires_at=='2026-09-14T12:01:00Z'
    assert resolve_claims(o,h,l,[page.capture],as_of=NOW)[0].status=='UNKNOWN'

def test_partial_capture_has_no_eligible_claim(make_page,pack):
    page=make_page(HTML,complete=False);h,o,l=records(pack,[page])
    assert resolve_claims(o,h,l,[page.capture],as_of=NOW)[0].status=='UNKNOWN'

def test_revoked_capture_cannot_support(make_page,pack,store):
    page=make_page(HTML);h,o,l=records(pack,[page]);store.save_findings('t',h,o,l)
    store.revoke('t',page.capture.capture_id,'test revocation')
    assert store.stored_claims('t',as_of=NOW)[0].status=='UNKNOWN'

def test_different_predicates_are_not_merged(make_page,pack):
    raw=deepcopy(pack.raw);r=deepcopy(raw['rules'][0]);r.update(id='mention',predicate='vendor.mentioned');raw['rules'].append(r)
    page=make_page(HTML);h,o,l=records(RulePack.compile(raw),[page])
    assert len(o)==2

def test_different_products_are_not_merged(make_page,pack):
    raw=deepcopy(pack.raw);r=deepcopy(raw['rules'][0]);r.update(id='different',product_id='product:other');raw['rules'].append(r)
    page=make_page(HTML);h,o,l=records(RulePack.compile(raw),[page])
    assert len(o)==2

def test_different_modes_are_not_merged(make_page,pack):
    pages=[make_page(HTML),make_page(HTML,mode='RENDERED_DOM')];h,o,l=records(pack,pages)
    assert len(resolve_claims(o,h,l,[p.capture for p in pages],as_of=NOW))==2

@pytest.mark.parametrize('change',[{'tenant':'other'},{'subject':'account:other'},{'url':'https://other.example.test/'}])
def test_no_cross_boundary_host_pool(make_page,pack,change):
    a=make_page(HTML);b=make_page(HTML,run='r2',**change)
    with pytest.raises(ContractError):match_pages(pack,[a,b])

def test_support_from_wrong_capture_rejected(make_page,pack):
    a=make_page(HTML);b=make_page(HTML,url='https://example.test/contact')
    h,o,l=records(pack,[a,b]);bad=replace(l[0],match_id=next(x.match_id for x in h if x.capture_id!=o[0].capture_id))
    # Bind this deliberately to o[0], independent of sorted link ordering.
    bad=replace(bad,observation_id=o[0].observation_id)
    with pytest.raises(ContractError):resolve_claims(o,h,[bad],[a.capture,b.capture],as_of=NOW)

def test_conflicting_values_remain_visible(make_page,pack):
    a=make_page(HTML);h,o,l=records(pack,[a]);first=o[0]
    # Unit test resolver's general conflicting-value behavior; scanner only emits positives.
    contrary=replace(first,observation_id='other',object_value=False)
    contrary_hit=replace(h[0],match_id='contrary',object_value=False)
    from keensight_scrapling.core import SupportLink
    v=resolve_claims([*o,contrary],[*h,contrary_hit],[*l,SupportLink('other','contrary')],[a.capture],as_of=NOW)[0]
    assert v.status=='CONFLICT' and v.object_value is None

def test_rule_order_is_deterministic(make_page,pack):
    raw=deepcopy(pack.raw);raw['rules'].reverse()
    other=RulePack.compile(raw);assert other.digest==pack.digest
    p=make_page(HTML);assert records(other,[p])==records(pack,[p])
