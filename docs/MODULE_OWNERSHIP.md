# Full module and submodule ownership

All 39 IDs from the provided product inventory are retained. Proposed service placement is a future deployment grouping, not current deployed code. Current implementation detail is in the stage cards and repair report.

## S0 Control and programs

### GTM-01 — Program, audience and offer design

**Submodules:** service-line objectives, versioned ideal-customer criteria, exclusions and existing-customer policies, geography and scope, offer and playbook catalog, per-program acquisition and outreach limits.

**Inputs:** ProgramDraft, OfferCatalog, DataAccessPolicy.

**Outputs:** ProgramDefinition, AudienceDefinition, OfferDefinition.

**Ownership invariant:** Configuration is targeting and offer policy, never observed company truth.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

### GTM-02 — Account sourcing, selection and research planning

**Submodules:** CSV and Harvest intake adapter, permitted discovery-source queries, candidate origin tracking, deduplication through identity service, fit selection without truth promotion, coverage gaps and bounded enrichment planning.

**Inputs:** ProgramDefinition, AudienceDefinition, SourceRecord, SubjectBinding, CRMAccountView, KnowledgeView.

**Outputs:** AccountSeed, LeadSelection, ResearchPlan, IntakeRequest.

**Ownership invariant:** A discovery-source row or domain match cannot silently become verified account identity; every rejected/deferred target has a reason.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

### CTL-01 — Contracts and release compiler

**Submodules:** schema registry, domain catalogs, 38-command registry, function allowlist, release compatibility.

**Inputs:** CapabilityProfile, VersionedDefinitions, ImplementationManifest.

**Outputs:** ReleaseLock, ValidationReport.

**Ownership invariant:** Reject unknown implementations and incompatible exact schema versions before execution.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### CTL-02 — Intake and batch coordination

**Submodules:** target intake, operation identity, dependency order, per-target completion, checkpoint and resume.

**Inputs:** IntakeRequest, ReleaseLock, ProgramDefinition, ResearchPlan.

**Outputs:** BatchRun, ModuleRequest, TargetResult, RunReport.

**Ownership invariant:** A completed target is published only after its required outputs commit. Partial batches retain independent target results.

**Replay policy:** ORCHESTRATES_EXPLICIT_MODE. **Effects:** NONE.

### CTL-03 — Access, source policy and budget admission

**Submodules:** trusted authentication context, tenant authorization, source rights, purpose restrictions, budget allocation.

**Inputs:** TrustedPrincipal, DataAccessPolicy, CapabilityProfile, BudgetAccount.

**Outputs:** AuthorizedContext, AccessDecision, BudgetReservation.

**Ownership invariant:** Tenant and authority come from trusted authentication; child calls share parent budget and cannot reset it.

**Replay policy:** CURRENT_CHECK_OR_RECORDED_HISTORICAL_DECISION. **Effects:** NONE.

## S1 Capture and fingerprints

### ING-02 — Scrapling discovery and capture planner

**Submodules:** normalization, robots policy integration, sitemaps, well-known paths, template discovery, follow-up queue.

**Inputs:** IntakeTarget, ReleaseLock, Capture, Surface.

**Outputs:** ScanPlan, AcquisitionSpec, DiscoveryDecision.

**Ownership invariant:** Discovery does not silently expand origin permission; every retry/probe/redirect consumes the declared budget.

**Replay policy:** STORED_DISCOVERY_ONLY. **Effects:** NONE.

### ING-03 — Scrapling transport and evidence capture

**Submodules:** static HTTP, bounded browser, headers/cookies, original bytes, rendered DOM, network events, timeouts.

**Inputs:** AcquisitionSpec, BudgetReservation, AuthorizedContext.

**Outputs:** AcquisitionAttempt, Capture, Artifact, CaptureCapabilities.

**Ownership invariant:** No bytes is a legitimate failure; partial/truncated capture cannot claim complete coverage.

**Replay policy:** NO_NETWORK_IN_REPLAY. **Effects:** APPROVED_NETWORK_READ.

### ING-04 — Surface extraction

**Submodules:** 17 EXTRACT commands, DOM/node locators, full JSON-LD, prose, surface completeness.

**Inputs:** Capture, Artifact, ParserRelease.

**Outputs:** Surface, PageEvidence, ExtractionReport.

