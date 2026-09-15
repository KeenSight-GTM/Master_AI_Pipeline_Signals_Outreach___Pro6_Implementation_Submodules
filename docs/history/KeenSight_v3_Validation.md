# KeenSight v3 validation report

Verified on September 14, 2026 in Linux with Python 3.13.5, jsonschema 4.26.0 and pytest 9.0.2.

## Actual results

| Check | Result |
|---|---|
| Regression suite | **148 passed; 0 failures/errors** |
| Draft-07 schema documents | 36, structurally valid |
| Generated registry JSON files | 14 |
| Typed predicate registrations | 87 — original 79 plus 8 explicit additions |
| Derivation flows | 23 with registered sources and outputs |
| Signal types | 18 |
| Synthetic instance records | 27 |
| Frozen numerical-kernel fixtures | 46 |
| Adversarial schema/semantic mutation cases | 46; all rejected without relying on release checksums |
| Dependency graph | 149 nodes, 468 typed edges; zero same-epoch cycles |
| Generated JSON files | 78 |
| Repeated generation | Byte-identical |
| Clean-room regeneration with schemas/registry/instances removed | Same paths and bytes; validator passes |
| Original uploaded archive | Unchanged |
| Remote repository changes or provider operations | None |

The 148 tests include the 46 kernel fixtures and 46 targeted rejection mutations; they are not 148 independent production defects, a coverage percentage, or a live-system accuracy estimate. Kernel fixtures are fixed authored expectations. The clean-room comparison uses the same recorded interpreter/environment; it is not a claim that every operating system, dependency version or architecture has been tested.

## Tested failure boundaries

Unsupported whole-message copy and question premises; UNKNOWN/absence/cross-account/candidate/stale/unbound hook evidence; candidate ancestry; incorrect or duplicate pack membership; empty resolved signals; invalid states/reasons/timestamps/TTLs/object values/operators; missing/incomplete/truncated/misattributed absence coverage; dangling references; missing execution/raw evidence; false derived fixture output; incorrect claim slots; output/reference linkage; self/multinode/control/provenance cycles; missing graph edges/endpoints; dirty propagation after authority, binding, membership, expiry, retraction or release changes; unsupported kernel version; multivendor/source retention; UNKNOWN non-eviction; numerical eligibility, rank-tie, zero-variance, temporal and repeated-exposure boundaries.

## What this does not prove

The bundle implements design-time generation/validation and pure reference helpers. It does not implement or test a persistent journal writer, production JCS serializer/hash chain, database replay/recovery, real fact-to-feature materializers, a complete extraction/subject-resolution scanner, a complete dynamic confound engine, paid API adapters, an LLM gateway/repair service, atomic budget reservations, durable job leases, outbox dispatch, provider reconciliation, CRM sync, privacy erasure or a real gold set.

The synthetic package is APPROVED only in DESIGN_TEST. Sources are fixture-only; production is disabled. The first claim renderer supports an observed vendor plus a vetted neutral question. Other operator names are reserved and fail closed until implemented.

Seven editable Mermaid diagram sources are included. Their source was reviewed for consistency; a Mermaid renderer/visual-layout test was not executed.

## Reproduce

```bash
python generate_structures.py --check
python validate.py
python -m pytest -q
```

See `reports/pytest.xml`, `reports/pytest.log`, `reports/validation.json` and `reports/reproducibility.json` for machine-readable evidence.
