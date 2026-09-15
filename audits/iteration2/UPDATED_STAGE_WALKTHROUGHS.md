# Expanded implementation walkthrough: 27 stages with feature/invocation links

Original F00–F26 titles, owners, inputs and outputs are preserved from the supplied stage_cards.json. New sections below link user-facing features, callable boundaries and this audit. No missing handler is silently treated as implemented.

## F00 — Define program and offer

**Owners:** GTM-01

**Original stated inputs:** ProgramDefinition, AudienceDefinition, OfferDefinition

**Original stated outputs:** Program revision and capability-profile reference

**Processing:** Check owner approval, geography, source purposes, service-line prerequisites, exclusions and budget. Freeze the revision used for a selection run.

**Transaction:** One configuration revision commits atomically. No account facts or provider calls are produced.

**Failure path:** Reject an invalid program; never translate an audience criterion into a fact that a prospect satisfies it.

**Identity:** (tenant, program_id, revision, content_hash)

**Original critique question:** Which exclusions and offers are mandatory, and who can approve a change?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM01: Define program, audience and offer | PROPOSED | No implementation; J10 |

**User walkthroughs:** J10. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F01 — Source and select account seeds

**Owners:** GTM-02

**Original stated inputs:** Program revision; CSV/Harvest or approved source records; existing CRMAccountView

**Original stated outputs:** AccountSeed, LeadSelection, ResearchPlan, IntakeRequest

**Processing:** Preserve original source and external IDs. Normalize provisional targets. Deduplicate seeds without assuming domain ownership. Record fit and exclusion decisions against their input snapshot.

**Transaction:** Commit seed provenance and selection decisions together. Discovery calls, when enabled, are separate acquisition attempts.

**Failure path:** Unresolved account or stale relevant CRM exclusion becomes HOLD, not invented identity or a lost seed.

**Identity:** (tenant, source_namespace, external_record, revision, program_revision)

**Original critique question:** What constitutes the same account: legal entity, location, brand or franchisee?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM02: Discover and select account seeds | PROPOSED | No implementation; J10 |

**User walkthroughs:** J10. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F02 — Bind subject and permitted scope

**Owners:** KN-01

**Original stated inputs:** Provisional target; existing subjects; literal identity evidence

**Original stated outputs:** Subject, SubjectBinding, resolved or unresolved target

**Processing:** Resolve organization/location/person/product/industry separately. Require evidence for website ownership and relationships. Keep aliases and external IDs namespaced. Redirect/canonical tags are claims, not automatic ownership proof.

**Transaction:** Subject and accepted binding decisions commit under one owner. Preserve rejected and ambiguous candidates.

**Failure path:** Ambiguity blocks account-specific admission/copy but may still allow a bounded diagnostic capture request.

**Identity:** (tenant, candidate_identity, binding_policy, evidence_digest)

**Original critique question:** When may a multi-location domain support organization-wide conclusions?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM16: Resolve production subject identity | PROPOSED | No implementation; J11 |

**User walkthroughs:** J11. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F01 — Identity-binding evidence is outside eligibility/provenance closure

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F03 — Authorize and pin execution

**Owners:** CTL-01, CTL-02, CTL-03

**Original stated inputs:** IntakeRequest; trusted principal; profile; installed implementation manifest

**Original stated outputs:** ReleaseLock, BatchRun, authorized context, bounded work specification

**Processing:** Resolve exact schemas/functions/rules/mappings and allowed operations. Verify acyclic dependency closure including self-edges. Obtain tenant and permissions from trusted local configuration or authentication, not caller text.

**Transaction:** Persist run configuration and idempotency identity before scheduling. The initial runner is sequential, not distributed.

**Failure path:** Missing implementation or incompatible schema is a startup failure. Disabled capabilities are recorded as disabled, not false business conditions.

**Identity:** (tenant, logical_request, normalized_config_hash, release_lock)

**Original critique question:** Which operations must fail the whole target rather than return a partial knowledge result?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM03: Validate rules, contracts and release metadata | REFERENCE | reference-checks; J08 |
| FM04: Run the synthetic scanner demonstration | LOCAL | demo; J01 |
| FM19: Capture broad third-party source families | PROPOSED | No implementation; J12 |