**Ownership invariant:** Exact artifact/node provenance and per-surface limits survive; absent output after a failed parser is not absence.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### ING-05 — Stored-evidence replay and comparison

**Submodules:** capability checks, byte verification, re-extraction, rematching, diffs, recapture requests.

**Inputs:** ReplayRequest, ScanBundle, ReleaseLock.

**Outputs:** ScanBundle, ReplayReport, DiffReport, RecaptureRequest.

**Ownership invariant:** No network during replay, no TTL refresh, no fabricated unavailable browser/DNS modalities.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### FP-01 — Fingerprint rule execution

**Submodules:** closed rule compiler, literal/alternative/regex/host/image matching, page/host correlation.

**Inputs:** ReleaseLock, PageEvidence, HostEvidenceIndex.

**Outputs:** Match, MatchEvaluation.

**Ownership invariant:** Keep every matching rule and evidence point; NO_MATCH is not a canonical NOT_FOUND fact.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### FP-02 — Collector observations and scan assembly

**Submodules:** observation identity, support links, claim projection, vertical qualification, priority, bundle output.

**Inputs:** Capture, Surface, Match, ReleaseLock.

**Outputs:** Observation, SupportLink, ClaimView, QualificationAssessment, PriorityAssessment, ScanBundle.

**Ownership invariant:** Deduplicate observations and claim views, not evidence. Priority cannot alter source authority.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### FP-03 — Fingerprint discovery and promotion

**Submodules:** unknown normalization, prevalence, bounded samples, donor import, quarantine, review, fixture and calibration gates.

**Inputs:** Surface, FingerprintCandidate, RuleReview, FixtureReport.

**Outputs:** CandidateRecord, ImportReport, RuleReleaseProposal.

**Ownership invariant:** Candidates never become approved through count or model confidence; release promotion is authorized and between runs.

**Replay policy:** ANALYSIS_REPLAY_ONLY_NO_PROMOTION. **Effects:** AUTHORIZED_RULE_RELEASE_ONLY.

## S2 Canonical knowledge

### KN-01 — Identity and subject binding

**Submodules:** organization/person/location/product/industry resolution, external IDs, domain ownership, aliases, merge/split review.

**Inputs:** IntakeTarget, SourceRecord, BindingEvidence, Subject.

**Outputs:** Subject, SubjectBinding, BindingDecision.

**Ownership invariant:** A provided subject name, redirect or canonical tag does not itself establish ownership; ambiguous bindings abstain.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### KN-02 — Canonical fact admission

**Submodules:** collector bridge, predicate-specific validation, source mapping, producer and lineage closure, coverage, idempotent insert.

**Inputs:** Observation, SupportLink, SourceRecord, TypedModelResult, SubjectBinding, AcquisitionAttempt.

**Outputs:** Fact, EvidenceSet, EvidenceLocator, ExecutionRecord, AdmissionReport, CandidateRecord.

**Ownership invariant:** One admitted observation per source identity and mapping version, retaining all eligible support; never insert one fact per overlapping rule.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### KN-03 — Canonical claim resolution

**Submodules:** complete claim grouping, scope/cardinality, freshness/authority, conflict policy, corrections.

**Inputs:** Fact, EvidenceSet, SubjectBinding, ChangeRecord, ResolutionPolicy.

**Outputs:** ClaimResolution.

**Ownership invariant:** Resolve the complete pinned group, not just favorable rows; UNKNOWN never erases a still-valid known observation.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### KN-04 — Knowledge queries and evaluation input selection

**Submodules:** typed filters, knowledge-only results, as-of/known-at reads, exact input manifests, upstream closure.

**Inputs:** KnowledgeQuery, BatchRun, Fact, ClaimResolution.

**Outputs:** KnowledgeView, InputSnapshot, QueryReport.

**Ownership invariant:** Persist actual membership and versions of consumed facts/bindings/samples, not only query text.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### PLAT-01 — Records, blobs and transactions

**Submodules:** immutable references, content hashes, record manifests, SQLite/local backend, atomic commit, checkpoints.

**Inputs:** ValidatedRecord, ArtifactBytes, WriteTransaction.

**Outputs:** RecordRef, CommitReceipt.

**Ownership invariant:** One canonical fact writer; content finalized before reference commit; identical keys with different bytes fail.

