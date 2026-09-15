# KeenSight code and end-to-end completeness audit

Date: 2026-09-15. Scope: the four uploaded local archives listed in `audited_input_hashes.json`.

## Verdict

The supplied material is a working local collector/reference test foundation plus an E2E product blueprint, not an implemented end-to-end product. The baseline tests pass, but additional executed probes reveal integrity, provenance, replay, publication and current-use gaps. Do not treat design-check counts or fixture counts as deployed capability counts.

This audit did not patch application behavior or modify either GitHub repository. It added executable reproduction scripts, machine-readable findings and an explicit incompleteness inventory. Source directories retain their uploaded implementation bytes (Python caches/test logs are excluded from the review-package source hashes).

## Baseline verification

| Package | Command / scope | Observed result |
|---|---|---|
| Collector 0.1.0 | `python -m pytest -q` | 155 passed, 1 skipped |
| Canonical contracts 4.1 | `python -m pytest -q` | 588 passed |
| Canonical contracts 4.1 | `python generate.py --check`; `python validate.py` | 116 generated files match; 75 schemas, 213 predicates, 89 metrics, 225 example records validate |
| Module protocol draft | `python -m pytest -q`; `python validate_protocol.py` | 33 passed; envelope/catalog example validation passes |
| Full E2E product design | `python validate_design.py` | PASS_DESIGN_INVENTORY_ONLY: 39 declared modules, 32 proposed product contracts, 38 command bindings and 5 acyclic example plans |

Total existing pytest results: **776 passed, 1 skipped**, across separate suites. These are not 776 end-to-end business scenarios. The 31 extra probes are 16 collector, 6 canonical/reference, and 9 common-protocol probes. They include controls and known limitations; they are not 31 independent bugs. See the raw results and per-finding reproductions.

The separate required-safety suite produced **25 failed expectations and 4 passing controls** on the unchanged code. Those failures are deliberately retained to show what must be repaired; they are not included in the 776 original passing tests.

## Test limitations

The actual Scrapling package is absent. Both the ordinary and explicit public-index download attempts failed in this environment; the logs do not establish that the version does not exist. The pinned official Scrapling source and package metadata were checked separately. Native browser capture remains disabled. No live target scan, provider/model call, donor-repository full-suite run, contact enrichment, campaign, send, CRM mutation or reply workflow was executed.

The source audit covers all 15 collector source modules; the important execution, eligibility, identity, lineage, rendering, export and validation code in the canonical reference package; the common protocol checker; and the product-design checker. Catalog prose and field lists are inspected as specifications, not claimed runtime implementation.

## Findings by priority

P1 means correct before live canonical admission, hosted mutation, or the affected downstream action. It does not mean a production incident was observed. P2 means a correctness/reliability defect to repair before claiming the affected capability complete.

| ID | Priority | Finding |
|---|---|---|
| C01 | P1 | Capture metadata is not bound to the stored authoritative record |
| C02 | P1 | Successful claim output can contradict failed producer diagnostics |
| C03 | P1 | Failed evaluation can publish supported findings to SQLite |
| C04 | P1 | Replay does not preserve live capture eligibility |
| C05 | P1 | Incomplete or absent extraction is reported as ordinary NO_MATCH |
| C06 | P1 | Resume forgets rate-limit state |
| C07 | P2 | Rule authorization digest excludes product-alias semantics |
| C08 | P2 | HTTP character encoding is ignored by extraction |
| C09 | P2 | Inert script contexts are not consistently modeled |
| C10 | P2 | Malformed source inputs escape local quarantine/diagnostics |
| C11 | P2 | Priority and diagnostic reports are not reproducibly validated |
| A01 | P1 | Model transcripts inflate corroboration counts |
| A02 | P1 | A refreshed current-use gate ignores newly admitted conflicts |
| A03 | P1 | In-run model artifacts cannot satisfy the frozen-input contract |
| A04 | P1 | ChangeRecord authorization remains open (previously deferred F) |
| A05 | P1 | Canonical fingerprint facts are not re-derived from their actual evidence |
| P01 | P1-before-integration | The proposed common protocol is structural, not an enforcing runtime interface |

## Detailed findings

