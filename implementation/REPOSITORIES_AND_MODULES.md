# Proposed organization, modules and submodules

All names are proposed under `<new-org>`. These are repository boundaries, not five running services. No repositories were created or modified in this planning pass.

| Repository | Ownership | Scope |
| --- | --- | --- |
| .github | Organization engineering policy | Reusable CI, review/ownership templates, security and cross-repository compatibility checks. No application runtime. |
| knowledge-contracts | Normative knowledge and exchange contracts | v4.1 catalog and schemas; typed values, validation, command/scan exchange contracts, compatibility manifests. No imports of either application. |
| fingerprint-library | Reviewed fingerprint content and releases | Vendor/product mapping, detector definitions, vertical qualification, priority policies, fixtures, calibration and immutable manifests. Data, not crawler code. |
| scrapling-ingestion | First executable product | All 38 commands, capture/discovery, extraction, matching, candidate harvesting, replay, scan bundles and a CLI/library interface. |
| signals-platform | Knowledge, research, reasoning and commercial application | Canonical facts and evidence indexes, other-source adapters, LLM gateway, combination-C context, signals, review/export, optional delivery/outcomes. |

Keep `SEO-FingerPrint-Scanner-Basic` and `Master_Signals_App_KeenSight` in the organization as pinned, read-only reference forks initially. Preserve source history and license notices. Do not make a wholesale historical-data migration a launch dependency. Create additional repositories only when ownership or independently released runtime packages actually require them.

## Dependency direction

```text
knowledge-contracts
   ↑                   ↑
scrapling-ingestion    signals-platform
   ↑                   |
fingerprint-library    └── calls the ingestion library/CLI or imports ScanBundle
```

`fingerprint-library` supplies versioned data checked by `knowledge-contracts`; it does not import the applications. `scrapling-ingestion` never imports the Master Signals application. Optional LLM review jobs consume candidate exports through a port; they do not run a model in the ordinary capture/match loop.

A release lock pins contracts, collector, fingerprint rules, predicate mapping, source/capture policies and application versions by immutable digest/commit. CI tests a complete lock combination, including schema-breaking upgrades. A new rule pack is loaded between runs, not mid-run.

## First deployment

Use an in-process/CLI application with bounded network concurrency and one writer. SQLite is suitable for the local reference deployment, with a filesystem blob backend behind a content interface. The platform may call the collector as a Python package in the same process. A separate collector CLI exchanges a manifest-based bundle when useful; this does not require a queue service. Introduce PostgreSQL or workers only after a workload and concurrency model justify them. Runtime databases, personal source material and credentials are not Git content.

## Module ownership

