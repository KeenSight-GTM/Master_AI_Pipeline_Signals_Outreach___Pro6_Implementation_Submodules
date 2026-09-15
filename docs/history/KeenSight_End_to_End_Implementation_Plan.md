# End-to-end implementation phases

This is the implementation plan against the uploaded v4.1 baseline. It preserves the broad fact catalog and combination-C research path. It does not patch or certify new runtime contracts. Phase gates are executable deliverables and tests, not elapsed-time estimates.

**Critical path:** `P0 → P1 → P2 → P3 → P4 → P6 → P7 → P8 → P9`. P5 source-family expansion runs alongside P6 after the fact-admission boundary exists. A specific signal/template cannot activate until its particular P5 inputs are available, but unrelated source integrations do not block a supported slice.

Scrapling is the first running product. P0 is only reproducibility, ownership, a thin capture/exchange boundary and tests—not a requirement to build the future platform before making a request.

| Phase | Deliverable | Dependencies |
| --- | --- | --- |
| P0 — Freeze the baseline and define the scanner boundary | A reproducible development organization/workspace and the minimal capture/exchange contracts. This is setup, not an application-platform build. | None |
| P1 — Ship the first live Scrapling evidence collector | Direct URL/host input → safe static capture → retained artifact/attempt → resumable versioned scan bundle, with no LLM or outreach. | P0 |
| P2 — Complete all 38 commands and the browser capture path | The complete workbook command suite, all extraction surfaces, host qualification/scoring and an evidence-preserving fact-candidate adapter. | P1 |
| P3 — Integrate dynamic fingerprint discovery, review and release | The scanner learns recurring unknown surfaces through a review-gated rule release loop, not runtime self-promotion. | P2 |
| P4 — Build the persistent knowledge application and close authorization | Scan bundles become queryable broad facts with complete producer/identity/coverage/claim-resolution checks. | P3 |
| P5 — Expand acquisition across all fact suites | Approved collectors and tested mappings for all 11 domain families, plus the 52-ledger source extensions, activated in source-specific batches. | P4 |
| P6 — Implement deterministic reasoning and combination-C research context | Selected complete signals and research priors from resolved claims and exact input/sample snapshots. This phase can progress alongside P5. | P4 |
| P7 — Deliver auditable intelligence and reviewed no-send outreach | Searchable account intelligence, supported previews, exact-revision review and a current-use-gated handoff. | P6 |
| P8 — Add explicit CRM/export and delivery integrations | Destination-specific remote handoffs and, only when enabled, controlled sending with durable identity/reconciliation. | P7 |
| P9 — Close outcome measurement and harden scale/operations | Mature descriptive performance metrics, operating dashboards, recovery and measured growth in throughput. | P8 |

## P0 — Freeze the baseline and define the scanner boundary

**Repositories:** `.github`, `knowledge-contracts`, `fingerprint-library`, `scrapling-ingestion`, `signals-platform`.

**Delivery boundary:** A reproducible development organization/workspace and the minimal capture/exchange contracts. This is setup, not an application-platform build.

### Modules and submodules

repository bootstrap, dependency lock, 38-command registry, capture exchange contracts, fixture harness.

### Work

1. Preserve both donor branches by commit, keep history/license provenance, and run their own tests in their locked environments before reuse.
2. Import the v4.1 contract baseline; retain its broad 213-predicate catalog and all current regression tests.
3. Record every workbook sheet and command ID. Add capability/command execution and scan bundle specifications without changing source terminology.
4. Pin Python, Scrapling 0.4.15 initially, browser binaries, schema/rule/profile versions; characterize the exact response/session API before coding against examples.
5. Set read-only/single-tenant local development defaults, no live spending or sending, approved fixture origins, secrets and CI boundaries.
6. Make the absent 99_MASTER_ALL footprint library and actual deployment/provider permissions explicit input dependencies, not invented data.

### Exit gate