### C01 — Capture metadata is not bound to the stored authoritative record

**Priority:** P1

**Observed:** Both probes pass the actual CLI check with --store and original_bytes_checked=true. One changes the capture date from September 14 to October 14 and recomputes a SUPPORTED October 15 claim. The other keeps the original no-embed HTML bytes but supplies a fabricated x-powered-by header and produces a supported product claim.

**Cause:** Store.body verifies the blob path and byte hash, but does not compare the supplied Capture metadata with the immutable captures table. CLI re-extraction then trusts the supplied headers, timestamp and other metadata. The capture_id is not recomputed or verified against that metadata.

**Required repair:** Resolve capture_id through the trusted store; compare the entire immutable capture record or its separately pinned digest before parsing or admission. Use trusted stored metadata for re-extraction. Test changes to timestamp, headers, source, subject, mode, completion and TTL, not only altered body bytes.

**Scope:** Demonstrated in local check/import paths; no remote attack or deployed incident was tested.

**Reproduction IDs:** `capture_timestamp_tamper_with_original_bytes_check`, `capture_header_tamper_creates_fact_with_byte_check`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/storage.py:122–131`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/cli.py:69–86`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/validation.py:23–41`.

### C02 — Successful claim output can contradict failed producer diagnostics

**Priority:** P1

**Observed:** A bundle with EXTRACT_SCRIPT_SRC=FAILED, MATCH_HOST_SUFFIX=FAILED and the rule evaluation=ERROR still validates and retains a SUPPORTED claim.

**Cause:** validate_bundle recomputes matches but discards the computed rule-evaluation report. It checks command-ID coverage, not producer state, execution links or completeness.

**Required repair:** Bind each output to a producing execution, compare executable rule evaluations and reject positive publication from failed producers. Validate command status and result linkage separately from the fact that all 38 command names appear.

**Scope:** The tested records were modified contradictory reports; this is a validation failure, not proof that a failed matcher spontaneously returned a false hit.

**Reproduction IDs:** `failed_command_and_rule_produce_supported_claim`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/validation.py:35–52`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:177–213`.

### C03 — Failed evaluation can publish supported findings to SQLite

**Priority:** P1

**Observed:** Calling evaluate with a duplicate PageEvidence fails with Duplicate captures identity. Nevertheless, one observation and its support have already been committed and stored_claims returns SUPPORTED.

**Cause:** save_findings and harvest run before final bundle validation, with their own commits. Publication is not gated by a committed successful evaluation.

**Required repair:** Validate candidates and input uniqueness before publication. Commit the validated evaluation manifest, observations and support atomically; keep failed-run diagnostics separate from currently eligible findings. Add interruption/fault-injection tests around every publication step.

**Scope:** Retaining diagnostic/raw evidence after failure is acceptable. Publishing eligible claim support without a successful corresponding evaluation is the concern.

**Reproduction IDs:** `failed_bundle_validation_leaves_supported_database_claim`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:177–213`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/storage.py:133–148`.

### C04 — Replay does not preserve live capture eligibility

**Priority:** P1

**Observed:** A robots.txt response containing HTML makes the original run fail closed with zero claims; replay turns that same response into one SUPPORTED technology claim. Conversely, an HTML page admitted by content sniffing without a Content-Type header produces one live claim and zero on replay.

**Cause:** Replay selects all complete HTTP-200 captures with an HTML Content-Type. It does not retain or reuse original resource roles, evaluation eligibility and content classification. Live and replay have separate selection logic.

**Required repair:** Persist a typed capture disposition/role and parser eligibility manifest. Reuse one eligibility/classification function in live and replay. Treat intentionally changed eligibility policy as a new, explicit evaluation policy; do not silently reinterpret a policy-denied metadata response.

**Scope:** Both cases use the same pinned rules and retained captures with no additional acquisition.

**Reproduction IDs:** `replay_admits_policy_rejected_robots_html`, `replay_drops_sniffed_html_with_missing_content_type`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:104–170`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:215–229`.

### C05 — Incomplete or absent extraction is reported as ordinary NO_MATCH

**Priority:** P1

**Observed:** A page with 2,001 script elements has EXTRACT_SCRIPT_SRC=PARTIAL/ITEM_LIMIT, but the detector reports NO_MATCH when the matching script is beyond the 2,000-item limit. With acquisition entirely failed, matcher commands are still COMPLETE and rule output is NO_MATCH.

**Cause:** Matching considers Capture.complete but ignores surface-specific CommandResult state. The zero-page case is not distinguished from a successful empty detector search.

**Required repair:** Declare required surface capabilities per rule. Use INCOMPLETE/NOT_EVALUATED/UNKNOWN when required extraction or capture did not complete; retain explicitly verified positive support from a complete element only under a declared partial-evidence policy.

**Scope:** The current collector does not emit absence facts, which prevents an immediate false NOT_FOUND. The erroneous detector status would still mislead diagnostics and downstream coverage.

**Reproduction IDs:** `partial_extraction_reported_as_complete_no_match`, `all_acquisition_failed_bundle_no_attempt_records`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:55–75`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:149–180`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:177–213`.