**User walkthroughs:** J01, J08, J12. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F05 — Generated-artifact handoff is accepted by one validator and rejected by another; F09 — Retained-file import does not pin subject identity in run configuration; F12 — No-byte failures lose invocation details and have no persisted evaluation manifest; F13 — Protocol rejects an honest timeout failure reported after its deadline; F15 — The protocol fixture does not constrain mode/effects against operation parameters

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F04 — Plan bounded Scrapling acquisition

**Owners:** ING-02

**Original stated inputs:** Target origin; robots/source policy; previous capture disposition; budget

**Original stated outputs:** ScanPlan and per-resource acquisition requests

**Processing:** Normalize URL. Apply origin policy to seeds, sitemap entries, redirects and probes. Rank requested templates. Budget attempts, not successes; count metadata and redirects. Do not submit forms or authenticate into public portals.

**Transaction:** Persist request identity before execution; a PENDING prior attempt is crash uncertainty. Resume cannot reset the budget.

**Failure path:** Malformed discoveries become diagnostics. Robots denial or cooldown prevents content capture; 429 is not a reason to bypass controls.

**Identity:** (tenant, capture_run, normalized_URL, capture_mode)

**Original critique question:** Is eight top-level attempts an acceptable fast-profile limit, and what triggers an expanded profile?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM04: Run the synthetic scanner demonstration | LOCAL | demo; J01 |
| FM05: Analyze retained HTML | LOCAL | analyze-file; J02 |
| FM06: Capture an authorized website with Scrapling | SDK_UNVERIFIED | scan (dependency-gated); J09 |

**User walkthroughs:** J01, J02, J09. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F09 — Retained-file import does not pin subject identity in run configuration

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F05 — Capture response or honest failure

**Owners:** ING-03

**Original stated inputs:** One approved request; transport policy; attempt budget

**Original stated outputs:** AcquisitionAttempt; Capture; original blob; headers; limitations

**Processing:** Use one checked static request, with explicit redirects/retries outside the SDK. Retain approved bytes and scrubbed headers. Bind capture metadata to the trusted stored record. A denied/no-byte request gets a diagnostic, not an empty response.

**Transaction:** Finalize blob before reference commit. Orphan blobs can be cleaned up; positive output cannot reference missing bytes. Attempts and response time remain distinct from evaluation time.

**Failure path:** Timeout, rate limit, body truncation, network denial or unavailable SDK records failure/incomplete status. Browser remains disabled until its separate egress and resource contract is tested.

**Identity:** (tenant, capture_run, request_key); capture ID does not collapse distinct observations by body hash

**Original critique question:** What response modalities and retention classes are permitted per source?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM04: Run the synthetic scanner demonstration | LOCAL | demo; J01 |
| FM06: Capture an authorized website with Scrapling | SDK_UNVERIFIED | scan (dependency-gated); J09 |
| FM07: Render JavaScript/browser/network evidence | DISABLED | No implementation; J09 |

**User walkthroughs:** J01, J09. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F12 — No-byte failures lose invocation details and have no persisted evaluation manifest

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F06 — Extract evidence surfaces

**Owners:** ING-04

**Original stated inputs:** Trusted Capture and retained bytes; parser release

**Original stated outputs:** PageEvidence, Surface records, per-extractor CommandResult

**Processing:** Decode with pinned BOM/transport/declaration/fallback policy. Run all applicable extraction functions. Preserve element context, raw JSON-LD, parsed subjects, errors, node-local attributes and surface completeness. Label static prose as not computed CSS visibility.

**Transaction:** No canonical business writes. Standalone output is a typed evidence artifact. Metadata and extraction can be verified by recomputing against original bytes.

**Failure path:** A failed extractor emits diagnostics without positive surfaces. Item/text limits are PARTIAL. An empty complete extraction is distinct from an unperformed check.

**Identity:** (capture_id, parser_release, extractor_parameters)

**Original critique question:** Which surface limits are safe for our target-site sizes?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM05: Analyze retained HTML | LOCAL | analyze-file; J02 |
| FM08: Extract the 17 surfaces as an independent process | LOCAL | extract; J03 |

