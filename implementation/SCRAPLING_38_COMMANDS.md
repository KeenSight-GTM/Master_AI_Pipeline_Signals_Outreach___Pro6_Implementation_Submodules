# All 38 workbook commands: implementation traceability

**Source:** `Scrapling_Fingerprint_Command_Suite(2).xlsx`, `02_COMMAND_CATALOG`, rows 2–39. The 11-sheet workbook supplies 38 commands; it does not supply the `99_MASTER_ALL` footprint catalog referenced by CATALOG_LOAD. Original row values are retained verbatim in `command_plan.json` and `WORKBOOK_SOURCE.md`.

All command IDs are preserved. All are planned components of `scrapling-ingestion`; 6 first appear in the minimal P1 slice and 32 in P2, with the complete suite gated at P2. These are planned handlers and acceptance cases, not a claim that this handoff contains their runtime implementation.

`COMPLETE_WITH_NO_MATCH` or zero extracted elements is distinct from `FAILED`, `BLOCKED`, `SKIPPED_POLICY`, `SKIPPED_BUDGET` and `NOT_APPLICABLE`. A conditional browser command need not run on every host, but the reason it was not selected is auditable. All 17 extractors run on applicable retained usable HTML; lack of a tag is an empty successful extraction, not an unreported omission.

| ID | Workbook row | First phase | Owner submodule | Output |
| --- | --- | --- | --- | --- |
| CATALOG_LOAD | 2 | P2 | rules.import_compile | RulePack + compile report |
| NORM_URL | 3 | P1 | intake.url_identity | NormalizedTarget |
| FETCH_STATIC | 4 | P1 | transport.http | AcquisitionAttempt + Artifact |
| FETCH_STEALTH | 5 | P2 | transport.browser | Browser capture + network artifacts |
| FETCH_SITEMAP | 6 | P2 | discovery.sitemaps | Sitemap artifacts + discovered resources |
| FETCH_ROBOTS | 7 | P1 | policy.robots | Policy decision + robots artifact |
| FETCH_WELL_KNOWN | 8 | P2 | discovery.path_probes | Attempted-path ledger + artifacts |
| DISCOVER_TEMPLATES | 9 | P2 | discovery.template_planner | Bounded URL plan |
| DISCOVER_CANONICAL | 10 | P2 | intake.redirect_binding | Resource identity/binding candidates |
| EXTRACT_RAW_HTML | 11 | P1 | extraction.raw_html | Raw artifact + match view |
| EXTRACT_SCRIPT_SRC | 12 | P2 | extraction.scripts | Script surface records |
| EXTRACT_SCRIPT_INLINE | 13 | P2 | extraction.scripts | Inline script records |
| EXTRACT_IFRAME_SRC | 14 | P2 | extraction.embeds | Embed surface records |
| EXTRACT_FORM_ACTION | 15 | P2 | extraction.forms | Form surface records |
| EXTRACT_ANCHORS | 16 | P2 | extraction.links | Link surface records |
| EXTRACT_IMAGES | 17 | P2 | extraction.images | Image and badge surface records |
| EXTRACT_LINKS_META | 18 | P2 | extraction.metadata | Link/meta surface records |
| EXTRACT_JSONLD | 19 | P2 | extraction.structured_data | JSON-LD blocks + parsed graph |
| EXTRACT_MICRODATA | 20 | P2 | extraction.structured_data | Microdata/RDFa surface records |
| EXTRACT_FOOTER | 21 | P2 | extraction.regions | Footer region records |
| EXTRACT_HEADER_NAV | 22 | P2 | extraction.regions | CTA region records |
| EXTRACT_DATA_ATTRS | 23 | P2 | extraction.attributes | Attribute surface records |
| EXTRACT_NOSCRIPT | 24 | P2 | extraction.noscript | Noscript surface records |
| EXTRACT_VISIBLE_TEXT | 25 | P2 | extraction.prose | Text spans + role context |
| EXTRACT_URL_FEATURES | 26 | P2 | extraction.url_features | URL/path surface records |
| EXTRACT_HEADERS | 27 | P1 | capture.headers_cookies | Header/cookie surface records |
| MATCH_SUBSTRING | 28 | P2 | matching.literal | FingerprintMatch |
| MATCH_OR_GROUP | 29 | P2 | matching.groups | FingerprintMatch |
| MATCH_REGEX | 30 | P2 | matching.regex | FingerprintMatch |
| MATCH_HOST_SUFFIX | 31 | P2 | matching.host | FingerprintMatch |
| MATCH_FOOTER_LITERAL | 32 | P2 | matching.regions | FingerprintMatch |
| MATCH_IMG_ALT | 33 | P2 | matching.images | FingerprintMatch |
| GATE_AND | 34 | P2 | qualification.vertical_guards | VerticalQualification |
| GATE_SCHEMA | 35 | P2 | qualification.schema_support | SchemaAssessment |
| GATE_NEGATIVE | 36 | P2 | ranking.negative_policy | DeprioritizationAssessment |
| ROLLUP_HOST | 37 | P2 | aggregation.host_index | HostEvidenceIndex + HostResult |
| SCORE_HOST | 38 | P2 | ranking.priority | PriorityAssessment |
| EMIT | 39 | P1 | output.scan_bundle | ScanBundle + HostResult/Hit projections |

