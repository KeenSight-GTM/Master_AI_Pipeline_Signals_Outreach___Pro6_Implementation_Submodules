from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlsplit
from .core import DependencyUnavailable, PolicyDenied
from .urls import NetworkPolicy, normalize_url


@dataclass(frozen=True)
class FetchResult:
    url: str
    status_code: int
    body: bytes
    headers: dict[str,str]
    complete: bool = True
    mode: str = 'RAW_HTML'
    limitations: tuple[str,...] = ()


class Transport(Protocol):
    def get(self,url: str) -> FetchResult: ...


def safe_headers(headers) -> dict[str,str]:
    values={}
    # Never persist cookie values, auth credentials or arbitrary response tokens.
    allowed={'content-type','server','x-powered-by','x-generator','content-security-policy','content-language','location','retry-after','link','cache-control','last-modified','etag'}
    cookie_names=set()
    try:
        items=headers.multi_items() if hasattr(headers,'multi_items') else headers.items()
    except AttributeError:
        items=[]
    for key,value in items:
        key=str(key).lower(); value=str(value)
        if key=='set-cookie':
            cookie_names.update(re.findall(r'(?:^|,\s*)([!#$%&\'*+\-.^_`|~0-9A-Za-z]+)=',value))
        elif key in allowed:
            values[key]=value[:8192]
        else:
            values[key]='[REDACTED]'
    if cookie_names:
        values['x-keensight-cookie-names']=','.join(sorted(cookie_names))
    return values


class ScraplingTransport:
    """Scrapling 0.4.15 session; one checked, DNS-pinned HTTP request per call.

    This uses the pinned release's private _curl_session extension point to
    set libcurl RESOLVE and disable environment proxies. Fail closed if that
    contract changes. Integration tests must run before upgrading Scrapling.
    No silent replacement with requests/urllib occurs when dependencies are absent.
    """
    def __init__(self,policy: NetworkPolicy,*,max_bytes: int=2_000_000,timeout: float=20.0):
        self.policy=policy; self.max_bytes=max_bytes; self.timeout=timeout

    def get(self,url: str) -> FetchResult:
        try:
            from scrapling.fetchers import FetcherSession
            from importlib.metadata import version
            from curl_cffi.const import CurlOpt
        except ImportError as exc:
            raise DependencyUnavailable('Install the live extra: pip install -e ".[live]"') from exc
        if version('scrapling')!='0.4.15':
            raise DependencyUnavailable('This adapter is pinned to Scrapling 0.4.15; characterize other versions first')
        return self._get(url,FetcherSession,CurlOpt)

    def _get(self,url,session_factory,curl_options) -> FetchResult:
        url=normalize_url(url)
        addresses=self.policy.resolve(url)
        p=urlsplit(url); address=addresses[0]
        address=f'[{address}]' if ':' in address else address
        resolve=f'{p.hostname}:{p.port or (443 if p.scheme=="https" else 80)}:{address}'
        chunks=bytearray(); overflow=False
        def consume(chunk):
            nonlocal overflow
            room=self.max_bytes-len(chunks)
            chunks.extend(chunk[:max(0,room)])
            if len(chunk)>room:
                overflow=True
                return 0  # libcurl abort: do not download an unbounded body
            return len(chunk)
        with session_factory() as session:
            curl=getattr(session,'_curl_session',None)
            if curl is None or not hasattr(curl,'curl_options'):
                raise DependencyUnavailable('Pinned Scrapling curl extension point is unavailable')
            curl.trust_env=False
            curl.curl_options[curl_options.RESOLVE]=[resolve.encode()]
            try:
                response=session.get(url,timeout=self.timeout,retries=1,retry_delay=0,
                                     follow_redirects=False,verify=True,impersonate=None,stealthy_headers=False,
                                     headers={'User-Agent':'KeenSightResearch/0.1','Accept':'text/html,application/xhtml+xml,application/xml,text/plain;q=0.9'},
                                     content_callback=consume,selector_config={'adaptive':False})
            except Exception:
                if overflow:
                    return FetchResult(url,0,bytes(chunks),{},False,limitations=('BODY_LIMIT_ABORTED',))
                raise
            body=bytes(chunks) if chunks else bytes(getattr(response,'body',b'') or b'')
            if len(body)>self.max_bytes:
                body=body[:self.max_bytes]; overflow=True
            final=normalize_url(str(response.url))
            if final!=url:
                raise PolicyDenied('Transport followed an unbudgeted redirect')
            return FetchResult(final,int(response.status),body,safe_headers(response.headers),not overflow,
                               limitations=('BODY_LIMIT_ABORTED',) if overflow else ())


class FixtureTransport:
    is_fixture = True
    """Explicitly synthetic transport for deterministic end-to-end tests/demo."""
    def __init__(self,responses: dict[str,FetchResult | Exception]):
        self.responses=responses; self.calls=[]
    def get(self,url):
        self.calls.append(url)
        value=self.responses.get(url,FetchResult(url,404,b'Not found',{'content-type':'text/plain'}))
        if isinstance(value,Exception): raise value
        return value


class ScraplingBrowserTransport:
    """Optional rendering hook. Requires reviewed external network isolation.

    Browser DNS, redirects, WebSockets and subresources need an enforced egress
    boundary. A Python DNS preflight alone is NOT that boundary. The default
    refuses public browser use; the caller must supply a reviewed sandbox adapter.
    """
    def __init__(self,render_adapter=None):
        self.render_adapter=render_adapter
    def get(self,url):
        if self.render_adapter is None:
            raise DependencyUnavailable('Browser transport disabled until a bounded egress-isolated Scrapling renderer is configured')
        response=self.render_adapter(url)
        if not isinstance(response,FetchResult) or response.mode!='RENDERED_DOM':
            raise DependencyUnavailable('Renderer must return an explicit rendered capture')
        return response