1. Clean setup runs baseline 588 tests (current rerun passed); donor tests are separately required, not claimed run here.
2. All 38 command IDs have a handler owner, phase and acceptance case in a checked registry.
3. No arbitrary registry-supplied Python import or command execution is allowed.
4. The app can proceed with reviewed donor/starter rules without claiming the missing 25-vertical master library is loaded.

## P1 — Ship the first live Scrapling evidence collector

**Repositories:** `scrapling-ingestion`, `knowledge-contracts`.

**Delivery boundary:** Direct URL/host input → safe static capture → retained artifact/attempt → resumable versioned scan bundle, with no LLM or outreach.

### Modules and submodules

intake.url_identity, policy.robots, transport.http, capture.headers_cookies, extraction.raw_html, storage, output.scan_bundle, telemetry.

### Work

1. Implement normalization, per-origin policy, public-address/redirect guards and request reservations before fetch.
2. Use Scrapling HTTP sessions; persist response bytes, encoding, response metadata, redirect chain, request identity and truncation.
3. Record timeouts, denied/no-byte attempts, rate-limit events and budget skips explicitly. Never manufacture empty HTML or a business absence.
4. Use a single writer, bounded queues and active-domain window, cancellation, resumable target state and atomic bundle completion.
5. Run extractor output against the actual bytes retained; incomplete/oversized captures remain limited evidence.

### Exit gate

1. A permitted test site produces a complete replayable capture with all source/evidence references.
2. Robots/policy denial, malformed URL, DNS failure, redirect to private address, 429 and oversized content have tested terminal states.
3. Kill/restart does not duplicate a completed capture or lose failed-target diagnostics.
4. Normal crawl has no model calls, no external form submissions and no outbound message operations.

## P2 — Complete all 38 commands and the browser capture path

**Repositories:** `scrapling-ingestion`, `fingerprint-library`, `knowledge-contracts`.

**Delivery boundary:** The complete workbook command suite, all extraction surfaces, host qualification/scoring and an evidence-preserving fact-candidate adapter.

### Modules and submodules

commands, discovery, transport.browser, extraction, matching, aggregation, qualification, ranking, bridge.

### Work

1. Implement all 17 extraction commands and the two discovery commands, preserving per-node and per-page provenance.
2. Compile typed catalog matchers and guards; run host accumulation before host matching/gating, then finalize output.
3. Add separately bounded browser rendering under the original FETCH_STEALTH ID; retain actual engine, trigger, static/rendered artifacts and capture limitations.
4. Capture network metadata through an explicitly version-tested browser hook when required; leave DNS/TLS and other extras as separately registered capabilities beyond the original 38.
5. Emit the workbook's HostResult and Hit projections plus the richer ScanBundle/attempts/evidence needed by v4.1.
6. Support no-send detection/scanning profiles and offline replay from day one; no source status or catalog score can grant production authority.

### Exit gate

1. 38/38 command handlers have positive/negative/error or not-applicable fixtures and evidence outputs; each run records every applicable command's disposition.
2. All template-path slots and selector surfaces from the workbook are mapped; skipped probes are not represented as missing software.
3. Boundary tests include hostname lookalikes, comments, quoted attributes, noscript, multiple JSON-LD subjects, deep seeds and same-host multi-page guards.
4. Budget counters include failures/redirects/retries and separately bound browser subrequests.
5. Recorded HTTP and browser captures replay to equivalent substantive detections without another live request.

## P3 — Integrate dynamic fingerprint discovery, review and release

**Repositories:** `scrapling-ingestion`, `fingerprint-library`, `knowledge-contracts`.

**Delivery boundary:** The scanner learns recurring unknown surfaces through a review-gated rule release loop, not runtime self-promotion.

### Modules and submodules

donor rule import, research.normalize, research.prevalence, research.candidates, research.exchange, rules.validation, rules.release, replay.

### Work