## CATALOG_LOAD

**Source:** `02_COMMAND_CATALOG` row 2; original phase `FETCH`. **Execution scope:** job.

**Proposed behavior:** Compile an approved JSON/JSONL release; offline workbook/source adapters feed the same typed rules. No XLSX parsing on every page.

**Acceptance boundary:** Missing 99_MASTER_ALL, ambiguous OR/guard text, duplicate IDs, unknown operators or incompatible versions are explicit import failures, not executable guesses.

## NORM_URL

**Source:** `02_COMMAND_CATALOG` row 3; original phase `FETCH`. **Execution scope:** input.

**Proposed behavior:** Keep original URL and path/query; normalize scheme/host, IDNA and fragment; validate public destination and ports.

**Acceptance boundary:** Reject userinfo tricks, private/link-local destinations, unsafe schemes and redirect escapes. Preserve meaningful path/query case.

## FETCH_STATIC

**Source:** `02_COMMAND_CATALOG` row 4; original phase `FETCH`. **Execution scope:** request.

**Proposed behavior:** Scrapling HTTP is the default; attach attempt identity, policy and budget before each network request.

**Acceptance boundary:** A 200 challenge, 304 without retained body, truncated response or transport error is not complete usable HTML. Count failed attempts and redirects.

## FETCH_STEALTH

**Source:** `02_COMMAND_CATALOG` row 5; original phase `FETCH`. **Execution scope:** conditional request.

**Proposed behavior:** Retain the workbook ID as the browser-fallback command; record actual DynamicFetcher or approved StealthyFetcher strategy and reason.

**Acceptance boundary:** 429 causes backoff, not stealth escalation. Empty shells may justify rendering. Do not cross authentication/access restrictions. Every navigation and subrequest is bounded.

## FETCH_SITEMAP

**Source:** `02_COMMAND_CATALOG` row 6; original phase `FETCH`. **Execution scope:** host.

**Proposed behavior:** Capture XML or retained non-success response; safely parse indexes/urlsets, deduplicate and limit child depth and entry counts.

**Acceptance boundary:** Sitemap counts are declared URL counts, not verified products/jobs. Bound compressed/decompressed size and reject external entities and disallowed targets.

## FETCH_ROBOTS

**Source:** `02_COMMAND_CATALOG` row 7; original phase `FETCH`. **Execution scope:** origin.

**Proposed behavior:** Consult cached or newly fetched robots policy before crawling target content; also extract Sitemap directives.

**Acceptance boundary:** This deliberately supersedes the workbook's 'sitemaps only' use. Failed retrieval is handled by an explicit policy, never a business absence.

