# KeenSight v4 — end-to-end architecture audit

**Review date:** September 14, 2026  
**Verdict:** Broad knowledge contracts are established; the delivered v4 is **not yet an end-to-end-complete application contract**. Important handoffs remain specified only in prose, and selected reference checks accept states that contradict those requirements.  
**Scope:** Unchanged uploaded `keensight-architecture-v4.zip`; no GitHub modifications, live collectors, paid calls, source licensing determinations, delivery, or runtime database tests. This report is not a patched v4 release.

## 1. Evidence and method

Archive SHA-256: `05afdbca993d3512862ad4d0d837ec2c34eacf488a5febb9540202a9335cdc45`.

Executed in the extracted archive:

```bash
python generate.py --check
python validate.py
python -m pytest -q --junitxml=baseline.xml
python probe_v4.py /path/to/keensight-architecture-v4
```

Generation consistency passes for **95 generated files**. The full fixture validator reports **58 schemas, 197 predicates, 89 metrics, 144 records and 27 semantic fact checks**. The existing suite passes **471 tests**. The baseline was rerun, not inferred from the previous report.

The independent diagnostic harness contains **28 targeted probes**. They are not 28 independent architectural defects and are not a production failure-rate sample:

| Category | Result | Interpretation |
|---|---:|---|
| Invalid/contradictory boundary mutations | 18 accepted | Missing invocation or consistency checks in the current reference path. Some require clarifying the per-account completion contract. |
| Minimum-support interpretation | 1 accepted | Two observation IDs from one origin satisfy a minimum of two; independence/counting unit is unspecified. |
| Reserved future delivery/outcome contracts | 2 accepted | Recorded here as future contract gaps; no live sender is enabled. |
| Legitimate pre-capture failure | 1 rejected | An UNKNOWN with no captured bytes cannot have a currently valid empty EvidenceSet. |
| JSON Pointer helper conformance | 1 accepted | Negative array indexing is accepted. |
| Historical visibility helper semantics | 1 accepted | Logical `as_of` is not a separate knowledge cutoff; exact pinned-set semantics need to govern use. |
| Rejection controls | 4 rejected | Bad timestamp, cross-account copy, incomplete coverage and expired supporting evidence remain rejected. |

Release-hash checking was disabled for mutations, and registry pins were recomputed when definitions changed. This deliberately tests semantic checks as if validating a newly authored release, not the trivial detection that a file changed. No fixture files in the original archive were edited.

Machine-readable records, exact mutation code, logs, source hashes and the unchanged baseline archive are in the accompanying review pack. `counterexamples.json` identifies the boundary called in each case; two helper probes intentionally do not call the complete validator.

## 2. What is worth preserving

Keep all eleven domain families and the broad fact/metric catalog. Keep independent capture, extraction and commercial-use activation. Keep ordinary relational persistence, a sequential runner, exact evidence links, product/industry subjects, explicit natures, typed metrics, scoped absence, candidate isolation and observation-led copy without universal maturity requirements.

The original `docs/IMPLEMENTATION_SCOPE.md` correctly disclaims live adapters, durable persistence, production selectors, source approvals, delivery, and privacy jobs. The current profile is deliberately DESIGN_TEST-only. Those limitations should remain explicit.

The principal problem is not insufficient fact breadth. It is that a set of schemas and helpers is being mistaken for a closed lifecycle between those schemas.

## 3. Confirmed boundary findings

### E01 — Failure states do not gate publication

The full validator accepts all of these while the original approved preview records remain:

* `run.demo.status = FAILED`.
* `ex.job_llm.status = FAILED`, retaining the observed job statement and approved package.
* `call.fixture.status = FAILED` with a terminal reason, retaining the same successful downstream records.
* An execution finish time after its output was recorded and its package approved.

**Correction:** Require proof that the relevant account evaluation and every producing execution completed successfully. An overall multi-account batch may fail partially without deleting independent completed account results, but that requires an explicit per-account completion record. Model output must reach a validated terminal state before it can create eligible facts. Run wall-clock completion may follow logical observation time; this is different from publishing a result before its producer completes.

**Source:** `keensight_contracts/validation.py:85–120,282–309,314–357`; execution/run/model schemas in `shapes.py:100–140`.

### E02 — Run provenance is not closed over every consumer

Accepted mutations remove `f.tech` from the run's input-fact list or clear its binding list while the signal/package continues using those records. Another mutation changes the job execution's artifact input to the homepage, recomputes its input hash, and leaves its job-evidence output unchanged. A model call can separately list an input set different from its consuming execution.

**Correction:** Every consumed record must be either a pinned external input or a completed same-run output with an explicit producing execution and matching artifact evidence. Bindings, conflict resolutions, research samples, eligible denominator records, context links, and configuration versions are inputs too. Model request inputs and extraction evidence must reconcile with execution inputs. A hash over an incomplete list is not complete provenance.

**Nuance:** A raw fact generated during the same batch need not have existed before capture. It must instead have a declared same-run producing operation and immutable evidence inputs; the contract should not silently confuse that case with an unpinned external fact.

