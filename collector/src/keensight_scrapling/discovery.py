from __future__ import annotations

from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from defusedxml.ElementTree import fromstring
from .core import ContractError
from .urls import normalize_url,origin,link_url

TEMPLATES=('contact','about','services','locations','booking','schedule','careers','jobs','shop','products','patient-portal','client-portal','pricing','integrations')
WELL_KNOWN=('/llms.txt','/contact','/about','/careers','/book','/locations')


def robots_policy(url: str,code: int,body: bytes,complete: bool) -> tuple[RobotFileParser | None,list[str],str]:
    parser=RobotFileParser(url)
    if code in {404,410}:
        parser.parse([]); return parser,[],'NO_ROBOTS_FILE'
    if code!=200 or not complete or body.lstrip().lower().startswith((b'<html',b'<!doctype html')):
        return None,[],'ROBOTS_UNAVAILABLE_FAIL_CLOSED'
    parser.parse(body.decode('utf-8',errors='replace').splitlines())
    return parser,parser.site_maps() or [],'ROBOTS_PARSED'


def sitemap_urls(body: bytes,base: str,*,max_entries: int=5000,max_decoded_bytes: int=8_000_000) -> tuple[list[tuple[str,str]],bool]:
    if max_entries < 1 or max_decoded_bytes < 1:
        raise ContractError('Sitemap limits must be positive')
    if body.startswith(b'\x1f\x8b'):
        import gzip, io
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
                body=stream.read(max_decoded_bytes+1)
        except (OSError, EOFError) as exc:
            raise ContractError('Invalid compressed sitemap') from exc
    if len(body)>max_decoded_bytes:
        raise ContractError('SITEMAP_DECOMPRESSED_LIMIT')
    try: root=fromstring(body)
    except Exception as exc: raise ContractError('Invalid or unsafe sitemap XML') from exc
    name=root.tag.rsplit('}',1)[-1]
    if name not in {'urlset','sitemapindex'}: raise ContractError('Not a sitemap/urlset')
    values=[]
    for el in root.iter():
        if el.tag.rsplit('}',1)[-1]!='loc' or not el.text: continue
        url=link_url(base,el.text)
        if url and origin(url)==origin(base):
            values.append(('sitemap' if name=='sitemapindex' else 'page',url))
    distinct=sorted(set(values),key=lambda x:(0 if x[0]=='sitemap' else 1,template_rank(x[1])))
    return distinct[:max_entries],len(distinct)>max_entries


def template_rank(url: str) -> tuple[int,str]:
    path=urlsplit(url).path.lower()
    return next((i for i,x in enumerate(TEMPLATES) if x in path),len(TEMPLATES)),url


def template_links(pages,seed: str) -> list[str]:
    urls={s.value for page in pages for s in page.surfaces if s.kind=='anchor_url' and origin(s.value)==origin(seed)}
    return sorted(urls,key=template_rank)


def canonical_claims(pages):
    return [{'capture_id':p.capture.capture_id,'url':s.value,'same_origin':origin(s.value)==origin(p.capture.url),'subject_rebound':False}
            for p in pages for s in p.surfaces if s.kind=='link_url' and 'canonical' in s.attributes.get('rel','').split()]