### C06 — Resume forgets rate-limit state

**Priority:** P1

**Observed:** The first scan captures HTTP 429 on the homepage and skips the sitemap. Immediately resuming the same run reuses the 429 capture but issues a new sitemap request despite Retry-After: 3600.

**Cause:** denied is only set on newly fetched 429 responses. The reused-capture return path does not reapply rate-limit state, and no durable cooldown is recorded.

**Required repair:** Persist per-origin cooldown/terminal-rate-limit disposition and apply it on both fresh and reused attempts. Check Retry-After and the current clock before any new request.

**Scope:** Fixture transport reproduces planner behavior without traffic to a third-party site.

**Reproduction IDs:** `resume_forgets_rate_limit`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:46–96`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:119–144`.

### C07 — Rule authorization digest excludes product-alias semantics

**Priority:** P2

**Observed:** Changing calendly from product:old to product:new changes the release but not the raw rule digest. Passing the new approved-rule digest set to stored_claims still marks product:old SUPPORTED.

**Cause:** The rule digest hashes the authored row, while emitted product_id is resolved through an external alias map. Current eligibility checks only that raw digest.

**Required repair:** Pin the semantic compiled rule/emission digest, including canonical product and mapping version, or authorize support by a release-plus-rule identity. A mapping change must require re-evaluation, not approve the previous meaning.

**Scope:** All support is retained correctly; the bug concerns which old support remains current under the new release.

**Reproduction IDs:** `alias_remap_keeps_old_product_currently_approved`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:50–72`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:115–131`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/claims.py:57–86`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/cli.py:102–109`.

### C08 — HTTP character encoding is ignored by extraction

**Priority:** P2

**Observed:** UTF-8 HTML with Content-Type: text/html; charset=utf-8 yields CafÃ© rÃ©sumÃ© instead of Café résumé.

**Cause:** The parser receives bytes but not the declared HTTP encoding. The raw-text view later follows the parser-selected encoding.

**Required repair:** Implement a deterministic encoding policy using valid transport charset, BOM and document declarations, with declared fallback and conflicts. Pin the decision and test non-ASCII text and quotes end to end.

**Scope:** This is reproducible text corruption that affects extraction, quotes and matching, not just presentation.

**Reproduction IDs:** `http_charset_ignored_during_parse`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:36–44`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:78–84`.

### C09 — Inert script contexts are not consistently modeled

**Priority:** P2

**Observed:** The collector promotes a script with type=text/plain to vendor.present under the narrow host rule. The canonical reference helper also matches scripts inside template and noscript, unlike the collector’s explicit inert-region exclusions.

**Cause:** External script surfaces drop the script type. Two separate fingerprint implementations have different context eligibility rules.

**Required repair:** Preserve script type and relevant attributes, distinguish stored marker vs potentially active embed, and reuse one detector implementation/fixture corpus at extraction and admission.

**Scope:** A public marker can still be retained as a mention. This does not prove that a third-party script executed.

**Reproduction IDs:** `inert_nonexecuting_script_promoted_to_presence`, `canonical_fingerprint_helper_disagrees_with_inert_scope`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/extraction.py:93–99`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/rules.py:152–157`; `architecture/keensight-architecture-v4.1/keensight_contracts/engine.py:110–139`.

