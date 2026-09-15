> **Review-and-repair 2026-09-15:** This subpackage is patched. Use the package-root README and `verification/REPAIR_REPORT.md` for current status, compatibility, tests, and remaining work. The historical narrative below is retained for context.

# KeenSight module and I/O contract design

**Proposed design only.** No collector or canonical application code was modified.

Start with `DESIGN.md`, then `MODULE_MATRIX.md` for all 30 modules and their submodules/inputs/outputs. `modules.json` is the machine-readable ownership inventory, not a runnable pipeline. `command_bindings.json` preserves all 38 collector command IDs. `schemas/` contains four common protocol draft schemas, and `examples/` contains explicitly non-production envelope fixtures.

The current collector's `Observation` remains distinct from canonical `Fact`. This design standardizes invocation, errors, references and diagnostics; it does not replace domain schemas with an untyped generic record.

Validate this design pack:

```bash
python -m pip install -r requirements.txt
python validate_protocol.py
python -m pytest -q
```

The result checks common-envelope and catalog consistency only. It does not prove that live collectors, all planned DTO schemas, authentication, canonical admission or sending have been implemented. See `VALIDATION.md` for the exact scope and original collector test rerun.
