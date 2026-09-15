> Consolidated workspace: run commands from the repository root. Use `python tools/workspace.py journeys --output ../keensight-journeys` for relocated paths. This is the retained audit walkthrough, not a claim that open bugs were fixed.

# Submodule, feature, invocation and bug traceability

The original 39 module IDs, names and submodule names are retained. This view does not turn every function into a network service. Feature status is finer grained than module status.

## CTL-01 — Contracts and release compiler

**Submodules:** schema registry; domain catalogs; 38-command registry; function allowlist; release compatibility

**Original inputs:** CapabilityProfile, VersionedDefinitions, ImplementationManifest

**Original outputs:** ReleaseLock, ValidationReport

**Feature coverage:** FM03 (REFERENCE)

**Invoke:** reference-checks

**Audit:** F15 The protocol fixture does not constrain mode/effects against operation parameters

## CTL-02 — Intake and batch coordination

**Submodules:** target intake; operation identity; dependency order; per-target completion; checkpoint and resume

**Original inputs:** IntakeRequest, ReleaseLock, ProgramDefinition, ResearchPlan

**Original outputs:** BatchRun, ModuleRequest, TargetResult, RunReport

**Feature coverage:** FM04 (LOCAL)

**Invoke:** demo

**Audit:** F05 Generated-artifact handoff is accepted by one validator and rejected by another; F09 Retained-file import does not pin subject identity in run configuration; F12 No-byte failures lose invocation details and have no persisted evaluation manifest; F13 Protocol rejects an honest timeout failure reported after its deadline

## CTL-03 — Access, source policy and budget admission

**Submodules:** trusted authentication context; tenant authorization; source rights; purpose restrictions; budget allocation

**Original inputs:** TrustedPrincipal, DataAccessPolicy, CapabilityProfile, BudgetAccount

**Original outputs:** AuthorizedContext, AccessDecision, BudgetReservation

**Feature coverage:** FM03 (REFERENCE); FM19 (PROPOSED)

**Invoke:** Proposed: no callable product operation; reference-checks

**Audit:** F15 The protocol fixture does not constrain mode/effects against operation parameters

## ING-01 — Source connector dispatcher

**Submodules:** ATS/jobs; reviews/forums; traffic and SEO; registries/filings; publications/case studies; authorized operations

**Original inputs:** SourceDefinition, AcquisitionSpec, AuthorizedContext

**Original outputs:** AcquisitionAttempt, Artifact, SourceRecord

**Feature coverage:** FM19 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## ING-02 — Scrapling discovery and capture planner

**Submodules:** normalization; robots policy integration; sitemaps; well-known paths; template discovery; follow-up queue

**Original inputs:** IntakeTarget, ReleaseLock, Capture, Surface

**Original outputs:** ScanPlan, AcquisitionSpec, DiscoveryDecision

**Feature coverage:** FM04 (LOCAL); FM05 (LOCAL); FM06 (SDK_UNVERIFIED)

**Invoke:** analyze-file; demo; scan (dependency-gated)

**Audit:** F09 Retained-file import does not pin subject identity in run configuration

## ING-03 — Scrapling transport and evidence capture

**Submodules:** static HTTP; bounded browser; headers/cookies; original bytes; rendered DOM; network events; timeouts

**Original inputs:** AcquisitionSpec, BudgetReservation, AuthorizedContext

**Original outputs:** AcquisitionAttempt, Capture, Artifact, CaptureCapabilities

**Feature coverage:** FM04 (LOCAL); FM06 (SDK_UNVERIFIED); FM07 (DISABLED)

**Invoke:** Proposed: no callable product operation; demo; scan (dependency-gated)

**Audit:** F12 No-byte failures lose invocation details and have no persisted evaluation manifest

## ING-04 — Surface extraction

**Submodules:** 17 EXTRACT commands; DOM/node locators; full JSON-LD; prose; surface completeness

**Original inputs:** Capture, Artifact, ParserRelease

**Original outputs:** Surface, PageEvidence, ExtractionReport

**Feature coverage:** FM05 (LOCAL); FM08 (LOCAL)

**Invoke:** analyze-file; extract

**Audit:** F06 HTML recovery can silently truncate the parse while reporting complete detection; F14 Collector and canonical matcher disagree on aside-region semantics

## FP-01 — Fingerprint rule execution

