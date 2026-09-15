"""Explicit POC acceptance tests; failures are intentionally not xfailed.

Several tests specify missing POC capabilities rather than regressions against
an already promised runtime. Consult REPORT.md before counting findings.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import poc_probes as p


def test_poc01_multipage_scan_is_independent_of_run_identity():
    r=p.multipage()
    assert r['failed_cases']==0, [(x['run_id'],x['error']) for x in r['cases'] if x['error']]

def test_poc02_follow_bounded_same_origin_robots_redirect():
    r=p.robots_redirect()
    assert r['claim_count']==1, r

def test_poc03_expired_cooldown_is_not_reported_as_active():
    r=p.recover_after_rate_limit()
    assert not r['cooldown_active']
    assert not any(x['status']=='SKIPPED_RATE_LIMIT' for x in r['dispositions']), r

def test_poc04_support_a_bounded_gzip_sitemap():
    r=p.gzip_sitemap()
    assert p.HOST+'/contact' in r['evaluated_urls'],r

def test_poc05_rank_sitemap_pages_by_declared_business_priority():
    r=p.sitemap_priority()
    assert p.HOST+'/contact' in r['evaluated_urls'],r

def test_poc06_claim_query_distinguishes_current_candidate_from_unknown():
    r=p.candidate_status()
    assert r['automatic_approvals']==0 and r['eligible_support_counts']==[0]
    assert r['query_states']==r['bundle_states']==['CANDIDATE'],r

def test_poc07_known_features_leave_the_unresolved_candidate_queue():
    r=p.resolved_candidate_queue()
    assert r['approved_claims']==1
    assert not r['after'] or all(x.get('status') in {'RESOLVED','HISTORICAL'} for x in r['after']),r

def test_poc08_tenant_wide_claims_include_account_identity():
    r=p.multi_account_query()
    assert set(r['returned_subject_ids'])=={'account:A','account:B'},r

def test_poc09_equal_numeric_measurements_do_not_conflict():
    r=p.numeric_resolution()
    assert r['schema_valid'] and r['same_claim_identity']
    assert r['resolution']['status']=='KNOWN',r

def test_control01_homepage_same_origin_redirect_is_already_supported():
    assert p.same_origin_page_redirect()['claim_count']==1

def test_control02_homepage_contact_link_outranks_sitemap_noise():
    r=p.sitemap_priority(anchor=True)
    assert p.HOST+'/contact' in r['evaluated_urls'] and r['claim_count']==1

def test_control03_identical_integer_measurements_agree():
    assert p.numeric_resolution(value=12000)['resolution']['status']=='KNOWN'

def test_control04_genuinely_different_measurements_conflict():
    assert p.numeric_resolution(value=13000)['resolution']['status']=='CONFLICT'

def test_control05_replay_preserves_observation_and_evidence_counts():
    r=p.unchanged_replay_support()
    assert r['observations_before']==r['observations_after']==1
    assert r['evidence_before']==r['evidence_after']==1
    assert r['source_groups_after']==1 and r['confidence'] is None
    assert r['additional_network']==0
