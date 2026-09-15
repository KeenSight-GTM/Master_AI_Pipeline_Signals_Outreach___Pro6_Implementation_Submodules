"""Validate internal design inventories only; this is not runtime validation."""
from pathlib import Path
import hashlib
import json
from graphlib import TopologicalSorter, CycleError

ROOT = Path(__file__).resolve().parent

def load(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def main() -> None:
    modules = load('module_catalog.json')
    baseline = load('reference/modules.json')
    commands = load('reference/command_bindings.json')
    contracts = load('proposed_product_contracts.json')['contracts']
    workflows = load('workflow_stage_plans.json')['workflows']
    inspection = load('baseline_contract_inspection.json')
    ids = [m['module_id'] for m in modules['modules']]
    old = [m['module_id'] for m in baseline['modules']]
    require(len(ids) == len(set(ids)) == modules['module_count'] == 39, 'module inventory mismatch')
    require(len(old) == 30 and set(old) <= set(ids), 'baseline module IDs were lost')
    require(len(set(ids)-set(old)) == 9, 'new module inventory mismatch')
    by_id = {m['module_id']: m for m in modules['modules']}
    for prior in baseline['modules']:
        current = by_id[prior['module_id']]
        require(current['name'] == prior['name'], 'baseline module silently renamed')
        require(set(prior['input_contracts']) <= set(current['input_contracts']), 'baseline inputs removed')
        require(set(prior['output_contracts']) <= set(current['output_contracts']), 'baseline outputs removed')
    cmd_ids = [c['command_id'] for c in commands['commands']]
    require(len(cmd_ids) == len(set(cmd_ids)) == commands['command_count'] == 38, '38-command inventory mismatch')
    require(all(c['module_id'] in by_id for c in commands['commands']), 'unknown command owner')
    names = [c['name'] for c in contracts]
    require(len(names) == len(set(names)) == 32, 'product contract inventory mismatch')
    for c in contracts:
        require(c['owning_module'] in by_id, 'unknown contract owner')
        require(c['name'] in by_id[c['owning_module']]['output_contracts'], f"undeclared output {c['name']}")
        require(c['status'] == 'PROPOSED_CONCEPT_NOT_JSON_SCHEMA', 'misrepresented contract status')
        require(bool(c['minimum_design_fields']) and bool(c['invariant']), 'incomplete concept definition')
    stages = 0
    for w in workflows:
        stage_ids = [s['stage_id'] for s in w['stages']]
        require(len(stage_ids) == len(set(stage_ids)), 'duplicate stage ID')
        for s in w['stages']:
            require(s['module_id'] in by_id, 'unknown workflow module')
            require(set(s['depends_on']) <= set(stage_ids), 'dangling dependency')
        tuple(TopologicalSorter({s['stage_id']:set(s['depends_on']) for s in w['stages']}).static_order())
        stages += len(stage_ids)
    require(inspection['UseGateDecision']['properties']['purpose']['enum'] == ['PREVIEW_EXPORT','CONTACT_EXPORT'], 'baseline send boundary misreported')
    for name in ['reference/schemas/Common.schema.json','reference/schemas/Diagnostic.schema.json','reference/schemas/ModuleRequest.schema.json','reference/schemas/ModuleResult.schema.json']:
        require(isinstance(load(name),dict),'invalid reference JSON')
    for path in ['DESIGN.md','HANDOFFS.md','MODULE_MATRIX.md','PRODUCT_CONTRACTS.md','DIAGRAMS.md','COMPATIBILITY.md','ACCEPTANCE.md','README.md']:
        require((ROOT/path).stat().st_size > 100,'missing design document')
    for path in (ROOT/'diagrams').glob('*.mmd'):
        require(path.read_text().splitlines()[0] in ['flowchart TD','sequenceDiagram','classDiagram'],'unexpected diagram header')
    if (ROOT/'FILE_MANIFEST.json').exists():
        for row in load('FILE_MANIFEST.json')['files']:
            require(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'],'manifest mismatch: '+row['path'])
    report = {
        'status':'PASS_DESIGN_INVENTORY_ONLY',
        'modules':len(ids),'baseline_ids_preserved':len(old),'new_proposed_modules':9,
        'collector_command_bindings_preserved':len(cmd_ids),
        'proposed_product_contract_field_lists':len(contracts),
        'acyclic_example_stage_plans':len(workflows),'example_stage_count':stages,
        'checks':['Unique module IDs and retained baseline inputs/outputs',
                  'All 38 original command names and known owners',
                  'Proposed product contract ownership and declared outputs',
                  'Workflow references and acyclic selected stage plans',
                  'Actual baseline export-only purpose enum preserved',
                  'Reference JSON readable and design documents present',
                  'Packaged file hashes checked when manifest is present'],
        'not_tested':['Runtime execution','Exact schemas for new product DTOs',
                      'Collector SDK/browser roundtrip','Business/authorization semantics',
                      'Source accuracy or provider access','Live sending/CRM/replies',
                      'Rendered Mermaid output'],
        'runtime_changes':'None'
    }
    (ROOT/'DESIGN_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
