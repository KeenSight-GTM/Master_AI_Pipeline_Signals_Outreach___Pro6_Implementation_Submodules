# Full product module matrix

Status: proposed full-system boundary map. All 30 prior IDs are retained; nine product-operation boundaries are proposed. These are modules, not services. A listed contract is not necessarily an implemented schema. Inputs/outputs enumerate record families across operations, not one function signature.

| ID | Module | Main inputs | Main outputs | Main submodules | Origin |
|---|---|---|---|---|---|
| CTL-01 | Contracts and release compiler | `CapabilityProfile`, `VersionedDefinitions`, `ImplementationManifest` | `ReleaseLock`, `ValidationReport` | schema registry; domain catalogs; 38-command registry; function allowlist; release compatibility | Retained/extended |
| CTL-02 | Intake and batch coordination | `IntakeRequest`, `ReleaseLock`, `ProgramDefinition`, `ResearchPlan` | `BatchRun`, `ModuleRequest`, `TargetResult`, `RunReport` | target intake; operation identity; dependency order; per-target completion; checkpoint and resume | Retained/extended |
| CTL-03 | Access, source policy and budget admission | `TrustedPrincipal`, `DataAccessPolicy`, `CapabilityProfile`, `BudgetAccount` | `AuthorizedContext`, `AccessDecision`, `BudgetReservation` | trusted authentication context; tenant authorization; source rights; purpose restrictions; budget allocation | Retained/extended |
| ING-01 | Source connector dispatcher | `SourceDefinition`, `AcquisitionSpec`, `AuthorizedContext` | `AcquisitionAttempt`, `Artifact`, `SourceRecord` | ATS/jobs; reviews/forums; traffic and SEO; registries/filings; publications/case studies; authorized operations | Retained/extended |
| ING-02 | Scrapling discovery and capture planner | `IntakeTarget`, `ReleaseLock`, `Capture`, `Surface` | `ScanPlan`, `AcquisitionSpec`, `DiscoveryDecision` | normalization; robots policy integration; sitemaps; well-known paths; template discovery; follow-up queue | Retained/extended |
| ING-03 | Scrapling transport and evidence capture | `AcquisitionSpec`, `BudgetReservation`, `AuthorizedContext` | `AcquisitionAttempt`, `Capture`, `Artifact`, `CaptureCapabilities` | static HTTP; bounded browser; headers/cookies; original bytes; rendered DOM; network events; timeouts | Retained/extended |
| ING-04 | Surface extraction | `Capture`, `Artifact`, `ParserRelease` | `Surface`, `PageEvidence`, `ExtractionReport` | 17 EXTRACT commands; DOM/node locators; full JSON-LD; prose; surface completeness | Retained/extended |
| FP-01 | Fingerprint rule execution | `ReleaseLock`, `PageEvidence`, `HostEvidenceIndex` | `Match`, `MatchEvaluation` | closed rule compiler; literal/alternative/regex/host/image matching; page/host correlation | Retained/extended |
| FP-02 | Collector observations and scan assembly | `Capture`, `Surface`, `Match`, `ReleaseLock` | `Observation`, `SupportLink`, `ClaimView`, `QualificationAssessment`, `PriorityAssessment`, `ScanBundle` | observation identity; support links; claim projection; vertical qualification; priority; bundle output | Retained/extended |
| FP-03 | Fingerprint discovery and promotion | `Surface`, `FingerprintCandidate`, `RuleReview`, `FixtureReport` | `CandidateRecord`, `ImportReport`, `RuleReleaseProposal` | unknown normalization; prevalence; bounded samples; donor import; quarantine; review; fixture and calibration gates | Retained/extended |
| ING-05 | Stored-evidence replay and comparison | `ReplayRequest`, `ScanBundle`, `ReleaseLock` | `ScanBundle`, `ReplayReport`, `DiffReport`, `RecaptureRequest` | capability checks; byte verification; re-extraction; rematching; diffs; recapture requests | Retained/extended |
| AI-01 | Bounded model gateway | `ModelTask`, `Artifact`, `EvidenceSet`, `BudgetReservation` | `ModelCall`, `RepairAttempt`, `TypedModelResult` | task/prompt registry; approved providers; raw I/O; structured parsing; bounded repair; cost and terminal state | Retained/extended |
| KN-01 | Identity and subject binding | `IntakeTarget`, `SourceRecord`, `BindingEvidence`, `Subject` | `Subject`, `SubjectBinding`, `BindingDecision` | organization/person/location/product/industry resolution; external IDs; domain ownership; aliases; merge/split review | Retained/extended |
| KN-02 | Canonical fact admission | `Observation`, `SupportLink`, `SourceRecord`, `TypedModelResult`, `SubjectBinding`, `AcquisitionAttempt` | `Fact`, `EvidenceSet`, `EvidenceLocator`, `ExecutionRecord`, `AdmissionReport`, `CandidateRecord` | collector bridge; predicate-specific validation; source mapping; producer and lineage closure; coverage; idempotent insert | Retained/extended |
| KN-03 | Canonical claim resolution | `Fact`, `EvidenceSet`, `SubjectBinding`, `ChangeRecord`, `ResolutionPolicy` | `ClaimResolution` | complete claim grouping; scope/cardinality; freshness/authority; conflict policy; corrections | Retained/extended |
| KN-04 | Knowledge queries and evaluation input selection | `KnowledgeQuery`, `BatchRun`, `Fact`, `ClaimResolution` | `KnowledgeView`, `InputSnapshot`, `QueryReport` | typed filters; knowledge-only results; as-of/known-at reads; exact input manifests; upstream closure | Retained/extended |
| RE-01 | Deterministic derivations and temporal/cohort calculations | `InputSnapshot`, `FunctionDefinition`, `TypedParameters` | `DerivedFactDraft`, `ExecutionRecord`, `DerivationReport` | input selectors; descriptors; history comparisons; membership aggregation; baselines/percentiles | Retained/extended |
| RE-02 | Research samples and priors | `InputSnapshot`, `ResearchSample`, `ResearchSupportPolicy`, `SampleRecordDecision` | `ResearchPriorDraft`, `ExecutionRecord`, `ResearchReport` | sample selection; deduplication; classifications; support policy; denominators/exclusions; priors | Retained/extended |
| RE-03 | Account-to-research context joins | `ClaimResolution`, `ContextJoinRule`, `ResearchPriorFact` | `ContextAssessment` | product relationships; industry membership; allowlisted cross-subject joins | Retained/extended |
| RE-04 | Case-study and lookalike analysis | `InputSnapshot`, `CaseStudyFacts`, `ComparisonPolicy` | `LookalikeMatch`, `ComparisonReport` | reported case-study extraction; quality assessment; feature versions; optional similarity; differences | Retained/extended |
| RE-05 | Signals and adjudication | `InputSnapshot`, `ClaimResolution`, `ContextAssessment`, `SignalDefinition` | `SignalEvaluation`, `SignalDecision`, `AdjudicationReport`, `VerificationRequest` | condition functions; confounds; explicit negative/unknown/error reasons; verification requests | Retained/extended |
| COM-01 | Opportunity and playbook selection | `SignalEvaluation`, `ContextAssessment`, `ComparisonReport`, `OfferPolicy` | `OpportunitySelection` | service-line mapping; audience/offer fit; priority; template eligibility; playbooks | Retained/extended |
| COM-02 | Grounded clauses and packages | `OpportunitySelection`, `InputSnapshot`, `TemplateDefinition`, `ClaimResolution` | `GroundedClause`, `OutreachPackage`, `PackageValidationReport`, `MessageArtifact` | approved renderers; whole-clause checks; quote context; assumption-labeled scenarios; package revisions | Retained/extended |
| COM-03 | Authorized review | `OutreachPackage`, `PackageValidationReport`, `TrustedPrincipal` | `ReviewDecision` | evidence viewer; revision comparison; reviewer permissions; approval/rejection | Retained/extended |
| COM-04 | Current-use gate and controlled export | `OutreachPackage`, `ReviewDecision`, `DestinationDefinition`, `CurrentRestrictionSnapshot`, `DeliveryIntent`, `CampaignApproval`, `CampaignReadiness`, `ContactAssessment` | `UseGateDecision`, `ExportReceipt`, `SendGateDecision` | freshness/rights/restrictions; purpose/destination; mapping; local/CRM export; receipts | Retained/extended |
| COM-05 | Delivery and reconciliation | `DeliveryIntent`, `UseGateDecision`, `OutreachPackage`, `TrustedRecipientBinding`, `SendGateDecision`, `MessageArtifact`, `StepEligibility` | `DeliveryAttempt`, `Exposure`, `ReconciliationRecord`, `SenderCapabilitySnapshot` | recipient resolution; send permissions; outbox; provider dispatch; unknown acceptance; unsubscribe | Retained/extended |
| COM-06 | Outcomes and descriptive performance | `OutcomeEvent`, `Exposure`, `AttributionPolicy`, `MeasurementWindow`, `CRMSyncReceipt` | `AttributedOutcome`, `MeasurementFactDraft`, `OutcomeReport` | webhook verification; event deduplication; exposure joins; mature windows; measurement | Retained/extended |
| PLAT-01 | Records, blobs and transactions | `ValidatedRecord`, `ArtifactBytes`, `WriteTransaction` | `RecordRef`, `CommitReceipt` | immutable references; content hashes; record manifests; SQLite/local backend; atomic commit; checkpoints | Retained/extended |
| PLAT-02 | Governance, corrections and retention | `AuthorizedChangeRequest`, `DataAccessPolicy`, `RecordRef`, `TrustedPrincipal` | `ChangeRecord`, `RevocationRecord`, `RetentionAction`, `RestoreReport` | authorized change records; rule/source revocation; deletion/tombstones; backup/restore; current-use invalidation | Retained/extended |
| PLAT-03 | Diagnostics and operator interface | `ModuleRequest`, `ModuleResult`, `RecordRef`, `Diagnostic` | `ExecutionTimeline`, `ExplanationReport`, `DebugBundle`, `RunReport` | execution index; structured logs; why/why-not; trace/diff; offline replay UI; safe debug bundles; metrics | Retained/extended |
| GTM-01 | Program, audience and offer design | `ProgramDraft`, `OfferCatalog`, `DataAccessPolicy` | `ProgramDefinition`, `AudienceDefinition`, `OfferDefinition` | service-line objectives; versioned ideal-customer criteria; exclusions and existing-customer policies; geography and scope; offer and playbook catalog; per-program acquisition and outreach limits | New proposal |
| GTM-02 | Account sourcing, selection and research planning | `ProgramDefinition`, `AudienceDefinition`, `SourceRecord`, `SubjectBinding`, `CRMAccountView`, `KnowledgeView` | `AccountSeed`, `LeadSelection`, `ResearchPlan`, `IntakeRequest` | CSV and Harvest intake adapter; permitted discovery-source queries; candidate origin tracking; deduplication through identity service; fit selection without truth promotion; coverage gaps and bounded enrichment planning | New proposal |
| AUD-01 | Contacts, role evidence and audience selection | `Subject`, `SubjectBinding`, `OpportunitySelection`, `SourceRecord`, `DataAccessPolicy`, `CurrentRestrictionSnapshot` | `ContactProfile`, `ContactAssessment` | person-account relationship evidence; approved endpoint enrichment; email/phone verification status; persona selection; recipient scope and source rights; endpoint alias and role changes | New proposal |
| CAM-01 | Campaign and sequence policy | `ProgramDefinition`, `OfferDefinition`, `TemplateDefinition`, `DestinationDefinition`, `SenderCapabilitySnapshot` | `CampaignDefinition`, `CampaignApproval`, `CampaignReadiness` | route mappings; ordered step definitions; template eligibility; sender constraints; timezone/calendar policy; frequency and cross-campaign caps; approval and remote-state preflight | New proposal |
| CAM-02 | Enrollment, scheduling and stop control | `CampaignDefinition`, `CampaignApproval`, `CampaignReadiness`, `ContactAssessment`, `ReviewDecision`, `CRMAccountView`, `UseRestriction`, `EnrollmentControl`, `DeliveryAttempt`, `ReplyAssessment` | `Enrollment`, `StepEligibility`, `DeliveryIntent` | contact/account enrollment deduplication; cross-program fatigue and exclusivity; durable next-step eligibility; holds and cancellation; reply-driven stops; out-of-order event handling; provider-managed schedule reconciliation | New proposal |
| ENG-01 | Conversations, replies and response handling | `OutcomeEvent`, `Exposure`, `ContactProfile`, `Enrollment`, `Artifact`, `TypedModelResult` | `Conversation`, `ReplyAssessment`, `EnrollmentControl`, `SalesHandoff`, `FollowUpTask`, `AuthorizedChangeRequest` | verified inbound routing; immediate safety stop path; reply thread and exposure linkage; bounded intent classification; out-of-office handling; human response drafts; referrals and new contact admission; meeting/sales handoff | New proposal |
| CRM-01 | CRM synchronization and sales handoff | `CRMMapping`, `SalesHandoff`, `ExportReceipt`, `Conversation`, `OutcomeEvent`, `AuthorizedContext` | `CRMAccountView`, `CRMSyncIntent`, `CRMSyncReceipt`, `OutcomeEvent`, `CRMMapping` | provider identity mapping; field ownership and schema mappings; existing account/deal exclusions; upsert and receipt reconciliation; sales tasks and meeting handoff; deal-stage and outcome ingestion; sync-loop prevention | New proposal |
| QA-01 | Evaluation, experiments and promotion assessment | `ExperimentDefinition`, `FixtureReport`, `CalibrationRecord`, `OutcomeReport`, `ExecutionRecord`, `RuleReleaseProposal` | `ExperimentAssignment`, `QualityAssessment`, `PromotionProposal`, `ExperimentDefinition` | gold-set evaluation; detector and semantic extraction quality; template review quality; measured source costs and coverage; campaign holdouts and assignment; drift checks; promotion/demotion proposals | New proposal |
| UX-01 | Product workspace and operator workflows | `KnowledgeView`, `RunReport`, `ExecutionTimeline`, `OpportunitySelection`, `OutreachPackage`, `ContactProfile`, `Enrollment`, `Conversation`, `CRMSyncReceipt`, `TrustedPrincipal` | `WorkspaceView`, `ModuleRequest` | program and source setup; account evidence and research browser; contact and candidate review; package and campaign review; inbox and sales queues; CRM and delivery health; audit permissions and diagnostic navigation | New proposal |

