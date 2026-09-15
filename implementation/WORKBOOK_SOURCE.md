# Workbook source transcription

This is a value transcription of the supplied workbook, not corrected instructions. Proposed changes are in the plan.
Source file SHA-256: `285558c8e4b40007c956cd5557f88f053f978702e86c6facdc430f26e9e1d807`.


## 00_README

**Row 1**

```json
[
  "Scrapling fingerprint command suite"
]
```

**Row 2**

```json
[
  "Direct-URL detector for the 25-vertical AI SEO Footprint Library. No Common Crawl. Every command below is something Scrapling must execute on a page or host. Runtime: Fetcher.get (static HTML) by default; StealthyFetcher only on block."
]
```

**Row 4**

```json
[
  "How to read this workbook"
]
```

**Row 5**

```json
[
  "01_RUN_ORDER is the exact sequence. 02_COMMAND_CATALOG is the full command list (id, phase, Scrapling call, selectors, output). 03_PER_PAGE is what runs on EVERY fetched HTML page. 04_PER_HOST is what runs once per hostname. 05_SURFACE_MAP ties each command to fingerprint classes in the library. 06_SELECTORS is copy-paste Scrapling CSS/XPath. 07_MATCH_RULES is how a catalog row becomes a hit. 08_TEMPLATE_PATHS is the same-host follow pack."
]
```

**Row 6**

```json
[
  "Hard rules"
]
```

**Row 7**

```json
[
  "1) Search raw HTML + tag attributes, never visible text alone. 2) Do not ignore <script> / <iframe> — that is where most vendors live. 3) Default fetcher is HTTP static (Fetcher). JS render is a fallback and must be flagged. 4) Match the UNION of pages on a host, then apply AND-terms at host level. 5) Cap ~8 GETs per host. 6) Partial/back-office vendors only count if a public URL/iframe/login is present."
]
```

**Row 8**

```json
[
  "Input / output"
]
```

**Row 9**

```json
[
  "IN: list of direct page URLs or hostnames + the footprint catalog rows. OUT per host: pages_fetched, script_hosts[], iframe_hosts[], outbound_hosts[], schema_types[], footer_text, path_features[], hits[]."
]
```

## 01_RUN_ORDER

**Row 1**

```json
[
  "Execution order",
  null,
  null,
  null,
  null,
  null
]
```

**Row 2**

```json
[
  "Run top to bottom. Commands in the same step can be parallel. Do not skip EXTRACT before MATCH.",
  null,
  null,
  null,
  null,
  null
]
```

**Row 4**

```json
[
  "Step",
  "Scope",
  "Command IDs",
  "When",
  "Success criteria",
  "On failure"
]
```

**Row 5**

```json
[
  "0",
  "Job",
  "CATALOG_LOAD",
  "Once at start",
  "All needles compiled into tokens + regex + AND-terms",
  "Abort job"
]
```

**Row 6**

```json
[
  "1",
  "Input URL",
  "NORM_URL, FETCH_STATIC",
  "Every input URL",
  "HTTP 200–399 and a body",
  "If 403/429 → step 1b; else record miss and stop host"
]
```

**Row 7**

```json
[
  "1b",
  "Input URL",
  "FETCH_STEALTH",
  "Only if static fetch blocked",
  "200–399; set js_rendered=True",
  "Mark host unreachable"
]
```

**Row 8**

```json
[
  "2",
  "This page",
  "EXTRACT_* suite (see 03_PER_PAGE)",
  "Every successful GET",
  "Haystacks built: raw, attrs, jsonld, footer, text, url",
  "Skip MATCH on this page; continue host"
]
```

**Row 9**

```json
[
  "3",
  "This page",
  "DISCOVER_TEMPLATES",
  "Homepage or first page of host",
  "0–8 same-host follow URLs queued",
  "Continue with well-known probes only"
]
```

**Row 10**

```json
[
  "4",
  "Host",
  "FETCH_WELL_KNOWN + FETCH_SITEMAP + FETCH_ROBOTS",
  "Once per host after first page",
  "Each path tried; 404 is a valid negative",
  "Ignore individual 404s"
]
```

**Row 11**

```json
[
  "5",
  "Host",
  "FETCH_STATIC on discovered templates",
  "Each queued URL, cap 8 total GETs",
  "Additional EXTRACT_* bags merged into host union",
  "Drop that URL"
]
```

**Row 12**

```json
[
  "6",
  "Host",
  "MATCH_* + GATE_AND + GATE_SCHEMA + GATE_NEGATIVE",
  "After all pages for the host",
  "Hit list with surface + and_term_ok",
  "Emit empty hit list"
]
```

**Row 13**

```json
[
  "7",
  "Host",
  "ROLLUP_HOST, SCORE_HOST, EMIT",
  "End of host",
  "One result object written",
  "Write partial result"
]
```

## 02_COMMAND_CATALOG

**Row 1**

```json
[
  "Command ID",
  "Phase",
  "Name",
  "Scrapling call",
  "Required args",
  "Exact selector / pattern",
  "Returns",
  "Required on every page?",
  "Notes"
]
```

**Row 2**

```json
[
  "CATALOG_LOAD",
  "FETCH",
  "Load fingerprint catalog",
  "openpyxl / pandas read of footprint xlsx (not Scrapling)",
  "path to 99_MASTER_ALL",
  "n/a",
  "list[{vertical,vendor,tokens[],and_terms[],surface,priority,confidence}]",
  "Once",
  "Split Search String on OR. Lowercase tokens. Keep quoted phrases intact."
]
```

**Row 3**

```json
[
  "NORM_URL",
  "FETCH",
  "Normalize input URL",
  "urllib.parse.urlparse + urlunparse",
  "raw input",
  "Add https:// if missing; strip fragment; keep path+query",
  "{scheme,host,origin,url}",
  "Every input",
  "If input is a bare host, set path to /."
]
```

**Row 4**

```json
[
  "FETCH_STATIC",
  "FETCH",
  "HTTP GET static HTML",
  "Fetcher.get(url, impersonate='chrome', stealthy_headers=True)",
  "url",
  "n/a",
  "Response: status, body, headers, cookies, history, encoding",
  "Every URL",
  "Primary fetcher. Matches view-source / static-HTML fingerprints."
]
```

