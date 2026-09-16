from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
import regex
from .core import canonical, ContractError, Match, PageEvidence, identity, strict_json
from .urls import host_match

OPERATORS = {'contains', 'equals', 'regex', 'host_suffix', 'host_equals', 'footer_literal', 'image_alt'}
KINDS = {'raw_html','script_url','inline_script','iframe_url','form_url','anchor_url','image','link_url','meta','jsonld','microdata','footer','header_nav','attribute','noscript','prose','url_features','header','cookie_name'}
DIRECT_KINDS = {'script_url','iframe_url','form_url','link_url','meta','header','cookie_name','attribute'}
PREDICATES = {'vendor.present','vendor.mentioned'}
MATCH_COMMAND = {'contains':'MATCH_SUBSTRING','equals':'MATCH_SUBSTRING','regex':'MATCH_REGEX','host_suffix':'MATCH_HOST_SUFFIX','host_equals':'MATCH_HOST_SUFFIX','footer_literal':'MATCH_FOOTER_LITERAL','image_alt':'MATCH_IMG_ALT'}

KIND_COMMAND = {
 'raw_html':'EXTRACT_RAW_HTML','script_url':'EXTRACT_SCRIPT_SRC','inline_script':'EXTRACT_SCRIPT_INLINE',
 'iframe_url':'EXTRACT_IFRAME_SRC','form_url':'EXTRACT_FORM_ACTION','anchor_url':'EXTRACT_ANCHORS',
 'image':'EXTRACT_IMAGES','link_url':'EXTRACT_LINKS_META','meta':'EXTRACT_LINKS_META',
 'jsonld':'EXTRACT_JSONLD','microdata':'EXTRACT_MICRODATA','footer':'EXTRACT_FOOTER',
 'header_nav':'EXTRACT_HEADER_NAV','attribute':'EXTRACT_DATA_ATTRS','noscript':'EXTRACT_NOSCRIPT',
 'prose':'EXTRACT_VISIBLE_TEXT','url_features':'EXTRACT_URL_FEATURES',
 'header':'EXTRACT_HEADERS','cookie_name':'EXTRACT_HEADERS'}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    digest: str
    status: str
    predicate: str
    product_id: str
    kinds: tuple[str, ...]
    operator: str
    patterns: tuple[str, ...]
    field: str
    selector: str | None
    guard_terms: tuple[str, ...]
    schema_types: tuple[str, ...]
    confidence: float | None
    source: dict


