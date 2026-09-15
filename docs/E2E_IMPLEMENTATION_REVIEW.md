# KeenSight implementation review: detailed E2E dataflow and UML

Version: review-and-repair 2026-09-15. Basis: the uploaded collector 0.1.0, canonical v4.1, common-protocol proposal, full E2E product design and September 15 code audit. Code changes in this package are collector 0.2.0 and canonical-reference 4.2.0; service interfaces below are explicitly proposed unless marked implemented.

## How to critique this document

Review the step cards in order. Each identifies its owner, exact boundary records, work, publication transaction, failure path, idempotency key, implementation status and a decision to resolve. Mark each decision ACCEPT / CHANGE / DEFER in `CRITIQUE_WORKSHEET.md`. A schema, a tested helper, a runnable module, an integrated pipeline and a deployed service are five different states.

The system remains broad: retain the 213 registered predicate families, all 89 metric definitions, eleven fact areas, the 52-idea placement distinctions, and all 38 collector command IDs. No narrower launch profile deletes evidence families; activation controls capture, extraction, reasoning and commercial use independently.

There are three valid terminal products: (1) knowledge + diagnostics; (2) reviewed no-send handoff; (3) separately authorized engagement and sales outcomes. A business program does not assert that a prospect has a problem. Research context is not account proof. Historical approval is not current permission.

## Current runnable boundary

The collector CLI and its new `ks-module` offline extraction, matching, bundle check and claim resolution entrypoints run separately. The canonical package exposes reference methods and a bundle validator, not a hosted Fact Service. The common envelope checker is hardened, but its only registered operation schema is still fixture-only. Contacts, campaigns, sends, replies and CRM are proposed product modules, not working services. No remote repository was changed.

## Standard records and clocks

Keep three identities separate: execution (request/run/attempt/release), knowledge (subject/scope/target/capture/claim), and business effect (package revision/enrollment/step/recipient/send identity). A new execution is not a new source or send permission.

Every proposed service operation uses `ModuleRequest -> ModuleResult` with exact schema-version/digest references, trusted tenant context, deadline, explicit operation, pinned release, declared/consumed inputs, outputs and structured diagnostics. Domain records remain typed: an Artifact, Observation, Fact, ContextAssessment, SignalEvaluation, ReviewDecision and Exposure are not interchangeable dictionaries.

Clocks are explicit: published/effective time describes the source; captured/observed time describes observation; recorded time describes knowledge availability; logical as_of describes the evaluation; execution start/finish describe computation; gate/dispatch time describes current external use. New model responses are run-produced artifacts. Do not backdate them into sealed external inputs. Replaying deterministic rules never refreshes source TTL and never performs a new provider call.

## Execution results versus domain decisions

SUCCEEDED/FAILED/SKIPPED/CANCELLED describe operation execution. CONFLICT is a successful claim-resolution outcome. NOT_EVALUATED and PARTIAL are not complete NO_MATCH. A denied UseGate is a successful policy evaluation. Provider-acceptance uncertainty is not proof a send failed. Domain status changes require versioned adapters, not silent enum renaming.

## Graphs and loops

Computation dependencies must be acyclic within the evaluation. Provenance ancestry must be causal and acyclic. Ordinary entity relationships may contain cycles. Feedback requests create later runs; fingerprint proposals create later releases. None requires a graph database. The first implementation uses validated sequential order and conservative target reruns, not a general distributed scheduler.

## Detailed step-by-step contract cards

### F00 — Define program and offer

**Owner:** GTM-01. **Current status:** DESIGN ONLY.

**Inputs:** ProgramDefinition, AudienceDefinition, OfferDefinition.

**Outputs:** Program revision and capability-profile reference.

**Processing:** Check owner approval, geography, source purposes, service-line prerequisites, exclusions and budget. Freeze the revision used for a selection run.

**Commit / side effects:** One configuration revision commits atomically. No account facts or provider calls are produced.

**Failure and recovery:** Reject an invalid program; never translate an audience criterion into a fact that a prospect satisfies it.

**Recommended identity:** `(tenant, program_id, revision, content_hash)`.