**Row 5**

```json
[
  "FETCH_STEALTH",
  "FETCH",
  "Blocked-host fallback",
  "StealthyFetcher.fetch(url, headless=True, network_idle=True)",
  "url",
  "n/a",
  "Response + js_rendered=True",
  "Only on 403/challenge/empty shell",
  "May invent JS-only tags. Never the default."
]
```

**Row 6**

```json
[
  "FETCH_SITEMAP",
  "FETCH",
  "GET /sitemap.xml",
  "Fetcher.get(origin + '/sitemap.xml')",
  "origin",
  "n/a",
  "XML text or 404",
  "Once per host",
  "Replaces CC sitemap index. Count <sitemap> and product/job <loc>."
]
```

**Row 7**

```json
[
  "FETCH_ROBOTS",
  "FETCH",
  "GET /robots.txt",
  "Fetcher.get(origin + '/robots.txt')",
  "origin",
  "Sitemap: lines",
  "Extra sitemap URLs",
  "Once per host",
  "Only used to find more sitemaps. Do not parse crawl-delay as a fingerprint."
]
```

**Row 8**

```json
[
  "FETCH_WELL_KNOWN",
  "FETCH",
  "Probe known paths",
  "Fetcher.get(origin + path) for each path in 08_TEMPLATE_PATHS",
  "origin, path list",
  "See 08_TEMPLATE_PATHS",
  "200 pages go through EXTRACT_*; 404 recorded as path_missing",
  "Once per host",
  "Do not wait for a homepage link. Booking/portal/financing often unlinked from nav."
]
```

**Row 9**

```json
[
  "DISCOVER_TEMPLATES",
  "DISCOVER",
  "Collect same-host follow URLs",
  "page.css('a[href]::attr(href)') then urljoin",
  "current page",
  "a[href]",
  "queue of same-host URLs scored by template keywords",
  "First page of host",
  "Keep only same host. Score paths containing book|schedule|contact|financ|portal|login|job|member|wholesale|inventory|pricing|demo."
]
```

**Row 10**

```json
[
  "DISCOVER_CANONICAL",
  "DISCOVER",
  "Canonical + redirect host",
  "page.css('link[rel=canonical]::attr(href)'); page.history",
  "response",
  "link[rel='canonical']",
  "final_host, canonical_url",
  "Every page",
  "Fingerprint the final host, not the input redirector."
]
```

**Row 11**

```json
[
  "EXTRACT_RAW_HTML",
  "EXTRACT",
  "Full source haystack",
  "page.body.decode(page.encoding or 'utf-8', errors='ignore').lower()",
  "response",
  "n/a — raw bytes",
  "hay_raw: str",
  "YES",
  "Primary haystack. Required for data-* attributes and inline snippets."
]
```

**Row 12**

```json
[
  "EXTRACT_SCRIPT_SRC",
  "EXTRACT",
  "External script hosts",
  "page.css('script[src]::attr(src)')",
  "page",
  "script[src]",
  "list of absolute script URLs + registrable hosts",
  "YES",
  "Highest-yield command. CallRail, HubSpot, Klaviyo, Schedule Engine, Shopify, Stripe, Intercom, Chili Piper."
]
```

**Row 13**

```json
[
  "EXTRACT_SCRIPT_INLINE",
  "EXTRACT",
  "Inline script text",
  "page.css('script:not([src])::text')",
  "page",
  "script:not([src])",
  "inline JS text joined",
  "YES",
  "Catches copied widget snippets, Magento_ namespaces, NexHealth paste, data-api-key Schedule Engine bootstraps."
]
```

**Row 14**

```json
[
  "EXTRACT_IFRAME_SRC",
  "EXTRACT",
  "Iframes / embeds",
  "page.css('iframe[src]::attr(src)'); page.css('embed[src]::attr(src)'); page.css('object[data]::attr(data)')",
  "page",
  "iframe[src], embed[src], object[data]",
  "embed URLs + hosts",
  "YES",
  "Boulevard, Jane, Vetstoria, Clio Grow, Lawmatics, GemFind, hotel booking engines, ATS job boards."
]
```

**Row 15**

```json
[
  "EXTRACT_FORM_ACTION",
  "EXTRACT",
  "Form endpoints",
  "page.css('form[action]::attr(action)'); page.css('form[data-hs-cf-bound]')",
  "page",
  "form[action]",
  "action URLs",
  "YES",
  "Intake CRMs, LawPay pay-now, HubSpot forms that post to hsforms."
]
```

**Row 16**

```json
[
  "EXTRACT_ANCHORS",
  "EXTRACT",
  "Outbound + internal links",
  "page.css('a[href]::attr(href)')",
  "page",
  "a[href]",
  "abs URLs split into same_host[] and outbound_hosts[]",
  "YES",
  "LawPay, Allē, ASPIRE, GIA reportcheck, AAML/AILA, patient portals, CareCredit apply."
]
```

**Row 17**

```json
[
  "EXTRACT_IMAGES",
  "EXTRACT",
  "Badge images + alt text",
  "page.css('img[src]::attr(src)'); page.css('img[alt]::attr(alt)')",
  "page",
  "img[src], img[alt]",
  "image hosts + alt strings",
  "YES",
  "Invisalign Provider, Super Lawyers, Avvo, Allergan/Galderma Elite, Rolex Official Retailer."
]
```

**Row 18**

```json
[
  "EXTRACT_LINKS_META",
  "EXTRACT",
  "link + meta tags",
  "page.css('link[href]::attr(href)'); page.css('meta')",
  "page",
  "link[rel], meta[name], meta[property], meta[content]",
  "canonical, og:url, shopify-digital-wallet, generator",
  "YES",
  "Shopify meta name=shopify-digital-wallet. og:url often still has myshopify.com."
]
```

**Row 19**

```json
[
  "EXTRACT_JSONLD",
  "EXTRACT",
  "JSON-LD blocks",
  "page.css('script[type=\"application/ld+json\"]::text') then json.loads",
  "page",
  "script[type='application/ld+json']",
  "list of objects; flatten @type (string or list) into schema_types[]",
  "YES",
  "Product, JobPosting, LegalService, Hotel, LodgingBusiness, Dentist, MedicalClinic, Physician, Car, DietarySupplement."
]
```

