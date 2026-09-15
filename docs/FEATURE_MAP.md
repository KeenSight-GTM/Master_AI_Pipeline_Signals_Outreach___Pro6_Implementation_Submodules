> Consolidated workspace: run commands from the repository root. Use `python tools/workspace.py journeys --output ../keensight-journeys` for relocated paths. This is the retained audit walkthrough, not a claim that open bugs were fixed.

# E2E feature map and invocation boundaries

This map covers all 39 logical module IDs through 36 user-facing feature areas. It is grounded in collector 0.2.0, canonical reference 4.2.0 and the supplied product design. Features are not declared implemented merely because a schema, diagram or module name exists.

## Readiness legend

- **LOCAL:** a narrow local operation is implemented and exercised by the offline journeys; not production sign-off.
- **REFERENCE:** only synthetic/reference functions or validation are executable; no real product workflow is implied.
- **SDK_UNVERIFIED:** a real adapter exists but its dependency/integration could not be run here.
- **DISABLED:** the delivered entrypoint deliberately refuses the capability.
- **PROPOSED:** design/contract only; no working invocation exists.

`walkthroughs/run_local_journeys.py` is a test/documentation harness, not a replacement execution engine. It makes no network requests or sends.

| Feature | User | Readiness | Modules | Journey / callable boundary |
|---|---|---|---|---|
| FM01 — Define program, audience and offer | Growth lead | PROPOSED | GTM-01 | J10: Not implemented; no command/API to invoke |
| FM02 — Discover and select account seeds | Research operator | PROPOSED | GTM-02 | J10: Not implemented; no command/API to invoke |
| FM03 — Validate rules, contracts and release metadata | Engineer | REFERENCE | CTL-01, CTL-03 | J08: reference-checks |
| FM04 — Run the synthetic scanner demonstration | Engineer | LOCAL | CTL-02, ING-02, ING-03, FP-02 | J01: demo |
| FM05 — Analyze retained HTML | Research engineer | LOCAL | ING-02, ING-04, FP-01, FP-02 | J02: analyze-file |
| FM06 — Capture an authorized website with Scrapling | Collection operator | SDK_UNVERIFIED | ING-02, ING-03 | J09: scan (dependency-gated) |
| FM07 — Render JavaScript/browser/network evidence | Collection operator | DISABLED | ING-03 | J09: Not implemented; no command/API to invoke |
| FM08 — Extract the 17 surfaces as an independent process | Debugger | LOCAL | ING-04 | J03: extract |
| FM09 — Match pinned rules as an independent process | Rule engineer | LOCAL | FP-01 | J03: match |
| FM10 — Inspect duplicate support and collector claim views | Analyst | LOCAL | FP-02 | J01, J03, J04: resolve / claims |
| FM11 — Verify bundle, metadata and original bytes | Debugger | LOCAL | PLAT-01, FP-02 | J03, J06: check |
| FM12 — Replay retained evidence under a selected rule release | Rule engineer | LOCAL | ING-05 | J04: replay |
| FM13 — Import the supported donor-rule subset | Rule curator | LOCAL | FP-03 | J05: import-donor |
| FM14 — Inspect recurring unknown technical features | Rule curator | LOCAL | FP-03 | J05: candidates |
| FM15 — Promote and distribute reviewed rules | Rule reviewer | PROPOSED | FP-03, QA-01 | J05, J18: Not implemented; no command/API to invoke |
| FM16 — Resolve production subject identity | Research analyst | PROPOSED | KN-01 | J11: Not implemented; no command/API to invoke |
| FM17 — Admit collector output as canonical facts | Knowledge engineer | PROPOSED | KN-02 | J11: Not implemented; no command/API to invoke |
| FM18 — Check canonical claim resolution and samples | Knowledge engineer | REFERENCE | KN-03, KN-04 | J07: canonical validate / Python fixture API |
| FM19 — Capture broad third-party source families | Research operator | PROPOSED | ING-01, CTL-03 | J12: Not implemented; no command/API to invoke |
| FM20 — Run bounded live model extraction and repair | Research engineer | PROPOSED | AI-01 | J12: Not implemented; no command/API to invoke |
| FM21 — Compute research priors and explicit context joins | Research analyst | REFERENCE | RE-02, RE-03 | J07, J12: canonical fixture validation / Python helpers |
| FM22 — Find comparable cases and rank lookalikes | Strategy analyst | PROPOSED | RE-04 | J12: Not implemented; no command/API to invoke |
| FM23 — Evaluate derivations and business conditions | Analyst | REFERENCE | RE-01, RE-05 | J07, J12: reference functions, not a product CLI |
| FM24 — Choose a supported commercial opportunity | Growth operator | PROPOSED | COM-01 | J13: Not implemented; no command/API to invoke |
| FM25 — Assess contact, role, endpoint and permission | Sales researcher | PROPOSED | AUD-01 | J13: Not implemented; no command/API to invoke |
| FM26 — Render existing reference packages | Content reviewer | REFERENCE | COM-02 | J07: Bundle.render(existing_package) |
| FM27 — Approve exact content through an authenticated workspace | Reviewer | PROPOSED | COM-03, UX-01 | J13: Not implemented; no command/API to invoke |
| FM28 — Export a local reference preview with idempotency | Reference tester | REFERENCE | COM-04 | J07: LocalPreviewExporter via walkthrough helper |
| FM29 — Configure campaigns and sequence ownership | Sales operations | PROPOSED | CAM-01 | J14: Not implemented; no command/API to invoke |
| FM30 — Enroll a contact and schedule/stop steps | Sales operations | PROPOSED | CAM-02 | J14: Not implemented; no command/API to invoke |
| FM31 — Dispatch and reconcile an exact authorized message | Sales operations | PROPOSED | COM-05 | J15: Not implemented; no command/API to invoke |
| FM32 — Route replies and immediate stop requests | Sales representative | PROPOSED | ENG-01, COM-06 | J16: Not implemented; no command/API to invoke |
| FM33 — Synchronize sales handoff with CRM | Sales owner | PROPOSED | CRM-01 | J16: Not implemented; no command/API to invoke |
| FM34 — Measure outcomes, experiments and calibration | Analyst/QA | PROPOSED | COM-06, QA-01 | J18: Not implemented; no command/API to invoke |
| FM35 — Govern evidence, bindings, changes and retention | Administrator | REFERENCE | PLAT-02, KN-03 | J17: Store.revoke or Bundle.validate_change (local/reference only) |
| FM36 — Inspect/debug individual modules and service boundaries | Engineer/operator | LOCAL | PLAT-01, PLAT-03, UX-01 | J03, J06, J08, J19: ks-module and offline walkthrough harness |