**Source:** `validation.py:282–310,334–359,389–438`; `engine.py:claim_key`; `docs/PERSISTENCE_BATCH.md`.

### E03 — Configuration disabling is not consistently enforced at use time

The validator accepts a registry whose enabled signal function points to a nonexistent entrypoint after the registry pin is updated. It also accepts a profile with empty `signal_ids` and `template_ids` while the stored signal and template-based package outputs remain active.

The original suite has a separate entrypoint-existence test for the bundled definitions. That does not make the runtime release linker enforce it for every new profile/release.

**Correction:** Resolve allowed implementation entrypoints at release load; validate required parameter interfaces and dependency closure. At consumption, enforce the pinned profile's signal/template/function selections. Historical outputs from a different profile remain historical, not implicitly enabled under the new one.

**Source:** `validation.py:197–231,334–361`; `tests/test_contracts.py:test_entrypoints_exist`.

### E04 — Claim conflict resolution is disconnected from signals and copy

A positive technology footprint and a covered NOT_FOUND observation were added with the same claim key and both were put in the signal's input set. `resolve_claim` reports `CONFLICT`, with no accepted fact IDs. Nevertheless, the full validator accepts the RESOLVED signal and renders the original product-observation copy.

**Correction:** Signals consume resolved claim views or explicitly validated conflict dispositions, not arbitrary existential matches among observations. Copy approval must also reject a contradictory unresolved claim family. A use-specific policy may deliberately permit a weaker scoped statement, but it must record that disposition instead of bypassing conflict resolution.

The same helper currently counts two copies of an observation from one evidence origin toward a minimum of two. Define whether a minimum counts records, distinct origins, periods, subjects, or independent source groups; do not infer independence from fact IDs.

**Source:** `engine.py:resolve_claim,evaluate_requirements`; `validation.py:render,334–345,365–371`.

### E05 — Research summaries omit semantic and denominator dependencies

A supporting theme classification can change to `stance=NEGATED` and `sentiment=POSITIVE` while the product pain prior still counts it as support. The current summary checks theme and subject, not a named support policy.

Deleting the third product-review artifact used only in the denominator also passes full validation. The prior still reports a two-out-of-three sample share and `usable(f.prior.product, at)` returns true. Its ancestry contains the two supporting classifications, not the denominator-only record.

**Correction:** Pin and validate all sample records that affect a statistic, not just supporting records. A versioned support rule distinguishes experienced negative pain, neutral workflow mentions, questions, negations, quotations, and unknown classifications. Pin the denominator definition and evaluation status of each included record. Sample eligibility must have the same current rights/retention checks as numerator evidence. Define historical display separately from current reuse.

An ABSTAINED ContextAssessment can also remain attached to a resolved signal and approved package. An abstention can be retained for audit but cannot influence an eligible decision as if it were an eligible prior.

**Source:** `validation.py:60–120,486–527,338–359`; `engine.py:theme_summary`.

### E06 — Coverage proof does not establish a completed detector execution

A coverage record dated before the capture is accepted. A well-formed but unresolvable detector-release hash is also accepted. Current checks establish successful listed captures and target correspondence, not that an identified detector ran successfully on those captures in the declared interval.

**Correction:** Bind coverage to the acquisition attempts and detector executions that establish it. Validate chronological order, actual supported modality, detector version/hash, target and queried resources. For paginated APIs/ATS, record query identity, cursor completion/termination, rate-limit interruptions and truncation. A complete bounded sample can prove only absence in that sample, not all-site or all-company absence.

**Source:** `validation.py:258–271,435–440`; `CoverageRecord` schema.

### E07 — Changes are not fully typed or tenant-scoped

A ChangeRecord from `tenant.other` can target `tenant.demo`'s `f.vendor1`; full validation accepts it and current-use evaluation disables that fact. A nonexistent `replacement_id` is also accepted. Current ChangeRecord processing checks whether a target ID exists somewhere, rather than checking a typed, authorized, same-tenant transition.

**Correction:** Require typed target references, same-tenant ownership, permitted transition, authorized actor, existing replacement with compatible type/identity, recorded time and effective time. Global registry/policy changes are distinct privileged transitions with explicit affected tenants. Never trust tenant/actor authority merely because it appears in a payload field.

**Source:** `validation.py:80–105,362–364`; `ChangeRecord` schema.

### E08 — An expected acquisition failure cannot be represented without inventing evidence

The no-byte policy-denial probe records an UNKNOWN observation but no artifact or parent fact. It fails at `EMPTY_EVIDENCE`. This should not be solved by inventing a provider response or allowing evidence-free positive facts.

**Correction:** Record an AcquisitionAttempt with status/reason even when no bytes were obtained. Usually that is enough for the account's acquisition report and an UNKNOWN signal decision. Where an UNKNOWN fact is useful, allow only an explicit attempt-backed operational reference. Such a reference is diagnostic and can never establish OBSERVED truth or NOT_FOUND coverage.

The initial input/capture bootstrap also needs an unresolved target form: v4's Scope already requires a subject, while real import/discovery may precede identity resolution.

**Source:** `validation.py:272–279`; `Scope`, `Artifact`, `CandidateRecord`, `ModelCall` and `EvidenceSet` schemas.

