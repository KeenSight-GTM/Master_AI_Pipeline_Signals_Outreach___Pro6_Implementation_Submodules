from keensight_scrapling.extraction import EXTRACTORS,extract
from pathlib import Path
import pytest


def test_all_17_extractors_run(make_page):
    p=make_page(Path(__file__).parents[1].joinpath('examples/page.html').read_text())
    assert len(p.commands)==17
    assert {r.command_id for r in p.commands}==set(EXTRACTORS)
    assert all(r.status=='COMPLETE' for r in p.commands)

@pytest.mark.parametrize('command',EXTRACTORS)
def test_each_extractor_has_explicit_result_on_empty_page(make_page,command):
    p=make_page('<html></html>')
    r=next(r for r in p.commands if r.command_id==command)
    assert r.status=='COMPLETE' and r.input_ids==[p.capture.capture_id]

def test_comments_do_not_create_script_nodes(make_page):
    p=make_page('<!-- <script src="https://assets.calendly.com/a.js"></script> -->')
    assert not [s for s in p.surfaces if s.kind=='script_url']

def test_protocol_relative_and_whitespace_attributes(make_page):
    p=make_page('<script src = "//assets.calendly.com/a.js"></script><div data-x = "y"></div>')
    assert any(s.kind=='script_url' and s.value=='https://assets.calendly.com/a.js' for s in p.surfaces)
    assert any(s.kind=='attribute' and s.attributes['name']=='data-x' and s.value=='y' for s in p.surfaces)

def test_image_alt_stays_with_its_image(make_page):
    p=make_page('<img src="/a" alt="first"><img src="/b" alt="second">')
    assert [(s.value,s.attributes['alt']) for s in p.surfaces if s.kind=='image']==[('https://example.test/a','first'),('https://example.test/b','second')]

def test_full_jsonld_graph_retained(make_page):
    p=make_page('<script type="application/ld+json">{"@graph":[{"@id":"x","@type":"Organization","name":"Test"}]}</script>')
    s=next(s for s in p.surfaces if s.kind=='jsonld')
    assert s.attributes['parsed']['@graph'][0]['name']=='Test'
    assert s.attributes['types']==['Organization']

def test_invalid_jsonld_is_partial_not_absence(make_page):
    p=make_page('<script type="application/ld+json">{bad}</script>')
    r=next(r for r in p.commands if r.command_id=='EXTRACT_JSONLD')
    assert r.status=='PARTIAL' and 'JSONLD_PARSE_ERROR' in r.limitations

def test_duplicate_json_keys_rejected(make_page):
    p=make_page('<script type="application/ld+json">{"name":"x","name":"y"}</script>')
    s=next(s for s in p.surfaces if s.kind=='jsonld')
    assert 'Duplicate JSON key' in s.attributes['parse_error']

def test_footer_context_survives(make_page):
    p=make_page('<footer><script src="https://vendor.example/a.js"></script></footer>')
    assert next(s for s in p.surfaces if s.kind=='script_url').context=='FOOTER'

def test_external_base_is_evidence_not_crawl_permission(make_page):
    p=make_page('<base href="https://external.example/"><a href="contact">go</a>')
    assert next(s for s in p.surfaces if s.kind=='anchor_url').value=='https://external.example/contact'

def test_query_values_not_in_research_url_features(make_page):
    p=make_page('<script src="/a.js?secret=abc"></script>')
    s=next(s for s in p.surfaces if s.kind=='url_features')
    assert 'abc' not in s.value and s.attributes['query_keys']==['secret']

def test_extraction_limits_are_explicit(make_page):
    page=make_page('<div>'+'x'*200+'</div>')
    short=extract(page.capture,b'<div>'+b'x'*200+b'</div>',max_text=30)
    assert any(r.status=='PARTIAL' and 'TEXT_LIMIT' in r.limitations for r in short.commands)

def test_no_script_text_in_prose(make_page):
    page=make_page('<script>secret()</script><p>Hello</p>')
    text=next(s.value for s in page.surfaces if s.kind=='prose')
    assert text=='Hello'
