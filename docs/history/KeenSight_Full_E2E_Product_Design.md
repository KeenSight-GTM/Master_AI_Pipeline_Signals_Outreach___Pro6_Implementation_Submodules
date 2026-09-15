# KeenSight — full end-to-end product architecture

**Status: proposed product-design continuation, not an implemented runtime release.** The previous module protocol remains the shared technical interface. This document extends the product lifecycle around it: programs, lead discovery, audience and contacts, campaigns, enrollment, replies, sales/CRM, outcomes, quality and operator workflows.

## 1. What “end to end” means

The system should turn a business program into evidence-backed account knowledge, supported commercial opportunities, appropriate contacts, reviewed messages, controlled campaign execution, handled replies, CRM handoffs, and measurable outcomes. It should also finish useful knowledge-only and research-only workflows without sending anything.

The full lifecycle is:

```text
Business objective and offer definitions
  → versioned audience / ICP
  → account discovery and initial selection
  → bounded acquisition and technical fingerprinting
  → attributable facts, history and resolved claims
  → enrichment, research context, comparisons and signals
  → service-line opportunity selection
  → contact / role / endpoint assessment
  → reviewed message packages and campaign policy
  → enrollment and durable step eligibility
  → fresh permission check and controlled dispatch
  → verified inbound events and immediate stop handling
  → conversations, human tasks, meetings and sales handoff
  → CRM lifecycle and attributable outcomes
  → evaluation and explicitly approved later releases
```

Facts remain broader than active campaigns or enabled signals. Rejecting an account for this audience does not delete its permitted evidence. A missing recipient does not prevent an account-intelligence result. A negative or unknown signal does not make a knowledge run fail. Research similarity does not establish target-account truth.

The product stops at lead intelligence, controlled outreach, conversations and sales handoff/outcome tracking. Delivering a client's consulting or software project is outside this system. A sales team's confirmed lifecycle updates can return as evidence-backed outcomes without pretending the system delivered the work.

## 2. Source basis and what is new

The retained basis is the supplied v4.1 architecture and 75-schema bundle; the collector 0.1.0 README/deduplication design; the Scrapling-first implementation plan; the 52-item ledger mapping; and the previous module-contract package. `BASELINE_SOURCES.json` records the input hashes. No fresh provider entitlement, pricing, model behavior or remote API capability was assumed or researched here.

The previous module catalog has 30 IDs. All are retained. Nine additional product boundaries are proposed: GTM-01, GTM-02, AUD-01, CAM-01, CAM-02, ENG-01, CRM-01, QA-01 and UX-01. They separate responsibilities previously absent or compressed inside a broad commercial module. They do not imply nine new deployed services.

New records in `PRODUCT_CONTRACTS.md` are field-level design contracts, **not generated or installed JSON Schemas**. The retained common-envelope schemas under `reference/` are unchanged proposal artifacts, not integrated wrappers. `baseline_contract_inspection.json` records relevant actual v4.1 shapes. No current runtime package is modified.

### Actual compatibility boundaries that must not be hidden

- Current `UseGateDecision.purpose` supports PREVIEW_EXPORT and CONTACT_EXPORT. It does not authorize SEND. The proposed SendGateDecision needs its own schema and consumer tests.
- Current ReviewDecision targets one exact OutreachPackage revision/hash. It does not approve a campaign, all future steps, or arbitrary channel rendering.
- Current OutreachPackage contains rendered text and clauses; exact channel subject, body, required footer and permitted transformations need the proposed MessageArtifact boundary.
- Exposure already permits null provider message ID and accepted time. Preserve this for unknown acceptance; do not invent acceptance just to fill a receipt.
- OutcomeEvent already permits an absent exposure reference with QUARANTINED attribution. Unmatched inbound events can be retained without inventing exposure linkage.
- The existing ChangeRecord authorization/replacement issue F remains unclosed. This design does not fix it. Hosted/multi-tenant mutation must remain blocked until authenticated ownership and legal transitions are implemented and tested.
- The last supplied collector report describes a locally tested core, an unverified actual Scrapling SDK roundtrip in that environment and disabled native browser capture. This continuation does not rerun that runtime or change its implementation status.

