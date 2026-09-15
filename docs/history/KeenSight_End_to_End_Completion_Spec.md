# KeenSight — end-to-end completion specification

**Proposed v4.1 contract delta · September 14, 2026**

This document specifies how to close the end-to-end gaps found in the unchanged v4 archive. It is an additive design specification, **not an implemented or machine-validated v4.1 schema release**. The broad v4 fact catalog, source-domain coverage, metric definitions and product/industry research model are retained. The independent review evidence is in `KeenSight_v4_End_to_End_Audit.md` and its accompanying pack.

## 1. The product boundary

The first complete runtime ends at an auditable, reviewed handoff, not an untracked file of generated messages:

**Import/discover targets → approve capture → retain artifacts → extract and bind facts → resolve claims → evaluate rules and research context → choose an opportunity → compose supported copy → review → recheck current use → export with receipt.**

A second, independently enabled profile adds **dispatch → delivery reconciliation → attributable outcomes → descriptive performance**. It is not a launch dependency for the first profile. Neither profile requires a distributed scheduler or graph database.

Knowledge capture is independently useful: a product, industry or account can finish with facts and a research report but no signal, no message and no recipient. No module may drop admitted facts merely because no enabled business signal consumes them.

### Runtime profiles

| Profile | Finished product | Required gates |
|---|---|---|
| KNOWLEDGE | Searchable, attributable facts, context and a capture/quality report | Approved capture, admission, retention, exact inputs and read authorization |
| REVIEWED_HANDOFF | An approved package plus a destination-specific export receipt | KNOWLEDGE + business-rule decisions, grounded copy, authorized review and current-use gate |
| DELIVERY | Reconciled exposures and attributable outcomes | REVIEWED_HANDOFF + suppression, recipient/provider mapping, idempotent delivery intent and reconciliation |

The existing DESIGN_TEST mode remains distinct. Synthetic approvals cannot be promoted by toggling a Boolean.

## 2. Architecture constraints

Keep one application, a sequential bounded batch runner, one transactional relational database and a content repository. Operations/review can be CLI/API-first; a UI is not required to establish the contract. Existing code can be reused behind interfaces after conformance tests. There is no requirement to migrate old data or make the wire formats backward compatible.

One dependency plan is validated at configuration load. It covers enabled computations and declared selectors, including sample membership and reference data. Execute in stable order. On a material change, re-evaluate the affected target conservatively. Current-use reads block immediately on applicable revocations even before recalculation finishes.

Entity relationships, evidence lineage and computation dependencies remain different concepts. Ordinary relationship cycles are permitted. Causal lineage and same-run computation cycles are not. Product/industry contextual joins remain internal; explicitly authorized membership aggregates are a separate, narrower function capability.

## 3. End-to-end stages and failure behavior

