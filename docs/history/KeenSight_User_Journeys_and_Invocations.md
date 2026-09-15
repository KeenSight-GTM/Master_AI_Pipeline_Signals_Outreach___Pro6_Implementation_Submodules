# Feature walkthroughs and user journeys

## What can be invoked now

Eight local/reference journeys below were executed in 20 separate subprocesses with expected exit codes. No network/provider operation was enabled. The real static Scrapling path is dependency-gated and unverified here; native browser is disabled. All business journeys without handlers are explicitly marked PROPOSED and have no pretend command or endpoint.

From the unpacked review package root:

```bash
python -m pip install -e './baseline/collector[test]'
python -m pip install -r ./baseline/canonical/requirements.txt
python walkthroughs/run_local_journeys.py --output ./journey-output --journey all-local
```

The harness also works from the source tree through PYTHONPATH without installing CLI entrypoints, provided the core dependencies already exist. It records command argv, working directory, exit code, stdout and stderr under the chosen output directory. Use a new output directory for a new review so old logs are not overwritten. The records use fixed **synthetic September 14, 2026 timestamps**; they do not grant current production permission.

**Artifact inspection loop:** request/command → capture metadata and bytes → surface locators → rule match → observation and support → collector claim. The next canonical admission step is missing and must not be replaced by manual renaming of fields.

| Journey | User goal | Readiness | Stages |
|---|---|---|---|
| J01 | First offline run: see duplicate fingerprints become one claim | LOCAL | F03–F07 |
| J02 | Analyze an already-retained page | LOCAL | F02,F05–F07 |
| J03 | Debug extraction, matching and resolution as separate processes | LOCAL | F06–F07,F26 |
| J04 | Replay retained evidence and compare before/after | LOCAL | F07–F08,F11 |
| J05 | Inspect unknown features and import donor candidates | LOCAL/PARTIAL | F08 |
| J06 | Investigate a failed check and preserve diagnostics | LOCAL/PARTIAL | F05,F07,F26 |
| J07 | Review the canonical reference path and produce a local preview | REFERENCE | F09–F18,F21 |
| J08 | Verify the shared protocol and product design inventories | REFERENCE | F03,F26 |
| J09 | Enable and verify a real permitted static capture | SDK_UNVERIFIED; BROWSER DISABLED | F03–F07 |
| J10 | Set up a sales program and select accounts | PROPOSED | F00–F03 |
| J11 | Move collector observations into canonical, searchable knowledge | PROPOSED BRIDGE | F02,F09–F11 |
| J12 | Build enriched account research and product/industry context | PROPOSED RUNTIME; REFERENCE CHECKS ONLY | F12–F15 |
| J13 | Choose an offer, assess a contact and review supported copy | PROPOSED PRODUCT; NARROW RENDERER REFERENCE | F16–F18,F21 |
| J14 | Approve a campaign, enroll and schedule one step | PROPOSED | F19–F20 |
| J15 | Authorize, dispatch and reconcile a message | PROPOSED | F21–F22 |
| J16 | Handle replies, stop outreach and hand off to sales/CRM | PROPOSED | F23–F24 |
| J17 | Correct identity or revoke evidence/authority | REFERENCE / LOCAL OWNER ONLY | F26 |
| J18 | Measure outcomes and improve rules/templates | PROPOSED | F08,F25 |
| J19 | Run submodules separately and prepare service extraction | LOCAL PROCESSES; PROPOSED SERVICES | F03,F26 |

## Step-by-step journey cards

### J01 — First offline run: see duplicate fingerprints become one claim

**Actor:** Engineer. **Readiness:** LOCAL. **Stages:** F03–F07.

**Features:** FM04, FM10. **Open findings:** See general implementation boundaries.

**Preconditions / inputs:** The included collector examples and installed core parser dependencies. No credentials.

1. List the 38 registered command IDs; this is an inventory, not all-38 live sign-off.
2. Run the synthetic two-page demonstration with fixture transport.
3. Inspect all 7 match records, 2 observations and 1 claim; keep the support links.
4. Check the bundle against its trusted metadata and original blobs.

**Outputs to inspect:** demo-store/scan-bundle.json, claims.json, scanner.sqlite3 and retained fixture blobs.

