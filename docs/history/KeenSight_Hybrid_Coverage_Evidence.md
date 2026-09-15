# KeenSight hybrid and fact-coverage review — evidence notes

## Scope

Local v3 archive and representative families in user table; no production adapters tested; no audit of 424 underlying catalog rows.
No source files or remote repositories were changed. Extraction and tests ran in a separate local review directory.

## Baseline rechecked

- Archive SHA-256: `b21087e3d8aff97caec455d1165eb4d569bb5ace71ffd3b4ffb056715874af4c`.
- `python generate_structures.py --check`: 78 generated JSON files match authoring.
- `python validate.py`: PASS.
- `python -m pytest -q`: 148 passed in 16.16s.
- 87 predicates, 23 derivations, 18 signal types, 86 fixture-only sources.
- 1 registered fingerprint, for Calendly; 3 vendor entities: Calendly, HubSpot, Make.
- The user table sums to 424 entries before deduplication; these are not 424 verified implementation units.

## Targeted current-contract checks

| Probe | Accepted? | Result |
|---|---|---|
| Existing hiring.role with an additional salary_range field | NO | Additional properties are not allowed ('salary_range' was unexpected) |
| Existing review.metrics with complaint_themes added | NO | Additional properties are not allowed ('complaint_themes' was unexpected) |
| SOFTWARE_PRODUCT subject kind | NO | 'SOFTWARE_PRODUCT' is not one of ['ORG', 'LOCATION', 'PERSON', 'BRAND', 'COHORT', 'ANGLE'] |
| API source emitting vendor.present | NO | SOURCE_TIER_NOT_ALLOWED |
| LLM source emitting company.business_model | NO | SOURCE_TIER_NOT_ALLOWED |

These rejections are evidence of current coverage boundaries, not reasons to loosen schemas indiscriminately. Each added capability needs an intentional schema/source/visibility change.

## Source locations within the archive

- `registry/predicates.json`: values, allowed tiers, cardinality, identity paths, subject kinds and visibility.
- `registry/sources.json`: registered emitters; all fixture-only.
- `registry/fingerprints.json` and `registry/entities.json`: current detection fixtures and canonical vendor IDs.
- `schemas/snapshot.schema.json`: raw content reference, hash, media type, time, classification and retention policy.
- `schemas/evidence.schema.json`: snapshot/input references, locator and independence groups.
- `schemas/subject.schema.json`: ORG, LOCATION, PERSON, BRAND, COHORT and ANGLE; no explicit product or industry subject.
- `validate.py:88–114`: eligibility and restricted cross-subject cohort join.
- `validate.py:156–157`: source-tier admission.
- `validate.py:299–328`: current package rules; maturity required; only observed_vendor rendering implemented.
- `contract_tools/identity.py`: claim, observation and current-per-source identity.
- `contract_tools/fingerprints.py`: one asset-host operator; no general DNS/browser-network matcher runtime.

## Important semantic gaps to design, not hide

- A document or API response is evidence; it is not itself a verified claim about all of a company’s operations.
- Vendor and industry research context needs a controlled subject/relationship model; do not weaken cross-account checks.
- More than one statement, credential, app, metric dimension or reporting period may need independent identity; singleton defaults must be reviewed.
- Current review monthly_counts lack per-element period labels; new historical metrics should be explicitly time-keyed.
- Source delivery channel (API, LLM, parser) and evidential meaning (measurement, attributed report, estimate, inference) must remain distinct.
- External data permissions and retention need source-specific enforcement before ingestion; a retained hash cannot replace missing evidence.

## Representative catalog mapping

| Section | Family | Existing related predicates (not complete coverage) |
|---|---|---|
| 1 | Careers and ATS | `hiring.role`, `hiring.velocity`, `content.page_inventory` |
| 2 | Technographics | `vendor.present`, `vendor.mentioned`, `dns.mx.provider`, `dns.cname.service` |
| 3 | Vertical software | `booking.present`, `crm.present`, `website.platform`, `integration.present` |
| 4 | Software pain priors | No dedicated family registered |
| 5 | Local reviews | `review.metrics`, `review.response_ratio` |
| 6 | Forums and industry context | No dedicated family registered |
| 7 | Traffic intelligence | No dedicated family registered |
| 8 | Broad data-provider enrichment | `seo.cwv.field`, `seo.keyword.footprint`, `seo.local.presence`, `review.metrics`, `ads.activity`, `app.mobile.present` |
| 9 | Vertical public registers | `industry.vertical`, `company.locations`, `firmo.employee_band` |
| 10 | Phone and intake | `vendor.present`, `booking.present`, `crm.present` |
| 11 | LLM website and workflow | `company.self_claim`, `industry.vertical`, `industry.subvertical`, `tag.business_type` |