**User walkthroughs:** J02, J03. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F06 — HTML recovery can silently truncate the parse while reporting complete detection; F14 — Collector and canonical matcher disagree on aside-region semantics

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F07 — Match, preserve support and consolidate

**Owners:** FP-01, FP-02

**Original stated inputs:** Page/host evidence; immutable rule pack; canonical product mapping

**Original stated outputs:** All Match records; Observation; SupportLink; ClaimView; ScanBundle

**Processing:** Evaluate declared surfaces, alternatives and correlation scope. Preserve each rule/element support, but make one observation per captured claim/value. Keep separate pages/scans as history. Do not combine authored confidence or count overlapping detectors as independent origins.

**Transaction:** Validate full candidate bundle before atomic publication of findings, research features and replay-selection manifest. Raw capture diagnostics may survive failure; supported claims must not.

**Failure path:** No pages is NOT_EVALUATED. Required truncated surface is PARTIAL, not ordinary NO_MATCH. Conflicting values stay conflict. Gates/scores affect selection, never source authority.

**Identity:** match=(semantic_rule_digest,release,capture,surface,branch); observation excludes rule ID

**Original critique question:** Are presence, mention, provider report and verified capability kept separate for each imported rule?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM04: Run the synthetic scanner demonstration | LOCAL | demo; J01 |
| FM05: Analyze retained HTML | LOCAL | analyze-file; J02 |
| FM09: Match pinned rules as an independent process | LOCAL | match; J03 |
| FM10: Inspect duplicate support and collector claim views | LOCAL | resolve / claims; J01, J03, J04 |
| FM11: Verify bundle, metadata and original bytes | LOCAL | check; J03, J06 |

**User walkthroughs:** J01, J02, J03, J04, J06. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F03 — Publication validates one payload and can persist a different argument set; F06 — HTML recovery can silently truncate the parse while reporting complete detection; F09 — Retained-file import does not pin subject identity in run configuration; F11 — Contradictory duplicate command outcomes are accepted; F14 — Collector and canonical matcher disagree on aside-region semantics

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F08 — Review dynamic fingerprint candidates

**Owners:** FP-03

**Original stated inputs:** Unknown technical features; bounded distinct-site samples; donor rows

**Original stated outputs:** Candidate records, quarantine report, review proposal, next immutable rule release

**Processing:** Normalize stable technical residues and count sites without counting repeated visits as new sites. Retain every donor row with disposition. A reviewer/model may propose a definition; only explicit approval after fixture/calibration checks can change production eligibility.

**Transaction:** The active scan never rewrites its pinned rule release. Technical index is rebuildable, not a second canonical fact store.

**Failure path:** Unsupported operators/mappings are quarantined. Candidate status, prevalence and high authored confidence never auto-promote a rule.

**Identity:** (feature_normalizer_version, feature_key); reviewed rule semantic digest

**Original critique question:** What gold-set precision and false-positive criteria authorize promotion?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM13: Import the supported donor-rule subset | LOCAL | import-donor; J05 |
| FM14: Inspect recurring unknown technical features | LOCAL | candidates; J05 |
| FM15: Promote and distribute reviewed rules | PROPOSED | No implementation; J05, J18 |

**User walkthroughs:** J05, J18. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F10 — Current candidate discovery counts unlabelled revoked evidence

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F09 — Admit canonical facts

**Owners:** KN-02

**Original stated inputs:** Collector/source output; concrete support; verified bindings; successful producer

**Original stated outputs:** Fact, EvidenceSet, EvidenceLocator, ExecutionRecord, admission report

**Processing:** Map collector meaning to a registered predicate/nature. Verify actual bytes/locators, successful production, object schema, scope, time, source rights and binding. Preserve complete provenance. A fixture proving a rule works is not proof this fact was detected.

**Transaction:** One fact transaction writes fact, lineage and admission decision. Reject duplicate identity with different payload. This bridge is still to implement; collector observations are not canonical Fact objects.

**Failure path:** Rejected candidates remain quarantined. Non-detection requires completed capture AND compatible successful detector coverage.

**Identity:** (tenant, subject, predicate, nature, scope, target, window, observation_origin)

