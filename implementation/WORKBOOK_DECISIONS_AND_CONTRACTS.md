# Explicit corrections and contract deltas

This document distinguishes the supplied workbook from the proposed implementation. All 38 commands are kept. The changes below resolve contradictions or preserve the v4.1 evidence boundaries; they are proposals to encode during implementation, not changes silently attributed to the workbook.

| Decision | Source location | Original concern | Proposed resolution | Acceptance |
| --- | --- | --- | --- | --- |
| D01 — Budget ambiguity | 00_README row 7; 08_TEMPLATE_PATHS row 2; 09_PSEUDOCODE row 3 | Workbook alternates between about eight GETs, eight HTML GETs, and counting only successful HTML pages. | Propose a conservative fast profile with max_top_level_attempts=8 across seed/home, robots/sitemaps, probes, redirects, retries and browser navigations. Reserve before issuing; a failed request still consumes the attempt. Browser subrequests have a separate explicit count/byte/time cap. An expanded profile may deliberately allow eight HTML targets and a larger total request cap, with a different profile hash. | A host with only 404s or retries stops at the configured budget; skipped probe paths are NOT_VISITED, not absent. |
| D02 — Robots and source policy precede content | 01_RUN_ORDER steps 1 and 4; 02_COMMAND_CATALOG FETCH_ROBOTS | The workbook uses robots only to discover sitemaps after a first page. | Consult an explicit cached/fetched robots and source-policy decision before content acquisition. A robots acquisition is itself separately budgeted and logged. Failed policy checks have defined denial/unknown behavior; do not infer facts from them. | A denied path is not fetched and does not satisfy NOT_FOUND coverage. |
| D03 — Rate limits versus permitted browser fallback | 01_RUN_ORDER step 1b; FETCH_STEALTH row | The run order escalates 403/429; the command notes also mention empty shells. | 429 schedules backoff or terminates within budget, not a stealth bypass. Empty shells may use a standard renderer. Preserve FETCH_STEALTH as the original command ID while recording actual engine and fallback reason. Source/access policy must permit any alternative fetch; no authentication/permission boundary is bypassed. | 429 cannot automatically invoke a browser; a JS-only fixture can use approved rendering and reports its mode. |
| D04 — Rollup ordering | 01_RUN_ORDER steps 6 and 7; 04_PER_HOST | Host matching and gates need the union, but final ROLLUP_HOST is listed afterward. | Use one host accumulator and two ROLLUP_HOST modes: accumulate/freeze input index before gates, finalize result afterward. A bounded seed/followup loop is not a cyclic computation graph. | A valid guard on a second allowed page is found; a guard on an unrelated subject is not borrowed. |
| D05 — Detection, vertical qualification and commercial priority | GATE_AND; GATE_NEGATIVE; SCORE_HOST | The workbook can drop unmatched vertical guards and labels negatives for outbound priority. | Keep the raw technology observation independently of vertical qualification. Preserve negative evidence and attach only a commercial deprioritization assessment. Score is not detection probability or production authority. | CallRail without family-law evidence remains a technical observation but does not label the account Family Law. |
| D06 — Hostname and weak-surface semantics | 07_MATCH_RULES rows 5, 6, 9 and 10 | Raw HTML/comment fallback is recommended alongside structured URL matching. | Use exact parsed hosts or dot-delimited subdomains for host rules. Keep raw/comment/vendor-name occurrences as mentions/candidates unless a registered rule establishes active-node and subject attribution. Partial/back-office rows require the declared public link/embed/form surface. | Lookalikes, path/query host text, comments and agency-footers do not support a product-deployment claim. |
| D07 — Typed guards, not executable prose | CATALOG_LOAD; 07_MATCH_RULES rows 4 and 8 | Search String and False-Positive Guard are free-text OR expressions. | Compile once using a quoted-token-aware importer into bounded ANY/ALL groups with explicit scope. Ambiguous prose stays quarantined with a row-level diagnostic. Do not introduce a general expression language or eval. | Quoted phrases survive import; malformed guards cannot be silently interpreted as no guard. |
| D08 — Raw bytes, parsed structure and original scopes | EXTRACT_RAW_HTML; EXTRACT_JSONLD; MATCH_REGEX | Lowercased/error-ignored raw text and flattened types are convenient match bags. | Store original permitted bytes separately; preserve encoding/truncation, full JSON-LD blocks and graphs, parsed node identities, and each extraction error. Regex is a bounded hint, not proof of valid parsed structure. | A malformed JSON-LD block yields an explicit parse limitation, not schema absence. |
| D09 — Redirect/canonical identity | DISCOVER_CANONICAL | Fingerprint the final host, not the redirector. | Adopt only validated redirects; retain requested/final resource identity and treat canonical tags as claims. Do not merge companies or pool subdomains solely because an eTLD+1 or canonical string matches. | A malicious cross-domain canonical cannot rebind the target or extend allowed acquisition. |
| D10 — Confidence and browser provenance | 07_MATCH_RULES rows 11 and 13 | The catalog supplies Verified/Likely labels and suggests JS-only findings are weaker. | Preserve authored confidence as metadata. Store capture mode and matching evidence separately from calibration and authority. Browser-only evidence is not automatically false or weak; it is observed under a particular mode and requires appropriate calibration. | Neither Verified metadata nor SCORE_HOST can promote an unreviewed rule. |
| D11 — Declared budget and complete scan semantics | FETCH_WELL_KNOWN; 09_PSEUDOCODE | All probe paths are suggested but the crawl must remain bounded; pseudocode risks refetching successes. | Rank candidate paths, fetch each permitted unique request once, reuse its body for extraction, and emit explicit terminal dispositions for unattempted resources. Successful capture plus successful detector is needed for scoped non-detection. | The loop never spends a second GET merely to extract a previously captured successful probe. |
| D12 — Adaptive selectors and hash-like markers | 07_MATCH_RULES row 15; donor extractors | No React hashes/data-reactroot as vendor evidence; the donor also extracts classes and IDs. | Retain stable, registered element markers where justified, but do not infer vendor identity from arbitrary React hashes. Any adaptive selector recovery is recorded and must be validated or treated as a candidate; it cannot silently change a detector. | Markup drift cannot silently upgrade an approximate/adapted match into approved production evidence. |
| D13 — API compatibility and resource blocking | Workbook Scrapling call examples | The workbook is an execution specification, not tested compatibility evidence for a pinned SDK. | Characterize every response property/selector/fetch hook against the locked Scrapling/browser versions. Turn off default ad blocking for fingerprint evidence when permitted, or record the blocked surfaces as unobserved. Never assume a network trace is complete merely because DOM load finished. | Pinned-version browser and static contract tests verify hooks, retention, time bounds and capture limitations. |

