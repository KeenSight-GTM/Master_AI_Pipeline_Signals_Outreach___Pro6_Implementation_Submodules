# Code repair report and compatibility — 2026-09-15

## Scope and status

This release **changes local code**, not only diagrams. It is based on the uploaded collector 0.1.0, canonical reference v4.1, shared-protocol proposal, full E2E design and previous audit. No GitHub repository, live account, provider, CRM or production database was modified.

- Collector **0.2.0**: deterministic local runtime and independently invocable operations repaired.
- Canonical contracts/reference functions **4.2.0**: selected admission, chronology, corroboration, current-use and mutation checks repaired.
- Shared protocol: checker hardened; the common enforcing runner is still missing.
- Product: 39 logical modules and future product record definitions remain a design, not 39 working services.

## Executed verification

| Package | Passed | Skipped | Failures/errors |
|---|---:|---:|---:|
| collector | 183 | 1 | 0 |
| canonical | 609 | 0 | 0 |
| protocol | 42 | 0 | 0 |

**834 tests passed, one skipped.** This is 58 added regression cases relative to the prior 776-passing baseline; the old positive tests are retained. Two old fixture expectations were deliberately adapted: collector code-version pinning, and an authorized source-revocation fixture now supplies the newly required actor/typed-target/recorded-time fields. No test was disabled to hide a defect.

The real Scrapling HTTP integration is the skipped test because `scrapling.fetchers` is unavailable here. Installation was attempted and did not succeed in this environment. That is not evidence that the public release does not exist. Native browser capture is disabled. No live-site accuracy, service deployment, paid provider, or sending behavior was tested.

Other executed checks:

- All 116 canonical generated files are byte-identical after deletion and clean regeneration.
- Canonical full bundle validation passes: 75 schemas, 213 predicates, 89 metrics and 225 synthetic records.
- A rebuilt wheel was installed into a fresh import directory; demo, extraction, matching, bundle check, historical claim resolution and CLI evidence check ran in separate processes using that installed wheel, not the source tree. These are offline fixture runs.
- Document inventory verifies 27 stage cards, 39 logical modules, 38 retained collector command IDs, 119 named record/value-object classes, 31 rendered SVG views and eight proposed service groups.
- Every rendered view has an editable Mermaid source. SVGs were parsed and selected complex class/flow renderings were visually inspected. Service/state sequence graphics are static review renderings; the machine-readable Mermaid sources are included.

Test counts are evidence of these cases, not a proof of correctness on every input or of a working E2E product.

## Findings and repairs

| Audit ID | Status and exact repair |
|---|---|
| C01 | **REPAIRED_AT_LOCAL_STORE_BOUNDARY** — Capture metadata must exactly match its trusted immutable database row before the original blob is read. Headers, time, mode, source, subject, status, completeness and TTL are bound. CLI checks also re-extract exact surfaces and command records. |
| C02 | **REPAIRED_REFERENCE_VALIDATION** — Rule evaluation reports and producer outcomes are recomputed; failed extract/match commands cannot retain eligible positive surfaces or matches. Required extraction command coverage is checked for selected captures. |
| C03 | **REPAIRED_SCANNER_PUBLICATION** — Validate complete evaluation first, then commit findings, support, research features, replay selection and evaluation manifest in one SQLite transaction. Raw captures/diagnostics may remain after failure; eligible findings do not. Fault-injection verifies rollback. |
| C04 | **REPAIRED_WITH_FORMAT_CHANGE** — ScanBundle 1.1 and stored replay selection identify captures actually selected for technical evaluation. Replay no longer reclassifies HTTP-200 robots HTML or discards originally sniffed HTML just because Content-Type is absent. |
| C05 | **REPAIRED_REFERENCE_MATCH_REPORTS** — Required missing/partial extraction surfaces produce PARTIAL, and no evaluated page produces NOT_EVALUATED; neither is a complete NO_MATCH. This release does not manufacture absence facts. |
| C06 | **REPAIRED_LOCAL_RESUME** — Rate-limit cooldown is persisted and checked on reused as well as fresh attempts. Retry-After seconds/date is handled; fallback is conservative. No claim of a distributed rate-budget service. |
| C07 | **REPAIRED_WITH_DIGEST_CHANGE** — Rule digest includes the resolved canonical product as well as the authored definition, so alias changes invalidate old semantic authorization. |
| C08 | **REPAIRED_EXTRACTOR** — Deterministic BOM/HTTP charset/HTML declaration/UTF-8 fallback policy; decoding choice is retained. Explicit HTTP UTF-8 non-ASCII regression passes. |
| C09 | **REPAIRED_NARROW_CONTEXTS** — Collector retains script type and INERT_SCRIPT context; presence matching excludes inert script MIME types. Canonical narrow matcher also excludes template/noscript/footer/aside. These rules do not constitute full browser execution verification. |
| C10 | **REPAIRED_TESTED_INPUT_BOUNDARIES** — Malformed discovered sitemap URLs are locally diagnosed, and non-string/unhashable donor IDs are quarantined instead of crashing the batch. Not a universal malformed-input fuzzing proof. |
| C11 | **REPAIRED_DETERMINISTIC_PROJECTIONS** — Priority/negative-selection outputs and rule/producer reports are recomputed. Other future provider or policy receipts still need their runtime authority boundary. |
| A01 | **REPAIRED_REFERENCE_CORROBORATION** — Full provenance remains available; substantive corroborating artifacts exclude model request/response/repair records and follow transforms back to original substantive origins. |
| A02 | **REPAIRED_REFERENCE_CURRENT_USE** — Historical evaluation retains the frozen inputs. Current-use eligibility examines all currently recorded same-claim observations and ancestral claim groups, blocking newly introduced conflicts. |
| A03 | **REPAIRED_MODEL_ARTIFACT_CONTRACT** — External inputs and run-produced artifacts are separate manifests. Successful producer output declarations, time windows, uniqueness and consumer chronology are enforced for model request/response/repair artifacts. |
| A04 | **REPAIRED_REFERENCE_AUTHORIZATION_NOT_HOSTED_AUTH** — ChangeRecord requires actor, typed target and recorded time; tenant ownership, grant permission, replacement compatibility and timing are checked. Invalid records are rejected and do not mutate usability. Trusted ActorGrants are configuration in this reference package, not authenticated user sessions. |
| A05 | **REPAIRED_NARROW_FINGERPRINT_ADMISSION** — Actual technology footprint matched host must be found by the registered narrow matcher in the fact’s retained artifact. Fixture success alone no longer authenticates the matched value. Full donor/collector-to-canonical bridge remains unimplemented. |
| P01 | **PARTIAL_CHECKER_HARDENED_RUNNER_NOT_IMPLEMENTED** — A trusted signature allowlist and payload resolver enforce consumed-reference closure, operation/schema versions, minimum inputs, output shape, digests and deadlines for the delivered fixture operation. General execution middleware, all handlers, read instrumentation, effects and hosted authentication are not implemented. |