**Original critique question:** Which source-specific mappings permit commercial use rather than internal storage only?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM17: Admit collector output as canonical facts | PROPOSED | No implementation; J11 |

**User walkthroughs:** J11. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F01 — Identity-binding evidence is outside eligibility/provenance closure; F05 — Generated-artifact handoff is accepted by one validator and rejected by another; F07 — A self-superseding fact raises RecursionError before semantic rejection; F14 — Collector and canonical matcher disagree on aside-region semantics; F16 — effective_at is stored but its decision semantics are undefined/unused

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F10 — Resolve the complete claim group

**Owners:** KN-03

**Original stated inputs:** All eligible observations for the claim identity; binding/source/change state

**Original stated outputs:** ClaimResolution and retained observation history

**Processing:** Group with target/cardinality and temporal dimensions, not just subject+predicate. Preserve vendors and source disagreements. Use explicit resolution rules; UNKNOWN does not erase usable knowledge. Multiple model transcripts are not independent support.

**Transaction:** Resolution is a derived projection; original facts are retained. Authorized corrections have typed targets, actors, tenant ownership, compatible replacements and chronology.

**Failure path:** Conflict is a successful resolution result, not a software exception. It blocks cherry-picked downstream proof.

**Identity:** (claim_key, input_membership_hash, resolution_policy, as_of)

**Original critique question:** Which conflicts require human adjudication instead of automatic precedence?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM18: Check canonical claim resolution and samples | REFERENCE | canonical validate / Python fixture API; J07 |
| FM35: Govern evidence, bindings, changes and retention | REFERENCE | Store.revoke or Bundle.validate_change (local/reference only); J17 |

**User walkthroughs:** J07, J17. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F01 — Identity-binding evidence is outside eligibility/provenance closure; F04 — Later supersession leaks into an earlier sealed evaluation; F07 — A self-superseding fact raises RecursionError before semantic rejection; F08 — Requirement minimum means fact count in the helper but origin count in validation; F16 — effective_at is stored but its decision semantics are undefined/unused

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F11 — Seal evaluation inputs and execute dependencies

**Owners:** KN-04, CTL-02

**Original stated inputs:** Requested account/product evaluation; current knowledge; exact release versions

**Original stated outputs:** InputSnapshot / BatchRun manifests and scheduled operations

**Processing:** Separate sealed external inputs from artifacts/facts produced in this run. Each produced record has one declared successful producer; a consumer cannot read it before completion. Keep logical as_of, knowledge cutoff, capture time and wall-clock execution time distinct.

**Transaction:** Publish complete targets independently. Do not hold one database transaction across model or HTTP calls.

**Failure path:** Unknown or unpinned references, self-produced input cycles, failed producers and unauthorized current reads abort that operation.

**Identity:** (tenant, target, external_input_digest, release_lock, logical_as_of)

**Original critique question:** Must selected facts be frozen per account or per program batch?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM04: Run the synthetic scanner demonstration | LOCAL | demo; J01 |
| FM18: Check canonical claim resolution and samples | REFERENCE | canonical validate / Python fixture API; J07 |

**User walkthroughs:** J01, J07. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F04 — Later supersession leaks into an earlier sealed evaluation; F05 — Generated-artifact handoff is accepted by one validator and rejected by another; F09 — Retained-file import does not pin subject identity in run configuration; F12 — No-byte failures lose invocation details and have no persisted evaluation manifest; F13 — Protocol rejects an honest timeout failure reported after its deadline

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F12 — Acquire enrichment and run bounded model tasks

**Owners:** ING-01, AI-01

**Original stated inputs:** Approved source/task request; selected evidence; model/prompt configuration; budget

**Original stated outputs:** Typed provider records, ModelCall, raw request/response artifacts, RepairAttempt

**Processing:** Keep all eleven fact areas and the ledger sources available as registered capabilities. Provider estimates stay estimates, statements stay attributed statements, hypotheses stay internal. Retain raw I/O before parse; every repair consumes the same bounded budget.

**Transaction:** External calls have durable attempt IDs. Generated model I/O enters the produced-artifact manifest, not backdated external inputs. Deterministic downstream replay consumes retained responses, not a new call.