| Stage | Input → output | Owner in the monolith | Required failure behavior |
|---|---|---|---|
| 0. Link capability profile | Versioned definitions → validated execution plan | RegistryLinker | Reject missing entrypoints, invalid parameters, missing producers, unimplemented enabled adapters or cycles before target work begins. |
| 1. Intake and normalize | CSV/API/CRM/Harvest input, resource URI or typed subject ID → IntakeRequest and target decisions | BatchRunner + SubjectResolver | Quarantine invalid/ambiguous targets without inventing a company binding. Namespaced input identity supports retries. |
| 2. Plan acquisition | Target, desired domains, source approval, limits → bounded acquisition plan | AcquisitionService | Record policy denial or budget denial before network access. No fake provider artifact. |
| 3. Capture/import | Planned requests → AcquisitionAttempts, optional Artifacts, coverage evidence | SourceAdapter + ContentRepository | Retain safe diagnostic metadata for timeout/error/denial. Partial pages, cursors and truncated bodies do not become full coverage. |
| 4. Parse and transform | Allowed bytes → normalized text/JSON/DOM and exact locators | ExtractionService | Record unsupported media, parse failure or repair exhaustion. Preserve links to original evidence; do not silently discard failed rows. |
| 5. Bind and admit | Typed candidate + evidence + accepted binding → Fact or CandidateRecord | SubjectResolver + FactAdmission | Wrong subject, unknown type, prohibited purpose or invalid value quarantines the candidate. Broad fact admission is independent of signal enablement. |
| 6. Freeze target inputs | Eligible facts, changes, bindings, samples and registry releases → sealed BatchRun target evaluation | AccountInputSelector / target selector | No moving latest-state reads. Missing inputs become an explicit account result. New evidence belongs to a new input selection. |
| 7. Resolve and compute | Exact observations → ClaimResolutions, completed Executions, ResearchPriors and ContextAssessments | Claim resolver + DerivationRunner + ContextJoiner | Conflict remains unknown for decisions requiring agreement. Failed producers, denominator loss or invalid context are not eligible evidence. |
| 8. Evaluate business conditions | Resolved input views + versioned functions → SignalEvaluations | SignalEngine | MATCH, NO_MATCH, UNKNOWN, ERROR and DISABLED are distinct. Operational suppression is a separate gate. |
| 9. Select opportunity | Eligible signals + service-line configuration → selected opportunity or recorded no-selection | BatchRunner commercial module | Use deterministic reviewed mappings initially. Product/industry priors are labeled context, not account claims. No invented confidence, pain or maturity. |
| 10. Compose and review | Selected supported opportunity → package revision + machine checks + ReviewDecision | TemplateRenderer + PackageValidator | Unsupported text remains DRAFT/WITHHELD. Reviewer cannot override evidence, rights, tenant or suppression hard failures. |
| 11. Current-use handoff | Exact reviewed revision + destination/purpose → UseGateDecision + ExportReceipt | PackageValidator + export adapter | Recheck current restrictions, expiry, retention and attribution. Any content edit invalidates the prior approval. Unknown external acceptance is reconciled. |
| 12. Optional dispatch | Eligible delivery intent → Exposure | Future delivery adapter | Never dispatch a design-test or unreviewed revision. Timeout after possible acceptance becomes UNKNOWN_DELIVERY; no blind resend. |
| 13. Optional outcomes | Provider/CRM events → evidence-backed OutcomeEvents | Future outcome adapter | Authenticate and deduplicate; quarantine unmatched events; unsubscribe/DNC writes a current restriction immediately. |
| 14. Maintenance | Revocations, retractions, changes and retention deadlines → blocked uses, deletion records and reevaluations | RetentionService + repository services | Prevent current reuse, retain only permitted explanations, and test restore/repair. No infinite retention promise. |

## 4. New records: five core operational families, not five new services

All identifiers and references below are tenant-scoped unless they refer to explicitly global, privileged immutable registry definitions. All persisted writes carry authenticated actor/service identity and an idempotency key at the repository boundary. Secrets are references to protected configuration, never raw values in these records.

### 4.1 IntakeRequest

| Field | Type / rule |
|---|---|
| intake_id, tenant_id | Stable scoped identifiers |
| requested_by | Authenticated principal reference |
| profile_ref | Immutable enabled-profile version/hash |
| input_origin | IMPORT, API, CRM, HARVEST or MANUAL; namespaced upstream identity |
| targets | Closed union of known SubjectRef, approved resource URI, or unresolved business descriptor |
| requested_purposes | Explicit collection/research/outreach/export purposes; downstream use is not implied |
| request_hash, idempotency_key | Same key/same payload reuses the record; changed payload fails |
| submitted_at, status | RECEIVED, VALIDATED, PARTIAL or REJECTED |
| target_results | Per-target normalization/binding result and reason; targets remain traceable when unresolved |

A batch may contain accounts, locations, products, industries or relevant public professional subjects. It is not restricted to prospect organization IDs. Discovery should precede accepted identity, not assume it.

### 4.2 AcquisitionAttempt