**Failure/hold path:** A dependency or contract error produces nonzero exit. No LLM, provider, campaign or sender is called.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J01
```

**Acceptance:** The shipped synthetic result is 7 matches → 2 observations → 1 claim, with no combined confidence. This count is an example, not a business scoring policy.

### J02 — Analyze an already-retained page

**Actor:** Research engineer. **Readiness:** LOCAL. **Stages:** F02,F05–F07.

**Features:** FM05. **Open findings:** F06, F09, F14.

**Preconditions / inputs:** HTML bytes, page URL, asserted collection timestamp, explicit subject/tenant, selected rule release.

1. Confirm your right to retain/process the page and record the actual collection time separately from today.
2. Choose explicit tenant and subject identifiers and a new single-target run ID.
3. Call analyze-file; the source is marked user-provided-snapshot.
4. Inspect the capture, extraction reports and observation support; run the trusted-store bundle check.

**Outputs to inspect:** imported-store/scan-bundle.json and original-content store.

**Failure/hold path:** The importer does not verify legal company ownership. F09 means a reused run can currently mix subjects: do not reuse a run across targets. F06 affects deep/malformed HTML.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J02
```

**Acceptance:** No network calls. Supported observations trace to the supplied bytes; user-supplied timestamps are not independently authenticated.

### J03 — Debug extraction, matching and resolution as separate processes

**Actor:** Debugger. **Readiness:** LOCAL. **Stages:** F06–F07,F26.

**Features:** FM08, FM09, FM10, FM11, FM36. **Open findings:** F03, F06, F11, F14.

**Preconditions / inputs:** An existing trusted collector store and ScanBundle.

1. Select a capture_id from observations or evaluated_capture_ids, not an arbitrary robots response.
2. Run ks-module extract and inspect PageEvidence and every extractor status.
3. Run ks-module match against those evidence records and a pinned rule pack.
4. Run check for the whole bundle; run resolve for its historical claim view.
5. Use IDs to follow claim → observation → support → match → surface → capture.

**Outputs to inspect:** page-evidence.json, matches.json, checked.json, resolved.json plus per-process logs.

**Failure/hold path:** Do not equate standalone match output with canonical Fact admission. F11 means a command-family timeline is not yet unambiguous; F03 is the publication API issue.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J03
```

**Acceptance:** Each process uses stored bytes and returns parseable JSON or an explicit nonzero failure. No service deployment is implied.

### J04 — Replay retained evidence and compare before/after

**Actor:** Rule engineer. **Readiness:** LOCAL. **Stages:** F07–F08,F11.

**Features:** FM10, FM12. **Open findings:** F04, F09.

**Preconditions / inputs:** Original store, original capture-run ID, evaluation-run ID, rule pack and evaluation as_of.

1. Keep the original capture run unchanged.
2. Choose an evaluation ID and rule release; the replay uses no transport.
3. Run replay and compare matches, observations, rule release and capture time.
4. Query historical collector claims under an explicit currently selected rule allowlist.

**Outputs to inspect:** replay.json; all original observations retain their captured timestamps.

**Failure/hold path:** Missing capture modalities require recapture; they cannot be reconstructed. F04 is a separate canonical historical-visibility defect, not a failure of this passing collector replay example.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J04
```

**Acceptance:** The smoke test asserts identical observations for unchanged evidence/rules. A separate control verifies a compatible changed release replays successfully.

### J05 — Inspect unknown features and import donor candidates

**Actor:** Rule curator. **Readiness:** LOCAL/PARTIAL. **Stages:** F08.

**Features:** FM13, FM14, FM15. **Open findings:** F10.

**Preconditions / inputs:** Retained captures, donor rows, canonical vendor mapping, reviewer policies for future promotion.

1. Run candidates against the local technical index; the demo lowers min-hosts to 1 only for inspection.
2. Import donor-shaped JSONL using an explicit vendor map.
3. Review IMPORTED_CANDIDATE versus QUARANTINED disposition for every input row.
4. Stop before promotion: no production approval or distribution command is implemented.

**Outputs to inspect:** imported-candidates.json, import-report.json and candidate-query output.

