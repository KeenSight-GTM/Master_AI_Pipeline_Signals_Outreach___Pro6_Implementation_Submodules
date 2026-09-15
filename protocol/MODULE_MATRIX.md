# Complete module input/output matrix

Proposed public module boundaries, not separate network services. Domain types without current schema counterparts are explicit proposed DTOs. The common protocol does not validate their payloads by itself. Each enabled operation must register exact type versions, input/output cardinalities, semantic gates, implementation identity and test coverage. Internal helper functions remain ordinary typed functions.

## Control and contracts

| ID / module | Inputs | Outputs | Submodules |
|---|---|---|---|
| **CTL-01 — Contracts and release compiler** | `CapabilityProfile`, `VersionedDefinitions`, `ImplementationManifest` | `ReleaseLock`, `ValidationReport` | schema registry; domain catalogs; 38-command registry; function allowlist; release compatibility |
| **CTL-02 — Intake and batch coordination** | `IntakeRequest`, `ReleaseLock` | `BatchRun`, `ModuleRequest`, `TargetResult`, `RunReport` | target intake; operation identity; dependency order; per-target completion; checkpoint and resume |
| **CTL-03 — Access, source policy and budget admission** | `TrustedPrincipal`, `DataAccessPolicy`, `CapabilityProfile`, `BudgetAccount` | `AuthorizedContext`, `AccessDecision`, `BudgetReservation` | trusted authentication context; tenant authorization; source rights; purpose restrictions; budget allocation |

**CTL-01 invariant:** Reject unknown implementations and incompatible exact schema versions before execution. **Current boundary:** v4.1 validation and collector rule loaders exist separately; unified release compiler proposed.

**CTL-02 invariant:** A completed target is published only after its required outputs commit. Partial batches retain independent target results. **Current boundary:** Collector batch orchestration exists; canonical application coordinator remains to implement.

**CTL-03 invariant:** Tenant and authority come from trusted authentication; child calls share parent budget and cannot reset it. **Current boundary:** Collector has local policy/budget controls; hosted authorization/shared accounting proposed.

## Collection and model-assisted extraction

| ID / module | Inputs | Outputs | Submodules |
|---|---|---|---|
| **ING-01 — Source connector dispatcher** | `SourceDefinition`, `AcquisitionSpec`, `AuthorizedContext` | `AcquisitionAttempt`, `Artifact`, `SourceRecord` | ATS/jobs; reviews/forums; traffic and SEO; registries/filings; publications/case studies; authorized operations |
| **ING-02 — Scrapling discovery and capture planner** | `IntakeTarget`, `ReleaseLock`, `Capture`, `Surface` | `ScanPlan`, `AcquisitionSpec`, `DiscoveryDecision` | normalization; robots policy integration; sitemaps; well-known paths; template discovery; follow-up queue |
| **ING-03 — Scrapling transport and evidence capture** | `AcquisitionSpec`, `BudgetReservation`, `AuthorizedContext` | `AcquisitionAttempt`, `Capture`, `Artifact`, `CaptureCapabilities` | static HTTP; bounded browser; headers/cookies; original bytes; rendered DOM; network events; timeouts |
| **ING-04 — Surface extraction** | `Capture`, `Artifact`, `ParserRelease` | `Surface`, `PageEvidence`, `ExtractionReport` | 17 EXTRACT commands; DOM/node locators; full JSON-LD; prose; surface completeness |
| **FP-01 — Fingerprint rule execution** | `ReleaseLock`, `PageEvidence`, `HostEvidenceIndex` | `Match`, `MatchEvaluation` | closed rule compiler; literal/alternative/regex/host/image matching; page/host correlation |
| **FP-02 — Collector observations and scan assembly** | `Capture`, `Surface`, `Match`, `ReleaseLock` | `Observation`, `SupportLink`, `ClaimView`, `QualificationAssessment`, `PriorityAssessment`, `ScanBundle` | observation identity; support links; claim projection; vertical qualification; priority; bundle output |
| **FP-03 — Fingerprint discovery and promotion** | `Surface`, `FingerprintCandidate`, `RuleReview`, `FixtureReport` | `CandidateRecord`, `ImportReport`, `RuleReleaseProposal` | unknown normalization; prevalence; bounded samples; donor import; quarantine; review; fixture and calibration gates |
| **ING-05 — Stored-evidence replay and comparison** | `ReplayRequest`, `ScanBundle`, `ReleaseLock` | `ScanBundle`, `ReplayReport`, `DiffReport`, `RecaptureRequest` | capability checks; byte verification; re-extraction; rematching; diffs; recapture requests |
| **AI-01 — Bounded model gateway** | `ModelTask`, `Artifact`, `EvidenceSet`, `BudgetReservation` | `ModelCall`, `RepairAttempt`, `TypedModelResult` | task/prompt registry; approved providers; raw I/O; structured parsing; bounded repair; cost and terminal state |

