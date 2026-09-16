"""Pure contract helpers. They are not a crawler, evidence truth oracle, or scheduler."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable

class ContractError(ValueError):
    """An explicit fail-closed boundary rejection."""

def require(condition: bool, code: str) -> None:
    if not condition: raise ContractError(code)

def read_json(path: Path) -> Any:
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,'DUPLICATE_JSON_KEY:'+k)
            result[k]=v
        return result
    def invalid(x):raise ContractError('NONFINITE_JSON:'+x)
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=invalid)

def canonical(value: Any) -> bytes:
    # Python reference format, not an assertion of RFC 8785/cross-language hashing.
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')

def digest(value: Any) -> str:
    return 'sha256:'+sha256(value if isinstance(value,bytes) else canonical(value)).hexdigest()

def instant(value: str) -> datetime:
    require(value.endswith('Z'),'TIMESTAMP_MUST_BE_UTC')
    return datetime.fromisoformat(value[:-1]+'+00:00')

def claim_key(fact: dict) -> tuple:
    """Nature is part of the claim channel; source identity remains on observations.

    Reports never silently overwrite direct observations. Measurement targets include
    provider/method/dimensions; PERIOD windows distinguish distinct measurements.
    """
    return (fact['tenant_id'],fact['subject_id'],fact['predicate_id'],fact['nature'],
            fact['scope_id'],canonical(fact['target']).decode(),canonical(fact['window']).decode())

def stable_order(nodes: Iterable[str], edges: Iterable[tuple[str,str]]) -> list[str]:
    ns=list(nodes);require(len(ns)==len(set(ns)),'DUPLICATE_GRAPH_NODE')
    depend={n:set() for n in ns};children=defaultdict(set)
    for a,b in edges:
        require(a in depend and b in depend,'DANGLING_GRAPH_EDGE')
        require(a!=b,'SELF_CYCLE')
        depend[b].add(a);children[a].add(b)
    ready=sorted(n for n in ns if not depend[n]);order=[]
    while ready:
        n=ready.pop(0);order.append(n)
        for child in sorted(children[n]):
            depend[child].remove(n)
            if not depend[child]:ready.append(child)
        ready.sort()
    require(len(order)==len(ns),'DEPENDENCY_CYCLE')
    return order

def pointer(document: Any,path: str) -> Any:
    require(path=='' or path.startswith('/'),'INVALID_JSON_POINTER')
    x=document
    for token in path.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        try:x=x[int(token)] if isinstance(x,list) else x[token]
        except (KeyError,ValueError,IndexError,TypeError) as e:raise ContractError('UNRESOLVED_POINTER:'+path) from e
    return x

def comparison_key(fact: dict) -> tuple:
    """A stricter series key for change calculations; reporting windows are excluded."""
    return claim_key(fact)[:-1]

def comparable(before: dict,after: dict) -> bool:
    return (before['state']==after['state']=='OBSERVED' and comparison_key(before)==comparison_key(after)
            and before['window'] is not None and after['window'] is not None
            and instant(before['window']['end'])<=instant(after['window']['start'])
            and (instant(before['window']['end'])-instant(before['window']['start']))
              ==(instant(after['window']['end'])-instant(after['window']['start'])))

def distinct_origins(artifacts: Iterable[dict]) -> set[tuple]:
    return {(a['origin_namespace'],a['origin_record_id']) for a in artifacts}

def semantic_value(value):
    """Exact JSON value equality, separate from evidence serialization/hashing.

    Numbers compare as their exact decimal values; booleans never compare as
    numbers. Units/dimensions/periods remain in the containing typed record/key.
    No rounding, tolerance, or lossy conversion is applied to source evidence.
    """
    from decimal import Decimal
    if value is None:return ('null',)
    if isinstance(value,bool):return ('boolean',value)
    if isinstance(value,(int,float)):
        number=Decimal(str(value));require(number.is_finite(),'NONFINITE_VALUE')
        return ('number',number)
    if isinstance(value,str):return ('string',value)
    if isinstance(value,(tuple,list)):return ('array',tuple(semantic_value(x) for x in value))
    if isinstance(value,dict):return ('object',tuple(sorted((k,semantic_value(v)) for k,v in value.items())))
    raise ContractError('UNSUPPORTED_JSON_VALUE')


def resolve_claim(facts: list[dict],as_of: str,eligible) -> dict:
    """Conservative reference: unknowns do not erase known facts; ties abstain.

    Explicit supersession removes only named prior observations. Different reports
    remain a conflict unless a separately approved resolution policy decides it.
    """
    require(bool(facts),'EMPTY_CLAIM')
    require(len({claim_key(f) for f in facts})==1,'MIXED_CLAIM_IDENTITIES')
    ids={f['fact_id'] for f in facts}
    stable_order(ids,[(f['supersedes_fact_id'],f['fact_id']) for f in facts if f['supersedes_fact_id'] in ids])
    removed={f['supersedes_fact_id'] for f in facts if f['supersedes_fact_id'] and f['state']!='UNKNOWN' and eligible(f,as_of)}
    candidates=[f for f in facts if f['fact_id'] not in removed and f['state']!='UNKNOWN' and eligible(f,as_of)]
    values={semantic_value((f['state'],f['object'])) for f in candidates}
    return {'status':'UNKNOWN' if not values else ('KNOWN' if len(values)==1 else 'CONFLICT'),
            'accepted_fact_ids':sorted(f['fact_id'] for f in candidates) if len(values)==1 else []}

def theme_summary(sample: dict,supporting: list[dict],artifacts: dict[str,dict],roots) -> dict:
    """Observed supporting-origin share; unclassified records remain explicit."""
    eligible=distinct_origins(artifacts[a] for a in sample['eligible_artifact_ids'])
    require(bool(eligible),'ZERO_ELIGIBLE_SAMPLE')
    supported=set()
    decisions=sample.get('record_decisions',[])
    for fact in supporting:
        matched=[d['artifact_id'] for d in decisions if d['status']=='SUPPORT' and fact['fact_id'] in d['classification_fact_ids']]
        require(len(matched)==1,'AMBIGUOUS_SUPPORTING_ORIGIN')
        require(matched[0] in roots(fact['fact_id']),'SUPPORT_OUTSIDE_LINEAGE')
        supported |= distinct_origins(artifacts[a] for a in matched)
    require(supported<=eligible,'SUPPORT_OUTSIDE_SAMPLE')
    unknown=distinct_origins(artifacts[d['artifact_id']] for d in decisions if d['status']=='UNCLASSIFIED')
    return {'support_count':len(supported),'eligible_count':len(eligible),'sample_share':len(supported)/len(eligible),'population_claim':False,
        'support_policy_id':sample['support_policy_id'],'classified_eligible_count':len(eligible-unknown),
        'unclassified_count':len(unknown),'denominator_definition':'ELIGIBLE_RETRIEVED_RECORDS_INCLUDING_UNCLASSIFIED'}

def fingerprint_hosts(definition: dict,html: str) -> set[str]:
    """Narrow HTML fixture matcher; not a 2,500-signature library or live browser."""
    from html.parser import HTMLParser
    from urllib.parse import urlsplit
    require(definition['operator']=='SCRIPT_HOST','MATCHER_NOT_IMPLEMENTED')
    class Parser(HTMLParser):
        def __init__(self):super().__init__();self.stack=[];self.hits=set()
        def handle_starttag(self,tag,attrs):
            if tag=='script' and dict(attrs).get('type','').strip().lower() in ('','module','text/javascript','application/javascript','application/ecmascript','text/ecmascript') and not any(x in ['footer','aside','template','noscript'] for x in self.stack):
                src=dict(attrs).get('src','')
                try:host=(urlsplit('https:'+src if src.startswith('//') else src).hostname or '').lower().rstrip('.')
                except ValueError:host=''
                domain=definition['match_value'].lower().rstrip('.')
                if host==domain or host.endswith('.'+domain):self.hits.add(host)
            if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(tag)
        def handle_endtag(self,tag):
            if tag in self.stack:
                while self.stack:
                    if self.stack.pop()==tag:break
    p=Parser();p.feed(html);p.close();return p.hits


def matches_fingerprint(definition: dict,html: str) -> bool:
    return bool(fingerprint_hosts(definition,html))


def evaluate_requirements(definition: dict,facts: list[dict],subject_id: str,as_of: str,eligible,
                          *,substantive_origins=None) -> str:
    """AND requirements count substantive origins, never fact rows or model I/O.

    Supply a trusted resolver returning origin namespace/record-ID pairs per fact.
    Without it, presence can satisfy minimum=1, but independence cannot be proven
    for higher minima. Duplicate or rephrased facts never manufacture support.
    """
    for req in definition['required_facts']:
        matching=[f for f in facts if f['subject_id']==subject_id and f['predicate_id']==req['predicate_id'] and
                  f['state']==req['state'] and f['nature'] in req['allowed_natures'] and eligible(f['fact_id'],as_of,allow_absence=req['state']=='NOT_FOUND')]
        if substantive_origins is None:
            if not matching or req['minimum']>1:return 'UNRESOLVED'
        else:
            origins={origin for f in matching for origin in substantive_origins(f['fact_id'])}
            if len(origins)<req['minimum']:return 'UNRESOLVED'
    return 'RESOLVED'


def code_digest(root: Path) -> str:
    """Pin reference Python implementation bytes, independent of checkout path."""
    paths=sorted((root/'keensight_contracts').glob('*.py'))+[root/'generate.py']
    return digest({str(p.relative_to(root)):digest(p.read_bytes()) for p in paths})