**Row 20**

```json
[
  "EXTRACT_MICRODATA",
  "EXTRACT",
  "Microdata itemtype",
  "page.css('[itemtype]::attr(itemtype)'); page.css('[typeof]::attr(typeof)')",
  "page",
  "[itemtype], [typeof]",
  "schema.org type URLs",
  "YES",
  "Fallback when JSON-LD is missing but itemtype='https://schema.org/Dentist' exists."
]
```

**Row 21**

```json
[
  "EXTRACT_FOOTER",
  "EXTRACT",
  "Footer credit strip",
  "page.css('footer'); page.css('[class*=footer]'); page.css('[id*=footer]'); page.css('[class*=copyright]')",
  "page",
  "footer, [class*='footer'], [id*='footer'], [class*='copyright']",
  "footer_html + footer_text",
  "YES",
  "Sesame / PBHS / Officite / ProSites / Clubessential / Powered by LawPay / DSO copyright."
]
```

**Row 22**

```json
[
  "EXTRACT_HEADER_NAV",
  "EXTRACT",
  "Header + nav CTAs",
  "page.css('header'); page.css('nav'); page.css('[class*=book]'); page.css('[class*=portal]')",
  "page",
  "header, nav, a:contains-ish via href keywords",
  "CTA hrefs (Book, Portal, Pay, Members)",
  "YES",
  "Finds booking/portal even when they are buttons rather than iframes."
]
```

**Row 23**

```json
[
  "EXTRACT_DATA_ATTRS",
  "EXTRACT",
  "data-* vendor markers",
  "regex on hay_raw",
  "hay_raw",
  "data-calltrk[-a-z]*=|data-api-key=|id=['\\\"]se-widget-embed['\\\"]|name=['\\\"]shopify-digital-wallet['\\\"]",
  "marker names found",
  "YES",
  "CallRail noswap, Schedule Engine embed id, Shopify wallet meta."
]
```

**Row 24**

```json
[
  "EXTRACT_NOSCRIPT",
  "EXTRACT",
  "noscript fallback HTML",
  "page.css('noscript') → html_content",
  "page",
  "noscript",
  "extra HTML often containing iframe pixels",
  "YES",
  "Some review/chat vendors leave a noscript iframe."
]
```

**Row 25**

```json
[
  "EXTRACT_VISIBLE_TEXT",
  "EXTRACT",
  "Prose haystack (secondary)",
  "page.get_all_text(separator=' ', strip=True, ignore_tags=('script','style'))",
  "page",
  "n/a",
  "hay_text",
  "YES — secondary only",
  "Use ONLY for prose fingerprints (iTero, flat fee divorce, Allē Rewards, initiation fee). Never as the only haystack."
]
```

**Row 26**

```json
[
  "EXTRACT_URL_FEATURES",
  "EXTRACT",
  "Path + query features",
  "urlparse(page.url or request url)",
  "url",
  "path, query keys",
  "path, query_keys[], facet_flags",
  "YES",
  "/products /jobs /members /wholesale /inventory /pricing /security /case-studies /quick-order; query color|size|page."
]
```

**Row 27**

```json
[
  "EXTRACT_HEADERS",
  "EXTRACT",
  "HTTP headers + cookies",
  "page.headers; page.cookies",
  "response",
  "Set-Cookie, X-*, server",
  "header map, cookie names",
  "First 200 of host is enough",
  "Only Magento Mage-Cache-SessId and similar. Do not require this for other rows."
]
```

**Row 28**

```json
[
  "MATCH_SUBSTRING",
  "MATCH",
  "Case-insensitive contains",
  "token in hay_raw or hay_struct",
  "token, haystacks",
  "plain lowercase token",
  "bool + surfaces[]",
  "Every catalog row",
  "Default matcher for vendor hosts: cdn.callrail.com, js.hs-scripts.com, joinblvd.com."
]
```

**Row 29**

```json
[
  "MATCH_OR_GROUP",
  "MATCH",
  "Any token of an OR row",
  "any(tok in hay for tok in tokens)",
  "tokens[]",
  "Split Search String on OR",
  "bool + which token",
  "Every catalog row",
  "Row hits if ANY alternative token hits."
]
```

**Row 30**

```json
[
  "MATCH_REGEX",
  "MATCH",
  "Structured regex",
  "re.search(pattern, hay_raw, I)",
  "pattern",
  "@type\"\\s*:\\s*\"(Product|JobPosting|LegalService|Hotel|Car|Dentist|MedicalClinic)\"",
  "match groups",
  "Schema + attribute rows",
  "Use for JSON-LD types and data-* markers, not for vendor names."
]
```

**Row 31**

```json
[
  "MATCH_HOST_SUFFIX",
  "MATCH",
  "URL host equals vendor",
  "registrable_domain(url) == vendor_host or endswith '.'+vendor_host",
  "extracted URLs",
  "e.g. callrail.com, boulevard.io, shopify.com",
  "bool",
  "S1/S2/S3 rows",
  "Prevents 'notcallrail.com' false prefix hits. Prefer this over raw substring for hosts."
]
```

**Row 32**

```json
[
  "MATCH_FOOTER_LITERAL",
  "MATCH",
  "Footer phrase",
  "phrase in footer_html or footer_text",
  "footer bags",
  "Powered by Sesame Communications | Powered by Clubessential | Powered by LawPay",
  "bool",
  "Footer-credit rows",
  "Search footer bags first; fall back to hay_raw."
]
```

**Row 33**

```json
[
  "MATCH_IMG_ALT",
  "MATCH",
  "Badge alt / nearby text",
  "any(needle in alt.lower() for alt in img_alts) or needle in hay_raw",
  "img alts",
  "Invisalign Provider | Super Lawyers | Official Rolex Retailer",
  "bool",
  "Badge rows",
  "Alt first, then raw HTML for CSS background badges with no alt."
]
```

**Row 34**

```json
[
  "GATE_AND",
  "GATE",
  "False-positive AND-term",
  "if and_terms: any(t in host_hay_raw or host_hay_text for t in and_terms) else True",
  "host union haystacks, and_terms[]",
  "From catalog column False-Positive Guard",
  "and_term_ok bool",
  "Every hit",
  "CallRail without divorce|custody|family law is not Family Law. Skip gate when catalog says none needed."
]
```

