# Sources, scope and validation

## Source-derived facts versus design proposals

The workbook command names, selectors, order, path slots and cautions are transcribed without replacing their wording. The implementation decisions are separately labeled in WORKBOOK_DECISIONS_AND_CONTRACTS.md. The cited GitHub commits are pinned; donor functionality was inspected but donor test suites were not executed here.

The v4.1 archive was actually unpacked and its generation check, validator and 588-test regression suite were rerun. That does not execute a live crawler or certify third-party access. The new handoff validates plan coverage and references only; it does not implement the planned modules.

| ID | Source | Observation |
| --- | --- | --- |
| W1 | Scrapling_Fingerprint_Command_Suite(2).xlsx | 11 worksheets; 38 distinct command rows in 02_COMMAND_CATALOG; 17 extraction commands. Separate 99_MASTER_ALL catalog is referenced but not present in this workbook. |
| A1 | keensight-architecture-v4.1.zip | 75 schemas; 213 predicates; 89 metrics; 225 fixture records; original 588 tests rerun successfully. Known F change-record authorization gap remains unpatched. |
| S1 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/pyproject.toml | Pins scrapling[fetchers]==0.4.15; Python >=3.11; scanner/catalog/rules CLI entrypoints. |
| S2 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/seo_scanner/data/fingerprints/manifest.json | Manifest reports 739 total and 511 runtime-eligible definitions; largely candidate statuses; five rule packs. Entire donor rule corpus was not executed in this review. |
| S3 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/seo_scanner/rules.py | Inspected lines 1–245: data-driven rules, candidate runtime statuses, RuleMatch, PageEvidence, bounded display samples. |
| S4 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/seo_scanner/runtime_fingerprints.py | Combines data-driven and legacy detectors; deduplication by category/key/value can discard separate rule supports. |
| S5 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/seo_scanner/research.py | Inspected lines 1–245: candidate/review/promotion tables; 3/10/50 unique-domain scheduling thresholds; auto-promotion disabled by default. |
| S6 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/RULE_PROMOTION.md | Documents candidate export/review, production validation, explicit candidate promotion and install flow; this is distinct from ordinary runtime status inclusion. |
| S7 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/seo_scanner/extractors.py | Inspected lines 1–220: structured selectors, raw evidence bounds, flattened JSON-LD types, footer text. Raw post-download slicing is not a transport-byte limit. |
| S8 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/seo_scanner/planner.py | Homepage-first, post-homepage discovery files, same-site sampling and bounded sitemap planning; workbook path slots require adaptation. |
| S9 | https://github.com/KeenSight-GTM/SEO-FingerPrint-Scanner-Basic/blob/66358454c98addb8fe297cb5192a32e2bd98f732/seo_scanner/rule_catalog.py | Inspected lines 1–210: stable event IDs, idempotent technical catalog and rule matching; current definitions are updated by ID. |
| M1 | https://github.com/KeenSight-GTM/Master_Signals_App_KeenSight/blob/c8103df9d14badcfc85e50c0a27daeee6cb3f973/docs/PIPELINE_ORCHESTRATION.md | Wider fingerprinting pages versus bounded semantic pages; context and opportunity/package boundaries; hardcoded 223-evaluation terminal requirement not appropriate for the new profile. |
| M2 | https://github.com/KeenSight-GTM/Master_Signals_App_KeenSight/blob/c8103df9d14badcfc85e50c0a27daeee6cb3f973/src/ai_first_signal_engine/runtime/fingerprint_registry.py | Inspected lines 1–225: separate approved/known registry and weighted matcher schema. Use as an input adapter if needed, not a competing runtime registry. |
| M3 | https://github.com/KeenSight-GTM/Master_Signals_App_KeenSight/blob/c8103df9d14badcfc85e50c0a27daeee6cb3f973/docs/LLM_ENFORCEMENT.md | Inspected lines 1–135: policy-enforced client, provider registration, conservative atomic budget reservation and trace boundary. Raw plugin code is not sandboxed. |
| D1 | https://scrapling.readthedocs.io/en/latest/fetching/dynamic.html | DynamicFetcher and sessions; page_setup before navigation, page_action after; optional XHR capture. Characterize behavior on pinned version rather than assuming every latest-page feature. |
| D2 | https://scrapling.readthedocs.io/en/latest/fetching/stealthy.html | Separate browser fetcher family; implementation must apply its own source-policy and fallback decisions. |

## Missing inputs and intentional non-assumptions

The workbook references a separate `99_MASTER_ALL` / 25-vertical footprint library. That catalog is not in the supplied workbook. A broader approximately 2,500-signature target has been discussed, but the files reviewed here do not establish that those definitions were delivered. These are catalog-completion dependencies, not reasons to delay the capture and rule-import implementation.

Provider access approvals, actual credentials, authorized recipient/destination settings and a new organization name/administration grant were not supplied for execution. This plan assumes they are provisioned by the relevant implementation phase; it does not invent them or create repositories.

GitHub review identified source and interface reuse candidates. The current scanner pins Scrapling 0.4.15; we propose retaining that starting pin until the compatibility suite justifies a change. We did not claim it is the latest release.

## Verification performed

- Source workbook imported and all 11 sheets read with artifact_tool.
- Exactly 38 unique command rows preserved and annotated; original source row values retained.
- v4.1 generation check and validation passed.
- v4.1 tests: 588 passed in 16.60 seconds in this runtime.
- Plan checker verifies phase acyclicity, all 38 source IDs, original row preservation, module/phase ownership, end-to-end phase reachability and complete 52-ledger ID preservation.
- No new live-site scan, provider request, rule promotion, repository write or send was performed.