## FETCH_WELL_KNOWN

**Source:** `02_COMMAND_CATALOG` row 8; original phase `FETCH`. **Execution scope:** host.

**Proposed behavior:** Deduplicated, ranked same-host candidate probes using the supplied template slots; reserve requests before issuance.

**Acceptance boundary:** A probe is fetched once and its body reused. 404 is scoped path evidence, not missing software. Record paths skipped by budget or policy.

## DISCOVER_TEMPLATES

**Source:** `02_COMMAND_CATALOG` row 9; original phase `DISCOVER`. **Execution scope:** seed/host.

**Proposed behavior:** Rank same-host links using all workbook slots; preserve deep input seed and separately consider home.

**Acceptance boundary:** External ATS/portal links are retained as evidence but require a separately approved source scope before following.

## DISCOVER_CANONICAL

**Source:** `02_COMMAND_CATALOG` row 10; original phase `DISCOVER`. **Execution scope:** page.

**Proposed behavior:** Record input, requested and final URLs, validated redirect chain, canonical claims and subject binding separately.

**Acceptance boundary:** A canonical tag alone cannot merge organizations or extend crawl scope. Exact accepted host scope is distinct from registrable-domain grouping.

## EXTRACT_RAW_HTML

**Source:** `02_COMMAND_CATALOG` row 11; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Retain original captured bytes in permitted storage; create a separate normalized match view with encoding and truncation metadata.

**Acceptance boundary:** Do not overwrite source bytes with lowercase/errors=ignore. Raw/comment matches alone cannot prove active deployment.

## EXTRACT_SCRIPT_SRC

**Source:** `02_COMMAND_CATALOG` row 12; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Extract per-element script URLs, parsed hosts and paths with precise evidence locators.

**Acceptance boundary:** A script from an agency example or unbound frame must not become the site's product deployment.

## EXTRACT_SCRIPT_INLINE

**Source:** `02_COMMAND_CATALOG` row 13; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Preserve scoped inline-script text and stable declared globals; never execute it in the static path.

**Acceptance boundary:** Keep values carrying keys/tokens out of routine exports; arbitrary 'AI' or library text is not product proof.

## EXTRACT_IFRAME_SRC

**Source:** `02_COMMAND_CATALOG` row 14; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Retain iframe, embed and object URLs with embedding-page and frame attribution.

**Acceptance boundary:** Capture reference does not authorize external/private portal navigation; do not combine different tenant frames.

## EXTRACT_FORM_ACTION

**Source:** `02_COMMAND_CATALOG` row 15; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Read form action, method and relevant attributes as metadata without submitting.

**Acceptance boundary:** No form submissions. An action/reference is not a verified backend CRM connection.

## EXTRACT_ANCHORS

**Source:** `02_COMMAND_CATALOG` row 16; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Retain node-level href, text, role and same-host/outbound classification.

**Acceptance boundary:** Keep anchor evidence distinct from loaded scripts. Mention, login link, appointment CTA and publisher credit require different mappings.

## EXTRACT_IMAGES

**Source:** `02_COMMAND_CATALOG` row 17; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Read each image's src/alt together; retain badge claim and element context.

**Acceptance boundary:** A displayed badge is a website assertion, not independent accreditation. Do not pair separate truncated src/alt arrays.

## EXTRACT_LINKS_META

**Source:** `02_COMMAND_CATALOG` row 18; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Read per-node link and meta attribute tuples, preserving duplicates and provenance.

**Acceptance boundary:** Do not independently zip name/content arrays or collapse conflicting meta values without a record.

## EXTRACT_JSONLD

**Source:** `02_COMMAND_CATALOG` row 19; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Retain every bounded raw block plus parsed object/array/@graph, local subject references and parse errors.

**Acceptance boundary:** Malformed blocks are not silently absent. Parsed graph identity must be retained; regex hints cannot stand in for a successful parse.

## EXTRACT_MICRODATA

**Source:** `02_COMMAND_CATALOG` row 20; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Read itemtype and typeof with item scope and parent/node identity.

