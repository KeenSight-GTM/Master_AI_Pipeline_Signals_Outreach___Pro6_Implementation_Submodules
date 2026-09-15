#!/usr/bin/env python3
"""Validate planning traceability; this does not execute the proposed crawler."""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
import hashlib

def load(root: Path, filename: str):
    return json.loads((root / filename).read_text(encoding="utf-8"))

def main() -> None:
    root = Path(__file__).resolve().parent
    phases = load(root, "phases.json")
    actions = load(root, "command_plan.json")
    modules = load(root, "modules.json")
    book = load(root, "workbook_extracted.json")
    ledger = load(root, "reference_52_ledger_map.json")
    work = load(root, "work_items.json")
    ids = {p["id"] for p in phases}
    assert len(ids) == len(phases) == 10, "Duplicate or missing phase"
    graph = {p["id"]: set(p["depends_on"]) for p in phases}
    assert all(d in ids for ds in graph.values() for d in ds), "Unknown prerequisite"
    seen, active = set(), set()
    def visit(node: str) -> None:
        assert node not in active, f"Cycle at {node}"
        if node in seen:
            return
        active.add(node)
        for dep in graph[node]:
            visit(dep)
        active.remove(node)
        seen.add(node)
    for node in graph:
        visit(node)
    # All later phases are reachable from the same reproducible baseline.
    def ancestors(node: str) -> set[str]:
        return set(graph[node]).union(*(ancestors(x) for x in graph[node])) if graph[node] else set()
    assert all("P0" in ancestors(x) for x in ids if x != "P0")
    rows = book["02_COMMAND_CATALOG"]
    headers = rows[0]
    expected = [dict(zip(headers, row)) for row in rows[1:] if row[0]]
    expected_ids = [r["Command ID"] for r in expected]
    assert len(expected_ids) == len(set(expected_ids)) == 38
    assert [a["command_id"] for a in actions] == expected_ids, "Commands changed or missing"
    roots = {(m["repo"], m["module"]) for m in modules}
    for a, original in zip(actions, expected):
        assert a["source"]["original"] == original, "Original workbook row altered"
        assert a["source"]["row"] == expected_ids.index(a["command_id"]) + 2
        assert a["repo"] == "scrapling-ingestion"
        assert (a["repo"], a["module"].split(".")[0]) in roots
        assert a["first_delivery_phase"] in {"P1", "P2"}
        assert a["completion_phase"] == "P2"
        assert a["implementation_status"] == "PLANNED"
        assert a["output"] and a["acceptance_focus"]
    assert len([a for a in actions if a["command_id"].startswith("EXTRACT_")]) == 17
    assert {r["id"] for r in ledger} == set(range(1,53))
    assert len({w["id"] for w in work}) == len(work) == 61
    assert all(w["phase"] in ids and w["status"] == "PROPOSED_NOT_CREATED" for w in work)
    assert all(m["first_phase"] in ids for m in modules)
    checks = {
        "status": "PASS",
        "scope": "Planning traceability only; not proposed runtime behavior",
        "workbook_sheets": len(book),
        "original_commands": len(actions),
        "extraction_commands": 17,
        "all_commands_assigned_to_collector": True,
        "command_completion_gate": "P2",
        "phases": len(phases),
        "phase_dependency_graph": "ACYCLIC",
        "modules": len(modules),
        "work_items": len(work),
        "preserved_ledger_ids": len(ledger),
        "baseline_reference_tests": "588 passed (see baseline-check.txt)",
        "donor_repository_tests_run_here": False,
        "new_crawler_implemented_here": False,
        "github_mutations": False,
    }
    print(json.dumps(checks, indent=2))
    (root / "plan_validation.json").write_text(json.dumps(checks, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