**Critique decision D00:** Which exclusions and offers are mandatory, and who can approve a change?

### F01 — Source and select account seeds

**Owner:** GTM-02. **Current status:** DESIGN ONLY.

**Inputs:** Program revision; CSV/Harvest or approved source records; existing CRMAccountView.

**Outputs:** AccountSeed, LeadSelection, ResearchPlan, IntakeRequest.

**Processing:** Preserve original source and external IDs. Normalize provisional targets. Deduplicate seeds without assuming domain ownership. Record fit and exclusion decisions against their input snapshot.

**Commit / side effects:** Commit seed provenance and selection decisions together. Discovery calls, when enabled, are separate acquisition attempts.

**Failure and recovery:** Unresolved account or stale relevant CRM exclusion becomes HOLD, not invented identity or a lost seed.

**Recommended identity:** `(tenant, source_namespace, external_record, revision, program_revision)`.

**Critique decision D01:** What constitutes the same account: legal entity, location, brand or franchisee?

### F02 — Bind subject and permitted scope

**Owner:** KN-01. **Current status:** REFERENCE CONTRACTS; RUNTIME MISSING.

**Inputs:** Provisional target; existing subjects; literal identity evidence.

**Outputs:** Subject, SubjectBinding, resolved or unresolved target.

**Processing:** Resolve organization/location/person/product/industry separately. Require evidence for website ownership and relationships. Keep aliases and external IDs namespaced. Redirect/canonical tags are claims, not automatic ownership proof.

**Commit / side effects:** Subject and accepted binding decisions commit under one owner. Preserve rejected and ambiguous candidates.

**Failure and recovery:** Ambiguity blocks account-specific admission/copy but may still allow a bounded diagnostic capture request.

**Recommended identity:** `(tenant, candidate_identity, binding_policy, evidence_digest)`.

**Critique decision D02:** When may a multi-location domain support organization-wide conclusions?

### F03 — Authorize and pin execution

**Owner:** CTL-01, CTL-02, CTL-03. **Current status:** PARTIAL REFERENCE / COLLECTOR RUN PINNING.

**Inputs:** IntakeRequest; trusted principal; profile; installed implementation manifest.

**Outputs:** ReleaseLock, BatchRun, authorized context, bounded work specification.

**Processing:** Resolve exact schemas/functions/rules/mappings and allowed operations. Verify acyclic dependency closure including self-edges. Obtain tenant and permissions from trusted local configuration or authentication, not caller text.

**Commit / side effects:** Persist run configuration and idempotency identity before scheduling. The initial runner is sequential, not distributed.

**Failure and recovery:** Missing implementation or incompatible schema is a startup failure. Disabled capabilities are recorded as disabled, not false business conditions.

**Recommended identity:** `(tenant, logical_request, normalized_config_hash, release_lock)`.

**Critique decision D03:** Which operations must fail the whole target rather than return a partial knowledge result?

### F04 — Plan bounded Scrapling acquisition

**Owner:** ING-02. **Current status:** LOCAL COLLECTOR IMPLEMENTED.

**Inputs:** Target origin; robots/source policy; previous capture disposition; budget.

**Outputs:** ScanPlan and per-resource acquisition requests.

**Processing:** Normalize URL. Apply origin policy to seeds, sitemap entries, redirects and probes. Rank requested templates. Budget attempts, not successes; count metadata and redirects. Do not submit forms or authenticate into public portals.

**Commit / side effects:** Persist request identity before execution; a PENDING prior attempt is crash uncertainty. Resume cannot reset the budget.

**Failure and recovery:** Malformed discoveries become diagnostics. Robots denial or cooldown prevents content capture; 429 is not a reason to bypass controls.

**Recommended identity:** `(tenant, capture_run, normalized_URL, capture_mode)`.

**Critique decision D04:** Is eight top-level attempts an acceptable fast-profile limit, and what triggers an expanded profile?

### F05 — Capture response or honest failure

**Owner:** ING-03. **Current status:** STATIC ADAPTER PRESENT; SDK UNVERIFIED; BROWSER DISABLED.