### C10 — Malformed source inputs escape local quarantine/diagnostics

**Priority:** P2

**Observed:** An invalid sitemap URL in robots.txt aborts the scan instead of recording a skipped discovery item. A donor row with an array-valued id raises TypeError during Counter construction before the row-level quarantine loop.

**Cause:** Untrusted URL normalization and raw ID hashing occur outside per-item error handling.

**Required repair:** Validate source items before queue construction or counting. Quarantine invalid donor rows and produce per-resource dispositions without masking unrelated valid items.

**Scope:** Both are local malformed-input reliability failures, not authorized capability bypasses.

**Reproduction IDs:** `malformed_robots_sitemap_aborts_entire_scan`, `malformed_donor_id_bypasses_row_quarantine`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:104–119`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/importer.py:38–47`.

### C11 — Priority and diagnostic reports are not reproducibly validated

**Priority:** P2

**Observed:** Changing a demo score to 100 and its SCORE_HOST details accordingly still passes validate_bundle. Rule qualification and resource dispositions are similarly not tied to an executed result in the verifier.

**Cause:** Recomputation stops at the claim view. Derived commercial-priority and execution-report fields are trusted payloads.

**Required repair:** Recompute deterministic priority/qualification or mark these explicitly untrusted projections with separate producing executions. Do not let them acquire business significance before validation.

**Scope:** Priority is explicitly not a truth probability; this is still a reproducibility and debugging gap.

**Reproduction IDs:** `host_priority_not_recomputed`

**Code:** `collector/keensight-scrapling-ingestion/src/keensight_scrapling/pipeline.py:197–213`; `collector/keensight-scrapling-ingestion/src/keensight_scrapling/validation.py:39–52`.

### A01 — Model transcripts inflate corroboration counts

**Priority:** P1

**Observed:** A signal requiring three origins resolves with one job-statement fact because roots() returns the job artifact, model request, and model response. The full canonical validator passes.

**Cause:** The code uses all provenance roots to count independent supporting origins. Provenance dependencies and corroborating evidence are not the same set.

**Required repair:** Preserve complete provenance but separately compute substantive evidence origins. Model requests/responses/repairs, transformations, and duplicate syndications must not contribute independent support. Use a declared evidence-independence policy, not raw root counts.

**Scope:** This is a confirmed counterexample, not a measured field precision rate.

**Reproduction IDs:** `one_job_plus_model_io_meets_three_source_minimum`

**Code:** `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:65–86`; `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:367–382`.

### A02 — A refreshed current-use gate ignores newly admitted conflicts

**Priority:** P1

**Observed:** After adding a contradictory fact outside the reviewed run’s snapshot and refreshing the gate’s version vector, the complete current claim resolves CONFLICT, but gate_reasons is empty, ALLOW validates, and the full bundle validates.

**Cause:** The version vector notices that state changed, but decision_eligible still resolves only facts available in the old run. A fresh vector is not a fresh claim-resolution query.

**Required repair:** Keep frozen resolution for historical evaluation. Add a distinct current-use eligibility query over the authorized current claim group and current bindings/restrictions; pin that gate snapshot. A new conflict should hold export without rewriting historical approval.

**Scope:** The repro uses the local preview/export gate. Live sending is not implemented.

**Reproduction IDs:** `refreshed_current_use_gate_ignores_post_snapshot_conflict`

**Code:** `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:117–127`; `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:240–244`; `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:246–320`.

### A03 — In-run model artifacts cannot satisfy the frozen-input contract

**Priority:** P1

**Observed:** Moving a model response into its producing execution (17:00:30 within the execution starting 17:00) and correcting its capture-attempt chronology yields ARTIFACT_AFTER_CUTOFF because the acquisition/evaluation run cutoff is 16:30.

**Cause:** Model requests and responses are forced into input_artifact_ids, all of which must predate the knowledge cutoff. There is no separately typed set for generated execution artifacts.

**Required repair:** Separate sealed external inputs from run-produced artifacts. A generated response must link to a successful execution and be visible only to subsequent dependent operations; do not advance or rewrite the external input cutoff to accommodate it.