**Row 35**

```json
[
  "GATE_SCHEMA",
  "GATE",
  "Vertical schema confirm",
  "intersection(schema_types, expected_types_for_vertical)",
  "schema_types[]",
  "See 05_SURFACE_MAP expected schema",
  "schema_ok bool or None if no schema present",
  "When JSON-LD exists",
  "Absence of schema is NOT a fail. Presence of the wrong type is a warning."
]
```

**Row 36**

```json
[
  "GATE_NEGATIVE",
  "GATE",
  "Deprioritize filters",
  "MATCH against negative-vendor list",
  "host union",
  "synxis.com, golfnow.com, teeoff.com, hilton.com/book, marriott.com/reservation, national DSO names",
  "deprioritize bool + reasons[]",
  "Every host",
  "Keep evidence; drop outbound priority."
]
```

**Row 37**

```json
[
  "ROLLUP_HOST",
  "ROLLUP",
  "Union page bags",
  "set unions across pages of host",
  "page extracts[]",
  "n/a",
  "host record with unique script_hosts, iframe_hosts, outbound_hosts, schema_types, paths, footer",
  "Once per host",
  "Matching is host-level, not page-level, except for recording page_found_on."
]
```

**Row 38**

```json
[
  "SCORE_HOST",
  "ROLLUP",
  "Priority score",
  "rules on hit set",
  "hits[]",
  "exclusive vendor + and_term_ok = high; generic pixel only = medium; negative = low",
  "score, priority_label",
  "Once per host",
  "Use catalog Priority for outbound as the base weight."
]
```

**Row 39**

```json
[
  "EMIT",
  "ROLLUP",
  "Write result",
  "json / csv / sheet append",
  "host record",
  "n/a",
  "One row per host, plus one row per hit",
  "Once per host",
  "Persist pages_fetched and js_rendered so Verified vs Likely can be audited."
]
```

## 03_PER_PAGE

**Row 1**

```json
[
  "Commands that MUST run on every fetched HTML page",
  null,
  null,
  null,
  null
]
```

**Row 2**

```json
[
  "If a GET returns HTML (content-type text/html or body starts with <), run this list in order. XML sitemaps use 04_PER_HOST sitemap parser instead.",
  null,
  null,
  null,
  null
]
```

**Row 4**

```json
[
  "Seq",
  "Command ID",
  "Writes into",
  "Skip if",
  "Fingerprint classes fed"
]
```

**Row 5**

```json
[
  "1",
  "DISCOVER_CANONICAL",
  "final_url, final_host",
  "non-HTML",
  "host identity"
]
```

**Row 6**

```json
[
  "2",
  "EXTRACT_RAW_HTML",
  "hay_raw",
  "empty body",
  "ALL substring needles, data-* markers"
]
```

**Row 7**

```json
[
  "3",
  "EXTRACT_SCRIPT_SRC",
  "script_urls[], script_hosts[]",
  "no script tags",
  "CallRail, HubSpot, Klaviyo, Attentive, Shopify, Stripe, Intercom, Drift, Qualified, Segment, Chili Piper, Calendly, Schedule Engine, Cloudbeds, Marketo, 6sense, Demandbase, Yotpo, Algolia, Affirm"
]
```

**Row 8**

```json
[
  "4",
  "EXTRACT_SCRIPT_INLINE",
  "inline_js",
  "no inline scripts",
  "NexHealth snippets, Magento_ namespaces, Schedule Engine bootstrap, widget configs"
]
```

**Row 9**

```json
[
  "5",
  "EXTRACT_IFRAME_SRC",
  "iframe_urls[], iframe_hosts[]",
  "no iframes",
  "Boulevard, Jane, Vetstoria, Clio Grow, Lawmatics, GemFind, hotel BE, ATS career portals"
]
```

**Row 10**

```json
[
  "6",
  "EXTRACT_FORM_ACTION",
  "form_actions[]",
  "no forms",
  "HubSpot forms, LawPay, intake CRMs"
]
```

**Row 11**

```json
[
  "7",
  "EXTRACT_ANCHORS",
  "same_host_links[], outbound_hosts[], outbound_urls[]",
  "no anchors",
  "LawPay, Allē, ASPIRE, GIA, AAML, AILA, NAELA, CareCredit, patient portals, OurFamilyWizard"
]
```

**Row 12**

```json
[
  "8",
  "EXTRACT_IMAGES",
  "img_srcs[], img_alts[]",
  "no images",
  "Invisalign, Super Lawyers, Avvo, manufacturer Elite badges, authorized dealer marks"
]
```

**Row 13**

```json
[
  "9",
  "EXTRACT_LINKS_META",
  "canonical, metas{}",
  "none",
  "Shopify wallet meta, myshopify og:url, generator"
]
```

**Row 14**

```json
[
  "10",
  "EXTRACT_JSONLD",
  "jsonld[], schema_types[]",
  "no JSON-LD",
  "Product, JobPosting, LegalService, Hotel, Car, Dentist, MedicalClinic, DietarySupplement"
]
```

**Row 15**

```json
[
  "11",
  "EXTRACT_MICRODATA",
  "microdata_types[]",
  "no itemtype",
  "same schema types when JSON-LD absent"
]
```

**Row 16**

```json
[
  "12",
  "EXTRACT_FOOTER",
  "footer_html, footer_text",
  "no footer node (still search hay_raw)",
  "Sesame, PBHS, Officite, ProSites, Clubessential, Powered by LawPay, DSO copyright"
]
```

**Row 17**

```json
[
  "13",
  "EXTRACT_HEADER_NAV",
  "cta_hrefs[]",
  "no header",
  "Book / Portal / Pay / Members buttons"
]
```

**Row 18**

```json
[
  "14",
  "EXTRACT_DATA_ATTRS",
  "markers[]",
  "none — always regex hay_raw",
  "data-calltrk-noswap, se-widget-embed, shopify-digital-wallet"
]
```

**Row 19**

```json
[
  "15",
  "EXTRACT_NOSCRIPT",
  "noscript_html",
  "no noscript",
  "fallback pixels / iframes"
]
```

**Row 20**

