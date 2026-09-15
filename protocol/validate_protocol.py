"""Validate this proposed interface pack, not the live KeenSight application.

The envelope examples are protocol-only fixtures. Production operation payloads,
authentication, output publication, lineage closure and provider effects require
their own runtime implementations and contract tests.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent
VERSION = "1.0.0-draft.1"
BASE = f"urn:keensight:module-protocol:{VERSION}:"


def load(path: Path) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        obj: dict[str, Any] = {}
        for key, value in items:
            if key in obj:
                raise ValueError(f"Duplicate JSON key: {key}")
            obj[key] = value
        return obj

    def bad(value: str) -> None:
        raise ValueError(f"Non-finite JSON number: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=bad)


def digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def validators() -> dict[str, Draft7Validator]:
    schemas = [load(p) for p in sorted((ROOT / "schemas").glob("*.json"))]
    registry = Registry()
    for schema in schemas:
        Draft7Validator.check_schema(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return {
        s["$id"].rsplit(":", 1)[-1]: Draft7Validator(s, registry=registry,
                                                    format_checker=FormatChecker())
        for s in schemas
    }


# Installed operation signatures are trusted application configuration, never
# arbitrary entrypoint names from a request. Only the delivered fixture adapter
# is registered here. Other proposed operations deliberately fail closed.
OPERATION_SIGNATURES = {
    ('FP-01','match'): {
        'inputs': {('urn:keensight:protocol-fixture:CaptureInput','example-only')},
        'parameters': ('urn:keensight:protocol-fixture:FingerprintParameters','example-only'),
        'release': ('urn:keensight:protocol-fixture:ReleaseLock','example-only'),
        'outputs': {('urn:keensight:protocol-fixture:MatchEvaluation','example-only')},
        'min_inputs': 1,'min_outputs': 1,
    }
}

def ref_type(ref):return (ref['schema_id'],ref['schema_version'])

def validate_payload_pair(request, result, resolve):
    """Resolve all referenced bytes through a trusted local record resolver.

    This is an admission/verification helper, not a process sandbox or an auth
    server. `resolve` must enforce tenant isolation and immutable storage.
    """
    validate_pair(request,result)
    refs=request['input_refs']+result['consumed_refs']+result['output_refs']+result['diagnostic_record_refs']
    refs += [request[k] for k in ('parameters_ref','release_lock_ref') if request[k]]
    for ref in refs:
        payload=resolve(ref)
        if digest(payload)!=ref['content_digest']:raise ValueError('Resolved record digest mismatch')
        expected=ref['schema_id'].rsplit(':',1)[-1]
        # This delivered operation is explicitly fixture-only, not a shortcut
        # accepting arbitrary production records in the generic envelope.
        if set(payload)!={'body','fixture_only','type'} or payload['fixture_only'] is not True or payload['type']!=expected:
            raise ValueError('Resolved record violates registered fixture contract')
        if not isinstance(payload['body'],dict):raise ValueError('Invalid fixture body')
        bodies={
          'CaptureInput':{'body_digest':{'type':'string','minLength':1},'observed_at':{'type':'string','format':'date-time'}},
          'FingerprintParameters':{'allow_network':{'const':False},'policy':{'const':'approved-only'}},
          'ReleaseLock':{'collector':{'type':'string'},'domain_contracts':{'type':'string'},'rule_release':{'type':'string'}},
          'MatchEvaluation':{'evidence_points':{'type':'integer','minimum':0},'matches':{'type':'integer','minimum':0},'verdict':{'enum':['MATCH','NO_MATCH','UNKNOWN']}},
        }
        if expected not in bodies:raise ValueError('No installed domain payload validator')
        body_schema={'type':'object','properties':bodies[expected],'required':list(bodies[expected]),'additionalProperties':False}
        Draft7Validator(body_schema,format_checker=FormatChecker()).validate(payload['body'])
    return True

def validate_pair(request: dict[str, Any], result: dict[str, Any]) -> None:
    vs = validators()
    vs["ModuleRequest"].validate(request)
    vs["ModuleResult"].validate(result)
    for key in ("request_id", "execution_id", "module_id", "operation", "context", "trace"):
        if request[key] != result[key]:
            raise ValueError(f"Request/result mismatch at {key}")
    if result["request_digest"] != digest(request):
        raise ValueError("Request digest mismatch")
    if datetime.fromisoformat(result["finished_at"]) < datetime.fromisoformat(result["started_at"]):
        raise ValueError("Result finished before it started")
    if result["reused_execution_id"] == result["execution_id"]:
        raise ValueError("Execution cannot reuse itself")
    if request["module_id"] != "CTL-01" and request["release_lock_ref"] is None:
        raise ValueError("Non-bootstrap operation requires a release lock")
    mids = {m["module_id"] for m in load(ROOT / "modules.json")["modules"]}
    if request["module_id"] not in mids:
        raise ValueError("Unregistered module")
    signature=OPERATION_SIGNATURES.get((request['module_id'],request['operation']))
    if signature is None:raise ValueError('Unregistered operation implementation/signature')
    if len(request['input_refs'])<signature['min_inputs'] or any(ref_type(r) not in signature['inputs'] for r in request['input_refs']):
        raise ValueError('Operation input schema/version mismatch')
    if request['parameters_ref'] is None or ref_type(request['parameters_ref'])!=signature['parameters']:
        raise ValueError('Operation parameters schema/version mismatch')
    if request['release_lock_ref'] is None or ref_type(request['release_lock_ref'])!=signature['release']:
        raise ValueError('Operation release schema/version mismatch')
    declared=request['input_refs']+[request[k] for k in ('release_lock_ref','parameters_ref','budget_reservation_ref') if request[k] is not None]
    allowed={r['record_id']:r for r in declared}
    if len(allowed)!=len(declared):raise ValueError('Duplicate declared input reference')
    consumed=result['consumed_refs']
    if len({r['record_id'] for r in consumed})!=len(consumed):raise ValueError('Duplicate consumed reference')
    if any(allowed.get(r['record_id'])!=r for r in consumed):raise ValueError('Consumed record not declared by exact reference')
    if result['execution_status']=='SUCCEEDED':
        if {r['record_id'] for r in consumed}!=set(allowed):raise ValueError('Successful operation did not report required inputs')
        if len(result['output_refs'])<signature['min_outputs']:raise ValueError('Successful operation omitted output')
    if any(ref_type(r) not in signature['outputs'] for r in result['output_refs']):raise ValueError('Operation output schema/version mismatch')
    if len({r['record_id'] for r in result['output_refs']})!=len(result['output_refs']):raise ValueError('Duplicate output reference')
    if any(r['record_id'] in allowed for r in result['output_refs']):raise ValueError('Output overwrites an immutable input')
    if datetime.fromisoformat(result['finished_at'])>datetime.fromisoformat(request['deadline_at']):raise ValueError('Operation finished beyond deadline')
    context = request["context"]
    if context["as_of"] and context["knowledge_cutoff"]:
        # These timestamps have different meanings: either may be earlier.
        # Do not invent an ordering relation between valid time and recorded time.
        pass
    allowed_codes = load(ROOT / "error_codes.json")["codes"]
    if any(d["code"] not in allowed_codes for d in result["diagnostics"]):
        raise ValueError("Unregistered diagnostic code")
    all_refs = request["input_refs"] + result["consumed_refs"] + result["output_refs"] + result["diagnostic_record_refs"]
    for key in ("release_lock_ref", "parameters_ref", "budget_reservation_ref"):
        if request[key] is not None:
            all_refs.append(request[key])
    if context["subject_ref"] is not None:
        all_refs.append(context["subject_ref"])
    for d in result["diagnostics"]:
        all_refs += d["record_refs"]
        if d["restricted_details_ref"] is not None:
            all_refs.append(d["restricted_details_ref"])
    seen: dict[str, dict[str, Any]] = {}
    for ref in all_refs:
        # This draft uses tenant-scoped references, including aliases for shared
        # releases. It does not implement cross-tenant authorization.
        if ref["tenant_id"] != context["tenant_id"]:
            raise ValueError("Cross-tenant reference")
        previous = seen.get(ref["record_id"])
        if previous is not None and previous != ref:
            raise ValueError("Immutable reference has conflicting metadata/digest")
        seen[ref["record_id"]] = ref


def validate_pack() -> dict[str, Any]:
    vs = validators()
    cat = load(ROOT / "modules.json")
    modules = cat["modules"]
    ids = [m["module_id"] for m in modules]
    if len(ids) != len(set(ids)) or len(ids) != cat["module_count"]:
        raise ValueError("Module IDs/count do not agree")
    for m in modules:
        for key in ("input_contracts", "output_contracts", "submodules"):
            if not m[key] or any(not x for x in m[key]):
                raise ValueError(f"Missing {key} on {m['module_id']}")
    bindings = load(ROOT / "command_bindings.json")
    rows = bindings["commands"]
    commands = [r["command_id"] for r in rows]
    if len(commands) != 38 or len(set(commands)) != 38:
        raise ValueError("38 unique command bindings required")
    if any(r["module_id"] not in ids for r in rows):
        raise ValueError("Command has no module owner")
    req = load(ROOT / "examples/request.json")
    res = load(ROOT / "examples/result.json")
    validate_pair(req, res)
    fixtures = load(ROOT / "examples/fixture_records.json")
    for ref in res["consumed_refs"] + res["output_refs"]:
        if digest(fixtures[ref["record_id"]]) != ref["content_digest"]:
            raise ValueError("Example reference digest mismatch")
    return {"proposal_version": VERSION, "module_definitions": len(ids),
            "command_bindings": len(commands), "common_schema_documents": len(vs),
            "example_pairs": 1, "example_reference_hashes": "PASS",
            "scope": "Design-pack consistency and common-envelope fixtures only; no runtime modules were integrated."}


if __name__ == "__main__":
    print(json.dumps(validate_pack(), indent=2))