**Inputs:** One approved request; transport policy; attempt budget.

**Outputs:** AcquisitionAttempt; Capture; original blob; headers; limitations.

**Processing:** Use one checked static request, with explicit redirects/retries outside the SDK. Retain approved bytes and scrubbed headers. Bind capture metadata to the trusted stored record. A denied/no-byte request gets a diagnostic, not an empty response.

**Commit / side effects:** Finalize blob before reference commit. Orphan blobs can be cleaned up; positive output cannot reference missing bytes. Attempts and response time remain distinct from evaluation time.

**Failure and recovery:** Timeout, rate limit, body truncation, network denial or unavailable SDK records failure/incomplete status. Browser remains disabled until its separate egress and resource contract is tested.

**Recommended identity:** `(tenant, capture_run, request_key); capture ID does not collapse distinct observations by body hash`.

**Critique decision D05:** What response modalities and retention classes are permitted per source?

### F06 — Extract evidence surfaces

**Owner:** ING-04. **Current status:** IMPLEMENTED; INDEPENDENT OFFLINE CLI.

**Inputs:** Trusted Capture and retained bytes; parser release.

**Outputs:** PageEvidence, Surface records, per-extractor CommandResult.

**Processing:** Decode with pinned BOM/transport/declaration/fallback policy. Run all applicable extraction functions. Preserve element context, raw JSON-LD, parsed subjects, errors, node-local attributes and surface completeness. Label static prose as not computed CSS visibility.

**Commit / side effects:** No canonical business writes. Standalone output is a typed evidence artifact. Metadata and extraction can be verified by recomputing against original bytes.

**Failure and recovery:** A failed extractor emits diagnostics without positive surfaces. Item/text limits are PARTIAL. An empty complete extraction is distinct from an unperformed check.

**Recommended identity:** `(capture_id, parser_release, extractor_parameters)`.

**Critique decision D06:** Which surface limits are safe for our target-site sizes?

### F07 — Match, preserve support and consolidate

**Owner:** FP-01, FP-02. **Current status:** IMPLEMENTED; LOCAL REFERENCE CLAIM VIEW ONLY.

**Inputs:** Page/host evidence; immutable rule pack; canonical product mapping.

**Outputs:** All Match records; Observation; SupportLink; ClaimView; ScanBundle.

**Processing:** Evaluate declared surfaces, alternatives and correlation scope. Preserve each rule/element support, but make one observation per captured claim/value. Keep separate pages/scans as history. Do not combine authored confidence or count overlapping detectors as independent origins.

**Commit / side effects:** Validate full candidate bundle before atomic publication of findings, research features and replay-selection manifest. Raw capture diagnostics may survive failure; supported claims must not.

**Failure and recovery:** No pages is NOT_EVALUATED. Required truncated surface is PARTIAL, not ordinary NO_MATCH. Conflicting values stay conflict. Gates/scores affect selection, never source authority.

**Recommended identity:** `match=(semantic_rule_digest,release,capture,surface,branch); observation excludes rule ID`.

**Critique decision D07:** Are presence, mention, provider report and verified capability kept separate for each imported rule?

### F08 — Review dynamic fingerprint candidates

**Owner:** FP-03. **Current status:** CANDIDATE HARVEST / SUBSET IMPORT IMPLEMENTED; FULL PROMOTION MISSING.

**Inputs:** Unknown technical features; bounded distinct-site samples; donor rows.

**Outputs:** Candidate records, quarantine report, review proposal, next immutable rule release.

**Processing:** Normalize stable technical residues and count sites without counting repeated visits as new sites. Retain every donor row with disposition. A reviewer/model may propose a definition; only explicit approval after fixture/calibration checks can change production eligibility.

**Commit / side effects:** The active scan never rewrites its pinned rule release. Technical index is rebuildable, not a second canonical fact store.

**Failure and recovery:** Unsupported operators/mappings are quarantined. Candidate status, prevalence and high authored confidence never auto-promote a rule.

**Recommended identity:** `(feature_normalizer_version, feature_key); reviewed rule semantic digest`.

