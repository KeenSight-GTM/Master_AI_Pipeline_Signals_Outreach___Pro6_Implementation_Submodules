# POC-focused standard-usage audit — September 15, 2026

## Verdict

The unchanged collector 0.2.0 and canonical reference 4.2.0 still have obstacles on ordinary feature paths. The most urgent newly reproduced defect is that an otherwise valid two-page scan can fail solely because the run ID changes the ordering of capture hashes. Other obstacles concern robots redirects, resuming after rate limits, sitemap handling, fingerprint-research read models, multi-account reporting, and numeric claim comparison.

This is an audit and executable POC acceptance package, **not a patched runtime release**. It separates defects from deliberately restrictive policies and missing capabilities. It does not revisit the entire future sales platform or claim to test unimplemented modules.

## Basis and verification

Basis: the `baseline/` in the user's latest Iteration 2 review archive, retaining collector 0.2.0, canonical 4.2.0, protocol checker, and product design. All 438 manifest-listed baseline files still match their original hashes. No GitHub reads/writes, live site scans, provider calls, model calls, CRM changes, or sends occurred.

| Check | Observed result | Meaning |
|---|---:|---|
| Collector existing suite | 183 passed, 1 skipped | Pinned Scrapling SDK remains unavailable. |
| Canonical existing suite | 609 passed | Reference code, schemas, and synthetic fixtures. |
| Protocol existing suite | 42 passed | Existing narrow checker, not an enforcing runtime. |
| New standard-usage probes | 17 executed | Nine POC findings, three separately classified existing limitations, five controls. |
| New POC acceptance suite | 9 failed, 5 passed | Explicit desired requirements; includes missing capabilities, not just bugs. No xfail hides failures. |
| Reviewed-preview journey J07 | Passed; three subprocesses | Synthetic canonical generation check, validation, and local export; **not** a collector-to-canonical integration test. |
| Baseline integrity | 438 files match | No application-source patch. |

The main two-page probe includes ten fixed run-ID cases. Four fail, six pass. This is an illustrative constructed corpus demonstrating order dependence, **not a 40% estimate of live failure rate**.

The nine failures below are not nine security vulnerabilities or nine equivalent severities. P0 means block a basic trusted POC; P1 means complete or explicitly exclude the affected journey. A restrictive safety policy should not be removed merely to improve coverage.

## Findings

### POC-01 — Normal multi-page scans can fail depending on capture hash order

**Priority:** P0. **Classification:** confirmed implementation bug. **Flow:** scan → extract → match → validate → publish.

**Ordinary scenario:** a homepage and contact page both contain the same Calendly script. The homepage links to the contact page. Both pages are fetched successfully. Only the logical run ID changes between ten independent fixture scans.

**Result:** four scans raise `ContractError: Rule execution outcomes do not reproduce`. The remaining six succeed. Failed evaluations correctly publish zero observations; the previous validate-before-publication repair still protects this path.

**Cause:** `Scanner.evaluate()` calls `match_pages()` in visit order but serializes `evaluated_capture_ids` in sorted-hash order. `validate_bundle()` rebuilds pages in that latter order. `match_pages()` accumulates each rule's `match_ids` and errors in page traversal order, and validation compares the report arrays exactly. The set of findings agrees; their list order does not.

**Source:** `collector/src/keensight_scrapling/pipeline.py:198–245`; `rules.py:139–195`; `validation.py:36–61`.

**Required repair:** define one canonical order for set-like fields in rule evaluation reports, including match IDs and error records; keep actual execution chronology in a separate ordered trace. Reuse the canonicalization at production and validation. Do not simply remove report validation. Check duplicate inputs before normalization.

**POC exit:** any permutation of the same valid page set and any run identity produce equivalent semantic outputs and validate. Repeating/replaying the scan must retain one claim with all evidence, without double-counting origins.

### POC-02 — A same-origin redirect of robots.txt prevents all content collection

**Priority:** P1. **Classification:** missing acquisition capability with a fail-closed outcome. **Flow:** URL intake → robots policy → static fetch.

**Scenario:** `/robots.txt` returns HTTP 301 to `/policy/robots.txt` on the exact same public origin. The target file permits the site.

**Result:** the only request is the initial robots URL. No redirect target or homepage is fetched. The scan returns zero claims and a `ROBOTS_UNAVAILABLE_FAIL_CLOSED` limitation. By contrast, the existing homepage redirect path follows a same-origin HTTP 302 and detects the marker.