**Replay policy:** READ_ONLY_IN_REPLAY. **Effects:** NONE.

### PLAT-02 — Governance, corrections and retention

**Submodules:** authorized change records, rule/source revocation, deletion/tombstones, backup/restore, current-use invalidation.

**Inputs:** AuthorizedChangeRequest, DataAccessPolicy, RecordRef, TrustedPrincipal.

**Outputs:** ChangeRecord, RevocationRecord, RetentionAction, RestoreReport.

**Ownership invariant:** F is still a blocker: foreign-tenant or unauthorized changes must be rejected before hosted production use.

**Replay policy:** HISTORICAL_READ_ONLY_NO_DELETION_REPLAY. **Effects:** AUTHORIZED_DATA_OR_POLICY_CHANGE.

## S3 Enrichment and model tasks

### ING-01 — Source connector dispatcher

**Submodules:** ATS/jobs, reviews/forums, traffic and SEO, registries/filings, publications/case studies, authorized operations.

**Inputs:** SourceDefinition, AcquisitionSpec, AuthorizedContext.

**Outputs:** AcquisitionAttempt, Artifact, SourceRecord.

**Ownership invariant:** Every connector returns the same evidence/attempt boundary; APIs do not bypass admission or labeling.

**Replay policy:** STORED_RESPONSES_ONLY. **Effects:** APPROVED_READ_OR_PAID_QUERY.

### AI-01 — Bounded model gateway

**Submodules:** task/prompt registry, approved providers, raw I/O, structured parsing, bounded repair, cost and terminal state.

**Inputs:** ModelTask, Artifact, EvidenceSet, BudgetReservation.

**Outputs:** ModelCall, RepairAttempt, TypedModelResult.

**Ownership invariant:** Model outputs remain untrusted extraction/classification/proposal results; successful raw persistence precedes parse and admission.

**Replay policy:** RECORDED_MODEL_OUTPUTS_ONLY. **Effects:** APPROVED_PAID_MODEL_CALL.

## S4 Research and intelligence

### RE-01 — Deterministic derivations and temporal/cohort calculations

**Submodules:** input selectors, descriptors, history comparisons, membership aggregation, baselines/percentiles.

**Inputs:** InputSnapshot, FunctionDefinition, TypedParameters.

**Outputs:** DerivedFactDraft, ExecutionRecord, DerivationReport.

**Ownership invariant:** Derived drafts return through admission; time, eligibility, denominator, algorithm and missingness are explicit.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### RE-02 — Research samples and priors

**Submodules:** sample selection, deduplication, classifications, support policy, denominators/exclusions, priors.

**Inputs:** InputSnapshot, ResearchSample, ResearchSupportPolicy, SampleRecordDecision.

**Outputs:** ResearchPriorDraft, ExecutionRecord, ResearchReport.

**Ownership invariant:** Every denominator and exclusion dependency is pinned; negative pain and neutral workflow mentions do not share implicit meaning.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### RE-03 — Account-to-research context joins

**Submodules:** product relationships, industry membership, allowlisted cross-subject joins.

**Inputs:** ClaimResolution, ContextJoinRule, ResearchPriorFact.

**Outputs:** ContextAssessment.

**Ownership invariant:** Context remains internal; company_claim_allowed=false; ABSTAINED context never qualifies a positive decision.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### RE-04 — Case-study and lookalike analysis

**Submodules:** reported case-study extraction, quality assessment, feature versions, optional similarity, differences.

**Inputs:** InputSnapshot, CaseStudyFacts, ComparisonPolicy.

**Outputs:** LookalikeMatch, ComparisonReport.

**Ownership invariant:** Similarity and a publisher-reported result do not prove a prospect outcome or transferable causality.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### RE-05 — Signals and adjudication

**Submodules:** condition functions, confounds, explicit negative/unknown/error reasons, verification requests.

**Inputs:** InputSnapshot, ClaimResolution, ContextAssessment, SignalDefinition.

**Outputs:** SignalEvaluation, SignalDecision, AdjudicationReport, VerificationRequest.

**Ownership invariant:** Business truth and operational permission stay separate; context or score cannot promote weak evidence.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### COM-01 — Opportunity and playbook selection

**Submodules:** service-line mapping, audience/offer fit, priority, template eligibility, playbooks.