```json
[
  "16",
  "EXTRACT_VISIBLE_TEXT",
  "hay_text",
  "none",
  "prose-only rows: iTero, flat fee divorce, Allē Rewards, PGT-A, initiation fee, net-30, WealthCounsel"
]
```

**Row 21**

```json
[
  "17",
  "EXTRACT_URL_FEATURES",
  "path, query_keys[]",
  "none",
  "IA fingerprints: /products /jobs /members /wholesale /inventory /pricing"
]
```

**Row 22**

```json
[
  "18",
  "EXTRACT_HEADERS",
  "headers, cookies",
  "optional after first page",
  "Magento Mage-Cache-SessId only"
]
```

## 04_PER_HOST

**Row 1**

```json
[
  "Commands that run once per hostname (not per page)",
  null,
  null,
  null,
  null
]
```

**Row 3**

```json
[
  "Seq",
  "Command ID",
  "Input",
  "What it does",
  "Stop condition"
]
```

**Row 4**

```json
[
  "1",
  "ROLLUP starts empty",
  "final_host from first page",
  "Open host accumulator",
  "n/a"
]
```

**Row 5**

```json
[
  "2",
  "DISCOVER_TEMPLATES",
  "first HTML page anchors",
  "Score and queue up to 8 same-host URLs",
  "Queue full or no keyword links"
]
```

**Row 6**

```json
[
  "3",
  "FETCH_WELL_KNOWN",
  "origin + 08_TEMPLATE_PATHS",
  "Probe book/contact/portal/pricing/jobs/members/wholesale even if unlinked",
  "Each path once; 404 ok"
]
```

**Row 7**

```json
[
  "4",
  "FETCH_SITEMAP",
  "origin/sitemap.xml + robots sitemaps",
  "Parse index vs urlset; count product/job locs",
  "One level of child sitemaps max (optional)"
]
```

**Row 8**

```json
[
  "5",
  "FETCH_STATIC × queued",
  "discovered + well-known that 200",
  "Run 03_PER_PAGE on each; merge bags",
  "Total HTML GETs for host ≥ 8"
]
```

**Row 9**

```json
[
  "6",
  "MATCH_OR_GROUP + MATCH_HOST_SUFFIX + MATCH_REGEX + MATCH_FOOTER_LITERAL + MATCH_IMG_ALT",
  "host union haystacks vs catalog",
  "Produce raw hit candidates",
  "Catalog exhausted"
]
```

**Row 10**

```json
[
  "7",
  "GATE_AND",
  "each candidate + host hay_raw/hay_text",
  "Drop or flag hits that fail vertical guard",
  "Done"
]
```

**Row 11**

```json
[
  "8",
  "GATE_SCHEMA",
  "schema_types vs vertical",
  "Warning only if schema contradicts vertical",
  "Done"
]
```

**Row 12**

```json
[
  "9",
  "GATE_NEGATIVE",
  "negative vendor list",
  "Set deprioritize if flag/DSO/CRS/public-tee-time stack",
  "Done"
]
```

**Row 13**

```json
[
  "10",
  "ROLLUP_HOST + SCORE_HOST + EMIT",
  "hits + bags",
  "Write host result",
  "Done"
]
```

## 05_SURFACE_MAP

**Row 1**

```json
[
  "Which command detects which fingerprint class",
  null,
  null,
  null,
  null,
  null
]
```

**Row 3**

```json
[
  "Fingerprint class (library)",
  "Primary command",
  "Secondary command",
  "Haystack",
  "Example needles",
  "AND-term typical?"
]
```

**Row 4**

```json
[
  "Script-tag vendor (CallRail, HubSpot, Klaviyo, Schedule Engine, Shopify, Stripe, Intercom, 6sense)",
  "EXTRACT_SCRIPT_SRC + MATCH_HOST_SUFFIX",
  "EXTRACT_RAW_HTML + EXTRACT_SCRIPT_INLINE",
  "script_hosts + hay_raw",
  "cdn.callrail.com | js.hs-scripts.com | embed.scheduleengine.net | cdn.shopify.com | js.stripe.com | static.klaviyo.com | j.6sc.co",
  "Yes if vendor is cross-vertical"
]
```

**Row 5**

```json
[
  "Iframe / booking engine / intake embed",
  "EXTRACT_IFRAME_SRC + MATCH_HOST_SUFFIX",
  "EXTRACT_ANCHORS + EXTRACT_HEADER_NAV",
  "iframe_hosts + cta_hrefs",
  "joinblvd.com | jane.app | vetstoria.com | grow.clio.com | hotels.cloudbeds.com | dashboard.boulevard.io",
  "Only if vendor spans verticals (Vagaro, NexHealth)"
]
```

**Row 6**

```json
[
  "Pay / portal outbound link",
  "EXTRACT_ANCHORS + MATCH_HOST_SUFFIX",
  "EXTRACT_FORM_ACTION",
  "outbound_hosts",
  "secure.lawpay.com | alle.com | aspirerewards.com | mycase.com | patientnow.com | mypatientvisit.com | reportcheck.gia.edu",
  "Yes for LawPay/CareCredit"
]
```

**Row 7**

```json
[
  "Footer builder / AMS credit",
  "EXTRACT_FOOTER + MATCH_FOOTER_LITERAL",
  "EXTRACT_RAW_HTML",
  "footer_html + footer_text",
  "Powered by Sesame Communications | Powered by PBHS | Powered by Clubessential | Powered by LawPay",
  "Usually no — vendor is exclusive"
]
```

**Row 8**

```json
[
  "Badge / award / OEM alt",
  "EXTRACT_IMAGES + MATCH_IMG_ALT",
  "EXTRACT_VISIBLE_TEXT",
  "img_alts + hay_text",
  "Invisalign Provider | Super Lawyers | Official Rolex Retailer | Allergan Partner",
  "Sometimes (Super Lawyers + family law)"
]
```

**Row 9**

```json
[
  "data-* / meta markers",
  "EXTRACT_DATA_ATTRS + EXTRACT_LINKS_META",
  "EXTRACT_RAW_HTML",
  "hay_raw + metas",
  "data-calltrk-noswap | shopify-digital-wallet | se-widget-embed",
  "No"
]
```

**Row 10**