1. Inventory/import all donor rule definitions with original IDs, hashes, statuses and a disposition report; account for all 739 manifest-listed rows.
2. Adapt RuleLibrary/FingerprintRuleEngine behavior, catalog normalization, candidate export/review and pack validation rather than treating old PageSignal values as new facts.
3. Preserve one observation for each distinct capture/support; deduplicate display rows without dropping rule IDs/evidence.
4. Queue repeated unknown normalized features using configurable unique-site thresholds; namespace private/tenant evidence and do not pool it without approval.
5. Use manual review initially; optional bounded LLM proposals may produce candidates only.
6. Validate fixture and mutation cases, shadow-compare, approve, release immutable rule packs, pin them per run and provide rollback/revocation.
7. Replay eligible stored captures with a new detection execution; request recapture for missing modalities and do not refresh observation time/TTL.

### Exit gate

1. Manifest inventory = imported + quarantined + non-executable records, with no silent omission.
2. One repeated unknown is exported, reviewed, installed, matched and replayed without recollecting compatible content.
3. Unsupported/candidate/research-only definitions never drive production signals or templates.
4. A running scan does not hot-load a new release; removal/demotion affects subsequent current-use checks.
5. Upstream thresholds 3/10/50 are scheduling defaults only, not proof of accuracy or statistical independence.

## P4 — Build the persistent knowledge application and close authorization

**Repositories:** `signals-platform`, `knowledge-contracts`, `scrapling-ingestion`.

**Delivery boundary:** Scan bundles become queryable broad facts with complete producer/identity/coverage/claim-resolution checks.

### Modules and submodules

facts.admission, facts.repositories, facts.identity, facts.provenance, facts.claims, facts.query, security, retention.

### Work

1. Implement v4.1 repositories and transactional admission; initially one logical database and local content backend, not a graph database.
2. Consume scanner evidence/candidates through one adapter; preserve direct observation, mention, inference, provider report and contextual roles.
3. Implement successful-producer, input-closure, conflict, coverage, no-byte and profile gates at runtime rather than only in fixture validation.
4. Complete the deliberately unclosed F ChangeRecord tenant/actor/typed-replacement checks before hosted mutation or multi-tenant production.
5. Enforce authenticated tenant context, source use policy, revocation, retention, current view versus historical evaluation and exact input snapshots.
6. Provide knowledge-only batch reports and evidence/claim search without requiring a commercial signal.

### Exit gate

1. Capture → fact admission → query works with retained real/controlled fixtures and exact locators.
2. A stale, cross-account, candidate, conflicted, failed-producer or revoked input cannot support eligible outward use.
3. ChangeRecord authorization/replacement tests pass and the previous F blocker is explicitly closed before production.
4. Reimports are idempotent; incompatible payload reuse fails; corrections preserve history.
5. No output depends on the legacy rule catalog as a second authoritative fact store.

## P5 — Expand acquisition across all fact suites

**Repositories:** `scrapling-ingestion`, `signals-platform`, `knowledge-contracts`.

**Delivery boundary:** Approved collectors and tested mappings for all 11 domain families, plus the 52-ledger source extensions, activated in source-specific batches.

### Modules and submodules

connectors.jobs_ats, connectors.technographics, connectors.reviews, connectors.communities, connectors.traffic_seo, connectors.registries, connectors.publications, connectors.authorized_operations, llm.gateway.

### Work

1. P5a: ATS/careers/posting history and vertical product/portal evidence; distinguish public description from verified operation.
2. P5b: permitted local/product/app reviews and discussions, exact statements, sample dispositions and independent origin IDs.
3. P5c: traffic estimates, search/ads/backlinks/mentions/apps/shopping with provider, method, dimensions, periods and units.
4. P5d: provider/professional/corporate registries, licenses, filings, permits and authorized phone/operational records.
5. P5e: website/job workflow extraction, publications/transcripts/events/case studies and remaining ledger families through approved capture adapters.
6. Use one bounded LLM gateway with raw I/O before parse, structured output, mandatory bounded repair, cost reservations and abstention.
7. Preserve every source's capture/extract/use status. Unavailable permissions block that connector explicitly; fixture coverage is not live access.

