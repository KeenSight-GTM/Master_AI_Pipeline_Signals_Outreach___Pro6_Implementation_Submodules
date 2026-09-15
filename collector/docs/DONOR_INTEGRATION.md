# Existing SEO fingerprinter integration

Basis: supplied `SEO-FingerPrint-Scanner-Basic` commit
`66358454c98addb8fe297cb5192a32e2bd98f732`, especially its rule definitions and
`RuntimeFingerprintEngine` shape. This module does not modify that repository.

The old category/key/value first-hit display deduplication must not precede the
new evidence ledger. Import definitions, execute matching against retained surfaces,
and emit all supports before producing a compact host/claim projection.

## Implemented subset

The donor adapter understands JSONL, JSON arrays, or an explicit `rules` envelope.
Each input row appears in the output report as IMPORTED_CANDIDATE or QUARANTINED.
Supported operator mappings are:

| Donor | Local |
|---|---|
| `contains_any` | `contains`, ANY alternatives |
| `equals` | `equals` |
| `regex` | bounded `regex` |
| `host_equals` | parsed `host_equals` |
| `meta_name_equals` | `equals` over meta name |
| `meta_value_contains` | `contains` over meta content |
| `meta_value_regex` | `regex` over meta content |
| `cookie_name` | `equals` over cookie name |
| `cookie_name_regex` | `regex` over cookie name |
| `header_name` | `equals` over header name |

Supported surfaces: scripts, stylesheets, iframes, form actions, links, raw HTML,
footer text, meta tags/names, cookie names, headers, and data attributes.

The adapter requires an explicit source-vendor-to-canonical-product mapping.
It does not guess product identity from labels or categories. All imported rules
are candidate-only and emit `vendor.mentioned`, even when the donor status says
validated/active. A subsequent deliberate rewrite/review is required for a narrow
presence rule. The original predicate/metadata is preserved for that review.

Composite/minimum-count, dependency, extraction, unsupported-scope and ambiguous
rules are quarantined intact. Broad contains matching is not silently changed
into hostname matching: that would change the donor's semantics. Better scoped
rules must be reviewed as new definitions.

## Not delivered

The whole 739-row donor corpus is not bundled or characterized. The six inspected
source rows were used to confirm shape, not to certify corpus-wide compatibility.
The examples in this package are explicitly synthetic donor-shaped records.

No automatic proposal generator, signed registry release service, complete promotion
UI, or cross-tenant research federation exists. The normalized unknown-feature index
and candidate import/export form the initial research boundary. Approval metadata
in locally authored packs is trusted local configuration, not hosted authentication.

## Next integration gate

Import the full pinned donor library and report every row's disposition. Extend the
compiler only for explicit, tested semantics. Add approved-rule fixture sets, shadow
precision evaluations, signature/provenance checks and controlled release publication.
Never promote 497 candidate-status definitions merely because the previous loader
considered them runtime-eligible. Run the real SDK integration tests before importing
this collector into a production application.
