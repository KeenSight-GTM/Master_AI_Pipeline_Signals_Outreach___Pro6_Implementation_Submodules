# Iteration 2: submodule audit and implementation decisions

## Verdict and scope

The repaired local source still passes its existing test suites, but several adjacent boundaries remain inconsistent. This is a **new audit, reproducible safety tests, and walkthrough addendum**, not a new runtime release. Collector 0.2.0, canonical reference 4.2.0, the draft protocol checker and product design remain unchanged.

The baseline's integrity verifier confirms all 438 manifest-listed packaged files. This review did not modify GitHub, contact providers, crawl public sites, send messages, or run CRM mutations. All injected records and exports are synthetic local fixtures.

## Executed evidence

| Verification | Result | Meaning |
|---|---|---|
| Collector original suite | 183 passed, 1 skipped | Actual Scrapling dependency is absent; native browser is still disabled. |
| Canonical original suite | 609 passed | Reference contracts and retained fixture tests. |
| Protocol original suite | 42 passed | Fixture signature/payload checker, not a general runner. |
| New probes | 23 executed | 16 concrete contract counterexamples, 1 separately classified temporal-policy question, 6 passing controls. |
| Required-behavior suite | 16 failed, 6 passed | Failures deliberately express unimplemented repairs; no xfail/skip hides them. |
| Walkthrough smoke run | 8 journeys; 20 subprocesses | Offline local commands/reference fixtures; all expected exit codes and assertions passed. |

The 16 safety counterexamples are grouped into **15 code/contract findings** because two probes describe different parts of the same diagnostic gap. F16 is a separate temporal-policy decision. Passing the 834 original tests is not evidence that the new failing cases are safe. The local walkthroughs exercise narrow working paths, not a complete deployed business workflow.

## Priority convention

P0 means close before trusting autonomous outward use or a shared admission/publication boundary. P1 means close before completing the corresponding user journey or service extraction. P2 means a reference/interface design gap that must be settled before enabling that operation. These are review priorities, not externally scored security ratings.

## Summary

| ID | Priority | Finding | Boundary |
|---|---|---|---|
| F01 | P0 | Identity-binding evidence is outside eligibility/provenance closure | FULL_VALIDATOR_ACCEPTS_INVALID_BOUNDARY |
| F02 | P0 | Demoted templates pass the standalone current-use/export boundary | LOCAL_REFERENCE_EXPORTER_GAP |
| F03 | P0 | Publication validates one payload and can persist a different argument set | INTERNAL_API_CONTRACT_SPLIT |
| F04 | P1 | Later supersession leaks into an earlier sealed evaluation | HISTORICAL_QUERY_INCONSISTENCY |
| F05 | P1 | Generated-artifact handoff is accepted by one validator and rejected by another | INCOMPATIBLE_VALIDATOR_LAYERS |
| F06 | P1 | HTML recovery can silently truncate the parse while reporting complete detection | EXECUTED_COLLECTOR_DEFECT |
| F07 | P1 | A self-superseding fact raises RecursionError before semantic rejection | UNCONTROLLED_INVALID_INPUT_FAILURE |
| F08 | P1 | Requirement minimum means fact count in the helper but origin count in validation | REFERENCE_FUNCTION_CONTRACT_MISMATCH |
| F09 | P1 | Retained-file import does not pin subject identity in run configuration | EXECUTED_CLI_IDENTITY_DEFECT |
| F10 | P1 | Current candidate discovery counts unlabelled revoked evidence | RESEARCH_INDEX_ELIGIBILITY_GAP |
| F11 | P1 | Contradictory duplicate command outcomes are accepted | COMMAND_REPORT_IDENTITY_GAP |
| F12 | P1 | No-byte failures lose invocation details and have no persisted evaluation manifest | DIAGNOSTIC_AND_COMPLETENESS_GAP |
| F13 | P1 | Protocol rejects an honest timeout failure reported after its deadline | FAILURE_REPORT_CONTRACT_GAP |
| F14 | P1 | Collector and canonical matcher disagree on aside-region semantics | CROSS_MODULE_MATCHER_POLICY_MISMATCH |
| F15 | P2 | The protocol fixture does not constrain mode/effects against operation parameters | DRAFT_CHECKER_INCOMPLETENESS |
| F16 | P2 | effective_at is stored but its decision semantics are undefined/unused | POLICY_DECISION_REQUIRED |