**Critique decision D08:** What gold-set precision and false-positive criteria authorize promotion?

### F09 — Admit canonical facts

**Owner:** KN-02. **Current status:** VALIDATOR PATCHED; PERSISTENT BRIDGE MISSING.

**Inputs:** Collector/source output; concrete support; verified bindings; successful producer.

**Outputs:** Fact, EvidenceSet, EvidenceLocator, ExecutionRecord, admission report.

**Processing:** Map collector meaning to a registered predicate/nature. Verify actual bytes/locators, successful production, object schema, scope, time, source rights and binding. Preserve complete provenance. A fixture proving a rule works is not proof this fact was detected.

**Commit / side effects:** One fact transaction writes fact, lineage and admission decision. Reject duplicate identity with different payload. This bridge is still to implement; collector observations are not canonical Fact objects.

**Failure and recovery:** Rejected candidates remain quarantined. Non-detection requires completed capture AND compatible successful detector coverage.

**Recommended identity:** `(tenant, subject, predicate, nature, scope, target, window, observation_origin)`.

**Critique decision D09:** Which source-specific mappings permit commercial use rather than internal storage only?

### F10 — Resolve the complete claim group

**Owner:** KN-03. **Current status:** REFERENCE FUNCTIONS IMPLEMENTED; HOSTED REPOSITORY MISSING.

**Inputs:** All eligible observations for the claim identity; binding/source/change state.

**Outputs:** ClaimResolution and retained observation history.

**Processing:** Group with target/cardinality and temporal dimensions, not just subject+predicate. Preserve vendors and source disagreements. Use explicit resolution rules; UNKNOWN does not erase usable knowledge. Multiple model transcripts are not independent support.

**Commit / side effects:** Resolution is a derived projection; original facts are retained. Authorized corrections have typed targets, actors, tenant ownership, compatible replacements and chronology.

**Failure and recovery:** Conflict is a successful resolution result, not a software exception. It blocks cherry-picked downstream proof.

**Recommended identity:** `(claim_key, input_membership_hash, resolution_policy, as_of)`.

**Critique decision D10:** Which conflicts require human adjudication instead of automatic precedence?

### F11 — Seal evaluation inputs and execute dependencies

**Owner:** KN-04, CTL-02. **Current status:** REFERENCE CLOSURE CHECKS IMPLEMENTED; GENERAL RUNNER MISSING.

**Inputs:** Requested account/product evaluation; current knowledge; exact release versions.

**Outputs:** InputSnapshot / BatchRun manifests and scheduled operations.

**Processing:** Separate sealed external inputs from artifacts/facts produced in this run. Each produced record has one declared successful producer; a consumer cannot read it before completion. Keep logical as_of, knowledge cutoff, capture time and wall-clock execution time distinct.

**Commit / side effects:** Publish complete targets independently. Do not hold one database transaction across model or HTTP calls.

**Failure and recovery:** Unknown or unpinned references, self-produced input cycles, failed producers and unauthorized current reads abort that operation.

**Recommended identity:** `(tenant, target, external_input_digest, release_lock, logical_as_of)`.

**Critique decision D11:** Must selected facts be frozen per account or per program batch?

### F12 — Acquire enrichment and run bounded model tasks

**Owner:** ING-01, AI-01. **Current status:** MOST LIVE ADAPTERS/GATEWAY MISSING; CONTRACTS PRESENT.

**Inputs:** Approved source/task request; selected evidence; model/prompt configuration; budget.

**Outputs:** Typed provider records, ModelCall, raw request/response artifacts, RepairAttempt.

**Processing:** Keep all eleven fact areas and the ledger sources available as registered capabilities. Provider estimates stay estimates, statements stay attributed statements, hypotheses stay internal. Retain raw I/O before parse; every repair consumes the same bounded budget.

**Commit / side effects:** External calls have durable attempt IDs. Generated model I/O enters the produced-artifact manifest, not backdated external inputs. Deterministic downstream replay consumes retained responses, not a new call.

**Failure and recovery:** Invalid output/repair exhaustion yields abstention. Source denial, rate limits, unknown costs and unsupported fields remain explicit.