```json
[
  "JSON-LD / schema type",
  "EXTRACT_JSONLD + MATCH_REGEX",
  "EXTRACT_MICRODATA",
  "schema_types",
  "@type Product | JobPosting | LegalService | Hotel | Car | Dentist | MedicalClinic",
  "Pair with vertical AND-term on body"
]
```

**Row 11**

```json
[
  "Prose / commercial-intent copy",
  "EXTRACT_VISIBLE_TEXT + MATCH_SUBSTRING",
  "EXTRACT_RAW_HTML",
  "hay_text",
  "flat fee divorce | Allē Rewards | iTero | initiation fee | net-30 | PGT-A | WaveLight",
  "Often the AND-term IS the needle"
]
```

**Row 12**

```json
[
  "Path / information architecture",
  "EXTRACT_URL_FEATURES + DISCOVER_TEMPLATES",
  "FETCH_WELL_KNOWN",
  "paths[]",
  "/products /jobs /members /wholesale /inventory /pricing /case-studies /quick-order",
  "No"
]
```

**Row 13**

```json
[
  "Sitemap catalog proxy",
  "FETCH_SITEMAP",
  "FETCH_ROBOTS",
  "sitemap xml",
  "<sitemapindex>, sitemap_products, job <loc> count",
  "No"
]
```

**Row 14**

```json
[
  "HTTP cookie / header only",
  "EXTRACT_HEADERS",
  "none",
  "cookies/headers",
  "Mage-Cache-SessId",
  "No"
]
```

**Row 15**

```json
[
  "Negative chain / flag / DSO",
  "EXTRACT_FOOTER + EXTRACT_IFRAME_SRC + GATE_NEGATIVE",
  "EXTRACT_ANCHORS",
  "footer + iframe_hosts",
  "synxis.com | golfnow.com | identical multi-host footer (cluster later)",
  "n/a — this IS the filter"
]
```

## 06_SELECTORS

**Row 1**

```json
[
  "Copy-paste Scrapling selectors",
  null,
  null
]
```

**Row 3**

```json
[
  "Bag name",
  "Scrapling selector(s)",
  "Post-process"
]
```

**Row 4**

```json
[
  "script_srcs",
  "page.css('script[src]::attr(src)')",
  "urljoin each; parse hostname; lowercase"
]
```

**Row 5**

```json
[
  "inline_scripts",
  "page.css('script:not([src])::text')",
  "join with newlines; lowercase copy for match"
]
```

**Row 6**

```json
[
  "iframes",
  "page.css('iframe[src]::attr(src)')",
  "urljoin; hostname"
]
```

**Row 7**

```json
[
  "embeds",
  "page.css('embed[src]::attr(src)')\npage.css('object[data]::attr(data)')",
  "same as iframes"
]
```

**Row 8**

```json
[
  "forms",
  "page.css('form[action]::attr(action)')",
  "urljoin; hostname + path"
]
```

**Row 9**

```json
[
  "anchors",
  "page.css('a[href]::attr(href)')",
  "urljoin; split same-host vs outbound; keep path"
]
```

**Row 10**

```json
[
  "img_src",
  "page.css('img[src]::attr(src)')",
  "urljoin; hostname (badge CDNs)"
]
```

**Row 11**

```json
[
  "img_alt",
  "page.css('img[alt]::attr(alt)')",
  "lowercase; keep raw for audit"
]
```

**Row 12**

```json
[
  "canonical",
  "page.css('link[rel=\"canonical\"]::attr(href)')",
  "urljoin"
]
```

**Row 13**

```json
[
  "other_links",
  "page.css('link[href]::attr(href)')",
  "urljoin (often shopify/cdn)"
]
```

**Row 14**

```json
[
  "meta_name",
  "page.css('meta[name]::attr(name)') + page.css('meta[name]::attr(content)')",
  "pair name→content; look for shopify-digital-wallet"
]
```

**Row 15**

```json
[
  "meta_prop",
  "page.css('meta[property]::attr(property)') + content",
  "og:url often exposes myshopify.com"
]
```

**Row 16**

```json
[
  "jsonld_text",
  "page.css('script[type=\"application/ld+json\"]::text')",
  "json.loads each; if list, flatten; collect @graph and @type"
]
```

**Row 17**

```json
[
  "microdata",
  "page.css('[itemtype]::attr(itemtype)')",
  "rstrip to type name after schema.org/"
]
```

**Row 18**

```json
[
  "footer_nodes",
  "page.css('footer')\npage.css('[class*=\"footer\"]')\npage.css('[id*=\"footer\"]')\npage.css('[class*=\"copyright\"]')",
  "concat .html_content and .get_all_text()"
]
```

**Row 19**

```json
[
  "header_nav",
  "page.css('header')\npage.css('nav')",
  "collect a[href] only"
]
```

**Row 20**

```json
[
  "noscript",
  "page.css('noscript')",
  ".html_content added into hay_raw"
]
```

**Row 21**

```json
[
  "visible_text",
  "page.get_all_text(separator=' ', strip=True, ignore_tags=('script','style'))",
  "lowercase; collapse whitespace"
]
```

**Row 22**

```json
[
  "raw_html",
  "page.body.decode(page.encoding or 'utf-8', errors='ignore')",
  "lowercase copy hay_raw; keep original for audit snippets"
]
```

**Row 24**

```json
[
  "Required regexes (run on hay_raw)",
  null,
  null
]
```

**Row 25**

```json
[
  "ID",
  "Regex",
  "Purpose"
]
```

**Row 26**

```json
[
  "RE_CALLTRK",
  "data-calltrk[-a-z]*",
  "CallRail DNI marker"
]
```

**Row 27**

```json
[
  "RE_SE_WIDGET",
  "id\\s*=\\s*['\\\"]se-widget-embed['\\\"]|embed\\.scheduleengine\\.net",
  "ServiceTitan Schedule Engine"
]
```

**Row 28**

```json
[
  "RE_SHOPIFY_META",
  "shopify-digital-wallet|cdn\\.shopify\\.com|myshopify\\.com",
  "Shopify platform"
]
```

**Row 29**

```json
[
  "RE_JSONLD_TYPE",
  "\"@type\"\\s*:\\s*\"([^\"]+)\"",
  "All JSON-LD types including malformed spacing"
]
```