| Field | Type / rule |
|---|---|
| attempt_id, tenant_id, intake_id | Required scoped references |
| target_ref, source_release, adapter_release | Resolved/provisional target and exact executed source/adapter versions |
| operation_key, request_hash | Logical operation identity; credentials excluded |
| purpose, policy_decision_ref | Approval actually used before access |
| request_parameters | Endpoint-specific closed schema, including measurement/query scope |
| budget_limit, retry_limit, timeout_limit, body_limit | Bounded settings, with recorded measured usage when available |
| started_at, finished_at | Ordered wall-clock instants |
| status | SUCCEEDED, EMPTY_RESULT, PARTIAL, TIMEOUT, FAILED, POLICY_DENIED, BUDGET_DENIED or CANCELLED |
| artifact_ids | Zero or more; zero is valid for pre-capture failure |
| pagination_state, truncation, terminal_reason | Required when applicable; unknown completion is not COMPLETE |
| actual_cost, cost_status | Amount/unit/provider accounting if paid; UNKNOWN is not zero |

A diagnostic attempt never counts as positive or negative business evidence. An UNKNOWN fact may cite the attempt as operational support, or the target report may carry the unknown without creating a fact. OBSERVED facts still need actual evidence; NOT_FOUND still needs completed detection coverage.

### 4.3 ReviewDecision

| Field | Type / rule |
|---|---|
| review_id, tenant_id, reviewer_id | Authenticated reviewer and scoped decision |
| target_ref | Closed typed reference to candidate, binding, registry promotion or package revision |
| target_hash | Exact content reviewed; mutable display labels cannot alter approved wording |
| action | APPROVE, REJECT or REQUEST_CHANGE |
| reason, decided_at, policy_version | Required audit context |
| resolved_support_refs | Exact accepted evidence/claim disposition where relevant |

Candidate/binding review and package approval use distinct allowed action/target rules. Approval cannot elevate invalid evidence or grant a source license. Authorizing an account preview is not consent to send it.

### 4.4 UseGateDecision

| Field | Type / rule |
|---|---|
| gate_id, tenant_id, subject_id | Identity and scope |
| package_ref, content_hash | Exact approved revision, or a typed research-output reference |
| purpose | INTERNAL_VIEW, OUTREACH_REVIEW, EXPORT or SEND |
| destination_ref, recipient_ref | Required only for a destination/contact-specific operation |
| evaluated_at, valid_until | Decision validity; not a guarantee against intervening revocation |
| current_version_vector | Current policy, source authority, binding, restriction and evidence versions used |
| decision, reasons | ALLOW or BLOCK with typed reasons |
| evidence_refs, review_ref | Auditable support and required human review |

A downstream side effect must verify that the decision is still applicable. A content hash alone is not authorization. Historical views use the original pinned context and label themselves historical; actionable current views invoke this gate.

### 4.5 ExportReceipt

| Field | Type / rule |
|---|---|
| export_id, tenant_id, package_ref | Exact scoped revision |
| destination_ref, mapping_version | Internal file, CRM, or approved delivery-preparation destination |
| payload_hash, gate_id | Bytes/fields handed off and current-use authorization |
| idempotency_key, status | PREPARED, CONFIRMED, UNKNOWN or FAILED |
| requested_at, completed_at, external_reference | Ordered operation timestamps and destination identifier if known |
| attribution_rendered, restrictions | Required source attribution and authorized downstream uses |

Persist a prepared intent before an external mutation and record its receipt. For remote systems, reconcile an unknown result before retry. Use channel-appropriate escaping and protect CSV/formula/HTML contexts. Do not export internal product/industry priors as account factual claims.

## 5. Required extensions to existing contracts