**Recommended identity:** `(task_version, exact_inputs, prompt/config); new model call is not replay`.

**Critique decision D12:** Which sources are approved and which exact tasks should spend model budget?

### F13 — Build research samples and priors

**Owner:** RE-02. **Current status:** NARROW REFERENCE SUMMARY IMPLEMENTED; GENERAL PIPELINE MISSING.

**Inputs:** Product/industry review/discussion records; sample decisions; support policy.

**Outputs:** ResearchSample, classifications, prior drafts and execution report.

**Processing:** Record every retrieved item: eligible, support, contradict, no-theme, unclassified, excluded. Deduplicate original record identities. Distinguish workflow mention from negative experience. Pin all numerator, denominator and exclusion dependencies.

**Commit / side effects:** Calculation drafts pass canonical admission. A denominator-only deletion invalidates current use of the statistic even if supporting items remain.

**Failure and recovery:** No eligible denominator is UNKNOWN. A biased or selected sample cannot imply population prevalence or company-specific pain.

**Recommended identity:** `(sample_membership, dispositions, classification_release, window, support_policy)`.

**Critique decision D13:** What is the sample population and which selection bias must the UI display?

### F14 — Join contextual knowledge and case studies

**Owner:** RE-03, RE-04. **Current status:** CONTEXT REFERENCE CHECKS; LOOKALIKE DESIGN ONLY.

**Inputs:** Account product/industry links; admitted priors; case-study reports; join policy.

**Outputs:** ContextAssessment; optional LookalikeMatch; comparison report.

**Processing:** Require explicit account-to-product/industry relationship. Keep prior subject unchanged. Preserve reported case-study outcomes and methodology limitations; similarity is an algorithmic result, not transferred proof.

**Commit / side effects:** Context and comparisons are separate records from facts about the account. Embedding index, when built, is a rebuildable read model.

**Failure and recovery:** ABSTAINED context cannot influence eligible decisions. Context cannot enter a company factual clause unless an explicit attributed comparison renderer is implemented.

**Recommended identity:** `(account_snapshot, research_snapshot, join/matching_version)`.

**Critique decision D14:** Should context affect ranking, question selection, or neither in the first release?

### F15 — Compute descriptors and business conditions

**Owner:** RE-01, RE-05. **Current status:** NARROW REFERENCE FUNCTIONS; FULL ENABLED SIGNAL RUNTIME MISSING.

**Inputs:** Pinned resolved inputs; value conditions; function parameters; context.

**Outputs:** Derived-fact drafts; SignalEvaluation; adjudication; verification request.

**Processing:** Execute declared dependencies in a stable topological order. Implement ordinary versioned functions and exact input selectors. Distinguish complete false condition from insufficient evidence. Historical/peer metrics require comparable periods, dimensions and eligible denominators.

**Commit / side effects:** Derived facts reenter admission. Signals keep their exact inputs. Verification requests schedule another bounded acquisition/evaluation, not recursive same-epoch mutation.

**Failure and recovery:** Missing cohort implementation disables dependent signals. An ERROR is not a false condition; DNC belongs to operational permission, not a fact about the business.

**Recommended identity:** `(signal/function_version, input_snapshot, parameter_digest)`.

**Critique decision D15:** Which first three conditions have implementable input selectors and meaningful negative fixtures?

### F16 — Select a supported opportunity

**Owner:** COM-01. **Current status:** DESIGN ONLY.

**Inputs:** Signals, eligibility, offer prerequisites, bounded context, program policy.

**Outputs:** OpportunitySelection or explicit no-selection result.

**Processing:** Map support to a service line and relevant offer/audience. Keep selection score explanatory and separate from confidence or claim authority. Public observation-led questions do not require global maturity scoring.

**Commit / side effects:** Commit selection with reasons and policy revision. No contacts are invented or messages sent.

**Failure and recovery:** No compatible offer is a normal knowledge outcome. Do not weaken signal semantics just to improve match rate.

**Recommended identity:** `(program_revision, account_snapshot, offer_policy)`.

