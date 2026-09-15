# KeenSight full E2E product design

This design continues the module/protocol blueprint through programs and discovery, broad knowledge and research, contacts and offers, campaigns, enrollment, dispatch, replies, CRM and measured improvement.

Start with **DESIGN.md**. **MODULE_MATRIX.md** maps every module's inputs, outputs and submodules. **HANDOFFS.md** specifies the transitions. **PRODUCT_CONTRACTS.md** gives the proposed new field-level records. **DIAGRAMS.md** contains editable Mermaid. **COMPATIBILITY.md** states actual current-schema boundaries and unimplemented extensions. **ACCEPTANCE.md** lists scenarios to implement, not executed tests.

Machine-readable module, contract and workflow catalogs are included. The 30 earlier module IDs and all 38 command bindings are retained under `reference/`; nine product boundaries are added in the proposed catalog. The original proposed common-envelope schemas are included unchanged for reference, not as an integrated API release.

Run `python validate_design.py` for internal design-file consistency checks. No third-party dependencies are needed. These checks do not run the collector, v4.1 validators, browser, source adapters, business workflows or external integrations.

No source repository or runtime was modified. New product contract fields are conceptual definitions, not JSON Schemas. No provider access, price, rule accuracy or operational readiness is inferred from this document.