**ING-01 invariant:** Every connector returns the same evidence/attempt boundary; APIs do not bypass admission or labeling. **Current boundary:** Domain contracts exist; broad live adapters not delivered.

**ING-02 invariant:** Discovery does not silently expand origin permission; every retry/probe/redirect consumes the declared budget. **Current boundary:** urls.py, discovery.py and pipeline.py implement local paths; standard facade proposed.

**ING-03 invariant:** No bytes is a legitimate failure; partial/truncated capture cannot claim complete coverage. **Current boundary:** Static adapter exists but actual SDK test is skipped here; native browser disabled.

**ING-04 invariant:** Exact artifact/node provenance and per-surface limits survive; absent output after a failed parser is not absence. **Current boundary:** 17 parsing functions exist in extraction.py.

**FP-01 invariant:** Keep every matching rule and evidence point; NO_MATCH is not a canonical NOT_FOUND fact. **Current boundary:** rules.py implements a subset; complete donor coverage and production calibration pending.

**FP-02 invariant:** Deduplicate observations and claim views, not evidence. Priority cannot alter source authority. **Current boundary:** claims.py, storage.py and pipeline.py implement local behavior; canonical admission still mandatory.

**FP-03 invariant:** Candidates never become approved through count or model confidence; release promotion is authorized and between runs. **Current boundary:** Candidate index and conservative import exist; full review/promotion lifecycle to implement.

**ING-05 invariant:** No network during replay, no TTL refresh, no fabricated unavailable browser/DNS modalities. **Current boundary:** pipeline.py replay and validation implemented for collector.

**AI-01 invariant:** Model outputs remain untrusted extraction/classification/proposal results; successful raw persistence precedes parse and admission. **Current boundary:** v4.1 model/repair contracts and reference checks exist; live gateway to integrate.

## Canonical knowledge

| ID / module | Inputs | Outputs | Submodules |
|---|---|---|---|
| **KN-01 — Identity and subject binding** | `IntakeTarget`, `SourceRecord`, `BindingEvidence`, `Subject` | `Subject`, `SubjectBinding`, `BindingDecision` | organization/person/location/product/industry resolution; external IDs; domain ownership; aliases; merge/split review |
| **KN-02 — Canonical fact admission** | `Observation`, `SupportLink`, `SourceRecord`, `TypedModelResult`, `SubjectBinding`, `AcquisitionAttempt` | `Fact`, `EvidenceSet`, `EvidenceLocator`, `ExecutionRecord`, `AdmissionReport`, `CandidateRecord` | collector bridge; predicate-specific validation; source mapping; producer and lineage closure; coverage; idempotent insert |
| **KN-03 — Canonical claim resolution** | `Fact`, `EvidenceSet`, `SubjectBinding`, `ChangeRecord`, `ResolutionPolicy` | `ClaimResolution` | complete claim grouping; scope/cardinality; freshness/authority; conflict policy; corrections |
| **KN-04 — Knowledge queries and evaluation input selection** | `KnowledgeQuery`, `BatchRun`, `Fact`, `ClaimResolution` | `KnowledgeView`, `InputSnapshot`, `QueryReport` | typed filters; knowledge-only results; as-of/known-at reads; exact input manifests; upstream closure |