**Critique decision D16:** What minimum evidence and commercial relevance makes an opportunity worth contact enrichment?

### F17 — Assess the contact and endpoint

**Owner:** AUD-01. **Current status:** DESIGN ONLY.

**Inputs:** Account identity; opportunity; approved contact sources; restrictions.

**Outputs:** ContactProfile, ContactAssessment, accepted recipient binding.

**Processing:** Separate person/account relationship, role relevance, endpoint usability and permission. Keep observation/check times and provenance. A guessed email or verified inbox is not proof of role, employment or consent.

**Commit / side effects:** Endpoint enrichment has its own budget and attempt. Contact records use least-privilege fields; no raw credentials in telemetry.

**Failure and recovery:** No relevant verified contact yields HOLD. Referral names are new candidates, not automatic enrollment permissions.

**Recommended identity:** `(person/account_binding, endpoint, verification_method, checked_at)`.

**Critique decision D17:** What endpoint verification expires when, and which roles are eligible for each offer?

### F18 — Render and review exact content

**Owner:** COM-02, COM-03. **Current status:** THREE REFERENCE RENDERERS/LOCAL REVIEW CHECKS; PRODUCT UI MISSING.

**Inputs:** Opportunity; eligible account proof; template revision; audience.

**Outputs:** GroundedClause, OutreachPackage, MessageArtifact, ReviewDecision.

**Processing:** Validate fixed wording as well as inserted slots. Keep questions free of unsupported premises. Attribute quotes and reported comparison outcomes. Approve exact message bytes, revision, purpose and reviewer identity.

**Commit / side effects:** Rendered content is immutable by revision. A new revision requires a new review. Package validation and successful target completion precede approval.

**Failure and recovery:** Wrong-account, inferred, stale, conflicted or prohibited support blocks factual clauses. Human review cannot override hard evidence/permission failures.

**Recommended identity:** `(package_id, revision, rendered_content_hash, reviewer_decision)`.

**Critique decision D18:** What can be auto-rendered versus draft-only, and who signs off each template?

### F19 — Approve campaign policy

**Owner:** CAM-01. **Current status:** DESIGN ONLY.

**Inputs:** Program, approved templates, audience policy, channel/sender capabilities.

**Outputs:** CampaignDefinition, CampaignApproval, CampaignReadiness.

**Processing:** Define step order, delays, timezone, frequency limits, route identity, sender caps and stop conditions. Separate draft creation, append, activation and sending. Pick exactly one schedule owner: local or provider.

**Commit / side effects:** Campaign revision and activation approval are distinct from package review. Immutable revision references accompany enrollment.

**Failure and recovery:** Unsupported provider stop/cancel guarantees or unknown ownership block activation.

**Recommended identity:** `(campaign_id, revision, activation_decision)`.

**Critique decision D19:** Will the initial provider dispatch individual messages or own the entire sequence?

### F20 — Enroll and schedule one logical step

**Owner:** CAM-02. **Current status:** DESIGN ONLY.

**Inputs:** Campaign approval; contact assessment; reviewed content; CRM exclusions.

**Outputs:** Enrollment, StepEligibility, DeliveryIntent.

**Processing:** Reject duplicate active enrollment and apply cross-campaign contact limits. Determine due time from the approved policy. Stop/pause state is authoritative and must not be inferred from cached analytics.

**Commit / side effects:** Create stable business-send identity and durable intent in one transaction. The same logical step across retries retains the same effect identity.

**Failure and recovery:** Missing contact, unresolved CRM exclusion, opt-out, reply or overdue review puts the step on hold; a scheduler retry never creates a new intended send.

**Recommended identity:** `(tenant, campaign_revision, enrollment, step, channel)`.

**Critique decision D20:** Which replies stop all campaigns for a contact versus only this enrollment?

### F21 — Check current use and perform reviewed export

**Owner:** COM-04. **Current status:** LOCAL NO-SEND EXPORT REFERENCE IMPLEMENTED.

**Inputs:** Exact package/review; destination mapping; current complete claims/restrictions.

**Outputs:** UseGateDecision, ExportReceipt or blocked reason.