**Submodules:** closed rule compiler; literal/alternative/regex/host/image matching; page/host correlation

**Original inputs:** ReleaseLock, PageEvidence, HostEvidenceIndex

**Original outputs:** Match, MatchEvaluation

**Feature coverage:** FM05 (LOCAL); FM09 (LOCAL)

**Invoke:** analyze-file; match

**Audit:** F06 HTML recovery can silently truncate the parse while reporting complete detection; F11 Contradictory duplicate command outcomes are accepted; F14 Collector and canonical matcher disagree on aside-region semantics

## FP-02 — Collector observations and scan assembly

**Submodules:** observation identity; support links; claim projection; vertical qualification; priority; bundle output

**Original inputs:** Capture, Surface, Match, ReleaseLock

**Original outputs:** Observation, SupportLink, ClaimView, QualificationAssessment, PriorityAssessment, ScanBundle

**Feature coverage:** FM04 (LOCAL); FM05 (LOCAL); FM10 (LOCAL); FM11 (LOCAL)

**Invoke:** analyze-file; check; demo; resolve / claims

**Audit:** F03 Publication validates one payload and can persist a different argument set; F09 Retained-file import does not pin subject identity in run configuration; F11 Contradictory duplicate command outcomes are accepted

## FP-03 — Fingerprint discovery and promotion

**Submodules:** unknown normalization; prevalence; bounded samples; donor import; quarantine; review; fixture and calibration gates

**Original inputs:** Surface, FingerprintCandidate, RuleReview, FixtureReport

**Original outputs:** CandidateRecord, ImportReport, RuleReleaseProposal

**Feature coverage:** FM13 (LOCAL); FM14 (LOCAL); FM15 (PROPOSED)

**Invoke:** Proposed: no callable product operation; candidates; import-donor

**Audit:** F10 Current candidate discovery counts unlabelled revoked evidence

## ING-05 — Stored-evidence replay and comparison

**Submodules:** capability checks; byte verification; re-extraction; rematching; diffs; recapture requests

**Original inputs:** ReplayRequest, ScanBundle, ReleaseLock

**Original outputs:** ScanBundle, ReplayReport, DiffReport, RecaptureRequest

**Feature coverage:** FM12 (LOCAL)

**Invoke:** replay

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## AI-01 — Bounded model gateway

**Submodules:** task/prompt registry; approved providers; raw I/O; structured parsing; bounded repair; cost and terminal state

**Original inputs:** ModelTask, Artifact, EvidenceSet, BudgetReservation

**Original outputs:** ModelCall, RepairAttempt, TypedModelResult

**Feature coverage:** FM20 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** F05 Generated-artifact handoff is accepted by one validator and rejected by another

## KN-01 — Identity and subject binding

**Submodules:** organization/person/location/product/industry resolution; external IDs; domain ownership; aliases; merge/split review

**Original inputs:** IntakeTarget, SourceRecord, BindingEvidence, Subject

**Original outputs:** Subject, SubjectBinding, BindingDecision

**Feature coverage:** FM16 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** F01 Identity-binding evidence is outside eligibility/provenance closure

## KN-02 — Canonical fact admission

**Submodules:** collector bridge; predicate-specific validation; source mapping; producer and lineage closure; coverage; idempotent insert

**Original inputs:** Observation, SupportLink, SourceRecord, TypedModelResult, SubjectBinding, AcquisitionAttempt

**Original outputs:** Fact, EvidenceSet, EvidenceLocator, ExecutionRecord, AdmissionReport, CandidateRecord

**Feature coverage:** FM17 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** F01 Identity-binding evidence is outside eligibility/provenance closure; F05 Generated-artifact handoff is accepted by one validator and rejected by another; F07 A self-superseding fact raises RecursionError before semantic rejection; F14 Collector and canonical matcher disagree on aside-region semantics; F16 effective_at is stored but its decision semantics are undefined/unused

## KN-03 — Canonical claim resolution

**Submodules:** complete claim grouping; scope/cardinality; freshness/authority; conflict policy; corrections

**Original inputs:** Fact, EvidenceSet, SubjectBinding, ChangeRecord, ResolutionPolicy

**Original outputs:** ClaimResolution

**Feature coverage:** FM18 (REFERENCE); FM35 (REFERENCE)

**Invoke:** Store.revoke or Bundle.validate_change (local/reference only); canonical validate / Python fixture API