@dataclass
class RulePack:
    release_id: str
    digest: str
    fixture_only: bool
    rules: list[Rule]
    raw: dict

    @classmethod
    def load(cls, path: str | Path) -> 'RulePack':
        return cls.compile(strict_json(Path(path).read_text()))

    @classmethod
    def compile(cls, data: dict) -> 'RulePack':
        if not isinstance(data, dict) or set(data) - {'schema_version','release_id','fixture_only','aliases','rules','negative_terms'}:
            raise ContractError('Unknown rule-pack fields')
        if data.get('schema_version') != '1.0' or not isinstance(data.get('release_id'), str) or not data['release_id']:
            raise ContractError('Invalid rule pack version or release ID')
        if not isinstance(data.get('fixture_only'), bool) or not isinstance(data.get('rules'), list):
            raise ContractError('Pack must explicitly declare fixture_only and rules')
        aliases = data.get('aliases', {})
        if not isinstance(aliases, dict) or any(not isinstance(k,str) or not isinstance(v,str) or not k or not v for k,v in aliases.items()):
            raise ContractError('Alias map must contain nonempty strings')
        def canonical_product(product):
            visited = set()
            while product in aliases:
                if product in visited:
                    raise ContractError('Alias cycle')
                visited.add(product)
                product = aliases[product]
            return product
        for key in aliases:
            canonical_product(key)
        negative = data.get('negative_terms', [])
        if not isinstance(negative,list) or any(not isinstance(x,str) or not x for x in negative):
            raise ContractError('Invalid negative terms')
        ids, rules = set(), []
        for row in data['rules']:
            allowed = {'id','status','predicate','product_id','kinds','operator','patterns','field','selector','guard_terms','schema_types','confidence','review','source'}
            if not isinstance(row, dict) or set(row)-allowed:
                raise ContractError('Unknown rule fields')
            rid = row.get('id')
            if not isinstance(rid,str) or not rid or rid in ids:
                raise ContractError('Missing or duplicate rule ID')
            ids.add(rid)
            status = row.get('status')
            if status not in {'CANDIDATE','APPROVED','DISABLED'}:
                raise ContractError('Unknown authority status')
            if status == 'APPROVED':
                review = row.get('review')
                if not isinstance(review, dict) or not review.get('reviewer') or not review.get('fixture_report_hash'):
                    raise ContractError('Approved rule needs explicit review and fixture report reference')
            pred, product = row.get('predicate'), row.get('product_id')
            if pred not in PREDICATES or not isinstance(product,str) or not product:
                raise ContractError('An explicit supported emission and product are required')
            kinds, op, pats = row.get('kinds'), row.get('operator'), row.get('patterns')
            if not isinstance(kinds,list) or not kinds or set(kinds)-KINDS or op not in OPERATORS:
                raise ContractError('Unknown or empty operator/surface declaration')
            if not isinstance(pats,list) or not pats or len(pats)>128 or any(not isinstance(p,str) or not p or len(p)>4096 for p in pats):
                raise ContractError('Invalid patterns')
            if op == 'regex':
                for pattern in pats:
                    try: regex.compile(pattern)
                    except regex.error as exc: raise ContractError('Invalid regex') from exc
            if op in {'host_equals','host_suffix'}:
                if set(kinds)-{'script_url','iframe_url','form_url','anchor_url','link_url'}:
                    raise ContractError('Host matching requires structured URL surfaces')
                if any(not regex.fullmatch(r'[A-Za-z0-9.-]+',p) or p.startswith('.') or '..' in p for p in pats):
                    raise ContractError('Malformed hostname pattern')
            if op == 'image_alt' and kinds != ['image']:
                raise ContractError('image_alt requires image surface')
            if op == 'footer_literal' and kinds != ['footer']:
                raise ContractError('footer_literal requires footer surface')
            if pred == 'vendor.present' and (set(kinds)-DIRECT_KINDS or op in {'contains','regex','footer_literal','image_alt'}):
                raise ContractError('Presence needs an approved narrow active-surface rule; use vendor.mentioned for broad matching')
            f = row.get('field','value')
            if f not in {'value','name','alt','rel'}:
                raise ContractError('Unsupported match field')
            confidence = row.get('confidence')
            if confidence is not None and (isinstance(confidence,bool) or not isinstance(confidence,(int,float)) or not 0 <= confidence <= 1):
                raise ContractError('Invalid authored confidence')
            for prop in ('guard_terms','schema_types'):
                if not isinstance(row.get(prop,[]),list) or any(not isinstance(x,str) or not x for x in row.get(prop,[])):
                    raise ContractError('Malformed guard')
            selector = row.get('selector')
            if selector is not None and (not isinstance(selector,str) or not selector or len(selector)>512):
                raise ContractError('selector is a bounded literal XPath prefix, never executable code')
            rules.append(Rule(rid,identity('rule-semantic-v2',row,canonical_product(product)),status,pred,canonical_product(product),tuple(kinds),op,tuple(pats),f,selector,tuple(row.get('guard_terms',[])),tuple(row.get('schema_types',[])),confidence,row.get('source',{})))
        # Rule iteration order must not change evidence identities or the release hash.
        normalized = dict(data)
        normalized['rules'] = sorted(data['rules'],key=lambda r:r['id'])
        return cls(data['release_id'],identity('release',normalized),data['fixture_only'],sorted(rules,key=lambda r:r.rule_id),normalized)