**Processing:** Historical evaluation uses frozen inputs; this gate reads complete current claim groups. Check revocation, new contradictions, retention, correction, DNC, purpose, destination and reviewer scope immediately before action.

**Commit / side effects:** Gate binds exact revision/destination and expires. Prepare export intent before external handoff; successful local preview output is idempotent.

**Failure and recovery:** A refreshed version hash alone is not reevaluation. Restriction-service uncertainty blocks use. An old approval does not grant perpetual permission.

**Recommended identity:** `(tenant, destination, logical_export_key, exact_payload_hash)`.

**Critique decision D21:** How fresh must source/CRM/restriction checks be for each destination?

### F22 — Dispatch or reconcile a send

**Owner:** COM-05. **Current status:** DESIGN ONLY; NO SENDING ENABLED.

**Inputs:** DeliveryIntent, current SendGateDecision, recipient, campaign/sender state.

**Outputs:** DeliveryAttempt, acceptance/rejection/unknown record, Exposure.

**Processing:** Sending requires a separate contract: current UseGateDecision only covers exports. Dispatch exact reviewed bytes under stable effect identity. Record actual provider acceptance; do not label it inbox delivery.

**Commit / side effects:** Local outbox transaction ends before provider call. Recover by reconciliation/provider identity; cannot atomically commit a remote network action with SQLite.

**Failure and recovery:** Timeout after possible acceptance is UNKNOWN, never a blind retry. Failure to synchronize CRM cannot authorize another send. Restriction after provider acceptance cannot unsend that message.

**Recommended identity:** `(tenant, campaign_revision, enrollment, step, recipient, channel) independent of execution_id`.

**Critique decision D22:** What provider lookup/idempotency capability resolves uncertain acceptance?

### F23 — Handle inbound replies before measurement

**Owner:** COM-06, ENG-01. **Current status:** DESIGN ONLY.

**Inputs:** Authenticated provider/mailbox event; known exposure/thread; permitted content.

**Outputs:** OutcomeEvent, Conversation, ReplyAssessment, EnrollmentControl, task/handoff.

**Processing:** Verify webhook/message origin and deduplicate. Apply immediate local stop/hold before optional model classification or CRM calls. Correlate to exposure; unmatched messages stay quarantined. Opt-out restrictions are sticky until authorized release.

**Commit / side effects:** Commit inbox event plus stop intent atomically. If governance sync is delayed, local contact-level hold remains; downstream analytics does not own this safety action.

**Failure and recovery:** Uncertain sender identity or correlation requires human review. Out-of-office and referrals use explicit policy; model labels are assessments, not literal HUMAN facts.

**Recommended identity:** `(provider, tenant, event_id); fallback content identity is explicitly versioned`.

**Critique decision D23:** What is the safe default for any credible reply, and when may automation resume?

### F24 — Synchronize sales handoff and CRM

**Owner:** CRM-01. **Current status:** DESIGN ONLY.

**Inputs:** Conversation, task/handoff, account/contact links; CRM lifecycle events.

**Outputs:** CRMSyncIntent, CRMSyncReceipt, CRMAccountView, attributable sales outcomes.

**Processing:** Define field-level authority. CRM owns human sales owner/stage/customer state; KeenSight owns evidence and delivery history. Merge restrictions conservatively. Preserve external IDs and avoid update loops.

**Commit / side effects:** CRM writes retry through their own sync identity/outbox. They are never coupled to send retries. Human stage changes become attributed lifecycle evidence.

**Failure and recovery:** CRM outage creates pending handoff and operator task, not message resend. A blank CRM field does not release local DNC.

**Recommended identity:** `(destination, external_entity, owned_field_revision, sync_action)`.

**Critique decision D24:** Who owns each bidirectional field, and how are conflicting edits reconciled?

### F25 — Measure outcomes and propose improvements

**Owner:** COM-06, QA-01. **Current status:** REFERENCE MEASUREMENT RULES; FULL OUTCOMES PIPELINE MISSING.

**Inputs:** Exposures, attributed events, mature windows, calibrated gold sets.