**Audit:** F01 Identity-binding evidence is outside eligibility/provenance closure; F04 Later supersession leaks into an earlier sealed evaluation; F07 A self-superseding fact raises RecursionError before semantic rejection; F08 Requirement minimum means fact count in the helper but origin count in validation; F16 effective_at is stored but its decision semantics are undefined/unused

## KN-04 — Knowledge queries and evaluation input selection

**Submodules:** typed filters; knowledge-only results; as-of/known-at reads; exact input manifests; upstream closure

**Original inputs:** KnowledgeQuery, BatchRun, Fact, ClaimResolution

**Original outputs:** KnowledgeView, InputSnapshot, QueryReport

**Feature coverage:** FM18 (REFERENCE)

**Invoke:** canonical validate / Python fixture API

**Audit:** F04 Later supersession leaks into an earlier sealed evaluation

## RE-01 — Deterministic derivations and temporal/cohort calculations

**Submodules:** input selectors; descriptors; history comparisons; membership aggregation; baselines/percentiles

**Original inputs:** InputSnapshot, FunctionDefinition, TypedParameters

**Original outputs:** DerivedFactDraft, ExecutionRecord, DerivationReport

**Feature coverage:** FM23 (REFERENCE)

**Invoke:** reference functions, not a product CLI

**Audit:** F04 Later supersession leaks into an earlier sealed evaluation; F05 Generated-artifact handoff is accepted by one validator and rejected by another

## RE-02 — Research samples and priors

**Submodules:** sample selection; deduplication; classifications; support policy; denominators/exclusions; priors

**Original inputs:** InputSnapshot, ResearchSample, ResearchSupportPolicy, SampleRecordDecision

**Original outputs:** ResearchPriorDraft, ExecutionRecord, ResearchReport

**Feature coverage:** FM21 (REFERENCE)

**Invoke:** canonical fixture validation / Python helpers

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## RE-03 — Account-to-research context joins

**Submodules:** product relationships; industry membership; allowlisted cross-subject joins

**Original inputs:** ClaimResolution, ContextJoinRule, ResearchPriorFact

**Original outputs:** ContextAssessment

**Feature coverage:** FM21 (REFERENCE)

**Invoke:** canonical fixture validation / Python helpers

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## RE-04 — Case-study and lookalike analysis

**Submodules:** reported case-study extraction; quality assessment; feature versions; optional similarity; differences

**Original inputs:** InputSnapshot, CaseStudyFacts, ComparisonPolicy

**Original outputs:** LookalikeMatch, ComparisonReport

**Feature coverage:** FM22 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## RE-05 — Signals and adjudication

**Submodules:** condition functions; confounds; explicit negative/unknown/error reasons; verification requests

**Original inputs:** InputSnapshot, ClaimResolution, ContextAssessment, SignalDefinition

**Original outputs:** SignalEvaluation, SignalDecision, AdjudicationReport, VerificationRequest

**Feature coverage:** FM23 (REFERENCE)

**Invoke:** reference functions, not a product CLI

**Audit:** F08 Requirement minimum means fact count in the helper but origin count in validation; F16 effective_at is stored but its decision semantics are undefined/unused

## COM-01 — Opportunity and playbook selection

**Submodules:** service-line mapping; audience/offer fit; priority; template eligibility; playbooks

**Original inputs:** SignalEvaluation, ContextAssessment, ComparisonReport, OfferPolicy

**Original outputs:** OpportunitySelection

**Feature coverage:** FM24 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## COM-02 — Grounded clauses and packages

**Submodules:** approved renderers; whole-clause checks; quote context; assumption-labeled scenarios; package revisions

**Original inputs:** OpportunitySelection, InputSnapshot, TemplateDefinition, ClaimResolution

**Original outputs:** GroundedClause, OutreachPackage, PackageValidationReport, MessageArtifact

**Feature coverage:** FM26 (REFERENCE)

**Invoke:** Bundle.render(existing_package)

**Audit:** F02 Demoted templates pass the standalone current-use/export boundary

## COM-03 — Authorized review

**Submodules:** evidence viewer; revision comparison; reviewer permissions; approval/rejection

**Original inputs:** OutreachPackage, PackageValidationReport, TrustedPrincipal

**Original outputs:** ReviewDecision