**Failure path:** Invalid output/repair exhaustion yields abstention. Source denial, rate limits, unknown costs and unsupported fields remain explicit.

**Identity:** (task_version, exact_inputs, prompt/config); new model call is not replay

**Original critique question:** Which sources are approved and which exact tasks should spend model budget?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM19: Capture broad third-party source families | PROPOSED | No implementation; J12 |
| FM20: Run bounded live model extraction and repair | PROPOSED | No implementation; J12 |

**User walkthroughs:** J12. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F05 — Generated-artifact handoff is accepted by one validator and rejected by another

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F13 — Build research samples and priors

**Owners:** RE-02

**Original stated inputs:** Product/industry review/discussion records; sample decisions; support policy

**Original stated outputs:** ResearchSample, classifications, prior drafts and execution report

**Processing:** Record every retrieved item: eligible, support, contradict, no-theme, unclassified, excluded. Deduplicate original record identities. Distinguish workflow mention from negative experience. Pin all numerator, denominator and exclusion dependencies.

**Transaction:** Calculation drafts pass canonical admission. A denominator-only deletion invalidates current use of the statistic even if supporting items remain.

**Failure path:** No eligible denominator is UNKNOWN. A biased or selected sample cannot imply population prevalence or company-specific pain.

**Identity:** (sample_membership, dispositions, classification_release, window, support_policy)

**Original critique question:** What is the sample population and which selection bias must the UI display?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM21: Compute research priors and explicit context joins | REFERENCE | canonical fixture validation / Python helpers; J07, J12 |

**User walkthroughs:** J07, J12. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F14 — Join contextual knowledge and case studies

**Owners:** RE-03, RE-04

**Original stated inputs:** Account product/industry links; admitted priors; case-study reports; join policy

**Original stated outputs:** ContextAssessment; optional LookalikeMatch; comparison report

**Processing:** Require explicit account-to-product/industry relationship. Keep prior subject unchanged. Preserve reported case-study outcomes and methodology limitations; similarity is an algorithmic result, not transferred proof.

**Transaction:** Context and comparisons are separate records from facts about the account. Embedding index, when built, is a rebuildable read model.

**Failure path:** ABSTAINED context cannot influence eligible decisions. Context cannot enter a company factual clause unless an explicit attributed comparison renderer is implemented.

**Identity:** (account_snapshot, research_snapshot, join/matching_version)

**Original critique question:** Should context affect ranking, question selection, or neither in the first release?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM21: Compute research priors and explicit context joins | REFERENCE | canonical fixture validation / Python helpers; J07, J12 |
| FM22: Find comparable cases and rank lookalikes | PROPOSED | No implementation; J12 |

**User walkthroughs:** J07, J12. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F15 — Compute descriptors and business conditions

**Owners:** RE-01, RE-05

**Original stated inputs:** Pinned resolved inputs; value conditions; function parameters; context

**Original stated outputs:** Derived-fact drafts; SignalEvaluation; adjudication; verification request

**Processing:** Execute declared dependencies in a stable topological order. Implement ordinary versioned functions and exact input selectors. Distinguish complete false condition from insufficient evidence. Historical/peer metrics require comparable periods, dimensions and eligible denominators.

**Transaction:** Derived facts reenter admission. Signals keep their exact inputs. Verification requests schedule another bounded acquisition/evaluation, not recursive same-epoch mutation.

**Failure path:** Missing cohort implementation disables dependent signals. An ERROR is not a false condition; DNC belongs to operational permission, not a fact about the business.

**Identity:** (signal/function_version, input_snapshot, parameter_digest)

**Original critique question:** Which first three conditions have implementable input selectors and meaningful negative fixtures?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM23: Evaluate derivations and business conditions | REFERENCE | reference functions, not a product CLI; J07, J12 |

**User walkthroughs:** J07, J12. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F04 — Later supersession leaks into an earlier sealed evaluation; F05 — Generated-artifact handoff is accepted by one validator and rejected by another; F08 — Requirement minimum means fact count in the helper but origin count in validation; F16 — effective_at is stored but its decision semantics are undefined/unused

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F16 — Select a supported opportunity

**Owners:** COM-01

**Original stated inputs:** Signals, eligibility, offer prerequisites, bounded context, program policy

