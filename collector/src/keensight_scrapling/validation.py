from __future__ import annotations

from importlib.resources import files
from .core import ContractError, Capture, Match, Observation, SupportLink, Surface, PageEvidence, CommandResult, canonical, instant, strict_json, record, identity
from .claims import resolve_claims,observation_candidates
from .commands import COMMANDS
import jsonschema


def validate_bundle(data: dict) -> None:
    schema=strict_json(files('keensight_scrapling').joinpath('data/scan-bundle.schema.json').read_text())
    try:
        jsonschema.Draft7Validator(schema,format_checker=jsonschema.FormatChecker()).validate(data)
    except jsonschema.ValidationError as exc:
        raise ContractError('ScanBundle schema: '+exc.message) from exc
    execution_ids=[c['execution_id'] for c in data['commands']]
    if len(execution_ids)!=len(set(execution_ids)):
        raise ContractError('Duplicate command invocation terminal outcome')
    from .rules import RulePack,match_pages
    pack=RulePack.compile(data['rule_pack'])
    if pack.digest!=data['release_digest'] or pack.fixture_only!=data['fixture_only']:
        raise ContractError('Rule release digest or fixture policy mismatch')
    for key,field in [('captures','capture_id'),('surfaces','surface_id'),('matches','match_id'),('observations','observation_id'),('claims','claim_key')]:
        values=[r[field] for r in data[key]]
        if len(values)!=len(set(values)): raise ContractError('Duplicate '+key+' identity')
    caps={c['capture_id']:Capture(**c) for c in data['captures']}
    surfaces={s['surface_id']:s for s in data['surfaces']}
    for cap in caps.values():
        if (cap.tenant_id,cap.subject_id,cap.run_id)!=(data['tenant_id'],data['subject_id'],data['capture_run_id']):
            raise ContractError('Capture differs from evaluation identity')
        if instant(cap.observed_at)>instant(data['as_of']): raise ContractError('Future capture input')
    for s in surfaces.values():
        if s['capture_id'] not in caps: raise ContractError('Surface capture is missing')
    matches=[Match(**m) for m in data['matches']]
    for m in matches:
        if m.surface_id not in surfaces or surfaces[m.surface_id]['capture_id']!=m.capture_id:
            raise ContractError('Match does not point to its actual capture/surface')
        if m.release_digest!=data['release_digest']:
            raise ContractError('Mixed rule releases in evaluation')
    selected = data['evaluated_capture_ids']
    if not set(selected)<=set(caps):
        raise ContractError('Unknown evaluated capture')
    if any(s['capture_id'] not in selected for s in data['surfaces']):
        raise ContractError('Surface from capture excluded by acquisition disposition')
    from .extraction import EXTRACTORS
    pages=[]
    for cid in selected:
        cap=caps[cid]
        ss=[Surface(**s) for s in data['surfaces'] if s['capture_id']==cid]
        cmds=[CommandResult(**c) for c in data['commands'] if c['command_id'] in EXTRACTORS and c['input_ids']==[cid]]
        if len(cmds)!=len(EXTRACTORS) or {c.command_id for c in cmds}!=set(EXTRACTORS):
            raise ContractError('Missing or duplicate per-capture extraction execution')
        for command in cmds:
            produced=[s.surface_id for s in ss if s.command_id==command.command_id]
            if sorted(command.output_ids)!=sorted(produced):
                raise ContractError('Extraction output linkage mismatch')
            if produced and command.status not in {'COMPLETE','PARTIAL'}:
                raise ContractError('Failed extraction cannot publish surfaces')
        pages.append(PageEvidence(cap,ss,cmds))
    expected_matches,expected_reports=match_pages(pack,pages)
    if sorted(map(canonical,map(record,expected_matches)))!=sorted(map(canonical,data['matches'])):
        raise ContractError('Matches do not reproduce from pinned rules and surfaces')
    if canonical(expected_reports)!=canonical(data['rule_evaluations']):
        raise ContractError('Rule execution outcomes do not reproduce')
    from .rules import MATCH_COMMAND
    for operator in {r.operator for r in pack.rules}:
        cid=MATCH_COMMAND[operator]
        command_rows=[c for c in data['commands'] if c['command_id']==cid and c['details'].get('operator')==operator]
        reports=[r for r in expected_reports if next(x for x in pack.rules if x.rule_id==r['rule_id']).operator==operator]
        expected_status='FAILED' if any(r['status']=='ERROR' for r in reports) else 'PARTIAL' if any(r['status']=='PARTIAL' for r in reports) else 'SKIPPED' if not pages else 'COMPLETE'
        mids=sorted(m.match_id for m in matches if next(r for r in pack.rules if r.rule_id==m.rule_id).operator==operator)
        if len(command_rows)!=1 or not any(c['status']==expected_status and sorted(c['output_ids'])==mids and sorted(c['input_ids'])==sorted(selected) for c in command_rows):
            raise ContractError('Matcher command contradicts executable result')
    obs=[Observation(**o) for o in data['observations']]
    expected,links=observation_candidates(caps.values(),matches)
    if sorted(map(canonical,map(record,expected)))!=sorted(map(canonical,data['observations'])):
        raise ContractError('Observation target, identity, provenance or value is inconsistent')
    if sorted(map(canonical,map(record,links)))!=sorted(map(canonical,data['support_links'])):
        raise ContractError('Missing, duplicate or fabricated support link')
    views=resolve_claims(obs,matches,links,caps.values(),as_of=data['as_of'])
    if sorted(map(canonical,map(record,views)))!=sorted(map(canonical,data['claims'])):
        raise ContractError('Claim view does not recompute from its evidence')
    if set(c['command_id'] for c in data['commands'])!=set(COMMANDS):
        raise ContractError('Command manifest must account for all 38 IDs')

    text='\n'.join(s.value for p in pages for s in p.surfaces if s.kind=='prose').casefold()
    negatives=[x for x in pack.raw.get('negative_terms',[]) if x.casefold() in text]
    supported={v.claim_key for v in views if v.status=='SUPPORTED' and v.predicate=='vendor.present'}
    expected_score=0 if negatives else min(100,10*len(supported))
    scores=[c for c in data['commands'] if c['command_id']=='SCORE_HOST']
    if data['priority_score']!=expected_score or len(scores)!=1 or scores[0]['details'].get('score')!=expected_score:
        raise ContractError('Priority projection does not reproduce')
    gates=[c for c in data['commands'] if c['command_id']=='GATE_NEGATIVE']
    if len(gates)!=1 or gates[0]['details']!={'deprioritize':bool(negatives),'terms':negatives,'facts_deleted':False}:
        raise ContractError('Negative-selection projection does not reproduce')