## 3. Product outputs and independent readiness dimensions

| Product output | What the user receives | What is not required |
|---|---|---|
| Knowledge result | Account/location/product/industry records, attributable facts, history, coverage, failed checks and limitations | A signal, contact or campaign |
| Research-context result | Versioned product/industry samples, priors and explicit account-context links | Company-pain proof or outward use |
| Opportunity result | Supported service-line opportunity with reasons and known/unknown prerequisites | A deliverable contact |
| Reviewed handoff | Exact reviewed message/package and authorized export receipt | Automated sending |
| Managed engagement | Enrolled contact, accountable step progression, send/reconciliation records and conversation | Automatic sales qualification or a won deal |
| Outcome result | Mature, attributable measurements and CRM-reported sales states | Causal uplift claims |

Keep separate readiness axes: knowledge completeness, signal eligibility, contact readiness, package review, campaign readiness, delivery permission and conversation disposition. Do not use one `lead.status = ready` to encode all seven.

A company can be well researched but uncontactable. A contact can be valid but disallowed. A message can be reviewed but stale. A signal can match while the account is held because it is already a customer. These combinations are legitimate states, not exceptions to hide.

## 4. Product areas, owners and submodules

### 4.1 Program and offer design — GTM-01

Inputs: business goals, service-line and offer catalog, audience criteria, enabled capability profile, budgets and current policy. Outputs: ProgramDefinition, AudienceDefinition and OfferDefinition revisions.

Submodules: audience/ICP authoring, geography and segment filters, offer prerequisites, persona rules, exclusion rules, acquisition priorities, program budgets and approval. Cover AI SEO/search visibility, AI-first engineering/integration, strategy, and custom AI work through data-driven offer definitions rather than hardcoded funnels.

These are operating decisions, not facts about prospects. Do not turn “target businesses with scheduling friction” into an assertion that every selected business has that friction. The separate automation-playbook catalog remains an unsupplied content dependency; do not invent its entries.

### 4.2 Account sourcing and research planning — GTM-02, CTL-02, KN-01

Inputs: ProgramDefinition, AudienceDefinition, permitted source results/imports, CRMAccountView, existing knowledge. Outputs: AccountSeed, identity/binding requests, LeadSelection, ResearchPlan and IntakeRequest.

Submodules: CSV/manual/Harvest input adapters, discovery-query plans, namespaced origin records, provisional identity, deduplication, fit/exclusion checks, coverage gaps and bounded acquisition priorities. A provider acquisition still goes through ING-01 and CTL-03 rather than becoming a private shortcut in this module.

KN-01 owns actual canonical identity. GTM-02 does not merge companies merely because they share a name, agency, tracking account or domain redirect. A group, franchise system, location and franchisee may be different subjects. Selection records must explain inclusion, rejection, deferment or refresh-required status.

Historical knowledge can inform selection. Current operational exclusion—customer, open opportunity, restriction—must be refreshed or held when too stale for the intended use. A blocked selection is a business decision, not a failed network call.

### 4.3 Acquisition and fingerprints — ING-01 through ING-05, FP-01 through FP-03, AI-01

This remains the first implementation priority. Scrapling handles bounded static/browser capture, discovery, all 38 command identities and 17 surface extraction functions. Other approved adapters handle APIs, licensed imports, registries and permissioned records. The current browser implementation boundary is unchanged.

The broad source suites remain: hiring/ATS; SaaS and vertical software; product/local/app reviews; forums/communities; traffic estimates; search/ads/backlinks/business data; vertical and corporate registries; public/authorized phone operations; workflow/document analysis; publications/events/engineering/filings; and vendor case studies. Source permission, retention and attribution are adapter-specific. No stage silently treats “capture enabled” as “commercial use enabled.”

Preserve all matches, their element/byte/response locators and their release IDs. Deduplicate capture observations, not proof. One approved product footprint can have many supporting matches; overlapping detectors do not add probability or independent corroboration. Unknown fingerprints enter bounded candidate research and explicit review. A new rule release affects a later run or a separately identified replay, never an in-flight scan.

