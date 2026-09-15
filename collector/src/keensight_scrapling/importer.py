from __future__ import annotations

from collections import Counter
from pathlib import Path
from .core import ContractError, strict_json, identity
from .rules import RulePack

SCOPE_MAP={'scripts':'script_url','stylesheets':'link_url','iframes':'iframe_url','form_actions':'form_url','links':'anchor_url',
           'raw_html':'raw_html','footer_text':'footer','meta_tags':'meta','meta_names':'meta','cookies':'cookie_name',
           'cookie_names':'cookie_name','headers':'header','response_headers':'header','data_attributes':'attribute'}
# Only semantically equivalent operators are admitted. Everything else retains
# its full raw source in quarantine; no prose interpretation or Python eval.
OPS={'contains_any':('contains','value'),'equals':('equals','value'),'regex':('regex','value'),
     'host_equals':('host_equals','value'),'meta_name_equals':('equals','name'),
     'meta_value_contains':('contains','value'),'meta_value_regex':('regex','value'),
     'cookie_name':('equals','value'),'cookie_name_regex':('regex','value'),'header_name':('equals','name')}


def read_donor(path: str | Path) -> list[dict]:
    path=Path(path)
    if path.suffix=='.jsonl':
        rows=[]
        for line,raw in enumerate(path.read_text().splitlines(),1):
            if raw.strip():
                obj=strict_json(raw)
                if not isinstance(obj,dict): raise ContractError(f'Non-object on line {line}')
                rows.append(obj)
        return rows
    obj=strict_json(path.read_text())
    if isinstance(obj,list): rows=obj
    elif isinstance(obj,dict) and isinstance(obj.get('rules'),list): rows=obj['rules']
    else: raise ContractError('Expected donor JSONL, an array, or {rules:[...]}')
    if any(not isinstance(r,dict) for r in rows): raise ContractError('Non-object donor row')
    return rows


def import_donor(rows: list[dict],vendor_map: dict[str,str],*,release_id: str='donor-candidates-v1') -> tuple[dict,dict]:
    if not isinstance(vendor_map,dict) or any(not isinstance(k,str) or not isinstance(v,str) or not v for k,v in vendor_map.items()):
        raise ContractError('Explicit vendor mapping required')
    counts=Counter(row.get('id') for row in rows if isinstance(row,dict) and isinstance(row.get('id'),str))
    imported=[];dispositions=[]
    for index,row in enumerate(rows):
        rid=row.get('id') if isinstance(row,dict) else None; reason=None
        sig=row.get('signal',{}) if isinstance(row,dict) else {}; meta=sig.get('metadata',{}) if isinstance(sig,dict) else {}
        match=meta.get('match',{}) if isinstance(meta,dict) else {}
        try:
            if not isinstance(rid,str) or not rid or counts[rid]>1: raise ContractError('MISSING_OR_DUPLICATE_ID')
            status=meta.get('detector_status')
            if status in {'research_only','duplicate_reference','scoring_rule'}: raise ContractError('NON_DETECTOR_REFERENCE_ROW')
            if match.get('operator') not in OPS: raise ContractError('UNSUPPORTED_OPERATOR')
            if match.get('min_matches',1)!=1: raise ContractError('UNSUPPORTED_MINIMUM_MATCH_SEMANTICS')
            scopes=match.get('scope')
            if not isinstance(scopes,list) or not scopes or any(s not in SCOPE_MAP for s in scopes): raise ContractError('UNSUPPORTED_SCOPE')
            raw_value=sig.get('value')
            if not isinstance(raw_value,str) or raw_value not in vendor_map: raise ContractError('MISSING_CANONICAL_VENDOR_MAPPING')
            if meta.get('extraction') or row.get('extraction'): raise ContractError('EXTRACTION_RULE_REQUIRES_EXPLICIT_ADAPTER')
            op,field=OPS[match['operator']]
            rule={'id':rid,'status':'CANDIDATE','predicate':'vendor.mentioned','product_id':vendor_map[raw_value],
                  'kinds':sorted(set(SCOPE_MAP[s] for s in scopes)), 'operator':op,'patterns':match.get('patterns'), 'field':field,
                  'confidence':sig.get('confidence'),
                  'source':{'legacy_id':rid,'legacy_status':status,'raw_sha256':identity('legacy',row),'original':row,
                            'emission_policy':'candidate vendor.mentioned; reviewed narrow rule needed for presence'}}
            RulePack.compile({'schema_version':'1.0','release_id':'preflight','fixture_only':False,'rules':[rule]})
            imported.append(rule)
        except (ValueError,TypeError,KeyError,AttributeError) as exc:
            reason=str(exc)
        dispositions.append({'row_index':index,'legacy_id':rid,'status':'QUARANTINED' if reason else 'IMPORTED_CANDIDATE',
                             'reason':reason,'raw':row})
    pack={'schema_version':'1.0','release_id':release_id,'fixture_only':False,'aliases':{},'rules':imported}
    RulePack.compile(pack)
    report={'input_rows':len(rows),'imported_candidates':len(imported),'quarantined_rows':len(rows)-len(imported),
            'automatic_approvals':0,'dispositions':dispositions}
    return pack,report