## Detailed findings

### F01 — Identity-binding evidence is outside eligibility/provenance closure

**Priority:** P0. **Owners:** KN-01, KN-02, KN-03, COM-04. **Probes:** R2-A01.

**Observed:** A binding is changed to depend exclusively on a DELETED artifact. The account fact remains current-eligible, and full bundle validation passes. The binding artifact is not in roots(fact).

**Impact and scope:** A fact can lose the evidence establishing whose website or record it is while still supporting account-specific copy. Pinning a binding ID does not pin or preserve its supporting artifacts.

**Proposed repair:** Include accepted binding decisions, their exact evidence locators/artifacts and permitted source state in dependency closure. Separate substantive corroboration from this mandatory identity support. Admit/resolve bindings before dependent facts and invalidate current use when required binding evidence becomes unusable.

**Acceptance condition:** Deleted, expired, revoked, unpinned, or foreign binding support must block affected current claims. A valid alternative accepted binding should be an explicit new decision rather than an automatic guessed fallback.

**Affected journeys:** J07, J11, J17.

**Source:** `canonical/keensight_contracts/validation.py:65–118`; `canonical/keensight_contracts/validation.py:123–172`; `canonical/keensight_contracts/validation.py:297–303`; `canonical/keensight_contracts/completion.py:149–161`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F02 — Demoted templates pass the standalone current-use/export boundary

**Priority:** P0. **Owners:** COM-02, COM-03, COM-04. **Probes:** R2-A02.

**Observed:** After an existing template is demoted from ACTIVE to CANDIDATE and the current version vector is refreshed, LocalPreviewExporter writes the preview. The full bundle validator rejects the same state with MISSING_APPROVAL.

**Impact and scope:** Calling the local gate/export method independently has weaker authority rules than validating the whole bundle. This is a local fixture boundary, not a tested live sender bypass.

**Proposed repair:** Make current-use eligibility explicitly check the current template/renderer, offer where applicable, source and reviewed-release authority. Bind review to immutable historical bytes but perform current vetoes at export. Keep shared validation logic rather than relying on callers to rerun the entire fixture bundle.

**Acceptance condition:** Template demotion/retirement must block a new export without erasing the historic review. Existing permitted byte-identical exports retain their receipt; a fresh gate must not restore authority just by recomputing a hash.

**Affected journeys:** J07, J13, J17.

**Source:** `canonical/keensight_contracts/completion.py:298–377`; `canonical/keensight_contracts/handoff.py:19–43`; `canonical/keensight_contracts/validation.py:408–422`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F03 — Publication validates one payload and can persist a different argument set

**Priority:** P0. **Owners:** FP-02, PLAT-01. **Probes:** R2-C06.

**Observed:** Store.publish_evaluation receives a valid bundle describing one observation and separately receives empty match/observation/support arguments. It commits a successful manifest with one observation but zero observation rows.

**Impact and scope:** The normal Scanner passes consistent arguments; the defect is the public local-owner publication API. A future wrapper or refactor can commit an internally contradictory database even though the manifest validated.

**Proposed repair:** Accept one validated publication object and derive all database rows from it, or compare all separate arguments byte-for-byte before beginning the transaction. Re-extract trusted capture evidence at the boundary that owns admission; do not merely validate a sibling object.

**Acceptance condition:** Mismatch must reject before any findings or successful manifest commit. Add matching, missing, added and altered-row cases plus rollback fault injection.

**Affected journeys:** J03, J11, J19.

**Source:** `collector/src/keensight_scrapling/storage.py:211–258`; `collector/src/keensight_scrapling/pipeline.py:231–246`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F04 — Later supersession leaks into an earlier sealed evaluation

**Priority:** P1. **Owners:** KN-03, KN-04, RE-01. **Probes:** R2-A06.

**Observed:** The old run pins f.tech. A replacement recorded after its knowledge cutoff, but before its logical as_of, is not in that run. Historical resolution nevertheless becomes UNKNOWN because usable() searches every fact in the bundle for supersession.