Acquisition and detection completeness are distinct. Capture failure can produce an AcquisitionAttempt with zero artifacts. A stopped pagination walk or a parser error does not establish business absence. Replay uses retained compatible modalities and original capture time, with no new network/model calls or outbound actions.

### 4.4 Identity, facts and claim resolution — KN-01 through KN-04

Inputs: collector ScanBundle, source records, model extraction results, accepted bindings and producing executions. Outputs: admitted Fact/EvidenceSet/ExecutionRecord, ClaimResolution, KnowledgeView and a sealed InputSnapshot.

KN-02 is the single semantic writer for canonical facts, including derived calculations, reply statements and CRM-origin reports. PLAT-01 provides physical transactions and storage; it does not decide a fact's meaning. Failed, unbound, unsupported, unauthorized or unregistered proposals are quarantined or explicitly unknown rather than silently accepted.

Keep observations, first-party statements, third-party reports, provider estimates, registry records, inferences and derived measurements distinguishable. Preserve target/cardinality, reporting period, method, geography/device dimensions and original time. The canonical claim resolver considers complete pinned groups and cannot choose one favorable row while ignoring conflict.

A contact role can be admitted as an evidence-backed relationship. A model's inferred persona is not an observed job title. A respondent's statement about a problem is attributable evidence, not automatically an independently measured incident rate.

### 4.5 Research context, comparison and business reasoning — RE-01 through RE-05

RE-01 owns deterministic selectors/calculations and history/cohort operations when enabled. RE-02 owns sample selection, support policies, denominators, exclusions and priors. RE-03 owns explicit account-to-product/industry context joins. RE-04 owns case-study and lookalike comparison. RE-05 owns conditions, confounds and adjudication.

Derived outputs return through admission before consumers use them. A declared execution plan orders concrete executions; repeated use of the admission function is not a graph self-cycle. An actual derivation depending on its own same-run output is invalid.

Research priors retain their source subject. A company with Calendly and a product-level reporting complaint prior has potentially relevant research context—not a confirmed reporting problem. LookalikeMatch retains features, comparison sources, differences and version; similarity cannot transfer a case-study outcome to the target. Numeric marketing claims are not automatically credible or causal.

Inputs are pinned and all denominator-dependent evidence matters. A new source observation, correction, deleted denominator, rule release or permitted authority change can make current use invalid. For the first batch system, conservative account reruns and current-use checks are sufficient; no general incremental scheduler is required.

### 4.6 Opportunity and audience — COM-01, AUD-01

COM-01 selects service-line opportunities from eligible conditions, explicit context and offer policy. An internal opportunity is not a CRM sales deal. Priority expresses commercial preference; it does not change evidence truth or source authority.

AUD-01 obtains and assesses contacts through approved connectors and KN-01 identity. Submodules: person-account role evidence, business endpoint discovery, verification status and dates, catch-all/unknown results, source rights, persona fit, recipient restrictions and alternate-contact review.

Keep four questions separate: is this a real bound person/role, is the endpoint usable, is the person an appropriate audience for the offer, and is the intended contact permitted? A verified email does not answer all four. Guessed or model-invented emails must not become send-ready.

Contact acquisition can be deferred until an account has an eligible opportunity to reduce cost, but an account-level report does not require contact completion. Contact changes or stale employment evidence can hold an enrollment. A referral creates a new contact candidate and new checks, not automatic enrollment of everyone named in a reply.

### 4.7 Content and approval — COM-02, COM-03

Inputs: OpportunitySelection, compatible templates, exact account evidence, claim resolutions and optionally assessed contact/audience. Outputs: GroundedClause, OutreachPackage, proposed channel-specific MessageArtifact and ReviewDecision.

Submodules: deterministic evidence-bound renderers, quote attribution/context, neutral questions, optional assumption-labeled scenarios, report/scorecard artifacts, channel rendering, whole-message validation and exact-revision review. Arbitrary LLM text stays draft-only unless the required approval/validation exists.

