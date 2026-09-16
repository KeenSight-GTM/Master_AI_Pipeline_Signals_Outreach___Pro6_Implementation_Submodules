# POC/submodule repair verification — 2026-09-15

Base: GitHub main `6ec6640293d41597296b7ba61e91f6e0a586e611`. Verification applies to the repaired collector 0.3.0 / ScanBundle 1.2, canonical 4.2.0 reference and protocol checker, not proposed production services.

## Executed locally

| Suite | Passed | Failed | Skipped |
|---|---:|---:|---:|
| Collector | 197 | 0 | 1 |
| Canonical | 620 | 0 | 0 |
| Protocol | 47 | 0 | 0 |
| Workspace | 14 | 0 | 0 |
| POC acceptance | 14 | 0 | 0 |
| Iteration-2 acceptance | 22 | 0 | 0 |
| **Total** | **914** | **0** | **1** |

Before the patch, the two audit suites reproduced 9+16 failures. After the patch, their original assertions all pass; no audit file was changed or xfailed. Thirty new component regressions supplement them. Two existing collector tests were adapted only to the runtime version and explicit historical candidate-query time.

The root verification command now executes eleven stages: five generation/design checks, four existing component/workspace suites and both audit suites. All return zero. Eight offline journeys completed with twenty subprocess invocations and expected exit codes. They use synthetic/reference data; the canonical journey is not a collector-to-canonical bridge test.

Deleting all canonical generated directories and the release manifest in an isolated copy, then regenerating, produced **116 byte-identical files**. A subsequent `--check` passed. Domain breadth remains 213 predicates, 89 metrics and 75 canonical schemas.

Machine-readable counts: [POC_REPAIR_RESULTS.json](POC_REPAIR_RESULTS.json). Source changes and compatibility: [POC_REPAIRS.md](../docs/POC_REPAIRS.md).

## Not established by these results

The live Scrapling SDK is unavailable in the local environment, so one test is explicitly skipped. `live-check` remains a hard failure without the pinned SDK; a separate GitHub CI job is provided to exercise it when installable. No native browser, hosted authentication, canonical bridge, broad provider runtime, sending, reply or CRM workflow was exercised. Predicate-specific valid-time policy remains a design question.

Original assembly, repair and audit logs are retained as history. Current source integrity uses the refreshed root manifest; the original component manifest intentionally no longer matches edited files.