| Existing family | Required change |
|---|---|
| Scope / Artifact | Support pre-binding acquisition references. Resource capture is not accepted company attribution. Preserve original versus transformed/synthesized artifact lineage, including all model inputs where relevant. |
| EvidenceSet / CandidateRecord | Add a typed operational-attempt reference for UNKNOWN/diagnostic paths. Candidates can cite an attempt or artifact; they never acquire proof authority from an error record. |
| BatchRun | Separate collection identity from per-target evaluation identity. Add sealed_at, knowledge_cutoff, account/target completion status, exact input closure and result hash. Allow partial overall batches with independently completed targets. |
| ExecutionRecord | Require success before eligible output publication; record failure reason and input selection/plan version. All raw/derived/model inputs and outputs must reconcile. |
| ModelCall / RepairAttempt | An absent provider response is representable on failure. Require validated successful final output before eligible facts. Link repaired final bytes, model task/prompt/config and execution; bound calls/tokens/repairs and record all charged attempts. |
| ClaimResolution | Make resolution a consumed input or require an equivalent recorded conflict disposition. Distinguish reporting channels; do not force agreement among a direct measurement, estimate and third-party report as though they made the same claim. |
| FactRequirement / FunctionDefinition | Declare target/value selectors through typed function parameters, eligible support units, conflict policy, temporal windows and valid absence semantics. Resolve whitelisted entrypoints. No general expression language is required. |
| SignalEvaluation | Separate semantic verdict MATCH/NO_MATCH/UNKNOWN/ERROR/DISABLED from operational eligibility. Retain diagnostic input IDs and reasons. |
| ResearchSample / Prior | Pin numerator, denominator, exclusions, classification completeness, support policy, membership and all origin dependencies. NEGATED and unknown are not default pain support. |
| ContextAssessment | Only ELIGIBLE context can influence a decision. ABSTAINED context may appear in an audit appendix only. Bind the exact run, link, prior and join-rule versions. |
| CoverageRecord | Link completed acquisition attempts and detector executions, actual capture modes, resource/query/pagination completion, and chronological proof. |
| ChangeRecord | Typed target and replacement references; tenant ownership; actor authorization; legal transition; recorded_at/effective_at; distinguish global privileged authority changes from tenant data changes. |
| Template / Package | Explicit opportunity/service-line mapping, machine validation, review reference, exact revision/content hash, output purpose and current-use gate. Observation-led messages do not require maturity. |
| Exposure / OutcomeEvent | Enforce delivery-enabled profile, approved revision, accepted send identity, evidence reference, provider linkage and deduplication; remain disabled otherwise. |

These are versioned wire-contract changes. Do not call them implemented merely by updating a diagram or by retaining old v3 reference kernels. Release linking must validate the revised shapes and their semantic checks together.

## 6. Signal, conflict and commercial semantics

An enabled business rule is an ordinary versioned function plus a typed parameter/input-selection contract. For example, a verified connection rule tests the specific connection key and Boolean value; seeing any fact named `integration.connection.verified` is not sufficient to infer a disconnection.

| Verdict | Meaning |
|---|---|
| MATCH | Required inputs are eligible and the stated condition evaluates true. |
| NO_MATCH | Sufficient eligible inputs exist and the condition evaluates false. |
| UNKNOWN | Missing, incomplete, stale, ambiguous or conflicting evidence prevents evaluation. |
| ERROR | Implementation/provider/contract error prevented computation; never a business negative. |
| DISABLED | Capability intentionally not evaluated; never equivalent to NO_MATCH. |

The use gate separately returns ALLOW/BLOCK for policy, source, evidence, DNC, audience or channel restrictions. A true signal can be operationally blocked. An unknown signal cannot be made true by a reviewer.

A simple reviewed mapping can select service line, audience role, template and deterministic priority from MATCH results. Preserve supporting observations, internal hypotheses and research context in separate fields. Maturity-specific offers use their own gate; neutral questions do not. If no compatible reviewed template exists, return a research report or withheld draft instead of unconstrained prose.

## 7. Research and entity aggregation

### Complete measurement lineage

A research prior depends on the exact sample definition, every included/excluded record used by its counting rule, classification states, origin deduplication, period and support policy. Its execution input digest covers all those dependencies. Current-use checks cover the entire dependency set.

Use separate support policies, for example WORKFLOW_MENTION and REPORTED_NEGATIVE_EXPERIENCE. A question about automation is not an experienced negative report. A negated complaint does not enter a pain numerator. Record retrieved count, eligible count, classified-eligible count, unknown/excluded count, supporting count and exact chosen denominator. No unmeasured record is silently interpreted as a negative theme label.

Loss of permitted denominator evidence blocks new use of the old statistic until a new version is computed from eligible inputs. Historical display is allowed only to the extent retention permissions allow its explanation. Product/industry priors remain contextual and non-causal.