## Contract delta before full command activation

The current v4.1 `FingerprintDefinition` is deliberately narrow: one product, one emitted predicate, one capture mode and one operator chosen from SCRIPT_HOST, IFRAME_HOST, FORM_HOST, COOKIE_NAME, HEADER_VALUE, DNS_TARGET, JSON_VALUE and ATTRIBUTE_VALUE. That is not sufficient to losslessly represent the entire workbook or the donor's full rule language. Do not put unsupported meanings into `match_value`, raise confidence, or drop guards to make an import pass.

Use a versioned capture/rule extension with typed definitions and compatibility tests. Existing public schemas must receive a proper version transition where required fields or meanings change.

### Reuse existing contracts

Reuse `IntakeRequest`, `AcquisitionAttempt`, `Artifact`, `EvidenceLocator`, `EvidenceSet`, `Scope`, `BatchRun`, `ExecutionRecord`, `CoverageRecord`, `Fact`, `ClaimResolution`, `CandidateRecord`, `ReviewDecision`, `UseGateDecision` and `ExportReceipt`.

Do not fabricate a company subject to satisfy a field before binding is resolved. A scanner's operational action can finish with artifacts and diagnostics but no admitted fact.

### Add or extend small capture-local contracts

| Proposed contract | Essential fields and semantics |
| --- | --- |
| `CommandSpec` | Original command ID; versioned handler ID; allowed scope; typed arguments; input/output kinds; capture requirements; conditional selection; fixture IDs. |
| `ScanPlan` | Tenant/trusted principal; intake/targets; validated origin scope; direct seed/home policy; release lock; capture profile; request/browser limits; source purposes. |
| `CommandExecution` | Scan/command/version; scoped input references; start/finish/status/reason; emitted artifact/surface/match references; request counters. Fact-producing work also links to the normative producing execution. |
| `CaptureResult` | Attempt, requested/final URLs, redirect chain, actual engine/mode, original response and optional DOM/trace artifact references, encoding, truncation, blocked resources and policy decisions. |
| `SurfaceEvidence` / `PageEvidenceIndex` | Original artifact/locator, exact surface type, parsed value, node/frame/region identity, subject binding or unresolved role; no anonymous concatenation. |
| `HostEvidenceIndex` | Exact accepted host/subject scope, run input cut, page/surface references and per-surface completeness; never ownership inferred solely from a registrable domain. |
| `FingerprintRuleSpec` | ID/version/import provenance; typed matcher alternatives; same-element/page/host correlation requirements; target/emission schema; required capture capabilities; vertical guards kept apart; authority/calibration/fixtures. |
| `FingerprintMatch` | Rule and release, exact matched alternatives/surfaces/locators, binding, capture mode, eligibility and limitations. Preserve all supports even when a display row is deduplicated. |
| `ScanBundle` | Manifest, complete attempts/artifacts/command outcomes, bindings, surface index, matches, capture/detection coverage, failed/skipped resources and HostResult/Hit compatibility projections. |
| `FingerprintCandidate` / `RuleRelease` | Versioned normalized feature, scoped prevalence and sample references, proposed definition and review; immutable approved content and test/calibration/revocation records. Existing CandidateRecord/review contracts can back this rather than duplicating authority. |