**Inputs:** SignalEvaluation, ContextAssessment, ComparisonReport, OfferPolicy.

**Outputs:** OpportunitySelection.

**Ownership invariant:** Ranking selects eligible opportunities but cannot strengthen evidence or infer company pain.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### QA-01 — Evaluation, experiments and promotion assessment

**Submodules:** gold-set evaluation, detector and semantic extraction quality, template review quality, measured source costs and coverage, campaign holdouts and assignment, drift checks, promotion/demotion proposals.

**Inputs:** ExperimentDefinition, FixtureReport, CalibrationRecord, OutcomeReport, ExecutionRecord, RuleReleaseProposal.

**Outputs:** ExperimentAssignment, QualityAssessment, PromotionProposal, ExperimentDefinition.

**Ownership invariant:** Performance does not upgrade evidence authority. Reviewable proposals change later releases; observational response differences are not causal uplift.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

## S5 Audience and reviewed content

### AUD-01 — Contacts, role evidence and audience selection

**Submodules:** person-account relationship evidence, approved endpoint enrichment, email/phone verification status, persona selection, recipient scope and source rights, endpoint alias and role changes.

**Inputs:** Subject, SubjectBinding, OpportunitySelection, SourceRecord, DataAccessPolicy, CurrentRestrictionSnapshot.

**Outputs:** ContactProfile, ContactAssessment.

**Ownership invariant:** Contactability, current employer/role, intended audience fit, and permission are independent checks; guessed identities and model-generated emails cannot become send-ready.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

### COM-02 — Grounded clauses and packages

**Submodules:** approved renderers, whole-clause checks, quote context, assumption-labeled scenarios, package revisions.

**Inputs:** OpportunitySelection, InputSnapshot, TemplateDefinition, ClaimResolution.

**Outputs:** GroundedClause, OutreachPackage, PackageValidationReport, MessageArtifact.

**Ownership invariant:** Only eligible account proof supports account assertions; neutral templates do not require a maturity claim.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### COM-03 — Authorized review

**Submodules:** evidence viewer, revision comparison, reviewer permissions, approval/rejection.

**Inputs:** OutreachPackage, PackageValidationReport, TrustedPrincipal.

**Outputs:** ReviewDecision.

**Ownership invariant:** Review binds exact revision and content hash and cannot override hard policy/identity/evidence failure.

**Replay policy:** HISTORICAL_READ_ONLY_NEW_REVIEW_IS_NEW_ACTION. **Effects:** AUTHORIZED_REVIEW_WRITE.

### COM-04 — Current-use gate and controlled export

**Submodules:** freshness/rights/restrictions, purpose/destination, mapping, local/CRM export, receipts.

**Inputs:** OutreachPackage, ReviewDecision, DestinationDefinition, CurrentRestrictionSnapshot, DeliveryIntent, CampaignApproval, CampaignReadiness, ContactAssessment.

**Outputs:** UseGateDecision, ExportReceipt, SendGateDecision.

**Ownership invariant:** Gate uses current trusted state; exact revision/payload/destination and business-effect identity are preserved across retries.

**Replay policy:** NEVER_EXPORT_DURING_REPLAY. **Effects:** LOCAL_OR_REMOTE_EXPORT.

## S6 Engagement and sales handoff

### CAM-01 — Campaign and sequence policy

**Submodules:** route mappings, ordered step definitions, template eligibility, sender constraints, timezone/calendar policy, frequency and cross-campaign caps, approval and remote-state preflight.

**Inputs:** ProgramDefinition, OfferDefinition, TemplateDefinition, DestinationDefinition, SenderCapabilitySnapshot.

**Outputs:** CampaignDefinition, CampaignApproval, CampaignReadiness.

**Ownership invariant:** A reviewed account package does not approve a campaign or activate sending. Each campaign selects exactly one scheduling authority.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

### CAM-02 — Enrollment, scheduling and stop control

**Submodules:** contact/account enrollment deduplication, cross-program fatigue and exclusivity, durable next-step eligibility, holds and cancellation, reply-driven stops, out-of-order event handling, provider-managed schedule reconciliation.

**Inputs:** CampaignDefinition, CampaignApproval, CampaignReadiness, ContactAssessment, ReviewDecision, CRMAccountView, UseRestriction, EnrollmentControl, DeliveryAttempt, ReplyAssessment.