**Original stated outputs:** OpportunitySelection or explicit no-selection result

**Processing:** Map support to a service line and relevant offer/audience. Keep selection score explanatory and separate from confidence or claim authority. Public observation-led questions do not require global maturity scoring.

**Transaction:** Commit selection with reasons and policy revision. No contacts are invented or messages sent.

**Failure path:** No compatible offer is a normal knowledge outcome. Do not weaken signal semantics just to improve match rate.

**Identity:** (program_revision, account_snapshot, offer_policy)

**Original critique question:** What minimum evidence and commercial relevance makes an opportunity worth contact enrichment?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM24: Choose a supported commercial opportunity | PROPOSED | No implementation; J13 |

**User walkthroughs:** J13. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F17 — Assess the contact and endpoint

**Owners:** AUD-01

**Original stated inputs:** Account identity; opportunity; approved contact sources; restrictions

**Original stated outputs:** ContactProfile, ContactAssessment, accepted recipient binding

**Processing:** Separate person/account relationship, role relevance, endpoint usability and permission. Keep observation/check times and provenance. A guessed email or verified inbox is not proof of role, employment or consent.

**Transaction:** Endpoint enrichment has its own budget and attempt. Contact records use least-privilege fields; no raw credentials in telemetry.

**Failure path:** No relevant verified contact yields HOLD. Referral names are new candidates, not automatic enrollment permissions.

**Identity:** (person/account_binding, endpoint, verification_method, checked_at)

**Original critique question:** What endpoint verification expires when, and which roles are eligible for each offer?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM25: Assess contact, role, endpoint and permission | PROPOSED | No implementation; J13 |

**User walkthroughs:** J13. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F18 — Render and review exact content

**Owners:** COM-02, COM-03

**Original stated inputs:** Opportunity; eligible account proof; template revision; audience

**Original stated outputs:** GroundedClause, OutreachPackage, MessageArtifact, ReviewDecision

**Processing:** Validate fixed wording as well as inserted slots. Keep questions free of unsupported premises. Attribute quotes and reported comparison outcomes. Approve exact message bytes, revision, purpose and reviewer identity.

**Transaction:** Rendered content is immutable by revision. A new revision requires a new review. Package validation and successful target completion precede approval.

**Failure path:** Wrong-account, inferred, stale, conflicted or prohibited support blocks factual clauses. Human review cannot override hard evidence/permission failures.

**Identity:** (package_id, revision, rendered_content_hash, reviewer_decision)

**Original critique question:** What can be auto-rendered versus draft-only, and who signs off each template?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM26: Render existing reference packages | REFERENCE | Bundle.render(existing_package); J07 |
| FM27: Approve exact content through an authenticated workspace | PROPOSED | No implementation; J13 |

**User walkthroughs:** J07, J13. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F02 — Demoted templates pass the standalone current-use/export boundary

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F19 — Approve campaign policy

**Owners:** CAM-01

**Original stated inputs:** Program, approved templates, audience policy, channel/sender capabilities

**Original stated outputs:** CampaignDefinition, CampaignApproval, CampaignReadiness

**Processing:** Define step order, delays, timezone, frequency limits, route identity, sender caps and stop conditions. Separate draft creation, append, activation and sending. Pick exactly one schedule owner: local or provider.

**Transaction:** Campaign revision and activation approval are distinct from package review. Immutable revision references accompany enrollment.

**Failure path:** Unsupported provider stop/cancel guarantees or unknown ownership block activation.

**Identity:** (campaign_id, revision, activation_decision)

**Original critique question:** Will the initial provider dispatch individual messages or own the entire sequence?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM29: Configure campaigns and sequence ownership | PROPOSED | No implementation; J14 |

**User walkthroughs:** J14. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F20 — Enroll and schedule one logical step

**Owners:** CAM-02

**Original stated inputs:** Campaign approval; contact assessment; reviewed content; CRM exclusions

**Original stated outputs:** Enrollment, StepEligibility, DeliveryIntent

**Processing:** Reject duplicate active enrollment and apply cross-campaign contact limits. Determine due time from the approved policy. Stop/pause state is authoritative and must not be inferred from cached analytics.