**Feature coverage:** FM27 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** F02 Demoted templates pass the standalone current-use/export boundary

## COM-04 — Current-use gate and controlled export

**Submodules:** freshness/rights/restrictions; purpose/destination; mapping; local/CRM export; receipts

**Original inputs:** OutreachPackage, ReviewDecision, DestinationDefinition, CurrentRestrictionSnapshot, DeliveryIntent, CampaignApproval, CampaignReadiness, ContactAssessment

**Original outputs:** UseGateDecision, ExportReceipt, SendGateDecision

**Feature coverage:** FM28 (REFERENCE)

**Invoke:** LocalPreviewExporter via walkthrough helper

**Audit:** F01 Identity-binding evidence is outside eligibility/provenance closure; F02 Demoted templates pass the standalone current-use/export boundary

## COM-05 — Delivery and reconciliation

**Submodules:** recipient resolution; send permissions; outbox; provider dispatch; unknown acceptance; unsubscribe

**Original inputs:** DeliveryIntent, UseGateDecision, OutreachPackage, TrustedRecipientBinding, SendGateDecision, MessageArtifact, StepEligibility

**Original outputs:** DeliveryAttempt, Exposure, ReconciliationRecord, SenderCapabilitySnapshot

**Feature coverage:** FM31 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## COM-06 — Outcomes and descriptive performance

**Submodules:** webhook verification; event deduplication; exposure joins; mature windows; measurement

**Original inputs:** OutcomeEvent, Exposure, AttributionPolicy, MeasurementWindow, CRMSyncReceipt

**Original outputs:** AttributedOutcome, MeasurementFactDraft, OutcomeReport

**Feature coverage:** FM32 (PROPOSED); FM34 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## PLAT-01 — Records, blobs and transactions

**Submodules:** immutable references; content hashes; record manifests; SQLite/local backend; atomic commit; checkpoints

**Original inputs:** ValidatedRecord, ArtifactBytes, WriteTransaction

**Original outputs:** RecordRef, CommitReceipt

**Feature coverage:** FM11 (LOCAL); FM36 (LOCAL)

**Invoke:** check; ks-module and offline walkthrough harness

**Audit:** F03 Publication validates one payload and can persist a different argument set; F12 No-byte failures lose invocation details and have no persisted evaluation manifest

## PLAT-02 — Governance, corrections and retention

**Submodules:** authorized change records; rule/source revocation; deletion/tombstones; backup/restore; current-use invalidation

**Original inputs:** AuthorizedChangeRequest, DataAccessPolicy, RecordRef, TrustedPrincipal

**Original outputs:** ChangeRecord, RevocationRecord, RetentionAction, RestoreReport

**Feature coverage:** FM35 (REFERENCE)

**Invoke:** Store.revoke or Bundle.validate_change (local/reference only)

**Audit:** F10 Current candidate discovery counts unlabelled revoked evidence

## PLAT-03 — Diagnostics and operator interface

**Submodules:** execution index; structured logs; why/why-not; trace/diff; offline replay UI; safe debug bundles; metrics

**Original inputs:** ModuleRequest, ModuleResult, RecordRef, Diagnostic

**Original outputs:** ExecutionTimeline, ExplanationReport, DebugBundle, RunReport

**Feature coverage:** FM36 (LOCAL)

**Invoke:** ks-module and offline walkthrough harness

**Audit:** F11 Contradictory duplicate command outcomes are accepted; F12 No-byte failures lose invocation details and have no persisted evaluation manifest; F13 Protocol rejects an honest timeout failure reported after its deadline; F15 The protocol fixture does not constrain mode/effects against operation parameters

## GTM-01 — Program, audience and offer design

**Submodules:** service-line objectives; versioned ideal-customer criteria; exclusions and existing-customer policies; geography and scope; offer and playbook catalog; per-program acquisition and outreach limits

**Original inputs:** ProgramDraft, OfferCatalog, DataAccessPolicy

**Original outputs:** ProgramDefinition, AudienceDefinition, OfferDefinition

**Feature coverage:** FM01 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## GTM-02 — Account sourcing, selection and research planning

**Submodules:** CSV and Harvest intake adapter; permitted discovery-source queries; candidate origin tracking; deduplication through identity service; fit selection without truth promotion; coverage gaps and bounded enrichment planning

**Original inputs:** ProgramDefinition, AudienceDefinition, SourceRecord, SubjectBinding, CRMAccountView, KnowledgeView