### Exit gate

1. An 11-area source matrix reports actual live/fixture/disabled/blocked status and exact emitted predicates.
2. Each enabled source demonstrates evidence → typed facts, boundaries, pagination/timeouts and source-specific retention.
3. Cross-provider periods/units and current versus historical records cannot be conflated.
4. The 52 ledger entries remain tracked as source, fact, derivation, algorithm or template—not all reclassified as facts.

## P6 — Implement deterministic reasoning and combination-C research context

**Repositories:** `signals-platform`, `knowledge-contracts`.

**Delivery boundary:** Selected complete signals and research priors from resolved claims and exact input/sample snapshots. This phase can progress alongside P5.

### Modules and submodules

evaluation.input_selection, evaluation.dependency_plan, reasoning.derivations, reasoning.signals, reasoning.adjudication, research.samples, research.priors, research.context, reasoning.cohorts.

### Work

1. Port useful selectors, calculators and stage functions from Master Signals without importing its mandatory 223-evaluation terminal condition.
2. Implement versioned functions, typed value comparisons, UNKNOWN/error handling, temporal changes, confounds and independent support.
3. Bind sample support, full denominators/exclusions and every source permission to research prior eligibility.
4. Permit explicit product/industry links as internal context only; prevent company-pain claims from contextual priors.
5. Implement declared membership aggregates before provider/location rollups; keep cross-subject contamination guards.
6. Keep all 23 derivation designs and 18 prior signal identifiers, enabling only implemented dependency closures; implement peer/cohort algorithms before enabling their signals.
7. Treat compound ledger 33–40 as hypotheses/calculations requiring exact windows and evidence, not proxy-derived certainties.

### Exit gate

1. A condition with sufficient false evidence is NO_MATCH; missing evidence is UNKNOWN; operational restrictions remain separate.
2. Contradictions, abstained contexts or deleted denominator evidence cannot support an eligible decision.
3. Fixed-batch dependency order rejects same-run self/multi-node cycles; no dynamic scheduler is required.
4. Real stored-input integration tests complement numerical fixtures.
5. At least one product/industry research prior joins to account context without acquiring company-claim permission.

## P7 — Deliver auditable intelligence and reviewed no-send outreach

**Repositories:** `signals-platform`, `knowledge-contracts`.

**Delivery boundary:** Searchable account intelligence, supported previews, exact-revision review and a current-use-gated handoff.

### Modules and submodules

commercial.opportunity_selection, commercial.templates, commercial.claims, commercial.packages, review, exports, api_ui.

### Work

1. Map supported conditions to service line, audience and reviewed template; retain a valid no-opportunity outcome.
2. Enable observation-led questions without universal maturity gating; keep maturity/scenario/lookalike offers behind their specific proofs and implemented renderers.
3. Revalidate whole sentences, input ancestry and exact quotes; do not promote draft LLM prose.
4. Persist actual authenticated ReviewDecision, UseGateDecision and ExportReceipt records with revision/payload/destination identity.
5. Provide analyst views for captures, claims, candidate rules, contexts, rejections and approvals.
6. Reuse Master context/page selection and package mechanics only behind the new contract tests and no duplicate crawl path.

### Exit gate

1. Permitted live/retained evidence → supported preview → authenticated review → current-gated local export is demonstrated.
2. Corrected identity, DNC, evidence expiry/deletion or source revocation blocks stale reviewed packages.
3. Failed targets cannot publish approved partial output; one account failure does not erase independently completed accounts.
4. No sender is reachable from this profile.

## P8 — Add explicit CRM/export and delivery integrations

**Repositories:** `signals-platform`, `knowledge-contracts`.

**Delivery boundary:** Destination-specific remote handoffs and, only when enabled, controlled sending with durable identity/reconciliation.

### Modules and submodules