**Transaction:** Create stable business-send identity and durable intent in one transaction. The same logical step across retries retains the same effect identity.

**Failure path:** Missing contact, unresolved CRM exclusion, opt-out, reply or overdue review puts the step on hold; a scheduler retry never creates a new intended send.

**Identity:** (tenant, campaign_revision, enrollment, step, channel)

**Original critique question:** Which replies stop all campaigns for a contact versus only this enrollment?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM30: Enroll a contact and schedule/stop steps | PROPOSED | No implementation; J14 |

**User walkthroughs:** J14. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F21 — Check current use and perform reviewed export

**Owners:** COM-04

**Original stated inputs:** Exact package/review; destination mapping; current complete claims/restrictions

**Original stated outputs:** UseGateDecision, ExportReceipt or blocked reason

**Processing:** Historical evaluation uses frozen inputs; this gate reads complete current claim groups. Check revocation, new contradictions, retention, correction, DNC, purpose, destination and reviewer scope immediately before action.

**Transaction:** Gate binds exact revision/destination and expires. Prepare export intent before external handoff; successful local preview output is idempotent.

**Failure path:** A refreshed version hash alone is not reevaluation. Restriction-service uncertainty blocks use. An old approval does not grant perpetual permission.

**Identity:** (tenant, destination, logical_export_key, exact_payload_hash)

**Original critique question:** How fresh must source/CRM/restriction checks be for each destination?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM28: Export a local reference preview with idempotency | REFERENCE | LocalPreviewExporter via walkthrough helper; J07 |

**User walkthroughs:** J07. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F01 — Identity-binding evidence is outside eligibility/provenance closure; F02 — Demoted templates pass the standalone current-use/export boundary

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F22 — Dispatch or reconcile a send

**Owners:** COM-05

**Original stated inputs:** DeliveryIntent, current SendGateDecision, recipient, campaign/sender state

**Original stated outputs:** DeliveryAttempt, acceptance/rejection/unknown record, Exposure

**Processing:** Sending requires a separate contract: current UseGateDecision only covers exports. Dispatch exact reviewed bytes under stable effect identity. Record actual provider acceptance; do not label it inbox delivery.

**Transaction:** Local outbox transaction ends before provider call. Recover by reconciliation/provider identity; cannot atomically commit a remote network action with SQLite.

**Failure path:** Timeout after possible acceptance is UNKNOWN, never a blind retry. Failure to synchronize CRM cannot authorize another send. Restriction after provider acceptance cannot unsend that message.

**Identity:** (tenant, campaign_revision, enrollment, step, recipient, channel) independent of execution_id

**Original critique question:** What provider lookup/idempotency capability resolves uncertain acceptance?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM31: Dispatch and reconcile an exact authorized message | PROPOSED | No implementation; J15 |

**User walkthroughs:** J15. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F23 — Handle inbound replies before measurement

**Owners:** COM-06, ENG-01

**Original stated inputs:** Authenticated provider/mailbox event; known exposure/thread; permitted content

**Original stated outputs:** OutcomeEvent, Conversation, ReplyAssessment, EnrollmentControl, task/handoff

**Processing:** Verify webhook/message origin and deduplicate. Apply immediate local stop/hold before optional model classification or CRM calls. Correlate to exposure; unmatched messages stay quarantined. Opt-out restrictions are sticky until authorized release.

**Transaction:** Commit inbox event plus stop intent atomically. If governance sync is delayed, local contact-level hold remains; downstream analytics does not own this safety action.

**Failure path:** Uncertain sender identity or correlation requires human review. Out-of-office and referrals use explicit policy; model labels are assessments, not literal HUMAN facts.

**Identity:** (provider, tenant, event_id); fallback content identity is explicitly versioned

**Original critique question:** What is the safe default for any credible reply, and when may automation resume?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM32: Route replies and immediate stop requests | PROPOSED | No implementation; J16 |
| FM34: Measure outcomes, experiments and calibration | PROPOSED | No implementation; J18 |

**User walkthroughs:** J16, J18. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F24 — Synchronize sales handoff and CRM

**Owners:** CRM-01

**Original stated inputs:** Conversation, task/handoff, account/contact links; CRM lifecycle events