**Failure/hold path:** F10 means revoked evidence still affects unlabelled candidate counts. Never treat current output as automatically eligible promotion evidence.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J05
```

**Acceptance:** Automatic approvals remain zero and every row is accounted for. This is a subset adapter, not the full 739-definition donor corpus or 2,500-signature catalog.

### J06 — Investigate a failed check and preserve diagnostics

**Actor:** Engineer/operator. **Readiness:** LOCAL/PARTIAL. **Stages:** F05,F07,F26.

**Features:** FM11, FM36. **Open findings:** F07, F11, F12, F13.

**Preconditions / inputs:** A valid fixture store and the new audit tests.

1. Make a copy of a valid bundle; do not modify original capture bytes or the database.
2. Change one supplied metadata field in that copy and run check.
3. Expect exit 2 and inspect stderr; the original bundle must still validate.
4. For acquisition failures inspect attempts and run configuration with read-only SQL; do not fabricate a capture.
5. Run the separate required-behavior suite to see the still-failing diagnostic boundaries.

**Outputs to inspect:** tampered-bundle.json, expected rejection logs, valid-after-rejection.json.

**Failure/hold path:** F12 currently drops start fields at attempt finalization and omits zero-capture evaluation identity; F13 rejects honest post-deadline timeout reports. These are not repaired by the passing tamper test.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J06
```

**Acceptance:** The deliberate tamper must fail, while original data remains valid. New safety tests are intentionally failing until code fixes land.

### J07 — Review the canonical reference path and produce a local preview

**Actor:** Reference tester. **Readiness:** REFERENCE. **Stages:** F09–F18,F21.

**Features:** FM18, FM21, FM23, FM26, FM28. **Open findings:** F01, F02, F04, F05, F07, F08.

**Preconditions / inputs:** The shipped canonical fixture bundle, trusted synthetic actor.fixture grant and fixture destination.

1. Check canonical generated files and validate the shipped synthetic bundle.
2. Inspect existing bindings, facts, claim resolutions, sample priors, signals and package evidence.
3. Use the existing fixture review and gate at their fixed historical timestamps.
4. Export a local no-send JSON preview; repeat the same idempotency key and confirm reused bytes.

**Outputs to inspect:** reference/reference-preview.json and one idempotent local preview JSON.

**Failure/hold path:** This is not capture-to-canonical admission, real review/authentication, contact enrichment or current production permission. F01/F02/F04/F05/F08 remain blockers for the corresponding paths.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J07
```

**Acceptance:** Full reference validation passes, repeated export reuses bytes, send_allowed remains false, and no collector data is silently converted to canonical facts.

### J08 — Verify the shared protocol and product design inventories

**Actor:** Integration engineer. **Readiness:** REFERENCE. **Stages:** F03,F26.

**Features:** FM03, FM36. **Open findings:** F13, F15.

**Preconditions / inputs:** protocol/examples and product-design definitions.

1. Run the protocol fixture checker.
2. Inspect the exact registered operation: FP-01.match with example-only payload schemas.
3. Run the 39-module product-design inventory checker.
4. Compare desired deployment with the proposed eight ownership groups; do not deploy the checker as a worker.

**Outputs to inspect:** Protocol/example consistency and design-inventory reports.

**Failure/hold path:** F13/F15 show the checker still lacks correct failure/effect semantics. No arbitrary operation handler, auth server or HTTP endpoint is supplied.

**Invocation:**

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey J08
```

**Acceptance:** Passing reports explicitly remain fixture/design checks. Unknown implementation names are not treated as supported modules.

### J09 — Enable and verify a real permitted static capture

**Actor:** Collection operator. **Readiness:** SDK_UNVERIFIED; BROWSER DISABLED. **Stages:** F03–F07.

**Features:** FM06, FM07. **Open findings:** F06, F12.

**Preconditions / inputs:** Permitted target, installed pinned SDK, source-purpose approval, bounded ScanConfig and candidate-only rules.

1. Install the live extra in an environment that can obtain Scrapling 0.4.15.
2. Require the SDK import to succeed before running test_live_integration.py; a skipped test is not sign-off.
3. Run the controlled local HTTP fixture integration before an authorized public target.
4. Use the candidate-only live rule example; inspect limits, redirects, failures and coverage.
5. Keep browser capture disabled until egress, cookies, resources and cancellation have their own verified boundary.

**Outputs to inspect:** Real attempts, artifacts and scan bundle only after actual integration succeeds.

**Failure/hold path:** No live call was made in this iteration. F06/F12/F14 must be understood; never bypass rate limits or source restrictions to make a test green. Browser has no working default.

**Invocation:**

```bash
python -m pip install -e './baseline/collector[live,test]'
python -c "from scrapling.fetchers import FetcherSession; from importlib.metadata import version; assert version('scrapling') == '0.4.15'"
(cd baseline/collector && python -m pytest -q tests/test_live_integration.py)
```

**Acceptance:** Require actual execution (not skip), then real capture within declared policy. User-supplied target identity is still not canonical ownership evidence.

### J10 — Set up a sales program and select accounts

**Actor:** Growth lead. **Readiness:** PROPOSED. **Stages:** F00–F03.