**Scope:** Existing imported fixture transcripts pass. The contract blocks the natural live gateway placement described by the architecture.

**Reproduction IDs:** `genuine_in_run_model_response_cannot_fit_input_snapshot`

**Code:** `architecture/keensight-architecture-v4.1/keensight_contracts/completion.py:368–397`; `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:328–332`.

### A04 — ChangeRecord authorization remains open (previously deferred F)

**Priority:** P1

**Observed:** A schema-valid retraction from tenant.foreign targeting tenant.demo changes usable(f.tech) from true to false.

**Cause:** ChangeRecord has no actor contract and eligibility checks match target IDs without validating tenant ownership or privileged global scope.

**Required repair:** Implement authenticated actor, typed target, tenant ownership, permitted transition, replacement compatibility and explicit privileged-global changes.

**Scope:** Previously acknowledged, not a newly discovered regression. It blocks hosted/multi-tenant mutation.

**Reproduction IDs:** `known_F_cross_tenant_retraction`

**Code:** `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:93–119`.

### A05 — Canonical fingerprint facts are not re-derived from their actual evidence

**Priority:** P1

**Observed:** Changing f.tech.object.matched_value to an unsupported hostname leaves the full validator green. Registered fingerprint fixtures pass, but the supplied fact’s claimed match is not checked against its specific artifact.

**Cause:** The fact path checks output/product/capture-mode compatibility, whereas actual matching is executed only against the rule’s declared fixtures.

**Required repair:** Canonical admission must consume and validate a successful concrete FingerprintMatch/execution with exact retained surfaces; share the detector with the collector. Fixture success cannot authenticate future observations.

**Scope:** This is a missing admission connection, not a requirement to rerun every possible source extractor on every read.

**Reproduction IDs:** `fingerprint_fact_matched_value_not_checked_against_capture`

**Code:** `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:214–221`; `architecture/keensight-architecture-v4.1/keensight_contracts/validation.py:496–520`.

### P01 — The proposed common protocol is structural, not an enforcing runtime interface

**Priority:** P1-before-integration

**Observed:** The draft pair validator accepts an unrequested consumed record, an unregistered operation, a success result with no consumed inputs, and an arbitrary output schema. Evaluation records can also report network calls or late success without an associated capability/outcome policy.

**Cause:** It validates envelope shape, IDs, registered module and cross-tenant reference shape. There is no implementation/operation signature registry, declared-input resolver, effect-policy executor, deadline semantics, or domain-output admission behind it.

**Required repair:** Implement operation-specific input/output signatures and an execution wrapper. Resolve manifests/records, validate consumed-input closure, domain payloads, capabilities/effects and publication. Decide cancellation/deadline semantics explicitly rather than treating a log timestamp as enforcement.

**Scope:** Documented draft limitation. No live module currently uses this envelope, so these are integration blockers rather than an exploitable deployed API.

**Reproduction IDs:** `unrequested_consumed_record`, `unregistered_operation`, `success_with_no_actual_inputs`, `wrong_output_schema`, `run_evaluate_reports_network_calls`, `deadline_overrun_is_unqualified_success`

**Code:** `protocol/keensight-module-design/validate_protocol.py:58–114`.

## Completeness inventory