Review must cover all factual content, including subject line, fixed wording, follow-up references and any channel transformation. Footer and tracking changes must be declared and checked; a provider cannot be assumed to preserve approved bytes. Every sequence step has its own reviewed message or an explicitly approved deterministic rendering contract. Blanket approval of future arbitrary text is not supported.

Unknown automation maturity blocks maturity-specific claims, not every neutral observation-led question. Public scores measure public posture, not private organizational readiness. Cost scenarios distinguish assumed numbers from authorized measurements. The current three narrow preview renderers do not imply these broader renderers already exist.

### 4.8 Campaign policy and enrollment — CAM-01, CAM-02

CAM-01 owns campaign/route/sequence definitions and separate authorized CampaignApproval. Submodules: stable route identity, allowed audience/offer/template combinations, step order, delay semantics, timezone/calendar basis, sender/channel constraints, budget/frequency policy, stop conditions and readiness preflight.

CAM-02 owns Enrollment and step progression. Submodules: duplicate enrollment prevention, account and endpoint alias checks, cross-campaign fatigue limits, durable due times, expected-revision state transitions, holds, cancellation, reply-driven stops and reconciliation with a provider-managed schedule if that mode is used.

Creation, draft preparation, append-to-existing enrollment, campaign activation and sending are separate actions and permissions. Retain that separation when adapting the project's existing campaign behaviors; this design is not an assertion about a current remote provider configuration.

Exactly one component owns scheduling. The recommended initial mode is LOCAL: CAM-02 selects due steps and the provider only dispatches authorized messages. A PROVIDER-managed sequence is a separate adapter mode with verified pause/cancel/receipt semantics. Never leave both local and remote schedulers advancing the same enrollment. When a provider cannot support required stop behavior, do not enable that autonomous mode.

Scheduling is a bounded durable timer/queue, not the general knowledge-computation scheduler. It is necessary only when sequences are enabled. All delays and windows retain timezone basis; do not infer prospect locality from an unverified phone number or domain.

### 4.9 Current-use permission, handoff and dispatch — COM-04, COM-05

COM-04 owns current-use export checks and the proposed SendGateDecision. COM-05 owns sender capability/state observations, provider adapters, prepared effect identity, dispatch, receipts, retry classification and reconciliation.

An export gate is not send permission. Sending requires the exact recipient binding, reviewed MessageArtifact, campaign approval, fresh contact assessment, sender readiness, enrollment state, frequency reservation and current restriction/evidence vectors. A package's existence or a previous ALLOW decision is insufficient.

Use a stable logical business-effect key based on the authorized enrollment step/channel/recipient identity; retry or software version changes do not create a new intent. The exact payload digest is bound separately. Different payload under an existing effect key is a conflict, not a new send. Replacing a message before dispatch requires a new approved revision and a deliberate supersession decision; it must not accidentally authorize a second exposure.

Prepare the intent internally, recheck current state immediately before dispatch, serialize relevant local restriction/enrollment revisions against dispatch admission, then reconcile the external result. A remote effect and local transaction are not one atomic transaction. An opt-out that arrives after external acceptance cannot unsend the accepted message; cancel remaining work and record the race accurately.

A timeout after possible acceptance has acceptance UNKNOWN. Query or reconcile the existing effect before retry. Provider acceptance is not inbox delivery. CRM-sync or local-finalization failure cannot cause another message. A provider without reliable correlation/cancellation/idempotency must use a constrained adapter mode or remain disabled.

### 4.10 Replies, conversations and sales handoff — COM-06 ingress, ENG-01, CRM-01

COM-06 ingress verifies provider source/signature or authenticated mailbox origin, deduplicates the event using provider account and event identity, retains permitted content, and routes it. The event can remain unmatched/quarantined; do not invent exposure attribution.

ENG-01 owns the conversation interpretation workflow and requests enrollment controls. The immediate control path runs **before optional LLM classification or mature-outcome analytics**. Default proposal: a credible reply from an enrolled contact pauses the applicable automated sequence. An explicit verified opt-out requests an immediate durable restriction through PLAT-02 and cancellation/hold through CAM-02. Scope follows the actual request and applicable policy; do not silently unsubscribe an entire company from one ambiguous statement.

