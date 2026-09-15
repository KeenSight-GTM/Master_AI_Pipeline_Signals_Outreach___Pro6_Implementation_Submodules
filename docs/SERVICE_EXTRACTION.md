# Running modules independently and extracting services

## 1. Answer and implementation boundary

**Independent execution is supported for the delivered collector operations; independent deployment of every E2E module is not implemented.** A module, command, worker process and network service are different things.

| Form | Meaning | Status in this release |
|---|---|---|
| Python module | Call an explicit typed function/class with supplied inputs | Collector and selected canonical/reference functions exist |
| CLI / separate process | Execute one operation against retained inputs and write an inspectable artifact | `ks-scan` plus `ks-module extract`, `match`, `check`, `resolve` are implemented and process-tested |
| Local canonical validator | Validate the whole supplied contract/reference bundle | `canonical/validate.py` and its tests are implemented |
| Shared-protocol admission checker | Check operation signature, exact consumed-reference closure, output version and resolved payload | Hardened; only the delivered fixture operation is registered |
| Isolated worker with queue/auth/leases | Execute durably from a trusted command envelope | Proposed; not implemented |
| Authenticated HTTP/gRPC service | Remote callers, trusted identity, scoped object access, deployable lifecycle | Proposed; not implemented |

The independent collector CLI does not yet implement the common `ModuleRequest/ModuleResult` transport. It deliberately exposes narrow offline commands, not an arbitrary Python-entrypoint runner. The next integration should wrap these functions, not rewrite their extraction/matching logic.

## 2. Run the actual modules separately

From the root of the delivered package:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e './collector[test]'

# Create a completely synthetic local capture store; zero network calls.
ks-scan demo --output ./demo-store

# Inspect the capture ID that was actually selected for technical evaluation.
python -c 'import json; print(json.load(open("demo-store/scan-bundle.json"))["evaluated_capture_ids"][0])'

# Replace CAPTURE_ID with that printed ID. Each command runs as a fresh process.
ks-module extract \
  --tenant demo --capture-id CAPTURE_ID \
  --store ./demo-store --output ./page-evidence.json

ks-module match \
  --page ./page-evidence.json \
  --rules ./collector/examples/demo-rules.json \
  --store ./demo-store --output ./match-result.json

ks-module check \
  --bundle ./demo-store/scan-bundle.json \
  --store ./demo-store --output ./checked.json

ks-module resolve \
  --bundle ./demo-store/scan-bundle.json \
  --as-of 2026-09-14T12:00:00Z \
  --store ./demo-store --output ./claim-view.json