**Cause:** the initial robots request bypasses the redirect handling in the subsequent page/sitemap queue; `robots_policy()` rejects statuses other than 200/404/410.

**Source:** `pipeline.py:60–136`; `discovery.py:13–20`; compare `pipeline.py:152–158`.

**Repair:** share a bounded, budgeted redirect resolver across robots and content requests. Recheck destination policy on every hop; detect loops; retain hop attempts and policy outcomes. Failure must remain a crawl-policy failure, not permission to crawl anyway.

**Exit:** the allowed same-origin redirect works; private destinations, forbidden origins, loops, and exhausted redirect budgets remain blocked.

### POC-03 — Resume still reports rate limiting after the cooldown expires

**Priority:** P1, required for live recovery. **Classification:** recovery/status inconsistency; safe retry capability also missing. **Flow:** initial scan → 429 → wait → resume.

**Scenario:** the homepage responds 429 with `Retry-After: 3600`. After two hours, the fixture endpoint is healthy and the persistent cooldown is no longer active. The same run/configuration is resumed.

**Result:** zero new attempts, zero claims, and another `SKIPPED_RATE_LIMIT` disposition. The stored 429 response is reused and reasserts `denied=True` unconditionally.

**Cause:** completed HTTP-failure attempts are immutable, keyed only by URL/mode. The resumed request branch treats every reused 429 as an active limit regardless of the stored cooldown. There is no separate operator-controlled retry attempt.

**Source:** `pipeline.py:60–82,110–122`; `storage.py:69–83`.

**Repair:** distinguish historical attempt outcome from current cooldown. A completed acquisition record must remain immutable. Add an explicit bounded retry operation or retry policy that creates a new attempt with a `retry_of` reference after permission/budget checks. Do not blindly retry uncertain effectful operations; this finding concerns retrieval, not sending. Ordinary resume may intentionally reproduce old results, but must not label an expired cooldown as current or imply recovery occurred.

**Exit:** active cooldown blocks new attempts; expired cooldown is no longer reported active; an explicit retry can recover the failed resource without re-fetching every successful page or rewriting prior evidence.

### POC-04 — A supplied .xml.gz sitemap is treated as invalid XML

**Priority:** P1 when sitemap discovery is in the POC. **Classification:** missing discovery capability. **Flow:** robots → sitemap acquisition → discovery.

**Scenario:** robots points to a gzip-compressed sitemap served as `application/gzip`; its only contact URL contains the tested script. The ordinary `/sitemap.xml` path returns 404.

**Result:** `FETCH_SITEMAP` reports PARTIAL with `Invalid or unsafe sitemap XML`, and the contact URL is never discovered.

**Cause:** sitemap bytes go directly to the XML parser. There is no handling for a gzip file body. This test concerns a stored gzip file, not HTTP content-encoding decompression by the HTTP library.

**Source:** `discovery.py:23–35`; `pipeline.py:162–171`.

**Repair:** detect allowed compression; retain compressed bytes and decode into a derived artifact with explicit lineage. Bound decompressed bytes, expansion ratio, entries, and nesting before parsing. Preserve the secure XML parser. Reject malformed or oversized archives with truthful incomplete coverage.

**Exit:** the bounded compressed fixture yields the contact URL; corrupt data and expansion attacks remain safely rejected.

### POC-05 — Sitemap traversal bypasses the declared template priority

**Priority:** P1. **Classification:** planner inconsistency / recall gap. **Flow:** discovery → bounded page selection.

**Scenario:** the homepage contains no direct contact link. A sitemap lists two blog pages, privacy, terms, and finally contact. Contact alone contains the tested booking script. Default `max_pages=5` is used.

**Result:** homepage plus the first four sitemap entries consume the page limit. Contact is explicitly `SKIPPED_PAGE_LIMIT`; no claim is found. A paired control with a homepage contact link does fetch it before the low-priority sitemap entries.

**Cause:** `template_links()` ranks anchors, but sitemap URLs are directly appended to the FIFO queue in source order. Discovery channels therefore use different selection policies.

**Source:** `discovery.py:38–43`; `pipeline.py:139–195`.

**Repair:** merge discovered candidates into a stable prioritized frontier before scheduling. Apply role priorities and quotas regardless of discovery channel; preserve discovery provenance and skipped-reason reports. A total request budget alone is not a relevance strategy. Do not raise budgets just to mask selection order.