Then classification may distinguish interest, questions, objection, out-of-office, wrong person, referral, unsubscribe and ambiguity. Keep model interpretation and literal supporting statements separate. Out-of-office does not create automatic blanket reactivation; apply the declared policy or require human review. Negative/ambiguous replies cannot be turned into new automated follow-ups by changing confidence thresholds.

Outputs include Conversation, ReplyAssessment, FollowUpTask and SalesHandoff. A referral reenters contact admission. A suggested meeting is not a booked meeting. Calendar changes, human-response sending and sales-task creation each require the relevant action permission and receipt. Default human-review handling is useful before autonomous reply generation exists.

### 4.11 CRM synchronization and sales lifecycle — CRM-01

Submodules: external record links, field-level ownership, imported owner/customer/open-deal status, contact/account/task upserts, handoff assignment, meeting/deal updates, webhook/change ingestion, cursor/version tracking, idempotency and loop prevention.

Do not build a second CRM. Store the minimum typed CRMAccountView and link maps necessary for selection, exclusions and traceability. Proposal: CRM is authoritative for sales owner, human sales stage and customer/open-deal state; KeenSight is authoritative for evidence, research, its enrollments and send receipts. Restrictions use conservative merging: an external restriction may add a block, but a missing/blank field cannot release a local opt-out. Explicit authorized release is required.

CRMMapping specifies ownership or a reviewed conflict policy per field. External field changes are reports with provider revision and collection time. A stale critical exclusion produces refresh/hold at the gate, not an assumed clear state. Deduplicate tasks/deals by explicit handoff identity. Loop prevention retains originating system and version; avoid blind echo updates.

A positive reply may create a task or qualified sales handoff. The sales team may later report meeting booked, won/lost, value and reason. Keep reported financial outcomes attributable and restricted; never infer won revenue from opens, interest or a provisional meeting.

### 4.12 Measurement, quality and operator workspace — COM-06, QA-01, UX-01

COM-06 owns attributable outcome measurement: exposure identity, event deduplication, unmatched events, maturity windows, bounce/unknown treatment, selection windows and cross-campaign contamination. Derived metrics pass through KN-02. Technical request success, business opportunity yield and outreach response rate are separate measurements with explicit denominators.

QA-01 evaluates fingerprints, extraction, identity, signal correctness, package safety, source costs/coverage and campaign experiments. Proposed ExperimentDefinition pins eligible units, observational/randomized design, treatment versions, assignment, outcome/maturity and stopping rules. Do not imply causal effectiveness from ordinary response differences. Performance cannot promote candidate evidence; it can propose future reviewable changes.

FP-03 builds rule candidates; QA-01 assesses them; PLAT-02 authorizes the change; CTL-01 compiles a new immutable release. Counterexamples remain part of the gold set. Nothing changes an in-flight run's approved definitions.

UX-01 exposes a program console, evidence browser, account knowledge view, candidate review, contact workbench, package/campaign review, inbox, sales queue and integration status. PLAT-03 supplies timeline/why/replay/diff data. UI actions invoke the owning module under authenticated context; no UI or integration can write around admission, restriction or send checks.

## 5. Standardized public interfaces

Retain `ModuleRequest → ModuleResult` for every public operation. Reuse the existing proposed fields and RecordRef shape; domain records remain typed and versioned. Internal helper functions do not need envelopes. No microservice/RPC deployment is required.

A registered operation signature must declare exact input types and cardinalities, accepted schema versions, preconditions, optional/diagnostic inputs, effects, output types and status semantics. The module inventory lists families across operations; it is not an executable signature.

### Common correlation

Keep tenant, release lock, run, target, request, execution attempt and trace/span identity in the common envelope. Product correlation—program, account evaluation, opportunity, contact, package revision, campaign, enrollment, step, logical effect, conversation and CRM link—comes from typed referenced records. Do not add dozens of nullable top-level envelope fields to every parser call.

