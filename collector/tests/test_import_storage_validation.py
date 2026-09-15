from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import sqlite3
import pytest
from keensight_scrapling.core import ContractError,strict_json
from keensight_scrapling.importer import read_donor,import_donor
from keensight_scrapling.discovery import sitemap_urls
from keensight_scrapling.cli import demo,main
from keensight_scrapling.validation import validate_bundle


def test_donor_subset_quarantines_composite():
    rows=read_donor(Path(__file__).parents[1]/'examples/donor-shaped.jsonl')
    pack,report=import_donor(rows,{'calendly':'product:calendly'})
    assert report['input_rows']==2 and report['imported_candidates']==1 and report['quarantined_rows']==1
    assert pack['rules'][0]['status']=='CANDIDATE' and pack['rules'][0]['predicate']=='vendor.mentioned'
    assert report['dispositions'][1]['raw']==rows[1]

def test_duplicate_donor_ids_all_quarantined():
    rows=read_donor(Path(__file__).parents[1]/'examples/donor-shaped.jsonl')[:1]
    pack,r=import_donor(rows*2,{'calendly':'product:calendly'})
    assert not pack['rules'] and r['quarantined_rows']==2

def test_no_guessed_vendor_mapping():
    rows=read_donor(Path(__file__).parents[1]/'examples/donor-shaped.jsonl')
    pack,r=import_donor(rows,{})
    assert not pack['rules']

def test_approved_legacy_status_does_not_promote():
    row=read_donor(Path(__file__).parents[1]/'examples/donor-shaped.jsonl')[0]
    row['signal']['metadata']['detector_status']='validated'
    pack,r=import_donor([row],{'calendly':'product:calendly'})
    assert pack['rules'][0]['status']=='CANDIDATE'

@pytest.mark.parametrize('body',[
 b'<!DOCTYPE x [<!ENTITY ex SYSTEM "file:///etc/passwd">]><urlset><url><loc>&ex;</loc></url></urlset>',
 b'<not-a-sitemap/>',b'<broken',
])
def test_unsafe_sitemaps(body):
    with pytest.raises(ContractError):sitemap_urls(body,'https://example.com/sitemap.xml')

def test_sitemap_dedup_scope_and_limits():
    body=b'<urlset><url><loc>https://example.com/a</loc></url><url><loc>https://other.com/b</loc></url><url><loc>https://example.com/a</loc></url><url><loc>https://example.com/b</loc></url></urlset>'
    rows,limited=sitemap_urls(body,'https://example.com/sitemap.xml',max_entries=1)
    assert rows==[('page','https://example.com/a')] and limited

def test_blob_corruption_detected(make_page,store):
    page=make_page('<p>Hello</p>')
    (store.root/page.capture.body_path).write_bytes(b'corrupt')
    with pytest.raises(ContractError):store.body(page.capture)

def test_blob_path_traversal_rejected(make_page,store):
    page=make_page()
    with pytest.raises(ContractError):store.body(replace(page.capture,body_path='../../secrets'))

def test_cross_tenant_revocation_cannot_hit_other_tenant(make_page,store):
    cap=make_page().capture
    with pytest.raises(sqlite3.IntegrityError):store.revoke('other',cap.capture_id,'wrong tenant')

def test_capture_identity_collision_fails(make_page,store):
    a=make_page('<p>A</p>')
    with pytest.raises(ContractError):make_page('<p>B</p>')

def test_repeated_same_bytes_different_capture_history(make_page):
    a=make_page('<p>A</p>');b=make_page('<p>A</p>',run='r2')
    assert a.capture.capture_id!=b.capture.capture_id and a.capture.body_sha256==b.capture.body_sha256

@pytest.fixture
def bundle(tmp_path):
    output=tmp_path/'demo';demo(output)
    return strict_json((output/'scan-bundle.json').read_text())

@pytest.mark.parametrize('mutate',[
 lambda x:x.update(send_allowed=True),
 lambda x:x['matches'][0].update(surface_id='missing'),
 lambda x:x['observations'][0].update(subject_id='other'),
 lambda x:x['support_links'].pop(),
 lambda x:x['claims'][0].update(confidence=0.999),
 lambda x:x['claims'][0].update(source_group_count=99),
 lambda x:x['captures'][0].update(observed_at='tomorrow'),
 lambda x:x['commands'].clear(),
 lambda x:x.update(release_digest='different'),
 lambda x:x['observations'][0].update(expires_at='2099-01-01T00:00:00Z'),
])
def test_bundle_tampering_rejected(bundle,mutate):
    mutate(bundle)
    with pytest.raises(ContractError):validate_bundle(bundle)

def test_demo_cli_and_check(tmp_path):
    assert main(['demo','--output',str(tmp_path/'demo')])==0
    assert main(['check',str(tmp_path/'demo/scan-bundle.json')])==0

def test_commands_cli(capsys):
    assert main(['commands'])==0
    assert len(strict_json(capsys.readouterr().out))==38

def test_candidate_feature_privacy_and_dedup(make_page,store):
    pages=[make_page('<script src="https://unknown.vendor.com/api.js?secret=abcd"></script>'),
           make_page('<script src="https://unknown.vendor.com/api.js"></script>',url='https://example.test/contact'),
           make_page('<script src="https://unknown.vendor.com/api.js"></script>',run='r2',url='https://second.test/')]
    for p in pages:
        store.harvest('t',[p],matched_surface_ids=set())
        store.harvest('t',[p],matched_surface_ids=set())
    rows=store.candidates('t',2)
    assert len(rows)==1 and rows[0]['observed_origin_count']==2 and 'abcd' not in str(rows)
    assert store.candidates('other',1)==[]

def test_original_blob_verification_cli(tmp_path):
    root=tmp_path/'demo';demo(root)
    assert main(['check',str(root/'scan-bundle.json'),'--store',str(root)])==0

def test_analyze_user_snapshot_cli(tmp_path):
    project=Path(__file__).parents[1]
    output=tmp_path/'bundle.json'
    assert main(['analyze-file','--html',str(project/'examples/page.html'),'--url','https://example.test/',
                 '--observed-at','2026-09-14T12:00:00Z','--tenant','t','--subject','a','--run','import1',
                 '--rules',str(project/'examples/demo-rules.json'),'--store',str(tmp_path/'store'),'--output',str(output)])==0
    data=strict_json(output.read_text())
    assert data['captures'][0]['source_id']=='source:user-provided-snapshot'