**Features:** FM01, FM02. **Open findings:** See general implementation boundaries.

**Preconditions / inputs:** Program/audience/offer definitions, seed origin, current account/CRM exclusions and trusted principal.

1. Define services, audience, geography, exclusions, permitted sources and budgets.
2. Approve a versioned program and derive a research plan.
3. Import/discover seeds and deduplicate account identities without turning fit criteria into facts.
4. Authorize a bounded run with a pinned capability profile.

**Outputs to inspect:** Program revision, AccountSeed, LeadSelection, ResearchPlan, IntakeRequest and BatchRun.

**Failure/hold path:** No program UI or seed-selection handler exists. The one-URL collector is not an account-discovery engine.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Implement tests for exclusions, provenance, identity ambiguity, budget denial and zero eligible accounts before enabling this journey.

### J11 — Move collector observations into canonical, searchable knowledge

**Actor:** Knowledge engineer. **Readiness:** PROPOSED BRIDGE. **Stages:** F02,F09–F11.

**Features:** FM16, FM17. **Open findings:** F01, F03, F07, F14, F16.

**Preconditions / inputs:** Collector observations/support, canonical predicate/source release and accepted identity evidence.

1. Read the complete ScanBundle, not just host priority or one claim row.
2. Verify successful producers, original captures, subject bindings and typed predicate mappings.
3. Admit one captured observation with all its supports and exact provenance.
4. Resolve complete claim groups; separate historical and current visibility.
5. Publish a searchable knowledge result even when no commercial rule fires.

**Outputs to inspect:** Canonical Fact/Evidence/Execution plus admission report, ClaimResolution and InputSnapshot.

**Failure/hold path:** No executable production bridge or persistent canonical API exists. F01/F03/F04/F07/F09/F14 must be closed before the integration is trusted.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** A real stored capture traverses admission without manual fixture editing; missing identity, stale/candidate/conflicting evidence and zero results are handled honestly.

### J12 — Build enriched account research and product/industry context

**Actor:** Research analyst. **Readiness:** PROPOSED RUNTIME; REFERENCE CHECKS ONLY. **Stages:** F12–F15.

**Features:** FM19, FM20, FM21, FM22, FM23. **Open findings:** F05, F08, F16.

**Preconditions / inputs:** Permitted source records, InputSnapshot, versioned functions, sample/support policies and context rules.

1. Select approved source families and capture relevant hiring, technology, review, traffic, registry or publication artifacts.
2. Run typed extraction; any model task retains original I/O and bounded repair history.
3. Create samples with explicit eligible, excluded and unclassified members.
4. Compute priors and join them through declared product/industry links.
5. Run enabled derivations/signals over pinned complete claim groups.

**Outputs to inspect:** Typed facts, sample-bound priors, ContextAssessment, derivations and SignalEvaluation.

**Failure/hold path:** The current reference bundle illustrates records but does not execute the broad live flow. F05/F08/F16 require consistent decisions; context cannot become company-specific proof.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** A product-prior change or deleted denominator changes its eligibility. Failed model calls produce honest uncertainty. Duplicate origins cannot inflate support.

### J13 — Choose an offer, assess a contact and review supported copy

**Actor:** Growth operator/reviewer. **Readiness:** PROPOSED PRODUCT; NARROW RENDERER REFERENCE. **Stages:** F16–F18,F21.

**Features:** FM24, FM25, FM27. **Open findings:** F02, F08, F16.

**Preconditions / inputs:** Opportunity, account proof, contact assessment, approved template and trusted reviewer.

1. Select a supported service-line opportunity; allow no-opportunity as a valid result.
2. Resolve relevant person/account relation, role, endpoint status and permission separately.
3. Render approved clauses using eligible account evidence; context may guide a neutral question only.
4. Review the exact message revision and hash with an authenticated reviewer.
5. Obtain a fresh use decision for its specific purpose and destination.

**Outputs to inspect:** OpportunitySelection, ContactAssessment, GroundedClause, OutreachPackage, ReviewDecision and gate.

**Failure/hold path:** Live contacts, opportunity orchestration, review UI and authenticated service are not implemented. Reference preview is J07. Unknown maturity blocks maturity claims, not every neutral question.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Changed content invalidates old review; demoted template blocks current use; incomplete contact assessment holds contact-specific export.

### J14 — Approve a campaign, enroll and schedule one step

**Actor:** Sales operations. **Readiness:** PROPOSED. **Stages:** F19–F20.

