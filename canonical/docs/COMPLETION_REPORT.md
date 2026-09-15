# KeenSight v4.1 — implementation and ledger integration summary

## Decision

Keep the broad fact model and combination-C research context, but classify ledger entries by role rather than turning every idea into an observed business fact. The 52-row mapping preserves the supplied names and IDs in `docs/LEDGER_INTEGRATION.md` and `docs/LEDGER_MAP.json`.

## Selected patch boundary

**A–E, G and H are encoded and tested in local contract/reference code. F is unclosed.** This is not a live application deployment and does not imply that the previous audit's entire scope is resolved.

| Handoff | New requirement |
|---|---|
| Intake → acquisition | Explicit target and purpose; approved bounded acquisition attempt; legitimate no-byte failure. |
| Producer → fact | Successful complete producer, matched actual inputs, recording chronology and exact evidence ancestry. |
| Fact → signal/copy | Exact pinned inputs and full claim resolution, including ancestor conflicts and source-origin deduplication. |
| Review corpus → prior | Versioned meaning of support, full sample dispositions and complete denominator/exclusion dependencies. |
| Capture → absence | Completed capture plus compatible successful detector execution for the declared resource/target. |
| Preview → review | Authorized trusted fixture principal reviews exact revision and content hash. |
| Review → use | Fresh purpose/destination gate; revoked/expired/deleted evidence and operational restrictions can block old approval. |
| Use → local export | ALLOW for the exact payload/destination; stable business idempotency key; no sending or remote provider. |

## Knowledge breadth

Sixteen new typed predicates cover publications/statements/events, repository activity, public and permissioned event participation, shipments/procurement, legal filings, awards, patent records, franchise disclosures, financing/loan records and case-study reports/outcomes. They supplement, rather than replace, the 197 existing predicates. A source name is not itself a predicate; many sources feed the same typed fact families.

Compound conditions such as possible tool overlap or posting-language change belong to versioned derivations/signals. Stalled hire, false AI claim, failed project, mandate, current budget and revenue loss are not established by the ledger's proxy observations alone. Peer matching and case-study filters are software; outreach angles and automation playbooks are policies/templates; their evidence requirements remain explicit.

Case-study figures remain publisher-reported outcomes about the comparison company. Product and industry priors remain context, not company pain. Hypothetical cost models must disclose assumptions. Model confidence, exact percentages, recognizable brands and similarity scores do not establish truth, causal effectiveness or transferable results.

## Reference end-to-end slice

The retained synthetic slice loads captured/imported evidence, validates narrow successful extraction and raw-form detection, checks sample summaries and claims, produces three supported previews, records exact-revision reviews, evaluates a current-use gate and exports a local JSON preview. Run the test suite for failure branches and the exporter demonstration. No provider account, source permission, model API or real email is involved.

## Deferred and blocked

F's legacy ChangeRecord authorization and typed replacement checks remain a production blocker. No live adapters, 2,500-signature library, embedding index, full compound-rule set or additional case-study/quote-back renderers are provided. Schema design does not activate these capabilities. The Automation Playbooks tab was not supplied, and no playbook catalog is invented.

See `SYSTEM.md` for the architecture, `VALIDATION.md` for measured results, and the HTML diagram book for all updated contracts and proposed code interfaces.