## Feature outputs and limitations

### FM01 — Define program, audience and offer

**Expected output:** Versioned ProgramDefinition/AudienceDefinition/OfferDefinition.

**Boundary:** No program CLI, API or UI exists.

### FM02 — Discover and select account seeds

**Expected output:** AccountSeed, LeadSelection, ResearchPlan.

**Boundary:** The collector accepts a URL; it does not discover the complete prospect universe or import Harvest automatically.

### FM03 — Validate rules, contracts and release metadata

**Expected output:** Validation reports and fixture signature checks.

**Boundary:** No unified release compiler or effect-enforcing runner.

### FM04 — Run the synthetic scanner demonstration

**Expected output:** ScanBundle and deduplicated claim view.

**Boundary:** Synthetic transport and fixture authority; no real Scrapling call.

### FM05 — Analyze retained HTML

**Expected output:** Stored capture, evidence, matches, observations and ScanBundle.

**Boundary:** Operator asserts source/time/subject; use a unique run per target. F09.

### FM06 — Capture an authorized website with Scrapling

**Expected output:** Artifacts, attempts, bundle or diagnostics.

**Boundary:** SDK unavailable in the audit environment; no live integration claim.

### FM07 — Render JavaScript/browser/network evidence

**Expected output:** Proposed rendered Capture and network artifacts.

**Boundary:** FETCH_STEALTH is a disabled extension point. No public browser runtime.

### FM08 — Extract the 17 surfaces as an independent process

**Expected output:** PageEvidence with per-extractor reports.

**Boundary:** Parser-loss completeness and aside-region parity need F06/F14.

### FM09 — Match pinned rules as an independent process

**Expected output:** StandaloneMatchResult.

**Boundary:** Not canonical facts; no output publication to canonical store.

### FM10 — Inspect duplicate support and collector claim views

**Expected output:** One view per claim with all support links.

**Boundary:** Historical collector view, not a current commercial use gate.

### FM11 — Verify bundle, metadata and original bytes

**Expected output:** Valid response or nonzero rejection.

**Boundary:** Offline structural-only check without --store is weaker; use trusted store verification.

### FM12 — Replay retained evidence under a selected rule release

**Expected output:** New evaluation with original observation dates.

**Boundary:** Compatible release replay verified; no recapture, model call or TTL refresh.

### FM13 — Import the supported donor-rule subset

**Expected output:** Candidate rule pack and quarantine report.

**Boundary:** No inherited approval or complete donor-corpus integration.

### FM14 — Inspect recurring unknown technical features

**Expected output:** Candidate/prevalence rows.