```

`extract` reads a Capture from the trusted local store. `match` verifies each supplied PageEvidence against original bytes and pinned parsing behavior before matching. `check` verifies the bundle's structure, actual producer/report consistency, metadata, evidence and projections. `resolve` reproduces a historical claim view; it is not permission to export or send. For a current collector projection under a selected rule pack use `ks-scan claims --rules ... --as-of ...`; canonical current-use permission remains a separate application boundary.

These commands can be run in separate shells. The tests also invoke them in separate Python processes. Do not infer that a shared SQLite file is a safe multi-host database or that these local-owner CLIs implement tenant authentication.

Canonical reference checks are separately runnable:

```bash
python -m pip install -r ./canonical/requirements.txt
(cd canonical && python generate.py --check && python validate.py && python -m pytest -q)
(cd protocol && python validate_protocol.py && python -m pytest -q)
```

Live collection additionally requires `pip install -e './collector[live,test]'` and successful execution of the pinned-SDK integration test. Installation was attempted here but did not succeed; the test remains skipped. Native browser capture remains disabled until its egress, DNS, resource, cookie and cancellation boundaries are implemented and verified.

## 3. What not to turn into a service

Do not make one HTTP service per extractor, fingerprint operator or JSON schema. Script extraction, matching, grouping and evidence-link creation are cheap local operations over the same page; remote calls would copy data, fragment transactions and complicate debugging without an established benefit.

Keep these atomic groups together until there is a concrete deployment reason to split them:

- Capture metadata plus finalized blob reference plus attempt completion.
- Evaluation validation plus match/observation/support publication plus successful manifest.
- Canonical admission plus evidence/producer links plus admission disposition.
- Enrollment/step state plus business-send intent/outbox.
- Verified inbound event plus immediate local contact stop/hold.
- Exact package revision plus its content hash; review is separately linked to that immutable revision.

Function-level code separation and process-level testability are worthwhile immediately. Network separation is a later operational choice.

## 4. Proposed deployment groups and owned data

All 39 logical modules are assigned exactly once in `service_groups.json`; common ports can be imported by several groups without transferring write ownership.

| Group | Proposed responsibility | Owned mutable records | Hard boundary |
|---|---|---|---|
| S0 Control/programs | Programs, releases, intake, authorized execution and target coordination | Program revisions, run manifests, target completion, permission/budget decisions | Caller text cannot create authority; child tasks cannot reset parent budgets |
| S1 Capture/fingerprints | Scrapling, extraction, matches, technical discovery, replay | Captures/attempts, technical index, scan evaluation records | No canonical Fact writes, source rights bypass, or self-approved rule release |
| S2 Canonical knowledge | Subject identity, fact admission, complete claim groups, record resolution, authorized corrections | Subjects, bindings, facts, lineage, claim projections, ChangeRecord and governed restrictions | One authoritative writer per record; shared-release changes are not arbitrary tenant mutations |
| S3 Enrichment/model tasks | Approved provider adapters and bounded model processing | Provider/model attempts, costs, repair chains, typed output artifacts | All requests pass source/budget policy; no direct commercial effects |
| S4 Research/intelligence | Derivations, samples, priors, context joins, signals, opportunity/quality assessment | Execution/results, sample membership and decisions, prior/signal drafts | Canonical outputs reenter admission; context is not account proof |
| S5 Audience/reviewed content | Contact assessment, grounded content, reviews, current-use export decisions | Contact assessments, package/message revisions, reviews, gates, export intents/receipts | No send authority through a preview-export gate |
| S6 Engagement/sales | Campaigns, sequence state, sends/reconciliation, replies, CRM sync, outcomes | Enrollment, step/outbox, exposure, conversation, CRM link/sync receipts | Exactly one scheduler and stable external-effect identity |
| S7 Operator workspace | Authorized UI/API facades, trace/evidence views | Read-model caches and diagnostics; authoritative changes routed to owners | Never bypass writer APIs or copy sensitive evidence into logs |

Object bytes can live in one content service/bucket initially. Scoped references, immutable metadata and tenant authorization still apply. Database schemas may share one initial server but are not a license for cross-owner SQL writes after extraction into services. A technical fingerprint index or vector index is rebuildable and does not own factual truth.

### Safety-sensitive separation

Do not split restriction authority, current-use checking, enrollment stopping and dispatch until a consistent freshness protocol exists. If they become different processes:

1. Inbound reply processing commits a contact-level local stop/hold before asynchronous classification or CRM work.
2. The canonical restriction mutation is durable and authorized. Delivery remains blocked locally while propagation is pending.
3. Immediately before dispatch, the sender checks both authoritative current restriction state and local enrollment/contact holds; it never relies only on a stale allow token or cache.
4. If either authority is unavailable, dispatch is held. After remote acceptance, later restrictions stop subsequent messages but cannot unsend the accepted one.

This is a proposed operational contract, not a cross-service guarantee provided by the current reference code.

## 5. Transport-neutral operation contract

Use the same business handler through three adapters: in-process call, CLI/worker message, and authenticated service endpoint. Do not introduce a second implementation of business logic for HTTP.

A request should carry:

```text
protocol_version, module_id, operation
request_id, execution_id, attempt, idempotency_key
trusted tenant/principal reference, purpose, mode
run_id, target_key, trace/span links
release_lock_ref, parameters_ref, exact input_refs
deadline, explicit budget reservation or no-cost mode
as_of and knowledge_cutoff where the operation requires them
```

A result carries the echoed invocation identity/request digest, execution status, actual consumed references, committed output references, structured diagnostics, start/finish clocks and resource usage. Large payloads are referenced, not serialized repeatedly through the queue. A record reference includes tenant, record ID, schema ID/version and content digest; the resolver verifies bytes and permissions.

The current protocol patch rejects unregistered operation names, wrong schema versions, undeclared consumed refs, missing required consumption on success, duplicate refs, overwriting an input, and output past deadline. Its resolver helper verifies fixture payload bytes and shapes. **It still is not the general enforcing orchestrator**: resource/capability sandboxing, effect admission, manifests for all operations, durable execution state and authentication are future implementation work.

### Suggested network facade — proposal, not implemented routes

| Operation | Suggested route | Semantics |
|---|---|---|
| Submit an installed operation | `POST /v1/operations` | Authenticate principal; validate exact request; commit accepted command; return 202 + execution reference for durable work |
| Inspect execution | `GET /v1/executions/{id}` | Tenant-authorized status and result refs; no raw secrets |
| Inspect record metadata | `GET /v1/records/{id}` | Resolve exact schema/version/digest with read authorization |
| Obtain permitted evidence bytes | `POST /v1/records/{id}/read-capability` | Short-lived purpose-scoped read, not a public permanent URL |
| Request cancellation | `POST /v1/executions/{id}/cancel` | Best effort before effect boundary; accepted external actions may require reconciliation |
| Readiness/health | `/health/live`, `/health/ready` | Distinguish process alive from dependencies and configured capabilities ready |

No endpoint accepts arbitrary `module:path:function`, filesystem paths or a caller-owned tenant grant. Destination URLs for crawling are separately validated. Endpoint naming is a proposal; it is not an existing OpenAPI implementation.

## 6. Queue, retry and transaction behavior after service extraction

Assume at-least-once delivery of work messages. A consumer validates the contract, deduplicates the logical operation, leases it, resolves approved inputs, executes, stages outputs, validates them, then commits result plus completion event. An outbox publishes the event only after that commit. The receiving inbox deduplicates the event independently of the sender's request identity.

Keep separate keys:

| Key | Changes when | Must not imply |
|---|---|---|
| Request ID | A caller creates a logically new request | New source evidence |
| Execution/attempt ID | A retry or worker attempt starts | Permission for another send |
| Input-snapshot digest | Exact evaluated record set/version changes | New acquisition time for old artifacts |
| Semantic rule digest | Predicate/product/operator/mapping semantics change | Automatic production approval |
| Observation ID | New capture/source/value identity | Independent corroboration from overlapping detectors |
| Business-effect key | A deliberately new export/enrollment step is authorized | Different code version alone is sufficient |

The same idempotency key with changed normalized inputs/payload is rejected. A successfully completed pure operation can return its original result. An unknown external send cannot be rerun simply because its execution lease expired. Reconcile against the provider's message/operation identity or hold for an operator when the provider cannot resolve it.

Do not hold a database transaction open during HTTP/model/provider calls. Finalize permitted blobs before committing references; clean up abandoned blobs later. A database commit and a provider action do not share an atomic transaction. A cache cannot turn eventual event propagation into current authorization.

## 7. Failure matrix

| Failure | Local behavior | Across services | Never do |
|---|---|---|---|
| Missing declared artifact | Fail/abstain without eligible output | Retry only when producer/dependency is confirmed; otherwise quarantine | Manufacture evidence or reset capture time |
| Capture succeeded, extraction failed | Keep diagnostic capture; no successful interpretation | Publish failure reason/limits, not a positive-fact event | Count it as complete absence |
| Validation fails after computation | Roll back all eligible findings for that evaluation | Do not publish completion event | Leave supported projections committed |
| Worker dies after blob write | Leave orphan for cleanup | New attempt resolves durable state before re-executing | Assume blob presence means result committed |
| Dependency or source access revoked | Block current use and dependent actions | Propagate revocation and requery authority at use time | Keep using cached ALLOW |
| HTTP 429 | Persist cooldown; respect it on resume | Shared limiter/origin-state owner across workers | Create a new worker to evade the same limit |
| Model output invalid | Bounded repair, then abstain | All repairs use same task lineage and cost budget | Treat request/response/repair as three independent sources |
| Conflicting current claim after review | Block current-use gate | Query current complete claim group, record gate inputs | Refresh only a version vector |
| Provider accepted, caller timed out | UNKNOWN acceptance; reconciliation | Stable business-effect key across retries | Blind resend |
| Inbound opt-out during CRM outage | Stop local contact/enrollments immediately | Durable restriction intent + fail-closed sender | Wait for LLM or CRM to stop |
| CRM update fails | Retry CRM sync only | Dedicated sync identity and receipt | Repeat outreach |
| Evidence deletion includes sample denominator | Block dependent prior/statistic | Invalidate result/reference permissions | Preserve old fraction as still usable |

## 8. Service extraction sequence and exit gates

**Stage A — current:** functions and independent offline CLIs. One local owner and one database. Add the canonical admission bridge and one capture-to-preview integration before adding distributed infrastructure.

**Stage B — separate worker processes:** isolate capture/browser and expensive provider/model tasks for resource and network safety. Use the same handler contracts, shared durable work owner and scoped evidence access. Do not share a local SQLite database between machines.

**Stage C — extract a service only with evidence:** split because of different scaling, fault isolation, credentials/network rights, deployment cadence or ownership—not because a class exists. Likely first candidates are the bounded capture worker and model/provider worker. Keep cheap extraction/matching local to the captured evidence.

**Stage D — hosted product:** add trusted authentication, tenancy, persistent canonical APIs, review workspace and source governance. This is where configured reference ActorGrants must be replaced by trusted authenticated authorization; the repaired validation rules alone are insufficient.

**Stage E — engagement:** enable campaign/enrollment/send/inbound state machines only after send-specific gates, stop propagation, uncertain-send reconciliation and CRM ownership tests exist. Preview export is not sending.

For each extraction, require: versioned command/result and domain schemas; producer and consumer contract tests; identical pure results between in-process and worker paths; duplicate delivery tests; deadline/cancellation tests; crash-before/after-commit tests; trace propagation; denied cross-tenant record reads; permission revocation; and reproducible rollback/cutover. Route one test cohort first. Stop old writers before enabling new authoritative writers; never leave both owning the same state machine.

## 9. Debugging and observability

Every diagnostic identifies module, operation, request/execution, target, record refs and stable reason code. Preserve an unsampled authoritative execution ledger even if routine telemetry is sampled. Keep evidence separate from logs. Support evidence drilldown and why/why-not from account -> package -> clause -> fact -> execution -> original artifact.

Trace context correlates processes; it does not grant authority. Sanitize untrusted incoming context. Do not forward internal baggage, credentials, personal data or private trace identifiers to arbitrary scraped websites. OpenTelemetry's official propagation guidance specifically addresses these trust boundaries: https://opentelemetry.io/docs/concepts/context-propagation/ .

## 10. Implementation decisions still requiring approval

Choose the production database/object store, authenticated identity source, task broker only when distributed work is needed, initial sender/provider capabilities, operation timeout/cost budgets, service SLOs, retention policies, exact first signal profile and review owners. None of these deployments is created by this package. Existing donor repositories remain building blocks; they are not silently imported as additional authorities.