### Legitimate cross-subject aggregation

Company-level counts over licensed people, locations or other members require a declared MEMBERSHIP_AGGREGATION function with an accepted relationship snapshot, membership window, deduplication and authorized target. The output is a derived organization measurement whose lineage names the original member subjects. It does not relabel their raw facts as company observations.

Context joins remain a separate one-hop INTERNAL_RESEARCH path. Do not weaken the general same-subject restriction merely because legitimate aggregation needs a controlled exception.

## 8. Time, visibility and provenance

Use four explicit times: source observation/effective time, repository recorded time, input-set sealing/knowledge cutoff, and current-use evaluation time. Logical source `as_of` is not wall-clock completion.

External inputs must exist by the sealed knowledge cutoff and be recorded in the exact input set. Same-run outputs become eligible only after their successful producing execution commits. A later retrospective rerun may use newly ingested old observations, but it has a new sealed input set. Historical reproduction never reads arbitrary later records with a matching source timestamp.

Record IDs are immutable. Same ID/key with different content fails. Binding, sample, taxonomy, rule and source-policy versions are immutable references; current revocations can veto present use without rewriting historical decisions. Current-use permission is always distinct from historical truth.

## 9. Persistence, retry and operational safety

Use transactions for the fact row and evidence/execution references that must become visible together. Stage/finalize blob bytes before committing their database reference. Clean up permitted orphaned blobs after a failed transaction; never commit a positive fact pointing to unfinalized bytes. The database transaction does not also make a filesystem/object-store write or a provider action atomic.

A per-target evaluation publishes its final signal/package result and completion marker together. Failed computations retain diagnostics, not approved partial outputs. Idempotent operation identities permit independent target retries; changed inputs produce new evaluations.

For exports/sending, store the pending handoff and its reviewed revision in the same database transaction. A sequential worker can perform the external operation and reconcile receipts. No broker is necessary. External duplicates remain possible without provider deduplication, so the adapter contract must define stable business identity and reconciliation rather than claim end-to-end exactly-once delivery.

Minimum runtime controls include authenticated tenant/principal context, secrets outside evidence payloads, destination and redirect restrictions, request/body/time/rate limits, bounded model tasks and costs, safe parsing, process memory limits and current source-rights checks. These are obligations of existing modules, not separate deployed components.

Operational acceptance includes restore of database plus content references, corruption detection, failed-write cleanup, retry after interruption, source revocation and deletion propagation, and query/export authorization. Metrics should report target/stage failures, UNKNOWN reasons, unsupported candidates, stale inputs, policy denials, model repairs/cost, output blocks and export reconciliation. Numeric availability or accuracy guarantees require measured tests, not invented thresholds.

## 10. Optional delivery and outcomes

This profile remains OFF until its contracts are implemented. A DeliveryIntent links the exact reviewed package revision, current-use decision, recipient identity, sender/campaign configuration and business-send key. Its state is PENDING, DISPATCHING, ACCEPTED, UNKNOWN_DELIVERY, FAILED or CANCELLED.

Provider acceptance is not proof of inbox delivery. Uncertain acceptance is reconciled before retries. CRM sync is separate from sending and cannot trigger another send. Incoming events require authenticated origin, evidence and tenant/provider/message linkage. Unmatched events are quarantined, not thrown away or attached by guesswork.

DNC/unsubscribe creates a durable operational restriction that does not disappear when a fact TTL expires. Reply classification remains a derived result over the original reply. Mature performance needs an exposure unit, deduplication, response window and explicit denominator. No automated policy promotion follows from observational reply rates alone.

## 11. Read, review and control interfaces

Keep a small API/CLI surface: submit an intake, inspect a run/target, query typed facts, inspect a fact's complete evidence, inspect research context, review a candidate/binding/package, re-evaluate a target, export a reviewed revision, and process a retention/change request. Endpoint payloads use the same validated contracts as batch processing.