**Features:** FM29, FM30. **Open findings:** See general implementation boundaries.

**Preconditions / inputs:** Approved program/campaign, assessed contact, reviewed content and restrictions.

1. Define allowed audience, templates, sequence steps, sender limits, timezone and stop rules.
2. Choose exactly one scheduling authority: local application or provider.
3. Approve campaign readiness separately from reviewing one account message.
4. Enroll an eligible contact with deduplication and cross-campaign frequency limits.
5. Produce a due DeliveryIntent; do not send just because a package exists.

**Outputs to inspect:** CampaignApproval, Enrollment, StepEligibility and stable DeliveryIntent.

**Failure/hold path:** No campaign, enrollment or schedule-management CLI/API exists. Do not invent provider campaign IDs or activation commands.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Duplicate enrollment is idempotent, step progression has one owner, reply/opt-out/customer exclusions hold subsequent steps.

### J15 — Authorize, dispatch and reconcile a message

**Actor:** Sales operations. **Readiness:** PROPOSED. **Stages:** F21–F22.

**Features:** FM31. **Open findings:** See general implementation boundaries.

**Preconditions / inputs:** DeliveryIntent, exact message, authenticated authority and a dedicated send gate.

1. Resolve the exact reviewed message and stable logical send identity.
2. Check current contact, campaign, enrollment, source rights, restrictions and sender readiness.
3. Commit intent/outbox state before external dispatch.
4. Record acceptance, rejection or uncertainty.
5. Reconcile possible acceptance before retry; do not equate acceptance with inbox delivery.

**Outputs to inspect:** Delivery attempt, receipt, Exposure or unresolved reconciliation state.

**Failure/hold path:** No sender exists. Current canonical preview/contact export purposes are not send authority. New attempts and CRM retries never authorize duplicate sends.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Provider timeout after acceptance results in one reconciled send, not a blind retry. Late restrictions stop subsequent actions with actual chronology retained.

### J16 — Handle replies, stop outreach and hand off to sales/CRM

**Actor:** Sales representative. **Readiness:** PROPOSED. **Stages:** F23–F24.

**Features:** FM32, FM33. **Open findings:** See general implementation boundaries.

**Preconditions / inputs:** Verified event, permitted content, contact/exposure/enrollment IDs and current restrictions.

1. Authenticate and deduplicate inbound events; correlate the exposure and conversation.
2. Apply immediate pause/stop/restriction rules before optional model classification.
3. Route interest, questions, objections, out-of-office and referrals appropriately.
4. Create human response/sales-handoff tasks.
5. Synchronize CRM with field ownership and idempotent receipts; reconcile retries without resending outreach.

**Outputs to inspect:** Conversation, ReplyAssessment, EnrollmentControl, follow-up/SalesHandoff and CRM sync receipt.

**Failure/hold path:** No mailbox/webhook/CRM runtime exists here. An opt-out cannot wait for analytics or a model. Referrals create candidates, not automatic outreach permission.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Duplicate events do not duplicate effects; CRM failure retries only the CRM action; uncorrelated events are quarantined without invented exposure links.

### J17 — Correct identity or revoke evidence/authority

**Actor:** Administrator. **Readiness:** REFERENCE / LOCAL OWNER ONLY. **Stages:** F26.

**Features:** FM35. **Open findings:** F01, F02, F04, F10.

**Preconditions / inputs:** Trusted configured actor (reference only), exact target, reason, effective/recorded chronology and policy.

1. Identify the exact fact, binding, artifact, template or source and its dependencies.
2. Authorize the requested correction/revocation with typed target and tenant ownership.
3. Keep history while blocking current use and invalidating affected projections.
4. Separate historical reads from current action permission.
5. Verify all dependent research, identity and content surfaces report the changed state.

**Outputs to inspect:** Reference ChangeRecord validation or local collector capture revocation; production workflow still absent.

**Failure/hold path:** F01 binding support, F02 template gate and F10 research candidates are incomplete. Hosted auth/grant management/deletion workers remain unimplemented. Historical metadata retention is policy-specific.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Required-behavior tests for F01/F02/F10/F04 must pass before presenting a complete revoke/correct workflow.

### J18 — Measure outcomes and improve rules/templates

**Actor:** QA/analyst. **Readiness:** PROPOSED. **Stages:** F08,F25.

**Features:** FM15, FM34. **Open findings:** See general implementation boundaries.

**Preconditions / inputs:** Valid exposures/outcomes, evaluation sets, release versions and measurement policies.

