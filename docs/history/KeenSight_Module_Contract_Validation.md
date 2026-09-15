# Validation scope — module interface design pack

## Executed for this design

- Inspected the supplied collector 0.1.0 source, public record definitions, command coverage and canonical-admission boundary, plus v4.1 schemas and the repository/module plan.
- Reran the existing collector source suite: **155 passed, 1 skipped**. The skipped integration imports `scrapling.fetchers`, which is unavailable in this environment. Native browser capture remains disabled in the supplied collector. No new live acquisition was performed.
- Validated **4 common protocol JSON Schema documents** (Draft-07), including their internal reference resolution.
- Validated **30 module ownership definitions** and **38 unique command-to-module bindings**.
- Validated **1 synthetic request/result pair** and its four illustrative referenced records' hashes.
- Ran the design-pack tests: **33 passed**. They cover envelope closure, execution/result identity, trace format, date validation, chronology, cross-tenant references, contradictory immutable-reference metadata, non-success output restrictions, diagnostic codes, and explicit monetary uncertainty.

## What this does not verify

This is a proposed interface baseline, not a new collector or canonical-platform release. No existing runtime file or GitHub repository was changed. The common envelopes have not been wired into the collector. The tests do not establish full live or producer/domain/evidence correctness, authentication, source entitlements, semantic input closure, database transaction guarantees, or external-effect reconciliation.

`modules.json` describes named input/output vocabularies across each module. Each public operation still needs its exact domain-payload schemas, multiplicity rules, implementation and semantic checks before activation. Some named request/report types are proposed projections, not already-issued schemas. Generic RecordRef validation cannot substitute for those checks.

The example payloads are deliberately labeled `protocol-fixture`, not production Fact or ScanBundle records. Their hashes validate the illustrative bytes only. The 33 new tests are not added to the collector's 155-test count, and the full v4.1 architecture test suite was not rerun in this pass.

The previously unclosed v4.1 ChangeRecord authorization issue F remains a hosted/multi-tenant production blocker. Adding a trace, a tenant field or a self-declared security-context identifier does not fix authorization.

## Reproduction

```bash
python -m pip install -r requirements.txt
python validate_protocol.py
python -m pytest -q
```

The dependency ranges here are for checking this documentation/contract draft. They are not a replacement for the production application's exact dependency lock. Input hashes are recorded in BASELINE_SOURCES.json.