**KN-01 invariant:** A provided subject name, redirect or canonical tag does not itself establish ownership; ambiguous bindings abstain. **Current boundary:** Schemas/reference checks exist; production resolver and authenticated change path pending.

**KN-02 invariant:** One admitted observation per source identity and mapping version, retaining all eligible support; never insert one fact per overlapping rule. **Current boundary:** v4.1 validators exist; collector-to-canonical runtime adapter not implemented.

**KN-03 invariant:** Resolve the complete pinned group, not just favorable rows; UNKNOWN never erases a still-valid known observation. **Current boundary:** v4.1 reference resolver exists; persistent integration proposed.

**KN-04 invariant:** Persist actual membership and versions of consumed facts/bindings/samples, not only query text. **Current boundary:** Domain inventory exists; repository/query facade remains to implement.

## Research and reasoning

| ID / module | Inputs | Outputs | Submodules |
|---|---|---|---|
| **RE-01 — Deterministic derivations and temporal/cohort calculations** | `InputSnapshot`, `FunctionDefinition`, `TypedParameters` | `DerivedFactDraft`, `ExecutionRecord`, `DerivationReport` | input selectors; descriptors; history comparisons; membership aggregation; baselines/percentiles |
| **RE-02 — Research samples and priors** | `InputSnapshot`, `ResearchSample`, `ResearchSupportPolicy`, `SampleRecordDecision` | `ResearchPriorDraft`, `ExecutionRecord`, `ResearchReport` | sample selection; deduplication; classifications; support policy; denominators/exclusions; priors |
| **RE-03 — Account-to-research context joins** | `ClaimResolution`, `ContextJoinRule`, `ResearchPriorFact` | `ContextAssessment` | product relationships; industry membership; allowlisted cross-subject joins |
| **RE-04 — Case-study and lookalike analysis** | `InputSnapshot`, `CaseStudyFacts`, `ComparisonPolicy` | `LookalikeMatch`, `ComparisonReport` | reported case-study extraction; quality assessment; feature versions; optional similarity; differences |
| **RE-05 — Signals and adjudication** | `InputSnapshot`, `ClaimResolution`, `ContextAssessment`, `SignalDefinition` | `SignalEvaluation`, `SignalDecision`, `AdjudicationReport`, `VerificationRequest` | condition functions; confounds; explicit negative/unknown/error reasons; verification requests |

**RE-01 invariant:** Derived drafts return through admission; time, eligibility, denominator, algorithm and missingness are explicit. **Current boundary:** Prior numerical reference kernels exist; enabled runtime materializers incomplete.

**RE-02 invariant:** Every denominator and exclusion dependency is pinned; negative pain and neutral workflow mentions do not share implicit meaning. **Current boundary:** v4.1 reference statistics/lineage validation exist; full runtime proposed.

**RE-03 invariant:** Context remains internal; company_claim_allowed=false; ABSTAINED context never qualifies a positive decision. **Current boundary:** v4.1 contracts and reference checks exist.

**RE-04 invariant:** Similarity and a publisher-reported result do not prove a prospect outcome or transferable causality. **Current boundary:** Case-study fact families exist; LookalikeMatch is design-only.

**RE-05 invariant:** Business truth and operational permission stay separate; context or score cannot promote weak evidence. **Current boundary:** v4.1 uses RESOLVED/UNRESOLVED/SUPPRESSED/CANDIDATE; richer SignalDecision is proposed, not present.

## Commercial actions and outcomes