**Outputs:** Measurement facts, quality reports, experiment results, release proposals.

**Processing:** Use explicit exposure denominator, response maturity and exclusion rules. Dedupe provider events and cross-angle contamination. Separate detector quality from commercial outcomes; observational response rates are not causal effects.

**Commit / side effects:** Reviewed changes publish a new version for later evaluations. Never promote authority merely because an angle received replies.

**Failure and recovery:** Immature/uncertain denominators remain unmeasured. Drift can disable future use; it does not rewrite historical bytes.

**Recommended identity:** `(measurement_definition, population_snapshot, window, version)`.

**Critique decision D25:** Which decisions require experiments versus descriptive reporting?

### F26 — Govern, inspect, correct and recover

**Owner:** PLAT-01, PLAT-02, PLAT-03, UX-01. **Current status:** PATCHED REFERENCE CORRECTIONS; HOSTED CONTROLS/UI MISSING.

**Inputs:** Authorized read/administrative request; records; execution diagnostics.

**Outputs:** Timeline, why/why-not, ChangeRecord, tombstone, restore report.

**Processing:** Expose evidence back-links and exact versions from any package/exposure/fact. Enforce actor, tenant, typed target, compatible replacement and time on corrections. Keep logs redacted; retained evidence has separate access and deletion policies.

**Commit / side effects:** Each record type has one writer. Backups and restore are tested before production. Source-rights deletion must affect derived eligibility, including sample denominators.

**Failure and recovery:** Unavailable evidence cannot be replaced by a digest-only assertion. Unauthorized corrections never take effect; full admission rejects them. A local ActorGrant fixture is not hosted authentication.

**Recommended identity:** `(authorized_action_id, tenant, target_type/id, expected_revision)`.

**Critique decision D26:** What retention, audit, access and recovery guarantees are required before the first real account batch?

## Cross-boundary publication invariants

The caller only receives successful output references after the owning transaction commits. Captures/failure diagnostics may exist without a successful interpretation; they are not current claim support. The patched collector now commits evaluation, matches, observations, support and replay-selection together. It verifies complete stored Capture metadata plus body integrity, and re-extracts supplied surfaces before publishing. This does not make the local file/database owner an authenticated remote client.

The canonical bridge remains a missing implementation. It must verify actual Match/SupportLink/Execution records, not one new Fact per fingerprint hit. Approved and candidate supports stay separate. Alias/product mappings enter the semantic rule digest; changed mappings require reevaluation. Duplicate detectors on one script remain one evidence point. Requests, responses and repairs remain full provenance but do not create independent corroboration.

The current-use path must query complete current groups, separate from the original snapshot. A gate vector invalidates cached decisions, but refreshing the vector alone must not bypass new conflicting knowledge. A complete current query and its results must be recorded before effects. The reference gate now checks those current groups; a production repository must enforce the same behavior under concurrency.

## Service boundary references

See `SERVICE_EXTRACTION.md` for exact ownership, process entrypoints, an intentionally small proposed HTTP/queue facade, split criteria, state stores, failure matrices and cutover tests. See `CLASS_REFERENCE.md` and the diagram book for all actual contract classes and separately labeled proposed product classes.

## Trace to code and evidence

- `../collector/src/keensight_scrapling/`: actual local collector implementation, including `standalone.py`.
- `../canonical/keensight_contracts/`: actual reference validators/functions; not a persistent authenticated application.
- `../protocol/validate_protocol.py`: actual signature/reference checker; not the full runtime runner.
- `../product-design/`: retained 39-module inventory and 32 field-level product proposals.
- `../verification/`: executed tests, source diff, package hashes and repair-status report.

The original uploaded archives remain unchanged outside this release. The new bundle changes compatibility intentionally: collector ScanBundle 1.1 records evaluated-capture membership; semantic rule digests include canonical product mappings; canonical schema namespace v4.2 adds authorized change fields and produced-artifact manifests. Do not resume a 0.1 run as 0.2 or fabricate missing historic selection/producer information. Keep baseline data read-only and perform explicit re-import/re-evaluation under a new run.