**Impact and scope:** Reproducing an old result depends on later database contents. This is distinct from the intended current-use check, which should see newly recorded evidence.

**Proposed repair:** Give historical eligibility an explicit permitted input set/knowledge cutoff and snapshot-specific changes. Keep current-use eligibility as a different operation. Route supersession lookup through the same visibility context rather than scanning all rows.

**Acceptance condition:** Adding later observations/corrections must leave sealed historical results unchanged; a current view and use gate must still reflect those changes.

**Affected journeys:** J04, J07, J17.

**Source:** `canonical/keensight_contracts/validation.py:123–144`; `canonical/keensight_contracts/completion.py:170–199`; `canonical/keensight_contracts/engine.py:86–98`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F05 — Generated-artifact handoff is accepted by one validator and rejected by another

**Priority:** P1. **Owners:** AI-01, RE-01, CTL-02, KN-02. **Probes:** R2-A03.

**Observed:** A model response is correctly declared as a run-produced artifact, with a successful earlier producer. A later declared execution consumes it. validate_completion passes; Bundle.validate rejects ARTIFACT_OUTSIDE_RUN because an older loop still requires every execution artifact to be in input_artifact_ids.

**Impact and scope:** The repaired manifest can represent generated model I/O, but a downstream consumer cannot consistently use it in the same run.

**Proposed repair:** Use one available-artifact resolver in all validators. It must admit sealed external inputs or eligible prior outputs, enforce chronology and producer ownership, and reject self-consumption. Do not copy a generated response into the external-input list to satisfy the older check.

**Acceptance condition:** A two-stage generated-output→consumer path must pass both validators; unfinished, future, self-produced or undeclared inputs must fail.

**Affected journeys:** J07, J12.

**Source:** `canonical/keensight_contracts/completion.py:425–458`; `canonical/keensight_contracts/validation.py:340–356`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F06 — HTML recovery can silently truncate the parse while reporting complete detection

**Priority:** P1. **Owners:** ING-04, FP-01. **Probes:** R2-C05.

**Observed:** A retained page with 400 nested div elements and a later product script triggers parser recovery. Script extraction reports COMPLETE with zero surfaces, and its rules report NO_MATCH. The retained bytes do contain the marker.

**Impact and scope:** The previous fix handles explicit item/text caps, but not structural information discarded by the parser. No absence fact is emitted today; coverage/reporting is nevertheless wrong.

**Proposed repair:** Inspect parser diagnostics and classify information-losing recovery or depth/resource limits. Propagate an explicit partial capability state to all affected extractors and match evaluations. Harmless HTML repairs need a documented policy rather than blanket success or blanket failure.

**Acceptance condition:** Deeply nested, truncated and malformed inputs must not produce a complete negative when evidence was dropped. Ordinary recoverable pages should retain deterministic extraction.

**Affected journeys:** J02, J03, J09.

**Source:** `collector/src/keensight_scrapling/extraction.py:54–67`; `collector/src/keensight_scrapling/extraction.py:96–110`; `collector/src/keensight_scrapling/rules.py:158–191`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F07 — A self-superseding fact raises RecursionError before semantic rejection

**Priority:** P1. **Owners:** KN-02, KN-03. **Probes:** R2-A04.

**Observed:** Setting f.tech.supersedes_fact_id to f.tech causes full validation to raise RecursionError, rather than the intended ordered-supersession ContractError.

**Impact and scope:** The data does not become accepted, but an ordinary malformed record escapes the controlled contract-failure path and can abort a batch or obscure the actual invalid field.

**Proposed repair:** Validate supersession identity, ordering and acyclicity before eligibility recursion. Add an explicit recursion/visited guard to public read helpers so malformed unadmitted data cannot exhaust the stack.

**Acceptance condition:** Self and multi-record cycles receive stable diagnostic codes and no publication; valid historical chains remain queryable.

**Affected journeys:** J06, J07, J11.

**Source:** `canonical/keensight_contracts/validation.py:123–130`; `canonical/keensight_contracts/validation.py:485–489`; `canonical/keensight_contracts/completion.py:183–199`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F08 — Requirement minimum means fact count in the helper but origin count in validation

