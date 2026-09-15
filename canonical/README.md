> **Review-and-repair 2026-09-15:** This subpackage is patched. Use the package-root README and `verification/REPAIR_REPORT.md` for current status, compatibility, tests, and remaining work. The historical narrative below is retained for context.

# KeenSight v4.1 — selected end-to-end fixes and the 52-idea ledger

**Preserve broad facts; control what can be concluded or exported.** This is a patched contract/reference-code bundle, not a production application.

Implemented scope: prior-audit **A–E, G, H**. **F/E07 is not fixed.** Production and sending remain disabled.

## Review

- [Architecture and selected fix semantics](SYSTEM.md)
- [All 52 ledger ideas: classification and e2e location](docs/LEDGER_INTEGRATION.md)
- [Machine-readable 52-row map](docs/LEDGER_MAP.json)
- [Complete rendered UML book](KeenSight_v4_1_Diagrams.html)
- [Editable diagrams](docs/DIAGRAMS.md) and [all fields/classes](docs/CLASS_REFERENCE.md)
- [Measured validation](VALIDATION.md)
- [Known limitations and deliberately deferred fix F](docs/KNOWN_LIMITATIONS.md)

## Verify

```bash
python -m pip install -r requirements.txt
python generate.py --check
python validate.py
python -m pytest -q
```

Author contracts in `shapes.py`, `catalog.py`, `ledger_catalog.py` and the bootstrap modules; regenerate with `python generate.py`. Semantic guard code is in `validation.py` and `completion.py`; the no-send local reference exporter is in `handoff.py`. `python build_diagrams.py` requires Graphviz and rebuilds all 14 SVG/Mermaid views and the class reference.

75 schemas; 213 predicate definitions (197 retained + 16 added); 89 metrics; 225 synthetic records. Existing v4 API shapes gained required fields, so this design revision is not a drop-in wire-compatible schema upgrade.

The archived v4 and v3 material in `reference/` is non-normative history. Its old counts/statuses are not the status of this revision.