**Original outputs:** AccountSeed, LeadSelection, ResearchPlan, IntakeRequest

**Feature coverage:** FM02 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## AUD-01 — Contacts, role evidence and audience selection

**Submodules:** person-account relationship evidence; approved endpoint enrichment; email/phone verification status; persona selection; recipient scope and source rights; endpoint alias and role changes

**Original inputs:** Subject, SubjectBinding, OpportunitySelection, SourceRecord, DataAccessPolicy, CurrentRestrictionSnapshot

**Original outputs:** ContactProfile, ContactAssessment

**Feature coverage:** FM25 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## CAM-01 — Campaign and sequence policy

**Submodules:** route mappings; ordered step definitions; template eligibility; sender constraints; timezone/calendar policy; frequency and cross-campaign caps; approval and remote-state preflight

**Original inputs:** ProgramDefinition, OfferDefinition, TemplateDefinition, DestinationDefinition, SenderCapabilitySnapshot

**Original outputs:** CampaignDefinition, CampaignApproval, CampaignReadiness

**Feature coverage:** FM29 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## CAM-02 — Enrollment, scheduling and stop control

**Submodules:** contact/account enrollment deduplication; cross-program fatigue and exclusivity; durable next-step eligibility; holds and cancellation; reply-driven stops; out-of-order event handling; provider-managed schedule reconciliation

**Original inputs:** CampaignDefinition, CampaignApproval, CampaignReadiness, ContactAssessment, ReviewDecision, CRMAccountView, UseRestriction, EnrollmentControl, DeliveryAttempt, ReplyAssessment

**Original outputs:** Enrollment, StepEligibility, DeliveryIntent

**Feature coverage:** FM30 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## ENG-01 — Conversations, replies and response handling

**Submodules:** verified inbound routing; immediate safety stop path; reply thread and exposure linkage; bounded intent classification; out-of-office handling; human response drafts; referrals and new contact admission; meeting/sales handoff

**Original inputs:** OutcomeEvent, Exposure, ContactProfile, Enrollment, Artifact, TypedModelResult

**Original outputs:** Conversation, ReplyAssessment, EnrollmentControl, SalesHandoff, FollowUpTask, AuthorizedChangeRequest

**Feature coverage:** FM32 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## CRM-01 — CRM synchronization and sales handoff

**Submodules:** provider identity mapping; field ownership and schema mappings; existing account/deal exclusions; upsert and receipt reconciliation; sales tasks and meeting handoff; deal-stage and outcome ingestion; sync-loop prevention

**Original inputs:** CRMMapping, SalesHandoff, ExportReceipt, Conversation, OutcomeEvent, AuthorizedContext

**Original outputs:** CRMAccountView, CRMSyncIntent, CRMSyncReceipt, OutcomeEvent, CRMMapping

**Feature coverage:** FM33 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## QA-01 — Evaluation, experiments and promotion assessment

**Submodules:** gold-set evaluation; detector and semantic extraction quality; template review quality; measured source costs and coverage; campaign holdouts and assignment; drift checks; promotion/demotion proposals

**Original inputs:** ExperimentDefinition, FixtureReport, CalibrationRecord, OutcomeReport, ExecutionRecord, RuleReleaseProposal

**Original outputs:** ExperimentAssignment, QualityAssessment, PromotionProposal, ExperimentDefinition

**Feature coverage:** FM15 (PROPOSED); FM34 (PROPOSED)

**Invoke:** Proposed: no callable product operation

**Audit:** No new reproduced bug; implementation gaps remain as shown.

## UX-01 — Product workspace and operator workflows

**Submodules:** program and source setup; account evidence and research browser; contact and candidate review; package and campaign review; inbox and sales queues; CRM and delivery health; audit permissions and diagnostic navigation

**Original inputs:** KnowledgeView, RunReport, ExecutionTimeline, OpportunitySelection, OutreachPackage, ContactProfile, Enrollment, Conversation, CRMSyncReceipt, TrustedPrincipal

**Original outputs:** WorkspaceView, ModuleRequest

**Feature coverage:** FM27 (PROPOSED); FM36 (LOCAL)

**Invoke:** Proposed: no callable product operation; ks-module and offline walkthrough harness

**Audit:** No new reproduced bug; implementation gaps remain as shown.