**Row 30**

```json
[
  "RE_POWERED_BY",
  "powered by\\s+([a-z0-9 .&-]+)",
  "Footer builder catch-all"
]
```

**Row 31**

```json
[
  "RE_MAGENTO",
  "Magento_|/static/version|Mage-Cache-SessId",
  "Magento / Adobe Commerce"
]
```

**Row 32**

```json
[
  "RE_FACET",
  "[?&](color|size|page|filter)=\\w+",
  "Faceted ecom URLs on anchors"
]
```

## 07_MATCH_RULES

**Row 1**

```json
[
  "How a catalog row becomes a hit",
  null
]
```

**Row 3**

```json
[
  "Rule",
  "Definition"
]
```

**Row 4**

```json
[
  "Tokenize",
  "Split Search String on OR. Strip quotes. Lowercase. A token may be a host (cdn.callrail.com), a phrase (powered by lawpay), or a path (/on/demandware.store/)."
]
```

**Row 5**

```json
[
  "Host tokens",
  "If token looks like a domain (contains a dot, no spaces), match with MATCH_HOST_SUFFIX against script_hosts + iframe_hosts + outbound_hosts + raw URL strings. Do not use naive 'in html' only — but DO also check hay_raw because some hosts appear only in comments or JSON."
]
```

**Row 6**

```json
[
  "Phrase tokens",
  "If token contains spaces or 'powered by', run MATCH_FOOTER_LITERAL then MATCH_SUBSTRING on hay_raw and hay_text."
]
```

**Row 7**

```json
[
  "OR semantics",
  "Row hits if ANY token hits."
]
```

**Row 8**

```json
[
  "AND-term gate",
  "If False-Positive Guard is empty, 'n/a', or starts with 'none needed', and_term_ok=True. Else split guard on OR and require one token in host hay_raw or hay_text."
]
```

**Row 9**

```json
[
  "Surface preference",
  "Record which bag produced the token (script, iframe, anchor, footer, img_alt, jsonld, prose, path, header). Prefer that over a raw-html-only hit when scoring."
]
```

**Row 10**

```json
[
  "Partial rows",
  "Confidence starting with Partial: only emit if surface is iframe, anchor login, or form action. Ignore prose mention of the vendor name."
]
```

**Row 11**

```json
[
  "Verified vs Likely",
  "Does not change matcher. Store catalog confidence on the hit so you can audit later."
]
```

**Row 12**

```json
[
  "Negative rows",
  "If Priority contains 'Negative' or vendor is a known flag/DSO/public-course stack, set host.deprioritize=True and keep the hit labeled negative."
]
```

**Row 13**

```json
[
  "js_rendered flag",
  "If any page on the host used FETCH_STEALTH, set host.js_rendered=True. Hits that appear only on stealth pages and not on static pages are weaker."
]
```

**Row 14**

```json
[
  "Page attribution",
  "A host hit should list page_found_on[] so you can re-open the exact URL."
]
```

**Row 15**

```json
[
  "No JS class matching",
  "Never add commands that hunt React class hashes or data-reactroot as vendor evidence."
]
```

## 08_TEMPLATE_PATHS

**Row 1**

```json
[
  "Same-host follow pack + well-known probes",
  null,
  null,
  null,
  null
]
```

**Row 2**

```json
[
  "DISCOVER_TEMPLATES scores homepage links whose path or anchor text matches Keywords. FETCH_WELL_KNOWN additionally GETs Probe path if not already queued. Cap 8 HTML GETs per host including the seed.",
  null,
  null,
  null,
  null
]
```

**Row 4**

```json
[
  "Slot",
  "Keywords in path or link text",
  "Probe paths (try even if unlinked)",
  "Verticals that need this slot",
  "What you expect to catch"
]
```

**Row 5**

```json
[
  "Home",
  "n/a (always fetch / if seed was deep)",
  "/",
  "All",
  "Global scripts, footer, schema"
]
```

**Row 6**

```json
[
  "Book / schedule",
  "book, schedule, appointment, reserve, request-appointment, book-now",
  "/book, /schedule, /appointments, /book-now, /request-appointment",
  "Medical, home services, hotels, clubs, PT, vet, med spa",
  "Boulevard, Jane, Vetstoria, Cloudbeds, Schedule Engine, Housecall, Jobber, ForeTees"
]
```

**Row 7**

```json
[
  "Contact / offices",
  "contact, location, locations, offices, our-office",
  "/contact, /locations, /contact-us",
  "Legal, medical, home services, dealers",
  "CallRail swapped numbers, LawPay, portals"
]
```

**Row 8**

```json
[
  "Financing / pay / plans",
  "financ, pricing, membership, pay-now, patient-financing, payment",
  "/financing, /pricing, /membership, /payments",
  "Medical, legal, jewelry, home services, SaaS",
  "CareCredit, PatientFi, LawPay, Kleer, Stripe, Affirm"
]
```

**Row 9**

```json
[
  "Portal / login / members",
  "portal, login, patient, client-portal, members, member-login",
  "/patient-portal, /login, /members, /member-login, /clients",
  "Medical, legal, clubs, staffing consultants",
  "myPatientVisit, MyCase, Docketwise, Clubessential login, talent portal"
]
```

**Row 10**

```json
[
  "Services / practice area",
  "service, practice, treatment, lasik, divorce, dui, implant",
  "first 2 service links from nav — do not blindly probe",
  "Legal + specialty medical",
  "Prose AND-terms, OEM badges, charge/procedure IA"
]
```

**Row 11**

```json
[
  "Shop / inventory / products",
  "shop, product, inventory, collection, diamond",
  "/products, /inventory, /shop, /collections",
  "Ecom, jewelry, dealers",
  "Shopify/Magento, Product schema, GIA links, Car schema"
]
```

**Row 12**

```json
[
  "Jobs / careers",
  "job, jobs, career, careers, apply",
  "/jobs, /careers, /job",
  "Staffing, agencies, SaaS",
  "Bullhorn/Avionté iframe, JobPosting schema"
]
```

**Row 13**

```json
[
  "Wholesale / trade",
  "wholesale, trade, reseller, net-30, quick-order",
  "/wholesale, /pages/wholesale, /quick-order",
  "B2B ecom",
  "Gated pricing, PunchOut mentions"
]
```