| E2E stage | What physically exists | What remains unimplemented or unverified |
|---|---|---|
| Programs, account sourcing, contacts | Proposed module IDs, records and workflows | Production schemas for the new records, handlers, persistence, identity/contact verification, permissions, adapters |
| Scrapling static acquisition | Adapter and fixture-tested orchestration | Actual pinned SDK execution; no successful live integration result in this environment |
| Browser capture | Disabled extension hook | Native bounded, egress-isolated browser/DOM/network implementation and tests |
| Extraction/matching | 17 actual extraction functions; typed matcher families; all 38 command IDs retained | Defects C01–C11; full donor composites/dependencies; unimplemented exact legacy HostResult/Hit formats |
| Dynamic fingerprints | Feature/prevalence storage, candidate query, subset importer, manual reviewed pack representation | Full donor import accounting, promotion/fixture-calibration pipeline, distribution/rollback; no supplied complete 2,500-signature catalog |
| Collector-to-canonical facts | Distinct record schemas and design bridge | Actual KN-01/KN-02 admission adapter, source/subject verification and production repository |
| Canonical facts and claims | Rich schema/catalog and synthetic bundle validator/reference functions | Persistent, authenticated admission and query service, atomic output publication, corrections F and completeness fixes A01–A05 |
| LLM and other sources | Typed records, few fixture extractors and example transcripts | Live source adapters, model task gateway, paid budgets, bounded runtime repair, generated-artifact lifecycle |
| Derivations/signals/research | Narrow requirement helper and sample/context reference calculations; earlier reference kernels retained in archives | Production input selectors, typed condition evaluation, all enabled business handlers and end-to-end execution |
| Review/export | Local design-test preview exporter and checks | Authenticated review UI and backend, current gate A02, domain-result wiring; exporter is not a sender |
| Campaigns, enrollment, delivery | Proposed records and handoffs | State machines, scheduling owner, production send gate, outbox, adapters, acceptance reconciliation |
| Replies, CRM, outcomes | Proposed product records, reserved outcome contracts | Inbound verification, immediate stop/opt-out path, conversation routing, CRM field ownership/reconciliation, measurement pipeline |
| Standard debugging protocol | Four draft common schemas and a pair validator | Wrappers in actual modules, operation registry, trusted record resolution, effect enforcement and unified target timeline |

All 39 product modules are logical design entries. The latest product archive contains a design validator, not 39 executable runtime implementations. Its 32 new product contracts are field lists, not JSON Schema contracts with state machines. The five example DAG checks do not execute the product.

## What is worth preserving

The original suites and the controls confirm useful safeguards: strict JSON, duplicate IDs, dot-boundary host matching, tenant-scoped observation identities, complete match-support retention, candidate/approved separation, content byte hashing, bounded regex, no automatic sending, and explicit disabling of native browser capture. Three additional protocol controls rejected mismatched request identity, failed output with inadequate diagnostic state, and cross-tenant input references. A genuine fixture header match remains a positive control. Preserve these while fixing the boundaries.

## Recommended repair batches

1. Collector integrity: C01–C04. Trust stored capture metadata, validate before publication, bind producer results, and share live/replay selection. Add the failing reproductions before changing code.

2. Collector runtime reliability: C05–C11. Propagate partial extraction; restore rate-limit state on resume; hash compiled emission semantics; respect encoding and inert contexts; quarantine malformed inputs; validate deterministic reports. Verify the pinned Scrapling integration in CI before claiming live capture works.

3. Canonical boundary: A01–A05 plus the actual collector admission adapter. Separate provenance from independent evidence; split historical evaluation from current-use resolution; distinguish external inputs from generated artifacts; close authorization F; consume real producer matches rather than just matching fixtures.

4. Integrate the shared wrapper and executable operation signatures. Domain schemas and authoritative writers must enforce the actual handoffs. Do not translate a command called COMPLETE into a trusted ModuleResult without verifying its outputs.

5. Implement one complete knowledge-to-reviewed-preview path, then contacts/campaigns/delivery/replies/CRM independently with their authorization and state-machine tests. Keep source/fact breadth; no new service split is required.

## Reproduction

From the unpacked audit directory:
```bash
python -m pip install -r audit-requirements.txt
python run_baselines.py
python probes/probe_collector.py
python probes/probe_architecture.py
python probes/probe_protocol.py
python -m pytest -q tests/test_required_safety.py
```

The last command is an intentional acceptance-gap suite: on the unchanged audited baseline, known unsafe behaviors are expected to FAIL. Its log must not be combined with the original passing baseline counts. Probes use synthetic local stores and do not make target requests or execute sends. Results contain the actual exceptions and observed behaviors.

### Primary dependency references checked

- Pinned official source: https://raw.githubusercontent.com/D4Vinci/Scrapling/v0.4.15/scrapling/engines/static.py
- Pinned package metadata: https://pypi.org/pypi/scrapling/0.4.15/json

These references were used only to check the pinned adapter/dependency boundary. All findings above derive from the uploaded source and local execution, not current GitHub branch contents.