# Workbook command coverage in 0.1.0

All 38 IDs are preserved. This is not a claim that all 38 have production-ready
implementations. A manifest entry marked NOT_APPLICABLE is not a successful test.

| Command | Delivered boundary | Verification |
|---|---|---|
| `CATALOG_LOAD` | Closed JSON/JSONL rules; subset donor adapter; unsupported input quarantined | Duplicate, unknown, mapping, and candidate-authority tests |
| `NORM_URL` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `FETCH_STATIC` | Static orchestration + Scrapling HTTP adapter implemented | Fixture transport/adapter controls tested; actual SDK test skipped locally |
| `FETCH_STEALTH` | Disabled extension point; native bounded renderer deferred | Fail-closed boundary tested; no native browser capture |
| `FETCH_SITEMAP` | Static orchestration + Scrapling HTTP adapter implemented | Fixture transport/adapter controls tested; actual SDK test skipped locally |
| `FETCH_ROBOTS` | Static orchestration + Scrapling HTTP adapter implemented | Fixture transport/adapter controls tested; actual SDK test skipped locally |
| `FETCH_WELL_KNOWN` | Static orchestration + Scrapling HTTP adapter implemented | Fixture transport/adapter controls tested; actual SDK test skipped locally |
| `DISCOVER_TEMPLATES` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `DISCOVER_CANONICAL` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_RAW_HTML` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_SCRIPT_SRC` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_SCRIPT_INLINE` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_IFRAME_SRC` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_FORM_ACTION` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_ANCHORS` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_IMAGES` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_LINKS_META` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_JSONLD` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_MICRODATA` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_FOOTER` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_HEADER_NAV` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_DATA_ATTRS` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_NOSCRIPT` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_VISIBLE_TEXT` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_URL_FEATURES` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `EXTRACT_HEADERS` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `MATCH_SUBSTRING` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `MATCH_OR_GROUP` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `MATCH_REGEX` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `MATCH_HOST_SUFFIX` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `MATCH_FOOTER_LITERAL` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `MATCH_IMG_ALT` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `GATE_AND` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `GATE_SCHEMA` | Advisory type support, not company subject binding | JSON-LD parsing and qualification tests; canonical schema-subject inference deferred |
| `GATE_NEGATIVE` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `ROLLUP_HOST` | Local handler/function implemented | Deterministic unit and/or fixture-pipeline tests |
| `SCORE_HOST` | Explicit uncalibrated unique-claim priority policy | Priority never changes fact or rule authority |
| `EMIT` | ScanBundle and deduplicated claims JSON | Schema, links, rerun matcher, view and blob checks; legacy exact HostResult/Hit schema not implemented |

The 17 EXTRACT commands are all real parsing functions. The six MATCH command
families map to the typed matcher, including ANY alternatives and exact parsed
hostname boundaries. Rule definitions do not execute arbitrary source text.

Not yet present: native bounded browser/network capture, the missing master
footprint catalog, complete donor composites/dependency operators, calibrated
production rule releases, canonical fact admission, and the workbook’s exact legacy
HostResult/Hit file formats. Every omission stays explicit.
