from pathlib import Path
import json
import pytest
from keensight_scrapling.storage import Store
from keensight_scrapling.rules import RulePack
from keensight_scrapling.extraction import extract

@pytest.fixture
def pack():
    return RulePack.load(Path(__file__).parents[1]/'examples/demo-rules.json')

@pytest.fixture
def store(tmp_path):
    s=Store(tmp_path/'store')
    yield s
    s.close()

@pytest.fixture
def make_page(store):
    def make(body='<html></html>',*,tenant='t',subject='account:a',run='r',url='https://example.test/',
             mode='RAW_HTML',when='2026-09-14T12:00:00Z',complete=True,headers=None,ttl=2592000):
        store.begin_run(tenant,run,{'purpose':'TEST_FIXTURE','run':run})
        cap=store.put_capture(tenant_id=tenant,subject_id=subject,run_id=run,url=url,observed_at=when,
                              body=body.encode(),headers=headers or {'content-type':'text/html'},mode=mode,
                              complete=complete,source_ttl_seconds=ttl)
        return extract(cap,body.encode())
    return make
