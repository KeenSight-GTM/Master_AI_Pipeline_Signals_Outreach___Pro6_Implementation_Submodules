from __future__ import annotations

import re
from urllib.parse import urlsplit
from lxml import etree, html
from .core import Capture, Surface, CommandResult, PageEvidence, identity, strict_json
from .urls import link_url

EXTRACTORS = (
    'EXTRACT_RAW_HTML', 'EXTRACT_SCRIPT_SRC', 'EXTRACT_SCRIPT_INLINE',
    'EXTRACT_IFRAME_SRC', 'EXTRACT_FORM_ACTION', 'EXTRACT_ANCHORS',
    'EXTRACT_IMAGES', 'EXTRACT_LINKS_META', 'EXTRACT_JSONLD',
    'EXTRACT_MICRODATA', 'EXTRACT_FOOTER', 'EXTRACT_HEADER_NAV',
    'EXTRACT_DATA_ATTRS', 'EXTRACT_NOSCRIPT', 'EXTRACT_VISIBLE_TEXT',
    'EXTRACT_URL_FEATURES', 'EXTRACT_HEADERS',
)


def compact(text: str) -> str:
    return ' '.join(text.split())


def region(node) -> str:
    tags = {str(n.tag).lower() for n in [node, *node.iterancestors()]}
    if str(node.tag).lower()=='script' and node.get('type','').strip().lower() not in {'','module','text/javascript','application/javascript','application/ecmascript','text/ecmascript'}:
        return 'INERT_SCRIPT'
    if 'template' in tags:
        return 'INERT_TEMPLATE'
    if 'noscript' in tags:
        return 'NOSCRIPT'
    if 'aside' in tags:
        return 'ANCILLARY'
    if 'footer' in tags:
        return 'FOOTER'
    if tags & {'header', 'nav'}:
        return 'HEADER_NAV'
    return 'PAGE'


