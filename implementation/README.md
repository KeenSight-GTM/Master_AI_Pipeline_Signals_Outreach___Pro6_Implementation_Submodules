# KeenSight — Scrapling-first implementation handoff

**Decision:** build the Scrapling evidence collector first, complete the entire 38-command workbook suite, integrate the existing dynamic-fingerprint learning loop, then implement the persistent knowledge/research/reasoning and controlled commercial layers.

This is a source-grounded implementation plan against v4.1. It contains planning records and a traceability checker, not a new scanner, a patched contract release or a deployed application.

## Read in this order

1. [End-to-end phases and acceptance gates](IMPLEMENTATION_PHASES.md)
2. [Organization, modules and submodules](REPOSITORIES_AND_MODULES.md)
3. [All 38 command placements](SCRAPLING_38_COMMANDS.md)
4. [Dynamic fingerprint reuse and release design](DYNAMIC_FINGERPRINT_INTEGRATION.md)
5. [Explicit workbook corrections and contract delta](WORKBOOK_DECISIONS_AND_CONTRACTS.md)
6. [Implementation dataflows and scanner UML](DATAFLOWS_AND_UML.md)
7. [Source boundaries and executed validation](SOURCES_AND_VERIFICATION.md)

## Machine-readable handoff

- `command_plan.json`: original row + proposed owner/phase/output/test for all 38 commands.
- `phases.json`: ten phases, dependencies and exit criteria.
- `modules.json`: 36 module ownership entries and their submodules.
- `work_items.json`: 61 proposed issue candidates; no GitHub issues have been created.
- `command_traceability.csv`: flat view of the same action map.
- `reference_52_ledger_map.json`: unchanged ledger mapping from v4.1.
- `workbook_extracted.json` and `WORKBOOK_SOURCE.md`: source workbook values.
- `sources.json`: commit-pinned repository evidence and official documentation references.
- `baseline-check.txt`: executed v4.1 generation/validation/test log.
- `plan_validation.json`: results of `python validate_plan.py`.

## Important scope boundaries

The workbook's 38 commands are not the 52-idea ledger, 38 commercial signals, or 38 required network requests. They are a command suite mixing acquisition, extraction, matching, qualification and output. All are planned in `scrapling-ingestion`; whether an optional browser fetch actually runs depends on the profile and evidence need.

The separate `99_MASTER_ALL` / 25-vertical footprint catalog is not attached. The existing scanner manifest reports 739 rule definitions, not the approximately 2,500-signature target. Begin with reviewed donor/starter rules and import the missing catalog through the same future adapter when it is available.

The v4.1 baseline's F ChangeRecord authorization gap remains unpatched by this planning work. The plan schedules it before hosted writes/multi-tenant production. New raw captures and fixture approvals do not provide production authentication or rights to a source.

## Verification

The v4.1 baseline passed its generation check, semantic validation and all 588 tests in this session. The planning checker also validates all 38 original IDs and rows, module ownership, phase acyclicity and all 52 retained ledger IDs. Neither donor repository's full runtime test suite was executed here; that is a P0 task.

No GitHub organization, repository, branch, issue, rule release, live capture or send was created by this handoff.