The execution recorder builds a searchable correlation index from those validated references. A reply may arrive weeks after a scan: connect traces by record and causal links, not one never-ending trace. A new acquisition/evaluation run must not create a new enrollment or business-send identity by itself.

### Contract kinds

| Kind | Examples | What it can establish |
|---|---|---|
| Evidence | Artifact, EvidenceLocator, ModelCall raw response | What was captured or returned, subject to provenance and permissions |
| Knowledge | Fact, ClaimResolution, derived measurement | A typed observation or supported interpretation with declared nature |
| Intelligence | ContextAssessment, SignalEvaluation, OpportunitySelection, LookalikeMatch | A decision or comparison with bounded eligibility; not automatic outward proof |
| Operational state | ContactAssessment, Enrollment, ReviewDecision, restriction, gate | What an authorized workflow currently permits or requires |
| External-effect accounting | DeliveryIntent/Attempt, Exposure, ExportReceipt, CRMSyncReceipt | What was requested, accepted, uncertain, confirmed or reconciled |
| Diagnostics | ModuleResult, reason, trace, manifest | Why software did what it did; not business evidence merely because it is logged |

Keep domain status and execution status separate. Finding a conflict, an ineligible contact, a blocked gate or no opportunity may be a successful computation. A failed parser cannot publish eligible positive records. Unknown send acceptance is not a clean no-effect failure.

### No silent coercion

Wrong schema version, wrong tenant, unknown implementation, incomplete input closure or changed immutable bytes fail closed. API/LLM dictionaries and exception strings are not public contracts. An importer preserves original records and adds a conversion/admission receipt. It must not invent historical tracing, subject ownership or provider authority.

Current v4.1 SignalEvaluation enums remain unchanged in this design. A future richer SignalDecision requires an explicit schema and adapter; UNRESOLVED cannot silently mean NO_MATCH. Similarly, the new SendGateDecision is not squeezed into the export-only purpose enum.

## 6. End-to-end ownership and storage

Retain five active repositories: `.github`, `knowledge-contracts`, `fingerprint-library`, `scrapling-ingestion`, `signals-platform`, plus pinned reference forks of the older applications. New GTM/contact/campaign/conversation/CRM/QA/UI modules initially live in signals-platform. The collector never imports the commercial app.

One initial relational backend can hold logically separate groups:

1. Definitions and release manifests.
2. Subjects, facts, lineage, samples and rebuildable search projections.
3. Acquisition attempts, runs, executions and exact input/output manifests.
4. Programs, opportunities, contacts, packages, campaigns and enrollments.
5. Restrictions, reviews, gates, effect intents and provider receipts.
6. Conversations, CRM links, tasks and outcome events/measurements.

Evidence bytes use the content-store interface under permitted retention. A vector index, if enabled, is a rebuildable projection of a versioned eligible corpus; it is not canonical fact storage. A technical fingerprint research index similarly does not become a second fact database.

| Authoritative state | Owner |
|---|---|
| Subject identity and accepted relationships | KN-01 |
| Canonical fact/evidence admission | KN-02 |
| Claim resolutions | KN-03 |
| Program and offer definitions | GTM-01 |
| Contact operational assessment | AUD-01, using KN identity and admitted proof |
| Packages and exact channel artifacts | COM-02 |
| Package review | COM-03 |
| Campaign policy and campaign approval | CAM-01 |
| Enrollment progression and next-step eligibility | CAM-02 |
| Restrictions and authorized corrections | PLAT-02 |
| Current-use/send gate | COM-04 |
| Dispatch attempts and exposures | COM-05 |
| Verified events and measured outcomes | COM-06 |
| Conversation workflow and handoff requests | ENG-01 |
| CRM links, synchronization receipts and imported CRM view | CRM-01 |

Other modules issue commands to the owner. Physical record storage is shared infrastructure, not an exception to this rule. Safety stop requests can be processed in one local transaction spanning the appropriate repositories under explicit domain handlers; routine analytics and CRM delivery may follow later.

## 7. Operational state machines

The following new states are **proposed contract semantics**, not installed enum changes.

### Contact assessment