A target report must show successful observations, attempted checks, failures, disabled capabilities and limitations. UNKNOWN is not the same as an empty database query. Search output must show subject, state, nature, scope, source, times, resolution and current eligibility, with access-controlled evidence references.

BatchRunner returns a BatchResult containing target results and diagnostics, not only a list of outreach packages. This preserves useful broad-knowledge runs that intentionally produce no messages.

## 12. End-to-end acceptance specification

Tests below are required outcomes, not tests claimed to have passed in v4. The accompanying audit records the checks actually executed.

| Acceptance case | Required result |
|---|---|
| Valid account capture and supported template | Capture → parsed evidence → admitted fact → resolved claim → rule result → reviewed preview → gated export receipt with exact lineage. |
| Knowledge-only product/industry ingestion | Facts and attributable research outputs persist without any account signal or package. |
| Target unresolved or cross-account ambiguous | Quarantine/binding review; no forced company attribution. |
| Policy denial before any bytes | Failed/denied AcquisitionAttempt, clear target diagnostic, no fabricated artifact or absence. |
| Fetch timeout, partial body or incomplete API pagination | UNKNOWN/incomplete coverage, not NOT_FOUND. |
| Capture complete but detector unsupported or failed | Detector failure diagnostic; no proof of absence. |
| Model failure or exhausted repair | No eligible positive output; all permitted attempts and cost retained. |
| Execution output recorded before successful producer completion | Reject current eligible output/publication. |
| Multi-account batch with one failure | Other independently completed target results remain valid; failed target has no approved partial result. |
| Unpinned fact/binding/sample/config or failed same-run parent | Reject evaluation or make a new explicit input selection. |
| Same claim has contradictory eligible observations | No MATCH or factual clause requiring that unresolved claim. |
| Condition demonstrably false | NO_MATCH, distinct from missing data and from a suppressed true match. |
| Duplicate captures/IDs from one origin | Do not manufacture independent corroboration or duplicate exposures. |
| Negated or unclassified theme | Follow explicit theme policy; no default pain support. |
| Denominator-only record removed/revoked/expired | Block old prior's current use and recompute with a new sample version. |
| ABSTAINED context | Audit only; cannot influence eligible ranking or copy as usable context. |
| Member/location aggregate | Requires explicit accepted membership and complete eligible input lineage. |
| Other-tenant or wrong-type change | Reject before any target state changes. |
| Known source policy changes after review | Current-use gate blocks export regardless of historical approval. |
| Package content/recipient/destination changes | New revision/gate and review as required; old approval cannot authorize changed bytes. |
| Export retry after uncertain destination response | Reconcile stable export identity; no blind duplicate side effect. |
| Candidate/stale/fixture data reaches production gate | Fail closed. |
| Evidence deletion and restore | Current use blocked; restoration does not resurrect revoked access or deleted content. |
| Optional send from preview-only profile | Reject. |
| Optional reply without matching provider evidence | Quarantine; never infer a successful exposure. |
| Deterministic rerun from sealed inputs | Same substantive result and lineage, excluding declared wall-clock/operation-ID fields. |

Each enabled source family needs adapter-specific positive, negative, malformed, truncated, denied and identity-ambiguity cases. An aggregate family label or a schema specimen is not an extraction accuracy test. Existing 197 predicates need not all have live collectors before a selective runtime ships, but unimplemented capabilities must remain visibly disabled rather than reported as checked.

## 13. Application and sign-off

Apply the delta to schema authoring, semantic validation, source/function mappings, reference fixtures, all affected diagrams and the operational documentation. Keep existing rejection tests. Convert the diagnostic probes into intended-behavior regression cases, with the explicit per-target/history qualifications above.

Architecture sign-off requires every enabled boundary to have an input, output, owner, validator, failure state, retry rule and acceptance test. Contract sign-off additionally requires encoded schemas and invoked semantic tests. Runtime sign-off requires actual database/adapter/control-path tests. Live accuracy and commercial usefulness require permitted real samples and calibration.

No source file in the original v4 archive was changed by this review. This completion design is ready to guide the next revision, but the unresolved findings must not be marked fixed before that revision is encoded and tested.