**Acceptance boundary:** A type belonging to an embedded article or third party is not the site's organization classification.

## EXTRACT_FOOTER

**Source:** `02_COMMAND_CATALOG` row 21; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Extract and deduplicate footer/copyright nodes with text, HTML and role attribution.

**Acceptance boundary:** A 'powered by' or agency link may identify a site provider, not software owned or used internally by the prospect.

## EXTRACT_HEADER_NAV

**Source:** `02_COMMAND_CATALOG` row 22; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Preserve header/nav and CTA nodes with URL, text, element and role.

**Acceptance boundary:** Use approved public interactions only for rendered controls; no login, booking, payment or other state-changing action.

## EXTRACT_DATA_ATTRS

**Source:** `02_COMMAND_CATALOG` row 23; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Use parsed attributes first, with bounded regex only as raw candidate discovery.

**Acceptance boundary:** Whitespace, quoting and case fixtures; fake attribute text in comments/prose does not qualify as a real node.

## EXTRACT_NOSCRIPT

**Source:** `02_COMMAND_CATALOG` row 24; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Retain nested fallback markup with an explicit noscript scope and original locator.

**Acceptance boundary:** Fallback code is not evidence that a request executed in the rendered session.

## EXTRACT_VISIBLE_TEXT

**Source:** `02_COMMAND_CATALOG` row 25; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Use a text view excluding scripts/styles and mark static DOM text separately from browser-visible text.

**Acceptance boundary:** For prose rules only; not the sole technology surface. Do not label regex tag stripping as true browser visibility.

## EXTRACT_URL_FEATURES

**Source:** `02_COMMAND_CATALOG` row 26; original phase `EXTRACT`. **Execution scope:** page.

**Proposed behavior:** Parse path, query keys and relevant discovered link features; retain resource identity.

**Acceptance boundary:** Query values containing personal data or secrets are restricted/redacted; /jobs is a path, not a job count.

## EXTRACT_HEADERS

**Source:** `02_COMMAND_CATALOG` row 27; original phase `EXTRACT`. **Execution scope:** response.

**Proposed behavior:** Preserve status and safe header pairs, repeated headers and cookie names for each response; a host summary can reuse them.

**Acceptance boundary:** Transport observations must retain response provenance. Cookie values and secrets are not normal fingerprint exports.

## MATCH_SUBSTRING

**Source:** `02_COMMAND_CATALOG` row 28; original phase `MATCH`. **Execution scope:** rule/surface.

**Proposed behavior:** Case policy is explicit; match an allowed, bounded surface item and record the actual token/location.

**Acceptance boundary:** No generic raw substring shortcut for hostname authority; case-sensitive paths/IDs remain case-sensitive when required.

## MATCH_OR_GROUP

**Source:** `02_COMMAND_CATALOG` row 29; original phase `MATCH`. **Execution scope:** rule/surface.

**Proposed behavior:** Evaluate typed ANY alternatives while retaining original row semantics, matched branch and evidence.

**Acceptance boundary:** Do not split quoted phrases or arbitrary natural-language guards on every occurrence of OR.

## MATCH_REGEX

**Source:** `02_COMMAND_CATALOG` row 30; original phase `MATCH`. **Execution scope:** rule/surface.

**Proposed behavior:** Run compiled, allowlisted, resource-bounded patterns over their declared surfaces.

**Acceptance boundary:** Prefer parsed JSON-LD and attributes. Regex compilation alone is not timeout/cost safety.

## MATCH_HOST_SUFFIX

**Source:** `02_COMMAND_CATALOG` row 31; original phase `MATCH`. **Execution scope:** rule/URL.

**Proposed behavior:** Parse actual hostname; exact equality or dot-delimited suffix against the declared hostname; use PSL only for separate normalization.

**Acceptance boundary:** Reject notvendor.com, vendor.com.evil, vendor in path/query, and vendor.com@evil. Do not collapse a specific cdn hostname to its parent.

