from types import SimpleNamespace
import socket
import pytest
from keensight_scrapling.urls import normalize_url,NetworkPolicy
from keensight_scrapling.core import ContractError,PolicyDenied,DependencyUnavailable
from keensight_scrapling.transport import ScraplingTransport,ScraplingBrowserTransport,safe_headers

@pytest.mark.parametrize('raw,expected',[
 ('Example.com','https://example.com/'),('https://EXAMPLE.com:443/A?x=Y#frag','https://example.com/A?x=Y'),
 ('//example.com/a','https://example.com/a'),('https://bücher.example/','https://xn--bcher-kva.example/'),
])
def test_normalization(raw,expected):assert normalize_url(raw)==expected

@pytest.mark.parametrize('raw',[
 'https://user:pass@example.com/','https://example.com\\@127.0.0.1/','file:///etc/passwd','https://example.com/\nfoo',
 'https://example.com:invalid/','https://%31%32%37.0.0.1/','https://bad host.example/','https://.example.com/',
])
def test_unsafe_url_syntax(raw):
    with pytest.raises((ContractError,ValueError)):normalize_url(raw)

@pytest.mark.parametrize('ip',['127.0.0.1','10.0.0.1','169.254.169.254','::1','192.168.1.1','0.0.0.0','224.0.0.1'])
def test_private_dns_rejected(monkeypatch,ip):
    monkeypatch.setattr(socket,'getaddrinfo',lambda *a,**k:[(2,1,6,'',(ip,443))])
    with pytest.raises(PolicyDenied):NetworkPolicy(('https://example.com',)).resolve('https://example.com/')

def test_mixed_dns_addresses_fail_closed(monkeypatch):
    monkeypatch.setattr(socket,'getaddrinfo',lambda *a,**k:[(2,1,6,'',('8.8.8.8',443)),(2,1,6,'',('127.0.0.1',443))])
    with pytest.raises(PolicyDenied):NetworkPolicy(('https://example.com',)).resolve('https://example.com/')

def test_cookie_values_and_sensitive_headers_not_stored():
    result=safe_headers({'Set-Cookie':'session=secret; HttpOnly','Authorization':'secret','Server':'Acme','X-Token':'secret'})
    assert 'secret' not in str(result) and result['x-keensight-cookie-names']=='session'
    assert result['server']=='Acme'

def test_browser_is_disabled_without_reviewed_sandbox():
    with pytest.raises(DependencyUnavailable):ScraplingBrowserTransport().get('https://example.com/')

def test_static_adapter_passes_bounded_controls():
    # Adapter-contract test with fake SDK, NOT an actual Scrapling integration test.
    policy=SimpleNamespace(resolve=lambda url:['8.8.8.8'])
    state={}
    class Session:
        def __init__(self):self._curl_session=SimpleNamespace(curl_options={},trust_env=True)
        def __enter__(self):state['session']=self;return self
        def __exit__(self,*args):pass
        def get(self,url,**kwargs):
            state['kwargs']=kwargs
            kwargs['content_callback'](b'<html></html>')
            return SimpleNamespace(url=url,status=200,body=b'',headers={'content-type':'text/html'})
    reply=ScraplingTransport(policy)._get('https://example.com/',Session,SimpleNamespace(RESOLVE=10203))
    assert reply.body==b'<html></html>'
    assert state['kwargs']['follow_redirects'] is False and state['kwargs']['retries']==1
    assert state['kwargs']['verify'] is True and state['session']._curl_session.trust_env is False
    assert state['session']._curl_session.curl_options[10203]==[b'example.com:443:8.8.8.8']

def test_stream_limit_aborts_without_unbounded_retention():
    class Session:
        def __init__(self):self._curl_session=SimpleNamespace(curl_options={})
        def __enter__(self):return self
        def __exit__(self,*a):pass
        def get(self,url,**kwargs):
            assert kwargs['content_callback'](b'x'*100)==0
            raise RuntimeError('curl aborted')
    reply=ScraplingTransport(SimpleNamespace(resolve=lambda url:['8.8.8.8']),max_bytes=10)._get('https://example.com/',Session,SimpleNamespace(RESOLVE=1))
    assert len(reply.body)==10 and not reply.complete and reply.status_code==0