1. Join verified outcomes to deduplicated exposures and sample eligible mature windows.
2. Keep denominator, attribution, exclusions and missingness explicit.
3. Measure detector/extractor quality separately from outreach conversion.
4. Evaluate changes on appropriate gold sets or approved experiments.
5. Review promotion proposals and publish a new immutable release for later runs.

**Outputs to inspect:** Descriptive measurement facts, QualityAssessment and PromotionProposal.

**Failure/hold path:** No full metric/experiment/promotion runtime exists. Success rates cannot turn weak evidence into truth; observational comparison is not causal proof.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Retries, duplicate replies, immature response windows, selection bias and source-origin duplication are covered by acceptance tests before activation.

### J19 — Run submodules separately and prepare service extraction

**Actor:** Integration engineer. **Readiness:** LOCAL PROCESSES; PROPOSED SERVICES. **Stages:** F03,F26.

**Features:** FM36. **Open findings:** F03, F11, F12, F13, F15.

**Preconditions / inputs:** Existing package, typed contract plans, service ownership map, scoped storage and release locks.

1. Use J03 for extract/match/check/resolve in separate Python processes.
2. Retain one owner for publication, canonical admission, enrollment/send intent and restrictions.
3. Add a real enforcing runner and trusted record resolver before remote workers.
4. Close operation modes/effects, timeout diagnostics, auth, idempotency and transaction boundaries.
5. Extract a service only for a demonstrated isolation/scaling reason; do not deploy one service per cheap extractor.

**Outputs to inspect:** Today: standalone JSON artifacts/logs. Later: authorized worker requests/results with tested boundary parity.

**Failure/hold path:** There is no HTTP endpoint, broker, distributed tracing backend or generic task dispatcher. Shared SQLite across machines is not a service architecture.

**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.

**Acceptance:** Pure outputs agree across in-process and worker execution. F03/F11/F12/F13/F15 must be closed before wrapper behavior is relied on.

## Direct commands behind J03

After J01 creates `journey-output/demo-store`, these are the actual collector entrypoints (after editable installation). They are separate processes, not services:

```bash
# Select a technical capture that actually supports an observation.
CAPTURE_ID=$(python -c 'import json; print(json.load(open("journey-output/demo-store/scan-bundle.json"))["observations"][0]["capture_id"])')
ks-module extract --tenant demo --capture-id "$CAPTURE_ID"   --store ./journey-output/demo-store --output ./journey-output/page-evidence.json
ks-module match --page ./journey-output/page-evidence.json   --rules ./baseline/collector/examples/demo-rules.json   --store ./journey-output/demo-store --output ./journey-output/matches.json
ks-module check --bundle ./journey-output/demo-store/scan-bundle.json   --store ./journey-output/demo-store --output ./journey-output/checked.json
ks-module resolve --bundle ./journey-output/demo-store/scan-bundle.json   --as-of 2026-09-14T12:00:00Z --store ./journey-output/demo-store   --output ./journey-output/resolved.json
```

For reference validation, use `(cd baseline/canonical && python validate.py)`. It validates the included bundle; it does not accept a collector bundle or run the missing canonical service.

For the protocol, use `(cd baseline/protocol && python validate_protocol.py)`. Only the shipped example operation/signature is registered. There is no working `ks-program`, `ks-enroll`, `ks-send`, generic `--module KN-02`, or HTTP service command in this package.

## Read-only diagnostics for an existing local store

This inspection does not update attempts or claims:

```bash
python - <<'PYREAD'
from pathlib import Path
import sqlite3,json
path=Path('journey-output/demo-store/scanner.sqlite3').resolve()
with sqlite3.connect(path.as_uri()+'?mode=ro',uri=True) as db:
    db.row_factory=sqlite3.Row
    for row in db.execute('SELECT tenant,run_id,request_key,status,payload FROM attempts ORDER BY rowid'):
        r=dict(row);r['payload']=json.loads(r['payload']);print(json.dumps(r))
PYREAD
```

Local filesystem ownership is trusted. These CLI flags and reads are not authentication or multi-tenant authorization.

## Separate-process acceptance versus service deployment

The evidence here verifies local process invocation with a shared local owner. A service must additionally authenticate callers, resolve scoped immutable records, enforce exact operation/effect signatures, preserve successful/failed target manifests, and publish one consistent payload transactionally. The original service extraction document remains in `baseline/docs/SERVICE_EXTRACTION.md`; this audit adds blockers F03, F11, F12, F13 and F15 to its pre-service gate.