**Exit:** high-value contact/careers/integrations pages are selected under the declared profile before lower-priority material, within unchanged request/page limits.

### POC-06 — Imported candidate detections become UNKNOWN in the claims CLI

**Priority:** P1. **Classification:** read-model inconsistency. **Flow:** import donor → scan → `claims`.

**Scenario:** import a supported host-equality rule using an explicit product map; it remains CANDIDATE. Scan evidence matches it. Query the same store with the exact imported pack.

**Result:** scan bundle says `CANDIDATE`; `ks-scan claims` exits 0 but says `UNKNOWN`. All supporting match IDs remain, and no support is production eligible. No unauthorized approval occurs.

**Cause:** the CLI constructs its current release allowlist from APPROVED definitions only. Candidate rules are removed before the resolver decides whether usable shadow support exists.

**Source:** `cli.py:115–117`; `claims.py:63–76`; `storage.py:177–184`.

**Repair:** distinguish `present in the pinned/current release` from `eligible for approved support`. Expose candidate state without contributing to eligible evidence, commercial priority, or confidence. A removed/disabled rule should be distinguishable from a current candidate.

**Exit:** bundle and query agree on candidate state; current approved support remains empty; disabling/removing a rule is auditable and does not silently promote or retain it.

### POC-07 — Newly recognized features stay in the unresolved research queue

**Priority:** P1. **Classification:** stale derived research projection. **Flow:** unknown feature → reviewed rule → replay → research queue.

**Scenario:** scan the page with an empty fixture pack, producing an unknown `assets.calendly.com` feature. Replay the same stored capture with the existing approved fixture rule.

**Result:** the replay produces a supported claim, but `candidates(min_hosts=1)` returns the same unresolved-looking feature and counts, with no resolved/historical status.

**Cause:** `harvest()` skips newly matched surfaces but does not reconcile previously stored unmatched rows. `candidates()` has no join to the current rule release or its match evaluations.

**Source:** `storage.py:186–208,211–250`.

**Repair:** retain raw occurrence history, but compute unresolved-candidate eligibility against a specified rule release, capture capabilities, and revocation policy. Add dispositions such as unresolved/resolved/historical and sufficient evidence references to review them. Replay/promotion should update the current read model, not delete history.

**Relation to prior audit:** Iteration 2 F10 already found missing revocation handling. This is a distinct normal promotion/replay reproduction of the same broader need for a release/policy-aware research view, not a claim of wholly independent infrastructure.

**Exit:** a fully recognized feature is not presented as new unresolved work; demotion/new unknown variants remain visible; history remains retrievable.

### POC-08 — The multi-account claims query omits the account

**Priority:** P1 for a multi-account POC. **Classification:** output-contract / usability gap, not lost data. **Flow:** scan multiple accounts → tenant-wide claims query.

**Scenario:** two accounts on different origins each have a Calendly observation. Run `ks-scan claims` for the tenant.

**Result:** two distinct rows are returned, but neither contains `subject_id`, `scope_id`, origin, or observation time. They differ only by opaque identities/support IDs. Account identity is correctly retained in the underlying observations; there is no cross-account merge.

**Cause:** `ClaimView` omits the fields required for an account-facing report; the CLI has no `--subject` filter or record-inspection operation that expands the opaque observation references.

**Source:** `core.py:139–155`; `claims.py:70–76`; `cli.py:60–61,115–117`.

**Repair:** version the claim read model to include tenant/subject/scope, relevant resource origins, last eligible observation and expiry, and rule-policy identity. Add account filtering and a support drilldown. Keep the detailed observations authoritative.

**Exit:** a two-account operator can attribute every reported claim without querying SQLite manually; no inference of ownership from hash values is necessary.

### POC-09 — Equal numeric values can produce a false canonical conflict

**Priority:** P1 for measurement-based signals. **Classification:** reference-comparator bug; isolated helper test, not full live admission.

**Scenario:** the same typed traffic measurement is represented once with `value: 12000` and once with `value: 12000.0`. Both pass the Fact and dispatched predicate value schemas and have identical claim identity. The claim resolver is called with both eligible.

**Result:** `CONFLICT` with no accepted facts. Controls show that two integer 12000 values are KNOWN, and genuinely unequal 12000/13000 values correctly conflict.

**Cause:** equivalence is based on serialized whole-object JSON; integer and floating representations produce different byte strings.