Contact readiness should be a tuple of identity, role/employer binding, endpoint verification, permitted use and restriction state. A derived READY/HOLD/REJECT decision retains all component reasons and check times. Unknown endpoint verification is not assumed valid. Freshness policies differ by component and source.

### Enrollment

```text
PROPOSED → ELIGIBLE → ENROLLED → ACTIVE
                                  ├→ PAUSED
                                  ├→ COMPLETED
                                  ├→ CANCELLED
                                  ├→ STOPPED_REPLY
                                  └→ STOPPED_RESTRICTION
```

Transitions require expected enrollment revision and a causal event/action identity. Repeated stop events are idempotent. Resume requires an explicit authorized transition, current assessments and declared policy. A new model classification or expired ordinary fact TTL cannot remove a stop.

### Dispatch

```text
INTENT_PREPARED → FINAL_GATE_ALLOW → DISPATCH_ATTEMPT
    ├→ accepted, record provider/exposure identity
    ├→ explicitly rejected, record no-acceptance disposition
    └→ acceptance unknown, reconcile the existing intent
```

A failed response is not enough to infer non-acceptance. Cancellation after confirmed provider acceptance cannot undo that exposure. Account for it accurately and cancel remaining steps.

### Conversation

Verified inbound → immediate stop/hold routing → optional classification → human task or reviewed response → meeting/sales handoff → outcome. Source content is evidence; inferred intent is an assessment. Calendar, response sending and CRM writes remain separate external effects.

## 8. Three feedback paths, each with its own permissions

**Evidence feedback:** refresh requests, corrected identities, authoritative client statements and failed-check recovery create new observations/evaluations. A later observation does not rewrite the past.

**Operational feedback:** replies, opt-outs, customer status, bounces and sender state affect current use immediately. These do not wait for an outcome-learning batch. Stale or missed webhooks require reconciliation; an event from the wrong provider account is quarantined.

**Quality feedback:** reviewed fingerprint candidates, gold-set failures, calibrated extraction and measured campaign performance produce proposals for later releases. No automatic score-based increase in truth authority or silent prompt/template replacement occurs.

The lifecycle graph can show loops. The concrete same-run dependency plan remains acyclic and versioned. Discovery recursion is bounded by acquisition policy; campaigns have durable schedules; neither requires a general graph database.

## 9. Debugging the complete product

The operator must be able to start at a CRM deal, reply, send, package, signal, fact or capture and traverse backwards through exact references. The reverse traversal answers which current packages/statistics depend on revoked or corrected evidence.

Required views:

| View | Questions answered |
|---|---|
| Program funnel | How many discovered, resolved, researched, eligible, contact-ready, reviewed, enrolled, accepted, replied and handed off? What was excluded and why? |
| Account timeline | Which captures, facts, bindings, conflicts, priors and opportunities existed at each evaluation? |
| Evidence inspector | What exact bytes/node/response/quote and producer support this assertion? |
| Contact workbench | Which role/endpoint evidence, verification result and restriction determine recipient readiness? |
| Campaign/enrollment timeline | Who schedules, which step is due, why paused, and what already happened? |
| Message review | Which exact content revision was reviewed, rendered and actually handed off? |
| Send reconciliation | Did the provider accept? Which intent and receipt prevent a duplicate? |
| Conversation/sales view | Which inbound event stopped the sequence, who owns the task, and what reached CRM? |
| Release comparison | Did inputs, selector, fingerprint, prompt, policy or template change? |
| Budget and coverage | Which attempts failed or consumed cost? What was not checked? |

Common reason families remain stable; proposed additions include CONTACT.ROLE_UNRESOLVED, CONTACT.ENDPOINT_UNKNOWN, CAMPAIGN.ROUTE_MISMATCH, ENROLLMENT.DUPLICATE, ENROLLMENT.STOPPED_REPLY, MESSAGE.REVISION_CHANGED, SENDER.NOT_READY, EFFECT.ACCEPTANCE_UNKNOWN, CRM.STALE_EXCLUSION and CRM.SYNC_CONFLICT. These are registry additions to implement, not installed codes.