**Original stated outputs:** CRMSyncIntent, CRMSyncReceipt, CRMAccountView, attributable sales outcomes

**Processing:** Define field-level authority. CRM owns human sales owner/stage/customer state; KeenSight owns evidence and delivery history. Merge restrictions conservatively. Preserve external IDs and avoid update loops.

**Transaction:** CRM writes retry through their own sync identity/outbox. They are never coupled to send retries. Human stage changes become attributed lifecycle evidence.

**Failure path:** CRM outage creates pending handoff and operator task, not message resend. A blank CRM field does not release local DNC.

**Identity:** (destination, external_entity, owned_field_revision, sync_action)

**Original critique question:** Who owns each bidirectional field, and how are conflicting edits reconciled?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM33: Synchronize sales handoff with CRM | PROPOSED | No implementation; J16 |

**User walkthroughs:** J16. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F25 — Measure outcomes and propose improvements

**Owners:** COM-06, QA-01

**Original stated inputs:** Exposures, attributed events, mature windows, calibrated gold sets

**Original stated outputs:** Measurement facts, quality reports, experiment results, release proposals

**Processing:** Use explicit exposure denominator, response maturity and exclusion rules. Dedupe provider events and cross-angle contamination. Separate detector quality from commercial outcomes; observational response rates are not causal effects.

**Transaction:** Reviewed changes publish a new version for later evaluations. Never promote authority merely because an angle received replies.

**Failure path:** Immature/uncertain denominators remain unmeasured. Drift can disable future use; it does not rewrite historical bytes.

**Identity:** (measurement_definition, population_snapshot, window, version)

**Original critique question:** Which decisions require experiments versus descriptive reporting?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM15: Promote and distribute reviewed rules | PROPOSED | No implementation; J05, J18 |
| FM32: Route replies and immediate stop requests | PROPOSED | No implementation; J16 |
| FM34: Measure outcomes, experiments and calibration | PROPOSED | No implementation; J18 |

**User walkthroughs:** J05, J16, J18. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** No new reproduced issue for this stage; this is not completeness sign-off.

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.

## F26 — Govern, inspect, correct and recover

**Owners:** PLAT-01, PLAT-02, PLAT-03, UX-01

**Original stated inputs:** Authorized read/administrative request; records; execution diagnostics

**Original stated outputs:** Timeline, why/why-not, ChangeRecord, tombstone, restore report

**Processing:** Expose evidence back-links and exact versions from any package/exposure/fact. Enforce actor, tenant, typed target, compatible replacement and time on corrections. Keep logs redacted; retained evidence has separate access and deletion policies.

**Transaction:** Each record type has one writer. Backups and restore are tested before production. Source-rights deletion must affect derived eligibility, including sample denominators.

**Failure path:** Unavailable evidence cannot be replaced by a digest-only assertion. Unauthorized corrections never take effect; full admission rejects them. A local ActorGrant fixture is not hosted authentication.

**Identity:** (authorized_action_id, tenant, target_type/id, expected_revision)

**Original critique question:** What retention, audit, access and recovery guarantees are required before the first real account batch?

| Feature | Actual readiness in this audit | Invocation / journey |
|---|---|---|
| FM11: Verify bundle, metadata and original bytes | LOCAL | check; J03, J06 |
| FM27: Approve exact content through an authenticated workspace | PROPOSED | No implementation; J13 |
| FM35: Govern evidence, bindings, changes and retention | REFERENCE | Store.revoke or Bundle.validate_change (local/reference only); J17 |
| FM36: Inspect/debug individual modules and service boundaries | LOCAL | ks-module and offline walkthrough harness; J03, J06, J08, J19 |

**User walkthroughs:** J03, J06, J08, J13, J17, J19. See USER_JOURNEYS.md for steps and outputs.

**New issues to address:** F03 — Publication validates one payload and can persist a different argument set; F10 — Current candidate discovery counts unlabelled revoked evidence; F11 — Contradictory duplicate command outcomes are accepted; F12 — No-byte failures lose invocation details and have no persisted evaluation manifest; F13 — Protocol rejects an honest timeout failure reported after its deadline; F15 — The protocol fixture does not constrain mode/effects against operation parameters

**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.
