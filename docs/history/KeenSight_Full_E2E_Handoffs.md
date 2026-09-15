# Full E2E handoffs and contract standards

Status: proposed operations, not a new runtime release. The previous common protocol wraps each operation. This table names payload families and required semantic checks; exact JSON schemas/signatures are still required for new contracts.

| Transition | Producer / consumer | Typed payloads | Required check and failure disposition |
|---|---|---|---|
| Program → discovery | GTM-01 → GTM-02 | ProgramDefinition, AudienceDefinition, OfferDefinition | Versions, approved sources, purposes and bounded spend. Invalid config rejects before requests. |
| Source/import → provisional target | ING-01/GTM-02 → KN-01 | AccountSeed, original SourceRecord/Artifact refs | Resolve accepted account/resource relationships; quarantine ambiguity without guessing ownership. |
| Selection → capture plan | GTM-02 → CTL-02/ING-02 | LeadSelection, ResearchPlan, IntakeRequest | Preserve reasons, missing knowledge, exclusions and exact existing-input refs. |
| Plan → acquisition | ING-02/CTL-03 → ING-03 | ScanPlan, AcquisitionSpec, AuthorizedContext, BudgetReservation | Permissions and limits before attempt; no-byte failure is a legitimate AcquisitionAttempt. |
| Capture → extraction | ING-03 → ING-04 | Capture, Artifact, CaptureCapabilities | Resolve retained bytes and per-surface completeness; failed extraction cannot manufacture absence. |
| Extraction → matching → observations | ING-04 → FP-01 → FP-02 | Surface/PageEvidence, Match, SupportLink, Observation, ScanBundle | Preserve all supports; deduplicate observations not evidence; no confidence inflation. |
| Raw/derived proposal → canonical knowledge | FP-02/ING-01/AI-01/RE-* → KN-02 | Observation or typed draft, evidence, bindings and producing ExecutionRecord | Registered predicate semantics, successful producers, tenant/subject/rights, complete lineage. Reject/quarantine incompatible records. |
| Fact groups → decision snapshot | KN-02 → KN-03 → KN-04 | Fact, ClaimResolution, InputSnapshot | Resolve the complete group; pin selected and rejected/conflicting evidence, bindings and releases. |
| Research → account context | RE-02/KN-02/KN-03 → RE-03 | ResearchSample, admitted prior, resolved account link, ContextJoinRule | All support/denominator/exclusion inputs remain eligible; no account-pain laundering. |
| Evidence/context → opportunity | KN-04/RE-* → RE-05/COM-01 | InputSnapshot, SignalEvaluation, ContextAssessment, OpportunitySelection | Separate condition truth, uncertainty, commercial priority and permission. |
| Account opportunity → audience | COM-01 → AUD-01 | OpportunitySelection, person/account bindings, endpoint evidence, ContactAssessment | Independently assess role, current employer, endpoint and allowed purpose. Unknown does not mean contact-ready. |
| Opportunity/audience → reviewed content | COM-01/AUD-01 → COM-02/COM-03 | GroundedClause, OutreachPackage, MessageArtifact, ReviewDecision | Exact visible content/revision/hash; approved template requirements; review does not authorize campaign activation. |
| Campaign/contact/package → enrollment | CAM-01/AUD-01/COM-03 → CAM-02 | CampaignDefinition/Approval/Readiness, ContactAssessment, package review, CRMAccountView | One schedule owner, correct route, cross-campaign dedup/caps, current exclusion and restrictions. |
| Due enrollment → external effect | CAM-02 → COM-04 → COM-05 | StepEligibility, DeliveryIntent, SendGateDecision, DeliveryAttempt/Exposure | Fresh current-use check, stable logical effect identity, reviewed bytes, uncertain acceptance reconciliation. |
| Inbound event → stop and conversation | COM-06 → ENG-01/PLAT-02/CAM-02 | OutcomeEvent/raw verified event, Conversation, AuthorizedChangeRequest, EnrollmentControl | Verify provider/account, dedup, apply safety controls before optional model classification; no guessed exposure. |
| Conversation → sales | ENG-01 → CRM-01 | SalesHandoff, FollowUpTask, CRMSyncIntent/Receipt | Exact human owner, source evidence, field authority and idempotency. CRM retry cannot send. |
| CRM/provider state → measurements | CRM-01/COM-05 → COM-06 | versioned CRM reports, Exposure, OutcomeEvent, MeasurementFactDraft | Outcome attribution, maturity, exclusions and denominator; reply does not prove meeting or win. |
| Quality → next release | FP-03/COM-06 → QA-01/PLAT-02/CTL-01 | QualityAssessment, PromotionProposal, review, new ReleaseLock | Authorized promotion based on evidence; no change to in-flight definitions. |
| Correction/revocation → current use | PLAT-02 → KN-03/KN-04/COM-04/CAM-02 | authorized ChangeRecord/restriction, affected refs, control action | Recompute or hold dependent current results; cancel future sends; historical evidence remains truthfully labeled. |

## Standard invocation rules

1. Resolve a registered module and operation against an exact ReleaseLock. Arbitrary import paths are not a plugin protocol.
2. Validate ModuleRequest and each operation-specific typed input, including cardinality, versions, tenant scope and immutable bytes.
3. Derive trusted context independently of user-supplied values. Record approved purpose and budget.
4. Read only pinned or explicitly declared same-run inputs for evaluation. Current-use operations instead inspect current trusted state and record its versions.
5. Commit valid outputs and mandatory provenance before emitting SUCCEEDED. Diagnostic artifacts have their own references.
6. Return ModuleResult with request/execution identity, actual consumed refs, outputs, timings, usage and stable reasons. Business NO_MATCH/UNKNOWN/CONFLICT/BLOCK is not the same field as execution failure.
7. Index product correlation through typed refs: program → account → opportunity/contact → package → enrollment/step → effect/exposure → conversation → CRM receipt. Do not use a trace ID as business identity.
8. Apply idempotency to the logical operation and, separately, to the external business effect. Offline replay never invokes effects.

## Core identity rules

| Identity | Stable purpose |
|---|---|
| tenant_id | Isolation and trusted ownership; not inferred from external content |
| program_id + revision | Which targeting/offer policy is being executed |
| account/person/location/product subject IDs | Canonical identity under KN-01, independent of campaign/provider aliases |
| run_id + input snapshot + execution_id | What was evaluated and which attempt produced an output |
| observation origin + claim target/scope/window | Prevent duplicate facts and preserve independent records |
| package_id + revision + visible message digest | What was reviewed and can be used |
| campaign_id + revision + schedule_owner | Which approved step policy owns progression |
| enrollment_id + step_id + recipient/channel | Logical step identity and duplicate prevention |
| logical_effect_key + exact payload digest | One intended external action, irrespective of retries/software upgrades |
| provider account + provider event/message identity | External correlation; not necessarily a globally unique bare event ID |
| conversation_id + exposure links | Conversation handling without fabricating causal metric attribution |
| CRM external ID + mapping/version + sync intent | Idempotent bidirectional updates and loop prevention |

## State and idempotency consequences

A new research run does not authorize a new enrollment. A new detector match does not create a second independent observation. A retry does not extend capture time. An accepted send does not imply delivered inbox. An opt-out has no ordinary fact TTL that reactivates sending. A CRM task retry cannot resubmit a message. A changed payload under an existing effect key is a conflict. A new package revision is not automatically approved. A held recipient can still have valid account knowledge.