**Priority:** P1. **Owners:** RE-05, KN-03. **Probes:** R2-A08.

**Observed:** evaluate_requirements resolves minimum=2 from two eligible fact rows backed by the same substantive origin. The full signal validator requires two distinct substantive artifact origins.

**Impact and scope:** The allowlisted rule helper can compute a result that its consuming validator rejects. This is a helper-level comparison, not a claim that a fully admitted forged signal passed.

**Proposed repair:** Name the unit explicitly (observations, evidence elements, origins, independent corroboration) in the requirement contract. Share one support-selection/evaluation function between the rule and the validator. Multiple records from one origin cannot satisfy an origin threshold.

**Acceptance condition:** Duplicate rows/origins must not increase the selected unit. Independent eligible origins should satisfy a properly configured threshold.

**Affected journeys:** J07, J12, J13.

**Source:** `canonical/keensight_contracts/engine.py:143–150`; `canonical/keensight_contracts/validation.py:399–407`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F09 — Retained-file import does not pin subject identity in run configuration

**Priority:** P1. **Owners:** CTL-02, ING-02, FP-02. **Probes:** R2-C07.

**Observed:** Two analyze-file calls use the same tenant, run, URL, observation time and rules but different subjects. Both return exit 0. The resulting run contains both subjects, and replay fails with Cross-subject/tenant/origin host rollup forbidden.

**Impact and scope:** Independent CLI invocations can create a run that the replay contract cannot consume. The import path pins fewer identity fields than the live scan path.

**Proposed repair:** Use one immutable ScanPlan/run identity for live and imported capture. Include subject, input mode, code/parser version, source and content/import manifest. A single-target run rejects subject changes; a multi-target run requires explicit partitions.

**Acceptance condition:** The second changed-subject invocation must fail without appending its capture. A deliberate new run should work and replay independently.

**Affected journeys:** J02, J04.

**Source:** `collector/src/keensight_scrapling/cli.py:103–114`; `collector/src/keensight_scrapling/storage.py:59–67`; `collector/src/keensight_scrapling/pipeline.py:248–256`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F10 — Current candidate discovery counts unlabelled revoked evidence

**Priority:** P1. **Owners:** FP-03, PLAT-02. **Probes:** R2-C04.

**Observed:** After the only supporting capture is revoked, candidates(tenant,min_hosts=1) returns the same current candidate and prevalence counts. The query does not join revocation state.

**Impact and scope:** An operator can prioritize or export a research candidate without seeing that its support is no longer eligible. This probe concerns derived metadata, not continued export of the original revoked bytes.

**Proposed repair:** Separate historical occurrence counts from eligible support counts and expose both with an as_of/policy identity. Filter or flag revoked/expired support in current candidate selection; keep audit history according to policy.

**Acceptance condition:** Revoking all support must remove current eligibility or display an explicit unsupported/historical state. New eligible support can restore candidacy without erasing prior history.

**Affected journeys:** J05, J17.

**Source:** `collector/src/keensight_scrapling/storage.py:164–215`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F11 — Contradictory duplicate command outcomes are accepted

**Priority:** P1. **Owners:** FP-01, FP-02, PLAT-03. **Probes:** R2-C10.

**Observed:** Appending a FAILED MATCH_HOST_SUFFIX record with the same inputs alongside valid COMPLETE records still passes validate_bundle. The matcher check accepts any matching correct row; CommandResult has no invocation identity.

**Impact and scope:** A timeline cannot tell whether this is a retry, another operator using the same command name, or a contradiction. The baseline already has multiple COMPLETE rows because host_equals and host_suffix map to the same command.

**Proposed repair:** Assign command_execution_id, operator/version, target and attempt identifiers. Validate exactly one terminal outcome per invocation. Aggregate command-family status separately without discarding individual executions.

**Acceptance condition:** Contradictory terminal states for the same invocation fail. Legitimate distinct operators/attempts remain representable and inspectable.

**Affected journeys:** J03, J06, J19.