Persist mandatory execution/record manifests and effect receipts. Routine logs should be redacted and sampled independently from that audit trail. Do not put raw email, phone numbers, cookies, credentials or model prompts into metric labels. Authorized debug export can be incomplete after retention/deletion and must say so. A hash does not recreate missing evidence.

Offline replay never sends, scrapes, calls a model, promotes rules, deletes evidence, books meetings or mutates CRM. Reprocessing historical provider events in a simulation must not reissue their external effects.

## 10. Example trace: synthetic account to handled reply

This example specifies expected behavior; it is not an executed live trace.

1. A program targets a permitted SMB segment for a booking-follow-up service. Its audience and offer revisions are recorded.
2. A permitted source yields a provisional account; identity accepts the website-to-account binding. Existing-customer and restriction checks pass under a recorded CRM view.
3. Scrapling captures a page. Two rules match the same booking-script element. Both matches are retained, but they share one capture observation and one evidence point.
4. Admission validates source, binding and producer. Complete-group resolution finds no conflict. The opportunity is an observation-led investigation, not a claim of a disconnected private integration.
5. Product review context exists but is labeled internal. It does not support an assertion about this account's problems.
6. An authorized contact source supplies an appropriately bound operations role and usable endpoint. Contact assessment records separate fit and permission checks.
7. The renderer produces a supported observation and neutral question. The exact message artifact and package revision are reviewed.
8. A campaign route and step sequence have separate approval. Enrollment prevents an overlapping campaign from independently contacting the same endpoint/account contrary to frequency policy.
9. At the due time, the fresh send gate passes. The provider times out after dispatch. Acceptance is UNKNOWN; the worker reconciles rather than sends again.
10. Reconciliation finds the accepted provider message. A later verified reply pauses the sequence before optional intent classification.
11. The reply explicitly reports manual follow-up. That statement may enter fact admission with its correct attribution and rights; a model's “interested” label remains a separate assessment.
12. A sales handoff and task synchronize to CRM. If that write fails, only CRM synchronization retries. No second outreach send occurs.
13. Mature measurement records this attributable reply. It does not infer a won deal or causal uplift. Later human-confirmed CRM outcomes retain their separate evidence.

This chain must be inspectable through record links even though the capture, evaluation, send and reply have different runs and traces.

## 11. Implementation order and completeness criteria

Retain the Scrapling-first sequence. Defining the whole product does not require building every module before testing the collector.

| Milestone | Implemented slice required for exit |
|---|---|
| Capture | Real pinned Scrapling roundtrip; retained bytes, attempts, 38 command ownership and truthful capability coverage; bounded browser before enabling it |
| Fingerprint loop | Complete support preservation, donor import disposition, reviewed candidate release and historical replay |
| Canonical knowledge | Accepted bindings, Fact admission, complete claim resolution, searchable knowledge and authorized corrections; close F before hosted mutation |
| Account intelligence | Program/discovery, source expansion, exact inputs, relevant derivations, research joins, opportunity selection and no-send preview |
| Reviewed audience | Contacts/roles/endpoints, exact message review, campaign definition/approval and operational UI |
| Controlled engagement | Durable enrollment, one schedule owner, fresh send gate, reconciled effects, immediate replies/opt-outs and CRM handoff |
| Outcomes and improvement | Correct attribution/windows, CRM lifecycle ingestion, measured quality, reviewed promotion, backup/restore and scale tests |

Cross-module acceptance scenarios are specified in ACCEPTANCE.md. No acceptance scenario is marked passed merely because a schema or diagram exists. Existing reference-only modules remain disabled until realistic producer/consumer tests and failure paths pass.

## 12. Bottom line

The collector is the acquisition subsystem. The complete product is a governed account-research and engagement system around it: business programs, evidence and knowledge, research/decisions, contacts, reviewed content, campaigns, delivery, conversations, sales handoff and measured improvement.

The shared protocol makes each operation inspectable. Typed handoffs, clear state owners, exact identities and explicit permissions make the **whole lifecycle** understandable and safe to operate. Keep the architecture broad, keep deployment small, and do not confuse a detailed proposed boundary with already integrated software.