| ID / module | Inputs | Outputs | Submodules |
|---|---|---|---|
| **COM-01 — Opportunity and playbook selection** | `SignalEvaluation`, `ContextAssessment`, `ComparisonReport`, `OfferPolicy` | `OpportunitySelection` | service-line mapping; audience/offer fit; priority; template eligibility; playbooks |
| **COM-02 — Grounded clauses and packages** | `OpportunitySelection`, `InputSnapshot`, `TemplateDefinition`, `ClaimResolution` | `GroundedClause`, `OutreachPackage`, `PackageValidationReport` | approved renderers; whole-clause checks; quote context; assumption-labeled scenarios; package revisions |
| **COM-03 — Authorized review** | `OutreachPackage`, `PackageValidationReport`, `TrustedPrincipal` | `ReviewDecision` | evidence viewer; revision comparison; reviewer permissions; approval/rejection |
| **COM-04 — Current-use gate and controlled export** | `OutreachPackage`, `ReviewDecision`, `DestinationDefinition`, `CurrentRestrictionSnapshot` | `UseGateDecision`, `ExportReceipt` | freshness/rights/restrictions; purpose/destination; mapping; local/CRM export; receipts |
| **COM-05 — Delivery and reconciliation** | `DeliveryIntent`, `UseGateDecision`, `OutreachPackage`, `TrustedRecipientBinding` | `DeliveryAttempt`, `Exposure`, `ReconciliationRecord` | recipient resolution; send permissions; outbox; provider dispatch; unknown acceptance; unsubscribe |
| **COM-06 — Outcomes and descriptive performance** | `OutcomeEvent`, `Exposure`, `AttributionPolicy`, `MeasurementWindow` | `AttributedOutcome`, `MeasurementFactDraft`, `OutcomeReport` | webhook verification; event deduplication; exposure joins; mature windows; measurement |

**COM-01 invariant:** Ranking selects eligible opportunities but cannot strengthen evidence or infer company pain. **Current boundary:** Concepts in architecture/ledger; broad runtime mappings to implement.

**COM-02 invariant:** Only eligible account proof supports account assertions; neutral templates do not require a maturity claim. **Current boundary:** Narrow v4.1 renderers/checks exist; arbitrary prose and new renderer families disabled.

**COM-03 invariant:** Review binds exact revision and content hash and cannot override hard policy/identity/evidence failure. **Current boundary:** Synthetic actor/review reference behavior; production authentication/UI pending.

**COM-04 invariant:** Gate uses current trusted state; exact revision/payload/destination and business-effect identity are preserved across retries. **Current boundary:** v4.1 local preview exporter exists; remote export and production authorization pending.

**COM-05 invariant:** No blind retry after uncertain acceptance; existing no-send profiles cannot reach a sender. **Current boundary:** Reserved contracts/plans only; no sender implemented.

**COM-06 invariant:** Unmatched events are quarantined; reply denominators exclude immature/uncertain cases by declared policy; results remain non-causal. **Current boundary:** Domain contracts/plans exist; live outcomes/performance integration pending.

## Persistence, governance and debugging

| ID / module | Inputs | Outputs | Submodules |
|---|---|---|---|
| **PLAT-01 — Records, blobs and transactions** | `ValidatedRecord`, `ArtifactBytes`, `WriteTransaction` | `RecordRef`, `CommitReceipt` | immutable references; content hashes; record manifests; SQLite/local backend; atomic commit; checkpoints |
| **PLAT-02 — Governance, corrections and retention** | `AuthorizedChangeRequest`, `DataAccessPolicy`, `RecordRef`, `TrustedPrincipal` | `ChangeRecord`, `RevocationRecord`, `RetentionAction`, `RestoreReport` | authorized change records; rule/source revocation; deletion/tombstones; backup/restore; current-use invalidation |
| **PLAT-03 — Diagnostics and operator interface** | `ModuleRequest`, `ModuleResult`, `RecordRef`, `Diagnostic` | `ExecutionTimeline`, `ExplanationReport`, `DebugBundle`, `RunReport` | execution index; structured logs; why/why-not; trace/diff; offline replay UI; safe debug bundles; metrics |

**PLAT-01 invariant:** One canonical fact writer; content finalized before reference commit; identical keys with different bytes fail. **Current boundary:** Collector local blob/SQLite store exists; shared platform repository adapters pending.

**PLAT-02 invariant:** F is still a blocker: foreign-tenant or unauthorized changes must be rejected before hosted production use. **Current boundary:** Collector local revoke exists; v4.1 global ChangeRecord F remains unclosed.

**PLAT-03 invariant:** Trace is not evidence or authority; audit manifests are retained under policy even if routine telemetry is sampled. **Current boundary:** Collector command diagnostics exist; standardized traces and operator views proposed.