## Additional boundary found during patching

A caller could supply a hand-edited `PageEvidence` object whose surfaces did not come from the stated capture. The public evaluation and independent matching path now re-extract and compare the entire record against trusted original bytes, including its producer reports. A separate injected-persistence-fault test confirms all findings roll back together. The local Store remains a trusted owner API; access to its private database is not authenticated by these checks.

## Compatibility changes are deliberate

1. **ScanBundle schema 1.1** adds required `evaluated_capture_ids`. Runs pin collector 0.2.0 and changed compiled rule digests. Do not silently resume a 0.1.0 run under new semantics.
2. Old stores lacking a successful technical replay-selection manifest require an explicit reviewed import or recapture. No capture date or coverage history may be fabricated to populate it.
3. Canonical schema IDs now use **v4.2**. BatchRun requires `produced_artifact_ids`; ExecutionRecord requires `output_artifact_ids`. Existing retained transcripts can remain external inputs; newly generated model artifacts need real producing execution closure.
4. ChangeRecord requires `actor_id`, `target_type`, `recorded_at` and compatible permission/target semantics. Unauthenticated old records are not grandfathered in. Future scheduled changes use a separate scheduling command, not an effective timestamp after the record's time under this reference contract.
5. The protocol allowlist registers the fixture `FP-01.match` operation only. A new implementation needs an explicitly registered signature and exact payload validators. It is unsafe to advertise the checker as a deployed generic plugin or service runtime.

## Where the former F issue stands

F's cross-tenant/replacement bug is fixed **in canonical reference validation and usability checks**. Negative tests cover unknown actors, wrong tenants, wrong target types, missing replacements and invalid chronology. The concrete local collector still assumes its local owner is trusted. Hosted authentication, grant administration and a concurrency-safe canonical mutation transaction have not been built; therefore reference authorization passing is not hosted multi-tenant sign-off.

## Remaining implementation blockers

- Actual pinned Scrapling SDK HTTP test and bounded native browser integration.
- Full donor rule import characterization, reviewed distribution and vendor/calibration catalog.
- Executable collector Observation/Support to canonical Fact admission bridge and production identity resolution.
- Persistent canonical repository and authenticated trusted grant/current-restriction system.
- General module runner: operation registry, exact reads, reference resolution, domain validation, atomic publication and side-effect policy integrated with real handlers.
- All enabled broad-source collectors/materializers/LLM provider calls, production research/compound-signal functions, and source-rights enforcement.
- Contacts, campaigns, enrollment, messaging, replies, CRM, outbox and provider reconciliation runtime.
- Restore/load/concurrency/security and live accuracy acceptance tests.

These are not solved by adding containers around reference functions. Retain the module boundaries and extract services only after the runbook's ownership, identity, idempotency and failure gates are met.

## Reproduce

```bash
python -m pip install -e './collector[test]'
python -m pip install -r ./canonical/requirements.txt
(cd collector && python -m pytest -q)
(cd canonical && python generate.py --check && python validate.py && python -m pytest -q)
(cd protocol && python validate_protocol.py && python -m pytest -q)
python verification/check_document_inventory.py
```

Raw XML/text results, installed-wheel process logs, clean-generation evidence, repair dispositions and source patches are included in this directory. The previous audit source is not silently replaced: `baseline_audit_findings.json` preserves the original finding definitions.