**Boundary:** Revoked support is not filtered from current counts: F10.

### FM15 — Promote and distribute reviewed rules

**Expected output:** Reviewed immutable fingerprint release.

**Boundary:** No complete promotion/calibration/distribution runtime.

### FM16 — Resolve production subject identity

**Expected output:** Accepted binding with exact identity evidence.

**Boundary:** Fixture bindings exist; real resolver and admission workflow do not.

### FM17 — Admit collector output as canonical facts

**Expected output:** Fact/Evidence/Execution plus admission report.

**Boundary:** Executable bridge and persistent canonical repository absent.

### FM18 — Check canonical claim resolution and samples

**Expected output:** Reference validation and decision results.

**Boundary:** Not a hosted query API; sealed/current semantics need F04.

### FM19 — Capture broad third-party source families

**Expected output:** Approved artifacts and source-specific fact drafts.

**Boundary:** 213 predicate definitions are not 213 implemented collectors.

### FM20 — Run bounded live model extraction and repair

**Expected output:** ModelCall, artifacts, repair chain, typed output.

**Boundary:** Reference checks only; generated-output consumer bug F05.

### FM21 — Compute research priors and explicit context joins

**Expected output:** Sample-bound priors and internal ContextAssessment.

**Boundary:** No live-source research job; context is not outward company proof.

### FM22 — Find comparable cases and rank lookalikes

**Expected output:** Comparison and LookalikeMatch.

**Boundary:** No vector service/index or verified causal transfer.

### FM23 — Evaluate derivations and business conditions

**Expected output:** Derived drafts and signal decisions.

**Boundary:** Minimum-support units disagree: F08. Production selectors absent.

### FM24 — Choose a supported commercial opportunity

**Expected output:** OpportunitySelection.

**Boundary:** A detected tool does not automatically prove pain or offer fit.

### FM25 — Assess contact, role, endpoint and permission

**Expected output:** ContactProfile and ContactAssessment.

**Boundary:** No contact enrichment/verification runtime.

### FM26 — Render existing reference packages

**Expected output:** Grounded text from delivered fixture templates.

**Boundary:** No arbitrary-prose proof engine or all-channel renderer.

### FM27 — Approve exact content through an authenticated workspace

**Expected output:** ReviewDecision tied to exact revision/hash.

**Boundary:** Synthetic reviews and actor grants are fixtures, not human auth/UI.

### FM28 — Export a local reference preview with idempotency

**Expected output:** Local JSON preview; repeated key reuses bytes.

**Boundary:** No remote CRM export or send; current template veto F02.

### FM29 — Configure campaigns and sequence ownership

**Expected output:** CampaignDefinition/Approval/Readiness.

**Boundary:** No campaign manager or provider configuration mutation.

### FM30 — Enroll a contact and schedule/stop steps

**Expected output:** Enrollment, StepEligibility, DeliveryIntent.

**Boundary:** No durable enrollment/scheduler runtime.

### FM31 — Dispatch and reconcile an exact authorized message

**Expected output:** Attempt, receipt, Exposure.

**Boundary:** No sender; preview/export gates do not authorize sending.

### FM32 — Route replies and immediate stop requests

**Expected output:** Conversation, assessment, stop control, follow-up.

**Boundary:** No authenticated webhook/mailbox integration.

### FM33 — Synchronize sales handoff with CRM

**Expected output:** CRMSyncIntent/Receipt and linked handoff.

**Boundary:** No connected CRM mutations performed or implemented in this package.

### FM34 — Measure outcomes, experiments and calibration

**Expected output:** Attributable measurements and reviewed promotion proposals.

**Boundary:** Tests and schemas exist; no full exposure/attribution/experiment pipeline.

### FM35 — Govern evidence, bindings, changes and retention

**Expected output:** Revocation/change validation.

**Boundary:** No hosted auth, real retention worker or restore service. F01/F10 remain.

### FM36 — Inspect/debug individual modules and service boundaries

**Expected output:** JSON outputs and per-process logs.

**Boundary:** No operator UI, distributed trace backend or general ModuleRequest runner.

## Execution boundaries that must remain explicit

A call to `canonical/validate.py` checks the supplied fixture bundle. It does not run account research, create a canonical service, execute all derivations, or perform identity resolution. `protocol/validate_protocol.py` checks its shipped example and signature; it does not accept arbitrary runtime requests or provide an HTTP endpoint. `ks-module` calls are separate processes around collector functions, not the proposed ModuleRequest transport. The local reference exporter does not create review decisions or send messages.

Raw observations and product/industry context stay broad. Feature activation controls what can be computed or used, not whether the schema catalog must shrink to the initial few signals.