| Repository | Module | Submodules | First phase |
| --- | --- | --- | --- |
| .github | delivery-governance | workflow templates, branch/review policy, dependency security, artifact attestations, cross-repository release tests | P0 |
| knowledge-contracts | domain | subjects and bindings, fact state/nature/cardinality, sources and source policy, evidence/scopes/coverage, runs/executions/review/use/export | P0 |
| knowledge-contracts | capture-exchange | command schemas, ScanPlan/ScanBundle, capture and surface evidence, FingerprintMatch emissions, version compatibility | P0 |
| knowledge-contracts | validation | schema/link/semantic admission, producer and input closure, claim conflict/current use, source permissions, change authorization | P4 |
| fingerprint-library | catalogs | vendor/product identities, source imports with row provenance, typed matchers, vertical guards, negative and priority policies | P2 |
| fingerprint-library | assurance | positive/negative/adversarial fixtures, shadow reports, calibration approvals, immutable manifests, revocation/rollback | P3 |
| scrapling-ingestion | intake | url_identity, redirect_binding, CSV/direct-URL input, run/request identity | P1 |
| scrapling-ingestion | policy | robots, origin/SSRF checks, request budgets, source-purpose rights, cookie/session isolation | P1 |
| scrapling-ingestion | transport | http, browser, response classification, retry/backoff, timeouts/cancellation | P1 |
| scrapling-ingestion | capture | original bytes, rendered DOM, headers_cookies, network hooks, resource-limit recording | P1 |
| scrapling-ingestion | discovery | template_planner, sitemaps, path_probes, deduplicated queue, scope-explicit external followups | P2 |
| scrapling-ingestion | extraction | raw_html, scripts, embeds, forms, links, images, metadata, structured_data, regions, attributes, noscript, prose, url_features | P2 |
| scrapling-ingestion | matching | literal, groups, regex, host, regions, images, compiled donor operator adapters | P2 |
| scrapling-ingestion | rules | import_compile, operator capability checks, immutable release loader, rule-to-predicate mapping | P2 |
| scrapling-ingestion | aggregation | host_index, per-surface provenance, same-page versus host correlation, display deduplication | P2 |
| scrapling-ingestion | qualification | vertical_guards, schema_support, scope/confound checks | P2 |
| scrapling-ingestion | ranking | negative_policy, priority, uncalibrated-score reporting | P2 |
| scrapling-ingestion | research | normalize, prevalence, candidates, bounded sampling, exchange | P3 |
| scrapling-ingestion | replay | capability coverage check, stored-byte parsing, new-rule replay, historical detection comparison, recapture requests | P3 |
| scrapling-ingestion | bridge | surface-to-fact candidates, provenance linking, mention/presence/provider distinction, canonical binding handoff | P2 |
| scrapling-ingestion | storage | blob backend, SQLite capture/research indexes, single writer, checkpoint/resume, bundle finalization | P1 |
| scrapling-ingestion | output | scan_bundle, HostResult/Hit projections, JSONL export, streaming progress | P1 |
| scrapling-ingestion | telemetry | command outcomes, crawl counters, heartbeat/watchdog, capture diagnostics, resource usage | P1 |
| signals-platform | facts | admission, repositories, identity, provenance, claims, query, changes, retention | P4 |
| signals-platform | evaluation | input_selection, version pinning, dependency_plan, per-target completion, conservative account rerun | P6 |
| signals-platform | connectors | jobs_ats, technographics, reviews, communities, traffic_seo, registries, publications, authorized_operations | P5 |
| signals-platform | llm | gateway, provider adapters, prompt/task registry, raw I/O retention, repair, budget admission, abstention | P5 |
| signals-platform | research | samples, classifications, priors, context, case-study corpus, lookalike matching when enabled | P6 |
| signals-platform | reasoning | input selectors, derivations, signals, adjudication, membership aggregates, cohorts, temporal comparisons | P6 |
| signals-platform | commercial | opportunity_selection, audience routing, templates, claims, scenario/scorecard policies, packages | P7 |
| signals-platform | review | authenticated principal, exact-revision decisions, evidence viewer, policy release | P7 |
| signals-platform | exports | local preview, mapping, destination approvals, current-use gates, receipts | P7 |
| signals-platform | delivery | recipient resolution, outbox, gates, providers, reconciliation, DNC/unsubscribe | P8 |
| signals-platform | outcomes | ingress, deduplication, attribution, maturity windows, measurement | P8 |
| signals-platform | api_ui | knowledge search, account analysis, scan status, candidate review, package review, audit queries | P7 |
| signals-platform | ops | deployment, storage migrations, backup/restore, alerts, load/cost testing, access/retention enforcement | P4 |

## Test and release boundaries

The contracts repository owns invariant and schema fixtures. The collector owns capture/matcher and all 38 command behavior tests. The fingerprint library owns rule-family fixtures and reviewed promotion evidence. The platform owns cross-repository evidence-to-fact-to-export tests; it is the integration-test home until a separate repository is warranted.

Live network tests, paid providers and sending are explicit opt-ins with bounded credentials and a kill switch. Pull-request CI uses retained/synthetic fixtures and controlled local HTTP/browser test sites. Review authority and tenant principals are taken from trusted configuration/authentication, never a client-authored field. Source migrations and rule imports are reviewed independently of ordinary capture runs.

## Reuse candidates, not a second competing implementation

The scanner donor's `planner.py`, `extractors.py`, `rules.py`, `runtime_fingerprints.py`, `research.py`, and `rule_catalog.py` were inspected for this plan. Preserve useful queueing, rules and research algorithms; change their interfaces/evidence semantics where the new contracts require it.

Master's pipeline documentation and fingerprint-registry implementation were inspected. Use its page-selection separation, context inventory, candidate boundary, opportunity/package concepts and policy-enforced LLM design as building blocks. Its documentation's branch labels can differ from the URL ref; the commit-pinned source is authoritative for this review. Do not adopt the hardcoded 223-evaluation completion requirement or make its crawler/fingerprint registry a competing authority.
