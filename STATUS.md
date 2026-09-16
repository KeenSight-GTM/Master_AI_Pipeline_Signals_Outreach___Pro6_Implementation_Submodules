# Current implementation status

Snapshot: **2026-09-15-poc-repairs.1**. Code base: repository `main` at `6ec6640293d41597296b7ba61e91f6e0a586e611`. Machine-readable counterpart: [STATUS.json](STATUS.json).

## Implemented repairs

Collector **0.3.0 / ScanBundle 1.2** fixes deterministic multipage reports, bounded same-origin robots redirects, explicit failed-GET retries, gzip sitemaps, common discovery ranking, candidate/research projections, account identity in claim views, parser-loss reporting, one-payload publication, invocation identity, and no-byte diagnostic persistence.

Canonical **4.2.0 reference implementation** now includes binding evidence in eligibility (not corroboration), checks current renderer authority at standalone export, resolves supersession in the selected claim group, shares generated-artifact availability and origin-count logic, rejects cycles cleanly, and compares numeric values semantically without altering original hashes.

The protocol checker permits truthful late failure diagnostics but rejects late positive publication and modes/effects forbidden by its installed reference signature. It is not yet a runtime sandbox.

## Verification

**914 tests pass; one optional live SDK test is skipped locally.** Totals include both repaired audits (14 POC + 22 iteration-2 tests), 30 added component regressions, and the existing workspace tests. No original audit assertions were removed or weakened. Eight offline journeys (20 subprocess commands) pass. Canonical generated artifacts remain reproducible.

`verify` includes both audit suites. CI also declares a separate mandatory SDK-import/loopback job; a declared CI job is not evidence that it ran. See the published commit's Actions results for remote status.

## Explicit boundaries

The broad catalog remains **213 predicates, 89 metrics and 75 canonical schemas**. All 38 collector command IDs remain, but native browser execution is disabled and no full donor/2,500-signature integration is claimed. Collector output is still a pre-admission record family, not an authenticated canonical Fact Service.

The canonical fixture exporter is not hosted review or sending. Contacts, campaigns, enrichment providers, dispatch/reconciliation, replies, CRM and the general module runner remain outside this repair. F16's predicate-specific valid-time semantics remain undecided. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Document precedence

This file, the root README, [POC_REPAIRS.md](docs/POC_REPAIRS.md), and [POC_REPAIR_VALIDATION.md](verification/POC_REPAIR_VALIDATION.md) describe the current snapshot. Original assembly, repair, and audit reports remain historical evidence; their old failing counts do not supersede these verified repairs.
