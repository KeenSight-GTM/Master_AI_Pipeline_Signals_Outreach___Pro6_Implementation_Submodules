# Compatibility and implementation boundary

This continuation preserves current semantics and proposes new product contracts. It does not patch v4.1, the collector, the module-protocol package, any GitHub repository, or a provider configuration.

## Confirmed by reading the supplied v4.1 schemas

| Existing contract | Actual shape | Implication |
|---|---|---|
| UseGateDecision | Purpose enum is PREVIEW_EXPORT or CONTACT_EXPORT | SEND needs a separately defined/validated gate. Export cannot be treated as send permission. |
| ReviewDecision | Contains package_id, revision and content_hash | Existing review is package-scoped. Campaign approval and channel rendering require explicit new contracts or a deliberate versioned extension. |
| OutreachPackage | Has clauses, rendered_text, template/review refs and send_allowed | Exact channel subject/body/footer and allowed provider transformations are not defined by simply returning more text. Proposed MessageArtifact needs validation and review linkage. |
| Exposure | provider_message_id and accepted_at permit null | Unknown acceptance is representable; preserve it and reconcile rather than inventing values. |
| OutcomeEvent | exposure_id permits null; attribution can be MATCHED or QUARANTINED | Inbound events can be retained before attribution. Do not create fictional exposure links. |

`baseline_contract_inspection.json` contains the extracted required fields and properties from those actual schemas. This is source inspection, not a test of every validator path.

## Preserved design constraints

The supplied v4.1 design retains a broad 213-predicate catalog and 89 metrics, explicit research-context separation, producer/lineage/conflict/coverage checks, no-byte acquisition failures and review/export reference behavior. The collector deduplicates capture observations while preserving individual match support. The previous module design provides a proposed common invocation envelope and 30 module IDs. These are retained as the basis for this continuation; runtime tests and inventories were not rerun here.

## Proposed changes only

Nine product-operation boundaries and 32 field-level contract designs fill out sourcing, contacts, campaign management, conversations, CRM, quality and the workspace. Their exact type schemas, persistence transactions, state-specific validation, authorization and integrations remain implementation work. No count of these designs should be presented as a count of live modules or working APIs.

The active repository plan remains five repositories, not five deployments. The first running work remains Scrapling capture, then dynamic fingerprint support and canonical fact admission. Broad provider collection, campaign execution, reply automation and CRM writes are independently enabled later.

## Explicit blockers and limits

- Fix F in legacy ChangeRecord remains open and blocks hosted/multi-tenant mutation.
- The supplied collector reports unverified actual Scrapling SDK execution in its environment and disabled native browser capture. This continuation does not change that status.
- No full 2,500-signature library or missing Automation Playbooks tab is manufactured.
- The existing source/ledger cost, entitlement, effectiveness and causal claims remain author-provided planning metadata unless separately verified.
- Existing SignalEvaluation statuses are not silently remapped to a new MATCH/NO_MATCH/UNKNOWN decision enum.
- Offline replay never authorizes external acquisition, model calls, campaign changes, sending, meetings, deletion or CRM writes.