These are DTO/record families, not new deployed services. Prefer composition or explicit artifact references over creating a second universal event journal. Match/operator fields are closed and handler-specific; no arbitrary Python/javascript supplied by a catalog is executed.

### Fact emission distinctions

- `technology.script`, `technology.form_action`, `technology.cookie`, `technology.header`, `technology.csp`, `technology.network_request` and `technology.footprint` can hold correctly scoped evidence.
- `vendor.mentioned` differs from `vendor.present`; public capability links map to `portal.observed` or `integration.public_marker` as appropriate.
- `schema.jsonld.present`, `schema.jsonld.types` and `schema.subject_binding` require the appropriate parse/attribution rules.
- Displayed badges are attributed claims, not independent license/credential verification.
- `GATE_NEGATIVE` and `SCORE_HOST` produce selection assessments, not business truth or DNC facts.
- Per-rule mapped claims cannot use unsupported predicates or promote a candidate source. Source/function/rule release and producer input closure must all resolve.
- One capture mode cannot claim completion of another. If multi-modal rules need multiple coverage records, introduce a typed composition or versioned coverage-reference list; do not pretend one raw-HTML CoverageRecord proves network or DNS absence.

### Cross-cutting requirements from v4.1

Retain A–E, G and H: successful producing execution and per-target completion; exact input closure; whole-claim conflict handling; complete sample denominators; capture-plus-detector coverage; no-byte failure; profile/review/current-use/handoff gates. Schedule F's missing ChangeRecord authorization and replacement checks in P4, before hosted writes or multi-tenant production.

Raw capture may contain personal data or secrets. Source-specific policies govern whether it may be retained, encrypted/restricted, redacted or processed by a model. Store safe derived surfaces for ordinary use and preserve exact evidence locators into the permitted retained version. Do not claim deleted/unavailable raw data is still replayable.

## Execution invariants

A schema or compiled matcher does not establish actual source access or detector accuracy. Host detection scores cannot alter source authority. Cross-host/cross-tenant pooling requires explicit authorization. Fallback, retry and replay do not extend original observation freshness. A raw fingerprint is an observation of a surface, not a conclusion about a private company's operations.