**Row 14**

```json
[
  "SaaS proof pages",
  "pricing, demo, security, changelog, status, customers, case",
  "/pricing, /demo, /security, /customers",
  "B2B SaaS, agencies",
  "Chili Piper, HubSpot forms, SOC2 copy"
]
```

**Row 15**

```json
[
  "Sitemap / robots",
  "n/a",
  "/sitemap.xml, /robots.txt",
  "Ecom, staffing, dealers",
  "Catalog / job URL volume"
]
```

## 09_PSEUDOCODE

**Row 1**

```json
[
  "Reference loop (implement against 02_COMMAND_CATALOG)"
]
```

**Row 3**

```json
[
  "def fingerprint_url(seed_url, catalog):\n    host_acc = empty_host()\n    seed = NORM_URL(seed_url)\n    page, js = FETCH_STATIC(seed.url)\n    if blocked(page):\n        page, js = FETCH_STEALTH(seed.url)\n        host_acc.js_rendered = True\n    if not page: return emit_unreachable(seed)\n\n    def ingest(page):\n        bags = run_03_PER_PAGE(page)          # commands EXTRACT_* + DISCOVER_CANONICAL\n        host_acc.merge(bags)\n\n    ingest(page)\n    queue = DISCOVER_TEMPLATES(page)          # same-host, keyword-scored\n    queue += FETCH_WELL_KNOWN.paths_not_in(queue)\n    sitemap = FETCH_SITEMAP(seed.origin)\n    host_acc.sitemap = parse_sitemap(sitemap)\n    FETCH_ROBOTS(seed.origin)                 # may append sitemap URLs only\n\n    html_gets = 1\n    for url in queue:\n        if html_gets >= 8: break\n        if url_already_fetched(url): continue\n        p, _ = FETCH_STATIC(url)\n        if p and is_html(p):\n            ingest(p)\n            html_gets += 1\n\n    candidates = []\n    for row in catalog:\n        hit = MATCH_OR_GROUP(row.tokens, host_acc)               or MATCH_HOST_SUFFIX(row.hosts, host_acc)               or MATCH_FOOTER_LITERAL(row.phrases, host_acc)               or MATCH_IMG_ALT(row.alts, host_acc)               or MATCH_REGEX(row.regexes, host_acc)\n        if not hit: continue\n        hit.and_term_ok = GATE_AND(row.and_terms, host_acc)\n        candidates.append(hit)\n\n    host_acc.schema_ok = GATE_SCHEMA(host_acc.schema_types, inferred_vertical(candidates))\n    host_acc.deprioritize = GATE_NEGATIVE(host_acc)\n    host_acc.hits = [h for h in candidates if h.and_term_ok or row_is_exclusive(h)]\n    SCORE_HOST(host_acc)\n    return EMIT(host_acc)\n"
]
```

## 10_OUTPUT_SCHEMA

**Row 1**

```json
[
  "Objects the suite must emit",
  null,
  null,
  null,
  null
]
```

**Row 3**

```json
[
  "Object",
  "Field",
  "Type",
  "Source command",
  "Required"
]
```

**Row 4**

```json
[
  "HostResult",
  "input_url",
  "str",
  "NORM_URL",
  "Y"
]
```

**Row 5**

```json
[
  "HostResult",
  "final_host",
  "str",
  "DISCOVER_CANONICAL",
  "Y"
]
```

**Row 6**

```json
[
  "HostResult",
  "pages_fetched",
  "list[str]",
  "FETCH_*",
  "Y"
]
```

**Row 7**

```json
[
  "HostResult",
  "js_rendered",
  "bool",
  "FETCH_STEALTH",
  "Y"
]
```

**Row 8**

```json
[
  "HostResult",
  "script_hosts",
  "list[str]",
  "EXTRACT_SCRIPT_SRC",
  "Y"
]
```

**Row 9**

```json
[
  "HostResult",
  "iframe_hosts",
  "list[str]",
  "EXTRACT_IFRAME_SRC",
  "Y"
]
```

**Row 10**

```json
[
  "HostResult",
  "outbound_hosts",
  "list[str]",
  "EXTRACT_ANCHORS",
  "Y"
]
```

**Row 11**

```json
[
  "HostResult",
  "schema_types",
  "list[str]",
  "EXTRACT_JSONLD",
  "Y"
]
```

**Row 12**

```json
[
  "HostResult",
  "footer_text",
  "str",
  "EXTRACT_FOOTER",
  "Y"
]
```

**Row 13**

```json
[
  "HostResult",
  "paths",
  "list[str]",
  "EXTRACT_URL_FEATURES",
  "Y"
]
```

**Row 14**

```json
[
  "HostResult",
  "sitemap_product_files",
  "int",
  "FETCH_SITEMAP",
  "N"
]
```

**Row 15**

```json
[
  "HostResult",
  "deprioritize",
  "bool",
  "GATE_NEGATIVE",
  "Y"
]
```

**Row 16**

```json
[
  "HostResult",
  "score",
  "float",
  "SCORE_HOST",
  "Y"
]
```

**Row 17**

```json
[
  "Hit",
  "vertical",
  "str",
  "catalog",
  "Y"
]
```

**Row 18**

```json
[
  "Hit",
  "vendor",
  "str",
  "catalog",
  "Y"
]
```

**Row 19**

```json
[
  "Hit",
  "needle_matched",
  "str",
  "MATCH_*",
  "Y"
]
```

**Row 20**

```json
[
  "Hit",
  "surface",
  "enum(script,iframe,anchor,footer,img,jsonld,prose,path,header,raw)",
  "MATCH_*",
  "Y"
]
```

**Row 21**

```json
[
  "Hit",
  "page_found_on",
  "list[str]",
  "page.url",
  "Y"
]
```

**Row 22**

```json
[
  "Hit",
  "and_term_ok",
  "bool",
  "GATE_AND",
  "Y"
]
```

**Row 23**

```json
[
  "Hit",
  "catalog_confidence",
  "str",
  "catalog",
  "Y"
]
```

**Row 24**

```json
[
  "Hit",
  "priority",
  "str",
  "catalog + SCORE_HOST",
  "Y"
]
```