exports.mapping, crm.adapter, delivery.outbox, delivery.gates, delivery.providers, delivery.reconciliation, outcomes.ingress.

### Work

1. Resolve recipients and account/contact mappings without fabricating them; restrict private/internal context in exported payloads.
2. Separate preview/export, draft creation, append-to-existing and activation/send permissions where the destination supports them.
3. Implement transactional outbox, provider idempotency/correlation, lease/claim semantics as needed and immediate pre-send restrictions.
4. Represent uncertain acceptance explicitly and reconcile before retrying; CRM-sync failures never cause another send.
5. Record provider events, unsubscribe/DNC decisions and exposure identity as soon as delivery is introduced.

### Exit gate

1. No-send profiles cannot dispatch; approval of a preview is not authorization for a campaign activation.
2. Duplicate jobs and webhooks do not duplicate exposure/outcome identities.
3. Timeout-after-acceptance and restart scenarios reconcile without blind resend.
4. Every external action has an exact payload, gate, receipt and permission scope.

## P9 — Close outcome measurement and harden scale/operations

**Repositories:** `signals-platform`, `scrapling-ingestion`, `.github`.

**Delivery boundary:** Mature descriptive performance metrics, operating dashboards, recovery and measured growth in throughput.

### Modules and submodules

outcomes.attribution, outcomes.measurement, quality.calibration, ops.observability, ops.recovery, ops.capacity.

### Work

1. Compute outcome metrics with mature response windows, explicit exposure units, pending/bounce/uncertainty handling and contamination rules.
2. Keep performance descriptive; ranking experiments cannot upgrade source authority or establish causal effectiveness automatically.
3. Measure scanner recall/precision by rule family/vertical/modality and monitor capture failures, drift, budget use and unsupported-surface rates.
4. Run restore, retention/deletion, revocation, authentication and tenant-boundary tests; these controls begin earlier and are stress-tested here.
5. Scale from bounded local batches to measured concurrency; introduce PostgreSQL/multiple workers only with concurrency tests and demonstrated need.
6. Add shared atomic budgets before concurrent paid operations, not after. Incremental scheduling remains optional and must match full recomputation.

### Exit gate

1. Operational and commercial denominators are independently audited.
2. Backups restore tested knowledge and receipts; revoked/deleted data cannot reappear through stale projections.
3. Load targets and cost ceilings are chosen from measured pilot results rather than workbook estimates.
4. Feature release can be rolled back; approved fingerprint packs and application versions are independently pinned.

## First implementation pull requests

1. Bootstrap donor-source locks, v4.1 verification, the 38-ID traceability registry and controlled local fixtures.
2. Implement `NORM_URL`, policy/robots, Scrapling static transport, capture metadata and a minimal `ScanBundle`; record no-byte failures.
3. Add a single-writer local sink, limits, restart/idempotency and replayable original bytes.
4. Implement all 17 extraction surfaces with original-byte/node references and an evidence index.
5. Add discovered/well-known/sitemap planning, same-host guardrails and the resolved budget semantics.
6. Add permitted browser fallback and pre-navigation network recording with modality-aware coverage.
7. Compile typed matching, host rollup, vertical/schema/negative assessments and priority; finish the 38-command acceptance gate.
8. Import donor rule packs, characterize compatibility and preserve multi-rule support; complete the dynamic candidate/review/release/replay loop.

These are implementation PRs to create later, not claims that issues or branches were created during this planning pass.

## End-to-end release checklist

A deployed feature is not complete merely because a schema exists. The release must demonstrate successful capture→extraction→fact admission, both conflict and insufficient-evidence outcomes, a context join without company-claim leakage, supported rendering, exact-revision review and a current-use-gated handoff. A knowledge-only run must be equally valid.

All source and fact families remain in the architectural catalog even when some collectors are source-blocked. A disabled/blocked integration is reported as such and never described as working. The optional send profile adds its own delivery and outcome gates; reviewed handoff can ship independently.