**Source:** `collector/src/keensight_scrapling/pipeline.py:211–218`; `collector/src/keensight_scrapling/validation.py:60–72`; `collector/src/keensight_scrapling/core.py:100–111`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F12 — No-byte failures lose invocation details and have no persisted evaluation manifest

**Priority:** P1. **Owners:** ING-03, CTL-02, PLAT-01, PLAT-03. **Probes:** R2-C01, R2-C09.

**Observed:** finish_attempt replaces the reserved request payload; after timeout, started_at, command_id and mode are gone. A no-byte scan emits a bundle with no top-level tenant/subject/run identity (only evaluation_id), no captures, and no stored evaluation row.

**Impact and scope:** The attempts table retains tenant/run and run configuration separately, so identity is not wholly lost in the store. But the exported failure is not self-identifying and cannot produce a complete attempt timeline or durable failed-target evaluation.

**Proposed repair:** Keep immutable request metadata and append/merge the terminal outcome without deleting start fields. Require explicit evaluation tenant, target and run identity independently of artifacts. Persist zero-output success/failure/abstention manifests as first-class results.

**Acceptance condition:** Two failed targets with the same human run label remain distinguishable. Start/end/command/mode survive timeout and resume, without manufacturing bytes or positive facts.

**Affected journeys:** J06, J09, J19.

**Source:** `collector/src/keensight_scrapling/pipeline.py:46–60`; `collector/src/keensight_scrapling/pipeline.py:76–126`; `collector/src/keensight_scrapling/storage.py:69–94`; `collector/src/keensight_scrapling/storage.py:214–236`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F13 — Protocol rejects an honest timeout failure reported after its deadline

**Priority:** P1. **Owners:** CTL-02, PLAT-03. **Probes:** R2-P01.

**Observed:** A FAILED result with no positive outputs and an explicit timeout diagnostic, finalized one second after deadline, is rejected as Operation finished beyond deadline.

**Impact and scope:** The system needs to deny late success/effects while still recording the real end time and failed outcome. Otherwise a worker must lie about finish time or lose its failure report.

**Proposed repair:** Separate execution deadline, cancellation/timeout outcome, report completion and late-effect handling. Accept truthful terminal diagnostics after a deadline without allowing success publication or new side effects.

**Acceptance condition:** Late FAILED/CANCELLED reports with appropriate reasons are admissible; a late success without approved semantics remains rejected and any uncertain side effect is reconciled.

**Affected journeys:** J06, J08, J19.

**Source:** `protocol/validate_protocol.py:92–151`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F14 — Collector and canonical matcher disagree on aside-region semantics

**Priority:** P1. **Owners:** ING-04, FP-01, KN-02. **Probes:** R2-C08.

**Observed:** For the same script in an aside element, the collector supports vendor.present; canonical fingerprint_hosts returns no match because it excludes aside.

**Impact and scope:** A future bridge can reject a collector finding that looked valid, or change its meaning. This review does not assert that every aside must be ignored or accepted.

**Proposed repair:** Choose and version one attribution/region policy; share a matcher/evidence representation or run parity fixtures through both implementations. Do not silently map the two predicate contracts as equivalent.

**Acceptance condition:** Identical content and the declared same rule policy yield compatible results across collection and admission; differences require explicit policy/version labels.

**Affected journeys:** J02, J03, J11.

**Source:** `collector/src/keensight_scrapling/extraction.py:23–35`; `collector/src/keensight_scrapling/rules.py:163–169`; `canonical/keensight_contracts/engine.py:117–138`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F15 — The protocol fixture does not constrain mode/effects against operation parameters

**Priority:** P2. **Owners:** CTL-01, CTL-03, PLAT-03. **Probes:** R2-P02.

**Observed:** The complete fixture payload check accepts FP-01.match in CAPTURE mode reporting five network attempts even though its validated parameters say allow_network=false.

**Impact and scope:** No network was performed; this is a checker-consistency test. The enforcing runner still does not exist, so the current envelope cannot be advertised as enforcing effect permissions.

**Proposed repair:** Extend trusted operation signatures with allowed modes, effect classes and budget policies; compare reported usage to those constraints and enforce them before execution through capability-limited dependencies. Diagnostics must remain truthful when policy is violated.