### E09 — Preview approval and export have no complete decision record

A preview currently has an approval timestamp but no signed-in reviewer identity, review decision, approved content hash, destination, use-purpose decision, suppression lookup result, or export receipt. Those requirements are mentioned in documentation, not represented as a complete operational contract. Only three narrow preview rules/templates are integrated; the old business signals remain reference assets.

**Correction:** Add an explicit machine-validation result, optional/required human review according to profile, and current-use gate bound to the exact package revision and destination. Separate factual support, signal match, commercial opportunity selection, approval, export and send permission. Do-not-contact status and other operational restrictions belong in the use gate; a TTL expiry must not silently remove a do-not-contact instruction.

Do not require a recipient for an account-level research preview. A destination and recipient identity become required only for a contact-specific handoff. Product/industry priors remain internal context throughout.

**Source:** `OutreachPackage`, `TemplateDefinition`, `SignalDefinition` schemas; `docs/PERSISTENCE_BATCH.md:Export and delivery`; `diagrams/12-proposed-code-interfaces.mmd`.

### E10 — Sending and outcome contracts are deliberately incomplete

A synthetic PROVIDER_ACCEPTED exposure can refer to a `send_allowed=false`, DESIGN_TEST_APPROVED package. A quarantined outcome can reference a nonexistent EvidenceSet. These pass the validator today. They are recorded as defects in reserved future contract validation, not evidence of a live sending incident.

**Correction before delivery activation:** Introduce a gated delivery intent, recipient/provider/campaign mapping, external idempotency/reconciliation strategy, latest suppression checks and a transactional export/outbox boundary. Validate outcome evidence, same-tenant exposure references, provider message matching and event ordering. An uncertain send must be reconciled rather than blindly retried. CRM synchronization must not trigger a second send.

**Source:** `validation.py:372–385`; `Exposure`/`OutcomeEvent` schemas; no sender implementation in archive.

### E11 — Additional helper and architectural limitations

`engine.pointer` resolves `/-1` against an array to its last element, which is not JSON Pointer array semantics. RFC 6901 section 4 requires an unsigned array index without leading zeros. Use a conforming resolver; reject malformed pointer escapes and invalid array indices.

The temporal helper accepts a record ingested after a requested historical `as_of`. Because v4 intentionally allows retrospective computation, this is not automatically a bug. It exposes the need to separate observation time, knowledge-cutoff time, run sealing, and current-use time. Historical evaluation must use the original pinned record set; retrospective re-evaluation is a new run with explicit new inputs.

Company/location/person aggregates are another design seam: `FunctionDefinition` permits relationship-oriented labels, but current execution validation enforces the same subject for every input. A declared membership aggregation is needed before using member/location facts to compute organization counts or organization-level statistics. Do not simply remove the subject check.

Operational completeness still needs import/read/review endpoints, actor authorization, bounded resource use, idempotent persistent writes, recovery, retention/deletion jobs, credential handling, monitoring and production source/promotion checks. These are runtime obligations, not justification for a new microservice per concern.

## 4. End-to-end status by product boundary

| Boundary | v4 status | Completion condition |
|---|---|---|
| Broad knowledge representation | Present at family/contract level | Actual enabled extractors and mappings pass evidence-to-fact tests. |
| Product/industry context | Present, with identified research dependency gaps | Full sample dependencies and eligible explicit joins enforced. |
| Evidence-to-preview reference path | Partial | Close E01–E09 and run from captures rather than hand-authored facts. |
| Real reviewed export | Specified only in prose | Explicit review/use gate/export contracts and implementation tests. |
| Autonomous sending/outcome feedback | Disabled / reserved | Independent enablement gate; do not label it complete from preview tests. |

## 5. Required closure, without scope inflation

The companion completion specification chooses a small set of new operational records and extensions to existing classes. It preserves the sequential batch runtime, broad facts and research context. It does not prescribe a graph database, distributed scheduler, universal event sourcing, or automatic feedback ranking.

The current archive should not be relabeled as patched or certified. Apply the chosen contract changes to `shapes.py`, `bootstrap.py`, `catalog.py`, the semantic validator, fixtures and diagrams; then convert these probes into regression tests with the corrected expected outcomes. Finally test real repository/adapter implementations at the enabled product boundary.

## 6. Primary technical references

These support the architectural constraints, not the local code findings:

* RFC 6901, section 4, JSON Pointer evaluation: https://www.rfc-editor.org/rfc/rfc6901.html#section-4
* SQLite atomic commit describes database-transaction atomicity, not an atomic transaction spanning separate content storage or a remote provider: https://www.sqlite.org/atomiccommit.html
* AWS transactional outbox guidance discusses dual writes, rollback and duplicate delivery; consumers still need idempotency: https://docs.aws.amazon.com/en_en/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html

## 7. Limits of this review

No finite selected mutation suite proves the absence of all defects. This review reran v4 checks and traced the listed seams; it did not enumerate every future provider endpoint, all 424 unsupplied catalog rows, the desired signature library, production security penetration tests, or live statistical calibration. All newly proposed contracts remain a completion design until encoded, tested and integrated.