**Outputs:** Enrollment, StepEligibility, DeliveryIntent.

**Ownership invariant:** Only this module owns logical step progression. New runs, edited copy, or CRM retry cannot create another business send.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

### COM-05 — Delivery and reconciliation

**Submodules:** recipient resolution, send permissions, outbox, provider dispatch, unknown acceptance, unsubscribe.

**Inputs:** DeliveryIntent, UseGateDecision, OutreachPackage, TrustedRecipientBinding, SendGateDecision, MessageArtifact, StepEligibility.

**Outputs:** DeliveryAttempt, Exposure, ReconciliationRecord, SenderCapabilitySnapshot.

**Ownership invariant:** No blind retry after uncertain acceptance; existing no-send profiles cannot reach a sender.

**Replay policy:** SIMULATION_OR_RECORDED_RECEIPTS_ONLY. **Effects:** EXPLICITLY_AUTHORIZED_SEND.

### COM-06 — Outcomes and descriptive performance

**Submodules:** webhook verification, event deduplication, exposure joins, mature windows, measurement.

**Inputs:** OutcomeEvent, Exposure, AttributionPolicy, MeasurementWindow, CRMSyncReceipt.

**Outputs:** AttributedOutcome, MeasurementFactDraft, OutcomeReport.

**Ownership invariant:** Unmatched events are quarantined; reply denominators exclude immature/uncertain cases by declared policy; results remain non-causal.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.

### ENG-01 — Conversations, replies and response handling

**Submodules:** verified inbound routing, immediate safety stop path, reply thread and exposure linkage, bounded intent classification, out-of-office handling, human response drafts, referrals and new contact admission, meeting/sales handoff.

**Inputs:** OutcomeEvent, Exposure, ContactProfile, Enrollment, Artifact, TypedModelResult.

**Outputs:** Conversation, ReplyAssessment, EnrollmentControl, SalesHandoff, FollowUpTask, AuthorizedChangeRequest.

**Ownership invariant:** Stop on a credible received reply before optional model classification. Authenticated opt-out signals request immediate restrictions through governance; uncertain classification cannot resume a stopped sequence.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

### CRM-01 — CRM synchronization and sales handoff

**Submodules:** provider identity mapping, field ownership and schema mappings, existing account/deal exclusions, upsert and receipt reconciliation, sales tasks and meeting handoff, deal-stage and outcome ingestion, sync-loop prevention.

**Inputs:** CRMMapping, SalesHandoff, ExportReceipt, Conversation, OutcomeEvent, AuthorizedContext.

**Outputs:** CRMAccountView, CRMSyncIntent, CRMSyncReceipt, OutcomeEvent, CRMMapping.

**Ownership invariant:** CRM-sync retries cannot invoke delivery. Prospecting opportunity selection and a CRM sales deal are different records. A blank external field cannot release a restriction.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

## S7 Operator workspace

### UX-01 — Product workspace and operator workflows

**Submodules:** program and source setup, account evidence and research browser, contact and candidate review, package and campaign review, inbox and sales queues, CRM and delivery health, audit permissions and diagnostic navigation.

**Inputs:** KnowledgeView, RunReport, ExecutionTimeline, OpportunitySelection, OutreachPackage, ContactProfile, Enrollment, Conversation, CRMSyncReceipt, TrustedPrincipal.

**Outputs:** WorkspaceView, ModuleRequest.

**Ownership invariant:** The UI invokes authorized module operations; it never directly edits canonical facts, restrictions, campaign state, or send receipts.

**Replay policy:** READ_ONLY_OR_SIMULATION; NO_EXTERNAL_EFFECTS. **Effects:** OPERATION_SPECIFIC_AUTHORIZATION_REQUIRED.

### PLAT-03 — Diagnostics and operator interface

**Submodules:** execution index, structured logs, why/why-not, trace/diff, offline replay UI, safe debug bundles, metrics.

**Inputs:** ModuleRequest, ModuleResult, RecordRef, Diagnostic.

**Outputs:** ExecutionTimeline, ExplanationReport, DebugBundle, RunReport.

**Ownership invariant:** Trace is not evidence or authority; audit manifests are retained under policy even if routine telemetry is sampled.

**Replay policy:** PURE_OR_STORED_INPUTS. **Effects:** NONE.