def extract(capture: Capture, body: bytes, *, max_items: int = 2000, max_text: int = 131072) -> PageEvidence:
    """Parse retained bytes deterministically. No network or adaptive selectors.

    lxml is an explicit parser backend, NOT a fallback HTTP client. Acquisition
    uses Scrapling. Static prose is not claimed to be computed browser visibility.
    """
    # Deterministic decode precedence: BOM, valid transport charset, then
    # valid HTML declaration, then UTF-8 (never environment-dependent guessing).
    import codecs
    declared = re.search(r"charset\s*=\s*[\"']?([^;\s\"']+)", capture.headers.get('content-type',''), re.I)
    doc = re.search(br"charset\s*=\s*[\"']?([a-zA-Z0-9._-]+)", body[:4096], re.I)
    choices = [('http',declared.group(1))] if declared else []
    if doc: choices.append(('html',doc.group(1).decode('ascii')))
    choices.append(('fallback','utf-8'))
    if body.startswith(codecs.BOM_UTF8): choices.insert(0,('bom','utf-8-sig'))
    elif body.startswith((codecs.BOM_UTF16_LE,codecs.BOM_UTF16_BE)): choices.insert(0,('bom','utf-16'))
    for encoding_source,encoding in choices:
        try: codecs.lookup(encoding); source=body.decode(encoding,errors='replace'); break
        except (LookupError,UnicodeError): continue
    parser = html.HTMLParser(encoding='utf-8',no_network=True, recover=True, huge_tree=False, remove_comments=False)
    try:
        root = html.document_fromstring(source.encode('utf-8') or b'<html></html>', parser=parser)
    except (etree.ParserError, ValueError) as exc:
        return PageEvidence(capture, [], [CommandResult(x, 'FAILED', [capture.capture_id], limitations=[type(exc).__name__]) for x in EXTRACTORS])
    tree = root.getroottree()
    base = capture.url
    for el in root.xpath('//base[@href]')[:1]:
        base = link_url(capture.url, el.get('href')) or capture.url
    results = {c: CommandResult(c, 'COMPLETE', [capture.capture_id]) for c in EXTRACTORS}
    damaging = [e for e in parser.error_log if e.level_name in {'FATAL','ERROR'}
                and (e.type_name not in {'HTML_UNKNOWN_TAG'} or 'excessive depth' in e.message.lower())]
    if damaging:
        for command, result in results.items():
            if command not in {'EXTRACT_RAW_HTML','EXTRACT_HEADERS'}:
                result.status = 'PARTIAL'
                result.limitations.append('PARSER_RECOVERY_LOSS')
                result.details['parser_errors'] = sorted({e.type_name for e in damaging})
    counts = {c: 0 for c in EXTRACTORS}
    surfaces: list[Surface] = []

    def add(command, kind, node, value, *, attrs=None, locator=None, context=None):
        if value is None:
            return
        result = results[command]
        if counts[command] >= max_items:
            result.status = 'PARTIAL'
            if 'ITEM_LIMIT' not in result.limitations:
                result.limitations.append('ITEM_LIMIT')
            return
        value = str(value)
        if len(value) > max_text:
            value = value[:max_text]
            result.status = 'PARTIAL'
            if 'TEXT_LIMIT' not in result.limitations:
                result.limitations.append('TEXT_LIMIT')
        loc = locator or (tree.getpath(node) if node is not None else kind)
        s = Surface(identity('surface', capture.capture_id, command, kind, loc, value, attrs or {}),
                    capture.capture_id, command, kind, loc, value,
                    context or (region(node) if node is not None else 'PAGE'), attrs or {})
        surfaces.append(s)
        counts[command] += 1
        result.output_ids.append(s.surface_id)

    add('EXTRACT_RAW_HTML', 'raw_html', None, source, locator='retained-body:decoded', attrs={'encoding': encoding, 'encoding_source': encoding_source})
    results['EXTRACT_RAW_HTML'].details['original_body_sha256'] = capture.body_sha256

    # Keep node-local attributes so one node cannot lend evidence to another.
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        tag = el.tag.lower()
        path = tree.getpath(el)
        attrs = dict(el.attrib)
        if tag == 'script':
            if el.get('src'):
                value = link_url(base, el.get('src'))
                if value:
                    add('EXTRACT_SCRIPT_SRC', 'script_url', el, value, locator=path+'/@src', attrs={'type': el.get('type','')})
            elif el.get('type', '').lower() != 'application/ld+json':
                add('EXTRACT_SCRIPT_INLINE', 'inline_script', el, el.text or '', attrs={'type': el.get('type', '')})
        if tag in {'iframe', 'embed', 'object'}:
            a = 'data' if tag == 'object' else 'src'
            value = link_url(base, el.get(a, '')) if el.get(a) else None
            if value:
                add('EXTRACT_IFRAME_SRC', 'iframe_url', el, value, locator=path+'/@'+a, attrs={'tag': tag})
        if tag == 'form':
            value = link_url(base, el.get('action', capture.url))
            if value:
                add('EXTRACT_FORM_ACTION', 'form_url', el, value, locator=path+'/@action', attrs={'method': el.get('method', 'GET').upper()})
        if tag == 'a' and el.get('href'):
            value = link_url(base, el.get('href'))
            if value:
                add('EXTRACT_ANCHORS', 'anchor_url', el, value, locator=path+'/@href', attrs={'text': compact(el.text_content())[:2000]})
        if tag == 'img':
            value = link_url(base, el.get('src') or el.get('data-src') or '')
            add('EXTRACT_IMAGES', 'image', el, value or '', attrs={'alt': el.get('alt', ''), 'title': el.get('title', '')})
        if tag == 'link' and el.get('href'):
            value = link_url(base, el.get('href'))
            if value:
                add('EXTRACT_LINKS_META', 'link_url', el, value, attrs={'rel': el.get('rel', '').lower()})
        if tag == 'meta':
            add('EXTRACT_LINKS_META', 'meta', el, el.get('content', ''), attrs={'name': el.get('name') or el.get('property') or el.get('http-equiv', '')})
        if tag == 'script' and el.get('type', '').lower() == 'application/ld+json':
            raw = el.text or ''
            data = {'parsed': None, 'types': [], 'parse_error': None}
            try:
                if len(raw) > max_text:
                    raise ValueError('JSONLD_TEXT_LIMIT')
                parsed = strict_json(raw)
                if not isinstance(parsed, (dict, list)):
                    raise ValueError('JSONLD_EXPECTS_OBJECT_OR_ARRAY')
                data['parsed'] = parsed
                types, stack, visited = set(), [parsed], 0
                while stack:
                    visited += 1
                    if visited > max_items:
                        raise ValueError('JSONLD_NODE_LIMIT')
                    node = stack.pop()
                    if isinstance(node, dict):
                        t = node.get('@type', [])
                        types.update(x for x in ([t] if isinstance(t, str) else t if isinstance(t, list) else []) if isinstance(x, str))
                        stack.extend(node.values())
                    elif isinstance(node, list):
                        stack.extend(node)
                data['types'] = sorted(types)
            except (ValueError, RecursionError) as exc:
                data['parse_error'] = str(exc)[:500]
                results['EXTRACT_JSONLD'].status = 'PARTIAL'
                results['EXTRACT_JSONLD'].limitations.append('JSONLD_PARSE_ERROR')
            add('EXTRACT_JSONLD', 'jsonld', el, raw, attrs=data)
        if any(x in attrs for x in ('itemscope', 'itemtype', 'typeof', 'vocab', 'property')):
            add('EXTRACT_MICRODATA', 'microdata', el, el.get('itemtype') or el.get('typeof') or '', attrs={k:v for k,v in attrs.items() if k in {'itemscope','itemtype','itemid','itemprop','typeof','vocab','property','about','resource'}})
        if tag == 'footer':
            add('EXTRACT_FOOTER', 'footer', el, compact(el.text_content()))
        if tag in {'header', 'nav'}:
            add('EXTRACT_HEADER_NAV', 'header_nav', el, compact(el.text_content()))
        for k, v in attrs.items():
            if k.lower().startswith('data-') or k in {'id','class'}:
                add('EXTRACT_DATA_ATTRS', 'attribute', el, v, locator=path+'/@'+k, attrs={'name': k})
        if tag == 'noscript':
            add('EXTRACT_NOSCRIPT', 'noscript', el, etree.tostring(el, encoding='unicode', method='html'))
    texts = root.xpath('//text()[not(ancestor::script or ancestor::style or ancestor::noscript or ancestor::template)]')
    add('EXTRACT_VISIBLE_TEXT', 'prose', None, compact(' '.join(map(str, texts))), locator='document:non-script-text', attrs={'visibility': 'STATIC_PROSE_NOT_COMPUTED_VISIBILITY'})
    results['EXTRACT_VISIBLE_TEXT'].limitations.append('CSS_VISIBILITY_NOT_EVALUATED')
    seen = set()
    for s in list(surfaces):
        if s.kind in {'script_url','iframe_url','form_url','anchor_url','link_url','image'} and s.value:
            p = urlsplit(s.value)
            # Query values may contain tokens; derive keys only for technical features.
            from urllib.parse import parse_qsl
            item = (p.hostname, p.path, tuple(sorted({k for k,_ in parse_qsl(p.query)})))
            if item not in seen:
                seen.add(item)
                add('EXTRACT_URL_FEATURES', 'url_features', None, s.value.split('?',1)[0], locator=s.locator,
                    attrs={'host': p.hostname or '', 'path': p.path, 'query_keys': list(item[2]), 'source_surface_id': s.surface_id}, context=s.context)
    for name, value in sorted(capture.headers.items()):
        if name.lower() == 'x-keensight-cookie-names':
            for cookie in value.split(','):
                if cookie:
                    add('EXTRACT_HEADERS', 'cookie_name', None, cookie, locator='response/cookie-name/'+cookie)
        else:
            add('EXTRACT_HEADERS', 'header', None, value, locator='response/header/'+name.lower(), attrs={'name': name.lower()})
    for command in results.values():
        command.details['surface_count'] = len(command.output_ids)
        if not capture.complete:
            command.status = 'PARTIAL'
            command.limitations.append('INCOMPLETE_CAPTURE')
    return PageEvidence(capture, surfaces, list(results.values()))