**Source:** `canonical/keensight_contracts/engine.py:24–29,37–44,86–98`.

**Repair:** keep original evidence bytes and content hashes intact, but compare a predicate/metric-normalized semantic value. Define exact quantity equality, units, missing values, and any domain-specific tolerance separately. Do not globally coerce booleans into numbers, round unrelated metrics, or equate different reporting periods/providers.

**Exit:** numerically equal compatible observations agree, genuinely different measurements conflict, and raw provenance remains unchanged.

## Existing policies and scope limits — not reclassified as new bugs

### POLICY-01: HTTP/HTTPS and bare/www canonical redirects

Exact-origin policy blocks `https://shop.example.test/` redirecting to `https://www.shop.example.test/`. The code intentionally restricts origins; removing that restriction would weaken safety. For a useful POC, either require operator-supplied final canonical URLs and report unsupported aliases clearly, or implement explicitly approved alias transitions with destination, DNS, robots, ownership, and per-hop checks. Mere string-suffix similarity is not sufficient.

### POLICY-02: Every script inside a footer is rejected as presence

The tested syntactically active script is detected in the body but not inside `<footer>`. This follows existing attribution policy, not an implementation regression. Decide whether an executable first-party page element should be distinguishable from agency credit text in the footer. Static markup does not prove actual execution or private product usage. Any change needs agency/comment/inert negative fixtures and shared canonical/collector semantics.

### SCOPE-01: analyze-file is a one-snapshot run

Adding a second URL with the same subject/run is rejected because URL/time are pinned in the run configuration. This differs from previously reported changed-subject acceptance: the subject here is unchanged. Preserve this explicit single-snapshot contract unless adding a real multi-snapshot import manifest. For now use distinct runs; do not promise that two independent imported files are a shared same-scan snapshot.

## Controls that still work

1. Same-origin homepage redirects consume the budget and can reach the detection.
2. Homepage-discovered contact links precede later FIFO sitemap additions.
3. Exact same numeric serialization resolves as known.
4. Genuinely unequal measurements conflict.
5. Replaying an unrelated rule-release change increases audited match executions but does not increase the observation count, element evidence count, source groups, or confidence. This is retained audit history, not a newly alleged duplicate-fact bug.

## POC implementation decision

A POC should prove a small **real** path:

`permitted target → static capture → reproducible surfaces/matches → collector observations → canonical admission → resolved claim → one enabled opportunity → reviewed no-send preview`.

The broad catalog remains available. Do not require all connectors, all compound ideas, cohorts, browser automation, campaigns, sending, replies, or CRM to finish before this path works. Conversely, do not call a synthetic preview an integrated POC; the executable collector-to-canonical bridge is still missing.

### Recommended work order

1. **Stabilize ordinary scanning:** POC-01, policy-aware robots redirect handling, truthful completed/failed target status, and a bounded safe-retrieval retry path.
2. **Improve useful discovery within budget:** merge/rank candidates; add bounded gzip sitemap support or explicitly exclude it. Freeze behavior in controlled fixtures.
3. **Make research and results usable:** release-aware candidate state, promotion reconciliation, account-attributed claim views. Do not change evidence authority to improve counts.
4. **Finish the single vertical slice:** verify the pinned SDK, implement the canonical bridge, share normalized numeric/support/claim helpers, and use one reviewed observation-led template.
5. **Close previously reported decision-boundary defects needed by that slice:** binding-evidence closure; template authority at export; one validated publication object; generated-artifact availability; historical/current separation; producer and invocation identity. These remain open and are not counted again here.

### Real POC sign-off

- Multi-page results do not depend on run-ID hashes or traversal order.
- Redirect, timeout, denial, malformed-content, rate-limit and no-match outcomes are distinguishable.
- An operator can recover a retryable capture without guessing whether it succeeded.
- A small controlled corpus plus permitted live sample is executed with the actual pinned Scrapling SDK, not a substitute HTTP implementation.
- Every account report identifies the account and links exact evidence; candidate observations remain visibly unapproved.
- The capture-to-canonical bridge produces an admitted, conflict-aware fact from actual collector support.
- A reviewed preview is derived from those admitted inputs and current-use checks, without fixture transcripts standing in for the integration.
- No automatic sending or uncontrolled source access is enabled.

The archive contains reproducible acceptance tests. Nine currently fail; the five controls pass. These tests are a focused repair target, not evidence that missing features have been implemented.