## Ownership refinements

### CTL-02 — Intake and batch coordination

Carry program/account evaluation correlation through independent target runs; long-lived campaigns and conversations are not BatchRun states.

### CTL-03 — Access, source policy and budget admission

Require first-source approval, sender/account permissions, authenticated ingress, and reservations before each enabled external action.

### KN-01 — Identity and subject binding

Own canonical people, organization, location, product identities and their accepted relationships; AUD-01 requests bindings rather than defining a second identity system.

### KN-02 — Canonical fact admission

Admission is the only canonical Fact writer, including reply statements, CRM reports, and derived metrics. Human-origin statements are not confused with model intent labels.

### COM-01 — Opportunity and playbook selection

Choose an account-level service-line opportunity, distinct from CRM-owned sales opportunities. Permit no-offer result while retaining knowledge.

### COM-02 — Grounded clauses and packages

Render and validate exact channel messages per proposed MessageArtifact, including subject/footer and any allowed transformations. Each later step has its own eligible evidence and approved revision.

### COM-03 — Authorized review

Existing ReviewDecision remains package-revision scoped. CampaignApproval is a separate new contract owned by CAM-01.

### COM-04 — Current-use gate and controlled export

Continue preview/contact export as currently modeled; add a separate SendGateDecision only with an explicit versioned contract. Do not interpret CONTACT_EXPORT as SEND.

### COM-05 — Delivery and reconciliation

CAM-02 owns scheduling, AUD-01 owns contact assessment; dispatch validates their records plus a fresh SendGateDecision. Sender capabilities/settings and uncertain-effect reconciliation belong here.

### COM-06 — Outcomes and descriptive performance

Provide a verified, deduplicated ingress route to ENG-01 before optional analytics; do not wait for mature performance measurement to stop outreach. Preserve unmatched events in quarantine.

### PLAT-02 — Governance, corrections and retention

Only authorized governance writes UseRestriction and ChangeRecord; F remains unclosed in baseline. Atomically signal stop requirements and invalidate current-use caches within the local system.

### PLAT-03 — Diagnostics and operator interface

Trace links connect acquisition, evaluation, enrollment, individual effects, replies and CRM receipts without requiring one trace spanning the entire lifecycle.

