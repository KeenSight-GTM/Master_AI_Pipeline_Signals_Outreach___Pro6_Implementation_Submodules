# KeenSight v4.1 — selected-fix validation report

## Scope

This release implements audit fixes **A, B, C, D, E, G and H** in the contract validator and limited reference execution/export code. It maps all 52 supplied ledger ideas and adds the missing typed record families. **F (legacy ChangeRecord authorization / typed replacement validation) is deliberately not repaired.** Nothing was pushed to GitHub. No live provider calls, CRM changes or sends were performed.

## Executed results

| Check | Result |
|---|---:|
| Unchanged v4 baseline tests | 471 passed |
| v4.1 full tests | **588 passed; 0 failed, 0 errors, 0 skipped** |
| Predicate definitions | **213**; all 197 prior identifiers retained, 16 additions |
| Metric definitions | **89** |
| Draft-07 schemas | **75** |
| Synthetic example records | **225**, including 28 fact records |
| Structural schema validations performed by Bundle.validate | **1,121** |
| Generated contract/fixture files | **116** |
| Byte-identical repeated generation | PASS |
| Byte-identical clean regeneration after deleting generated directories | PASS |
| Class/value objects covered by generated diagram partitions | **75**, each once |
| Proposed interfaces / rendered views | **22 / 14** |
| Supplied ledger placements | **52 / 52**, original IDs retained |

Commands executed: `python generate.py --check`, `python validate.py`, `python -m pytest -q --junitxml=reports/pytest.xml`, `python build_diagrams.py`. A second clean directory was generated and validated, with SHA-256 comparison of every generated path and byte sequence. Evidence: `reports/pytest.txt`, `reports/pytest.xml`, `reports/test-index.json`, `reports/release-verification.json`.

These counts do not imply 213 live extractors, a 2,500-signature library, 52 implemented business algorithms, or proven accuracy against real companies. All current sample artifacts, actor approvals, gates and source permissions are synthetic DESIGN_TEST material. Source pricing, legal permissions, access and claimed commercial effectiveness in the ledger were not verified in this task.

## Selected-fix coverage

| Fix | Implemented checks | Representative regression evidence |
|---|---|---|
| A — producer success and target completion | Failed/abstained runs, executions and model calls cannot substantiate successful facts or approved packages. Output/record/approval chronology and per-target completion are explicit. | `test_A_completion_rejects`, `test_A_failed_producer_not_currently_usable`, `test_A_partial_batch_preserves_completed_account`, failed no-response model path. |
| B — input closure | Facts, artifacts, bindings, resolutions, imported executions, generated outputs and full samples must be pinned. Direct evidence must match producing inputs. Model request/response and repairs are part of retained ancestry. | `test_B_dependency_closure`, wrong raw input with a recomputed hash, sample-byte mutation, request/response root and source veto checks. |
| C — resolved decision inputs | Signals/copy use complete pinned claim groups and check ancestor conflicts. Omitted conflict rows in a signal do not bypass the decision boundary. Independent vendors remain distinct. Duplicate upstream origins cannot satisfy minimum support twice. | `test_C_conflict_blocks_render_even_when_signal_hides_the_conflict`, `test_C_derived_prior_cannot_launder_input_conflict`, distinct vendors, UNKNOWN preservation, origin-count regression. |
| D — research semantics and full dependencies | Versioned support policies distinguish negative experiences from workflow mentions; negated, positive and unsupported question labels cannot become pain support. Every retrieved sample record receives an explicit disposition. Denominator-only artifacts affect current usability. | `test_D_nonpain_not_counted_as_pain`, denominator deletion/expiry, unclassified count, sample decision closure, support locator, abstained-context rejection. |
| E — scoped coverage | Capture attempts and actual successful detector executions are bound to target, source, modality, release and chronology. Pagination/truncation and partial captures cannot produce complete non-detection. | `test_E_absence_requires_execution`, actual raw-HTML form detector checks, detector/pagination/chronology mutations. The implemented form detector is a narrow demonstration, not all provider implementations. |
| G — no-byte failure | Zero-artifact attempts represent policy denial, budget denial, timeout and failure. Diagnostic evidence can support UNKNOWN without fabricating a provider response. It cannot prove positive state or absence. | Attempt-backed UNKNOWN fixture; unbound provisional target and no-derive-permission diagnostic tests; positive/absence laundering rejection. |
| H — activation and handoff | Enabled definitions resolve to explicit allowed callables; disabled signals/templates cannot publish. Reviews bind authorized fixture actors to exact revisions/hashes. Fresh purpose/destination gates include restrictions and evidence state. Local export is idempotent and never sends. | Disabled profile/function tests; review/hash/principal/gate tests; DNC and revoked evidence; idempotent file reuse/conflict; no-send exposure rejection. |

The tests exercise both full-bundle validation and individual decision boundaries. Semantic mutation tests disable release checksum checking and remove/restamp unrelated example handoffs where appropriate, so a stale file hash or gate does not masquerade as a semantic rejection.

## Explicitly open F

The release-verification report reproduces the legacy weakness for an unused vendor observation after recomputing dependent claim resolutions and removing unrelated fixture export gates: a foreign-tenant retraction and a nonexistent replacement still pass that legacy snapshot boundary. The retraction also affects usability. The new review/restriction principal checks do **not** repair it. Do not deploy this as multi-tenant production admission until F is addressed.

## Implementation limits

Production input selection, authenticated endpoints, durable transaction storage, live capture/model providers, distributed budgets, remote outbox/reconciliation, sending, privacy jobs and broad detector accuracy are not implemented. The local exporter accepts only fixture LOCAL_PREVIEW destinations and DESIGN_TEST packages; it assumes its principal was authenticated by its caller. Concurrent crash recovery for files fails closed rather than silently resending.

The eight compound proposals and lookalike, scenario, scorecard and playbook machinery are mapped and constrained, not all implemented. LookalikeMatch and ScenarioEstimate are DESIGN_ONLY shapes; case-study/competitor/quote-back copy renderers are not automatically enabled. The referenced Automation Playbooks tab is missing from the supplied ledger. JSON Pointer edge cases, unrestricted organization/member aggregation and complete historical-policy replay remain outside these selected fixes.

SVGs were rendered locally from the shared diagram model with Graphviz and a narrow sequence renderer. Editable Mermaid sources are included; Mermaid CLI parsing was not run. A finite test suite is evidence of tested behavior, not a proof of all possible runtime correctness.