def match_pages(pack: RulePack, pages: list[PageEvidence], *, production: bool = False) -> tuple[list[Match],list[dict]]:
    """Retain EVERY rule/surface/alternative hit. Deduplicate claims later."""
    if production and pack.fixture_only:
        raise ContractError("Fixture-only pack is not eligible for production matching")
    matches, evaluations = [], []
    # Never pool different subjects, tenants, or origins into the host index.
    from .urls import origin
    keys = {(p.capture.tenant_id,p.capture.subject_id,origin(p.capture.url)) for p in pages}
    if len(keys)>1:
        raise ContractError('Cross-subject/tenant/origin host rollup forbidden')
    prose = '\n'.join(s.value for p in pages for s in p.surfaces if s.kind in {'prose','header_nav'})
    types = {t for p in pages for s in p.surfaces if s.kind=='jsonld' and not s.attributes.get('parse_error') for t in s.attributes.get('types',[])}
    for rule in pack.rules:
        if rule.status=='DISABLED':
            evaluations.append({'rule_id':rule.rule_id,'status':'DISABLED','match_ids':[]})
            continue
        qualification = 'QUALIFIED' if all(x.casefold() in prose.casefold() for x in rule.guard_terms) and (not rule.schema_types or bool(types.intersection(rule.schema_types))) else 'UNQUALIFIED'
        found, errors, limited = [], [], []
        start = len(matches)
        for page in pages:
            command_states={c.command_id:c.status for c in page.commands}
            needed={KIND_COMMAND[k] for k in rule.kinds}
            if not page.capture.complete or any(command_states.get(c)!='COMPLETE' for c in needed):
                limited.append(page.capture.capture_id)
            for s in page.surfaces:
                if s.kind not in rule.kinds or (rule.selector and not s.locator.startswith(rule.selector)):
                    continue
                if rule.predicate=='vendor.present' and s.context in {'FOOTER','NOSCRIPT','INERT_TEMPLATE','INERT_SCRIPT','ANCILLARY'}:
                    continue
                if rule.predicate=='vendor.present' and s.kind=='link_url' and 'stylesheet' not in s.attributes.get('rel','').split():
                    continue
                value = s.value if rule.field=='value' else str(s.attributes.get(rule.field,''))
                for pattern in rule.patterns:
                    try:
                        if rule.operator in {'host_suffix','host_equals'}:
                            hit = host_match(value,pattern,exact=rule.operator=='host_equals')
                        elif rule.operator=='equals': hit = value.casefold()==pattern.casefold()
                        elif rule.operator=='regex': hit = bool(regex.search(pattern,value[:131072],timeout=0.025))
                        elif rule.operator=='image_alt': hit = pattern.casefold() in str(s.attributes.get('alt','')).casefold()
                        else: hit = pattern.casefold() in value.casefold()
                    except TimeoutError:
                        errors.append({'capture_id':page.capture.capture_id,'reason':'REGEX_TIMEOUT'})
                        continue
                    if hit:
                        authority = 'APPROVED' if rule.status=='APPROVED' else 'CANDIDATE'
                        mid = identity('match',rule.digest,pack.digest,page.capture.capture_id,s.surface_id,pattern)
                        matches.append(Match(mid,rule.rule_id,rule.digest,pack.digest,authority,page.capture.capture_id,s.surface_id,pattern,rule.predicate,rule.product_id,True,identity('evidence',page.capture.capture_id,s.locator),identity('rule_evidence',rule.digest,page.capture.capture_id,s.surface_id,pattern),rule.confidence))
                        found.append(mid)
        if errors:
            matches = matches[:start]
            found = []
        evaluations.append({'rule_id':rule.rule_id,'status':'ERROR' if errors else 'NOT_EVALUATED' if not pages else 'PARTIAL' if limited else 'MATCH' if found else 'NO_MATCH',
                            'match_ids':sorted(set(found)),'errors':sorted(errors,key=canonical),'incomplete_capture_ids':sorted(set(limited)), 'qualification':qualification,
                            'absence_fact_emitted':False})
    # Identical alternate patterns cannot create duplicate link rows.
    unique = {m.match_id:m for m in matches}
    return sorted(unique.values(),key=lambda x:x.match_id),evaluations