**Acceptance condition:** Offline matching cannot be authorized to capture; reported forbidden effects trigger a policy failure and alert rather than a successful eligible output.

**Affected journeys:** J08, J19.

**Source:** `protocol/validate_protocol.py:51–131`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

### F16 — effective_at is stored but its decision semantics are undefined/unused

**Priority:** P2. **Owners:** KN-02, KN-03, RE-05. **Probes:** R2-A05.

**Observed:** A fact with effective_at a month after the use gate remains current-eligible and passes full validation. The gate time, observed_at and recorded_at are distinct, but effective_at is not consulted.

**Impact and scope:** Some records describe future events and are valid observations now; others must not be interpreted as a currently effective status. The generic contract does not say which rule applies. This is separately reported, not an assumed universal failing requirement.

**Proposed repair:** Define per-predicate temporal semantics: observation of an announcement, asserted valid-time state, reporting period, and validity interval. Test the permitted language and signal conditions separately rather than universally dropping future-dated records.

**Acceptance condition:** A future license effective date cannot prove currently effective licensure; a supported statement that the record announces a future effective date remains possible.

**Affected journeys:** J11, J12, J13.

**Source:** `canonical/keensight_contracts/engine.py:37–44`; `canonical/keensight_contracts/validation.py:123–171`; `canonical/keensight_contracts/validation.py:452–493`. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.

## Existing repairs that still hold

Six controls passed: changed capture metadata is rejected; duplicate evaluation input does not publish findings; compatible rule-release replay succeeds; an unresolved binding blocks use; a cross-tenant ChangeRecord cannot veto the other tenant's fact; and an undeclared protocol input is rejected. These results distinguish residual gaps from blanket claims that previous repairs failed.

## Repair sequence

1. **One trusted decision dependency closure:** binding evidence, sealed versus current visibility, current template authority (F01, F02, F04). Keep the historical view separate from the current-use veto.
2. **One publication payload and invocation identity:** atomic persistence from the validated object, self-identifying zero-output evaluations, immutable attempts and command execution IDs (F03, F11, F12).
3. **Collector completeness and identity parity:** parser-loss diagnostics, shared region policy, run-subject identity and eligible research support (F06, F09, F10, F14).
4. **Canonical execution consistency:** one artifact-availability resolver, guarded supersession and shared requirement-counting logic (F05, F07, F08).
5. **Service protocol:** allow honest late failure reports and constrain operation modes/effects before exposing network workers (F13, F15). Decide predicate-specific effective-time behavior (F16).
6. Re-run the old suites, these safety tests, and the linked journeys. Only then broaden the capture→canonical→preview integration.

## Incompleteness remains explicit

There is no executable collector-to-canonical production admission bridge, persistent authenticated canonical service, general module runner, full donor-rule promotion service, native bounded browser, broad production connector suite, contact/campaign/enrollment implementation, sender, inbound conversation processor or CRM synchronization service in this baseline. The design provides module names, contracts and intended ownership. The feature map records these as proposed, not as callable endpoints.

The request in this iteration is to identify bugs and add critique/invocation walkthroughs. No application behavior has been patched. A local helper was added solely to run and log the documented offline journeys; it is not the proposed execution middleware.

## Reproduction

From this review package's root:

```bash
# Existing baseline; dependency installation may need network access in your environment.
python -m pip install -e './baseline/collector[test]'
python -m pip install -r ./baseline/canonical/requirements.txt
python baseline/verify_integrity.py
(cd baseline/collector && python -m pytest -q)
(cd baseline/canonical && python generate.py --check && python validate.py && python -m pytest -q)
(cd baseline/protocol && python validate_protocol.py && python -m pytest -q)

# New audit: expected to identify the documented defects against this unchanged baseline.
python audit_probes.py --output ./audit-output.json
python -m pytest -q tests/test_required_behaviour.py

# Narrow working user paths: offline and no-send, not full-system sign-off.
python walkthroughs/run_local_journeys.py --output ./journey-output --journey all-local
```

The failing safety suite should remain separate from the original passing-test count until patches intentionally change the expected outcomes. No defect is proven merely by a higher test count.