## MATCH_FOOTER_LITERAL

**Source:** `02_COMMAND_CATALOG` row 32; original phase `MATCH`. **Execution scope:** rule/region.

**Proposed behavior:** Match the actual footer region first. Raw fallback produces a lower-authority mention candidate unless region binding is established.

**Acceptance boundary:** Do not automatically turn footer provider credits into prospect product-use facts.

## MATCH_IMG_ALT

**Source:** `02_COMMAND_CATALOG` row 33; original phase `MATCH`. **Execution scope:** rule/element.

**Proposed behavior:** Match image alt or a verified element-local badge context.

**Acceptance boundary:** Whole-page raw fallback is candidate evidence only. Displayed credential is not credential verification.

## GATE_AND

**Source:** `02_COMMAND_CATALOG` row 34; original phase `GATE`. **Execution scope:** host/rule.

**Proposed behavior:** Evaluate compiled guard conditions over same-subject, same-run host evidence; retain all contributing locators.

**Acceptance boundary:** The workbook's named AND gate uses ANY among listed OR terms. Do not suppress a valid generic vendor observation when vertical qualification fails.

## GATE_SCHEMA

**Source:** `02_COMMAND_CATALOG` row 35; original phase `GATE`. **Execution scope:** host/rule.

**Proposed behavior:** Evaluate relevant bound schema types as contextual support, with missing/contradictory/ambiguous outcomes.

**Acceptance boundary:** No schema is not a failure; wrong or unbound type is a warning/confound, not an automatic negative.

## GATE_NEGATIVE

**Source:** `02_COMMAND_CATALOG` row 36; original phase `GATE`. **Execution scope:** host.

**Proposed behavior:** Apply a versioned commercial-deprioritization policy while preserving every underlying match.

**Acceptance boundary:** Commercial negatives neither retract facts nor count as operational DNC restrictions.

## ROLLUP_HOST

**Source:** `02_COMMAND_CATALOG` row 37; original phase `ROLLUP`. **Execution scope:** host.

**Proposed behavior:** Accumulate a provenance-preserving host index before gates; finalize the same index after all pages/commands terminate.

**Acceptance boundary:** Do not concatenate into anonymous strings, cross host/subject scope, or discard duplicate rule supports. Two modes avoid the workbook ordering ambiguity.

## SCORE_HOST

**Source:** `02_COMMAND_CATALOG` row 38; original phase `ROLLUP`. **Execution scope:** host.

**Proposed behavior:** Compute an explainable, versioned scan/commercial priority separate from detection confidence and fact authority.

**Acceptance boundary:** The workbook does not specify numerical weights. Mark proposed weights uncalibrated; never use score to promote a candidate fact.

## EMIT

**Source:** `02_COMMAND_CATALOG` row 39; original phase `ROLLUP`. **Execution scope:** host/run.

**Proposed behavior:** Write versioned ScanBundle with attempts, artifacts, coverage, surface index, matches, qualifiers, score and per-command outcomes; retain legacy host/hit projections.

**Acceptance boundary:** No-hit, incomplete and failed states remain distinct; write atomically/idempotently. HostResult alone cannot serve as the fact evidence store.

## Ordering

Registry load and request planning are job/host operations, not per-page selectors. The finite crawl loop expands seed and followup capture stages. We do not force repeated command IDs into a false acyclic graph.

```text
Load/pin catalog → normalize/authorize target → robots/policy → static seed
  → optional permitted browser fallback
  → canonical/redirect record + all applicable extraction
  → discover/probe bounded followups → capture/extract each once
  → provenance-preserving host accumulation
  → typed matcher evaluation → vertical/schema/negative assessments
  → final host rollup + score → emit
```

`ROLLUP_HOST` has accumulate/finalize operations under the same original ID: accumulation precedes host gates; finalization follows them. `MATCH_OR_GROUP` orchestrates typed alternatives rather than unconditionally trying unrelated operators. Header observations are retained per response even when a host-level summary uses the first applicable result.
