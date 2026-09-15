# KeenSight architecture audit
**Audit date:** September 14, 2026  
**Primary artifact:** `keensight-architecture.zip`  
**Disposition:** Preserve the architectural direction, but do not certify the bundle as fully semantically verified or implementation-complete.

## Executive assessment

The evidence → facts → signals → adjudication → derived descriptors/cohorts → outreach separation is a useful foundation. Immutable captures, explicit UNKNOWN, source authority, conservative absence semantics, reproducible projections, and bounded verification are the right kinds of boundaries to preserve.

The current bundle successfully generates consistent files. That is materially different from proving that its declared rules, examples, dependencies, and commercial claims are internally correct. Several stated invariants are not checked; some are contradicted by the supplied examples. Other behaviors remain prose specifications with significant implementation decisions outstanding.

No finding below establishes that a live production deployment sent a bad message. Runtime components for the new design are not implemented in the archive. The local bugs are in design-time code/contracts and their claimed assurances. Findings about the linked repositories are based on pinned inventory and selected source inspection, not execution of their full test suites.

## Scope and measured results

| Check | Observed result |
|---|---|
| Original generator | Completed successfully; 59 printed OK checks |
| JSON Schemas | 13; independently valid Draft-07 schemas |
| Example instances | **25, not 26**; all independently validate against their respective schemas, including format checks |
| Derivation records | 23; all independently validate against the current derivation schema |
| Registry content | 79 predicates, 23 flows, 18 signal types, 4 sample packs, 12 sample sources; 6 registry files |
| Repeated generation | Identical hashes for all 44 generated JSON files |
| Delete generated directories and regenerate | Identical generated paths and bytes; also matches the archive's generated JSON |
| Workbook | 5 sheets; all catalog cells match 78 FC, 18 SF, 23 DF, and 16 DA rows |
| Adversarial validation-boundary tests | 36 intended invalid cases accepted; four rejection controls rejected |
| Supplemental checks | Duplicate pack membership still accepted when injected before index construction; existing derived-fact reference incorrectly reported as dangling |
| On-disk validation test | Invalid extra fact JSON retained and ignored by regeneration |
| Design-time fingerprint matcher | Seven expected negatives fired; two expected positives did not fire |

The 36 cases are deliberately selected counterexamples, **not** a random sample, defect rate, production failure rate, or 36 independent root causes. Mutations are inserted immediately before the generator's validation section and exercise its actual checks; the generator has already emitted most baseline objects at that point. Thus these tests establish validation-boundary behavior, not end-to-end runtime behavior. The separate disk and pre-index tests address those boundaries explicitly.

The workbook was inspected read-only through its Open XML contents. Its visual rendering and its generator were not executed. No live crawling, provider API calls, LLM calls, CRM writes, delivery, real gold-set calibration, runtime journal replay, or remote repository test suites were executed.

### Pinned repository snapshots

- `KeenSight-GTM/SEO-FingerPrint-Scanner-Basic`, branch `experiment/fingerprint-ingestion-fact-store-v1`: `66358454c98addb8fe297cb5192a32e2bd98f732`.
- `KeenSight-GTM/Master_Signals_App_KeenSight`, branch `experiment/evidence-fingerprint-prototype-v1`: `c8103df9d14badcfc85e50c0a27daeee6cb3f973`.

Selected inspected code includes scanner inventory/README and CI definition, Master runtime inventory/README, and `src/ai_first_signal_engine/runtime/bridged_signal_evaluation.py`. A scanner commit-status lookup returned an empty statuses list; this is **not** a passing CI result or proof that CI is absent.

## Findings

Priority **P1** means resolve before approving the affected architecture or enabling the affected path. **P2** means specify/test before expansion or operation. **P3** means documentation/tooling cleanup. These are handoff priorities, not claims of an ongoing incident.

### A01 — P1: The approved sample message contains an unsupported assertion

**Evidence:** `instances/outreach-packages/outreach-package-01.json`; `generate_structures.py:821–833,899–918`.

The message says: “Saw Calendly on your site — booking and your CRM still don't talk.” Its sole hook reference is `f_acme_calendly_001`, which observes Calendly presence. That evidence does not establish the absence of a booking-to-CRM connection. Restricting template placeholders to OBSERVED facts does not constrain assertions hardcoded in the template itself.

**Resolution:** Require claim-level grounding for the whole rendered sentence, not just placeholders. Distinguish observations from hypotheses and questions. A safe alternative is: “I noticed Calendly on your site. How are booked appointments passed into your CRM today?” A stronger disconnection claim requires authorized API evidence or attributable human confirmation.

**Acceptance:** A template asserting disconnection with only vendor presence evidence must fail, even when its only interpolated value is OBSERVED.

### A02 — P1: The sample's approved state is not supported by the supplied pipeline

**Evidence:** `generate_structures.py:703–774,821–844,899–918`; `catalog.py:309–314`.

The Acme package is APPROVED. Its angle requires BOOKING_CRM_DISCONNECT and LOWCODE_ACTIVE, but the supplied Acme signals contain only the first as RESOLVED. The LOWCODE_ACTIVE example is for Northside and is SUPPRESSED. The maturity rubric requires at least two relevant resolved signals, but the supplied Acme maturity fact is L1 despite the example set lacking that support. The L1 package also does not demonstrate the stated “one rung up” rule from Acme's L1 maturity. Required slot `location.primary` is not populated. The sample LOWCODE_ACTIVE fact uses `vendor.present`, whereas the signal definition requires `automation.platform.present`; no projection rule connects those predicates.

**Resolution:** Declare AND/OR semantics for `requires_signals`, define current maturity versus offered rung, and generate the approved example from evaluated dependencies. Add explicit vendor-class-to-capability projections where intended. Samples may be partial, but must then be marked partial and must not purport to demonstrate end-to-end approval.

**Acceptance:** One replayable example reaches APPROVED from its own same-account inputs, while missing/suppressed prerequisites and missing required slots force abstention.

### A03 — P1: The validator does not enforce its advertised invariants

**Evidence:** `generate_structures.py:1031–1105`; `evidence/mutation_results.json`.

The check labeled “outreach package hooks cite known OBSERVED facts” only checks ID membership. It does not inspect state. The original validation accepts UNKNOWN or NOT_FOUND hook facts, cross-account evidence, candidate-authority sources, stale evidence, an incorrect but registered signal pack, empty resolved signal inputs, dangling adjudication references, nonexistent angle-pack references, and absent coverage evidence.

The generator does not invoke the OutreachPackage schema, AdjudicationRecord schema, or DerivationFlow schema on their respective objects. Independent validation shows the original examples are structurally valid today, but mutations such as an invalid package status or derivation rule type pass the original validation. A dictionary-based “exactly one pack” check loses multiplicity; a pre-index duplicate-membership test confirms the issue.

**Resolution:** Separate generation from validation. Discover and validate files on disk; apply schema validation, referential integrity, predicate-specific semantics, subject scope, state, coverage, freshness, authority ancestry, and package readiness. Use duplicate-preserving checks before constructing indexes.

**Acceptance:** Every intended invalid case fails for the expected reason, while valid cases remain accepted. Adding an invalid JSON instance anywhere in the declared artifact set must fail validation rather than be ignored.

### A04 — P1: Schema constraints leave contradictory or malformed states legal

**Evidence:** `generate_structures.py:37–93,150–182,202–232,290–318,950–956`; mutation results.

The Signal schema uses `not: {required: [unresolved_reason, suppressed_reason]}` for RESOLVED/CANDIDATE. This prohibits having both reason fields together, not having either one. A RESOLVED signal with `suppressed_reason: DNC` passes. Dates declared with `format: date-time` are not checked because the generator does not enable a FormatChecker; `not-a-date` passes. The TTL regex accepts `Potato`. Fingerprint operators are unrestricted objects; unknown operators and empty fixture lists pass. Predicate vocabularies are present as metadata but are not applied to fact objects: an L99 maturity value passes. Sixty-three of 79 predicates currently have object type `any`.

**Resolution:** Use explicit status-dependent record shapes, mandatory format validation, a defined duration representation, a closed operator union, meaningful minimum test coverage, and predicate-specific object validators. Keep UNKNOWN on the state field rather than inventing incompatible value enums.

**Acceptance:** Reject malformed dates/TTLs, invalid vocab values, unknown operators, unsupported state/reason combinations, and semantically incorrect object structures.

### A05 — P1: Absence is incompletely proven and sometimes means too much

**Evidence:** `instances/facts/fact-05.json`; evidence instances; `registry/signal-types.json`; `generate_structures.py:603–631,703–742,1059–1077`.

`f_acme_intgap_003` is NOT_FOUND with no LEDGER_COVERAGE_REF, yet its signal is RESOLVED. The generator only requires evidence for non-reproducible sources, not for every absence. Both SEO_SCHEMA_ABSENT and SEO_AI_INVISIBLE have `requires_coverage: false` despite relying on absence, because the flag is inferred by searching for the word “coverage” in prose.

More fundamentally, a completed public-site scan can show that no supported integration footprint was detected within the checked scope. It cannot, by that alone, establish that private backend systems are disconnected. Rendering failures, skipped pages, truncated snapshots, and provider errors also need explicit UNKNOWN semantics rather than business-wide absence.

**Resolution:** Encode scope/capture mode/completion/detector version in typed coverage records. Separate absence of public evidence from confirmed absence of business capability. Do not infer machine policy from wording.

**Acceptance:** Every NOT_FOUND fact links to a compatible complete coverage record; incomplete scans abstain. Public no-match evidence cannot authorize a private-workflow claim.

### A06 — P1: Registry closure is not complete

**Evidence:** `registry/derivations.json`, `registry/predicates.json`; `generate_structures.py:438–443,525–568,1089–1098`; `evidence/semantic_checks.json`.

Thirteen derivations declare **15 unregistered output strings**, including `automation.rung_basis`, `automation.next_rung_gap`, `cohort.size`, and `cohort.version`. Some outputs are descriptive strings such as `direction (good/bad)` and `regulated_regimes[]`, not usable predicate identifiers. The combined business-type/industry catalog entry produces only `tag.business_type`; `tag.industry` has no registered producing flow.

The source registry is explicitly a sample. It contains source registrations for only two of the 23 derivation flows. That is a completeness gap, not evidence that its supplied fact source references are broken. Specify whether release linking generates the remaining registrations or requires them explicitly.

Conversely, the fact-reference validator includes only base FACTS, excluding DERIVED_FACTS. An existing derived growth fact added to a GROWING_PAIN signal is rejected as a dangling reference.

**Resolution:** Distinguish output predicates from fields inside their object payloads. Register every actual emitted predicate and source, validate both directions, and use one fact index across base, derived, and cohort facts. Require explicit cross-subject relations where cohort facts are inputs to account-level signals.

**Acceptance:** Every declared output, source, referenced fact, ontology identifier, and pack resolves, with no silent aliasing or dictionary overwrite.

### A07 — P1: The recompute graph is incomplete, and its cycle check misses self-cycles

**Evidence:** `generate_structures.py:958–997`; `registry/recompute-graph.json`; semantic and mutation results.

The graph construction explicitly removes self-dependencies. A same-flow cycle therefore passes, although a two-flow cycle is rejected. Seven flows have no extracted machine-readable inputs: business-type, ICP-fit, data-quality, cohort baseline, percentile, trend, and outlier. Their narrative dependencies do not yield ordinary incoming predicate/signal dirty triggers.

The graph orders derivations but does not establish a global executable ordering across signal evaluation, adjudication, derivation, and cohorts. Yet growth descriptors feed GROWING_PAIN, stack descriptors feed confound handling, and cohort outputs feed SEO signals. The linear diagrams do not resolve those dependencies. Expiration, suppression changes, authority changes, entity rebinds, retractions, membership changes, and policy releases also need recomputation rules.

**Resolution:** Use an explicit typed dependency graph across phases. Preserve and reject same-epoch self-edges. Model legitimate temporal feedback as an explicit previous-epoch dependency, not as an omitted edge. Define timer-driven invalidation as well as data changes.

**Acceptance:** Every consumed datum/policy has a declared trigger; same-epoch cycles fail; changes and expirations invalidate all dependent facts, signals, and packages.

### A08 — P1: The 23 rubrics are registered descriptions, not executable algorithms

**Evidence:** `catalog.py:309–376,450–503`; `generate_structures.py:95–131,525–568`.

Rule expressions, UNKNOWN conditions, and temporal windows are mostly free text. Inputs are extracted from prose. Implementers still have to choose thresholds, weights, tie handling, missing-data behavior, and time boundaries. There are direct vocabulary conflicts: growth emits UNDETERMINED but the registered vocabulary uses STABLE; platform MIXED conflicts with mixed; readiness not-ready conflicts with not_ready; location single conflicts with single_location.

**Resolution:** Define a small typed expression language or bind each flow to a versioned deterministic function plus typed parameters. Make the algorithm return only registered values. Preserve prose as documentation, not as the normative executable rule.

**Acceptance:** Each flow has positive, negative, boundary, insufficient-data, and temporal fixtures with expected outputs; running those tests does not require inventing business policy.

### A09 — P1: The design-time fingerprint fixture executor does not implement its declared semantics

**Evidence:** `generate_structures.py:1002–1029`; `fixtures/`; `evidence/semantic_checks.json`.

The `host_suffix` implementation searches raw HTML with a broad regex rather than parsing URL hostnames. It fires on notcalendly.com, calendly.com.evil.example, and a Calendly string in an unrelated URL path. It also fires on a vendor link in a blog, an agency-footer consultation link, a commented-out embed, and a data-attribute name merely written in prose. It misses a protocol-relative asset URL and whitespace before the equals sign in an HTML attribute. Unknown operators are silently skipped; scope is not evaluated.

The supplied three files are small illustrative HTML fixtures, not a captured multi-site evaluation corpus with preserved capture provenance. The agency negative does not contain the target Calendly marker, so it does not test attribution of that marker to an agency rather than the target business. These findings concern the archive's `_match` helper, not the separately implemented live scanner matcher.

**Resolution:** Use the same parser/operator implementation for fixture tests and runtime. Parse hosts and attributes, declare which DOM scopes count, and test candidate attribution with the target marker actually present.

**Acceptance:** The nine counterexamples behave as declared, and shadow promotion is measured against an independently labeled evaluation set.

### A10 — P1: Current-state identity is too coarse for multivalued facts and corroboration

**Evidence:** `data-contracts-and-modules.md:88–96,274–275`.

“Latest active fact per (subject, predicate)” would collapse multiple simultaneously valid vendors, integrations, locations, identifiers, or observations from different sources. A newer vendor.present observation can replace an unrelated older vendor under that key. It also undermines independent corroboration. Recency-only supersession and weighted conflict precedence need separate, explicit responsibilities; a newer failed observation must not silently erase an otherwise fresh supported claim.

**Resolution:** Distinguish observation identity from claim identity. Include the relevant object/entity and scope in multivalued claim keys, retain source-specific observations, and adjudicate competing claims separately. Specify equal-time ordering, event time versus ingestion time, and retraction/merge semantics.

**Acceptance:** Two concurrently valid vendors survive projection and replay; genuine conflicting observations remain auditable; a timeout does not silently become evidence of removal.

### A11 — P1: The short fact contract needs a mandatory provenance path outside the fact

**Evidence:** `generate_structures.py:37–61`; `data-contracts-and-modules.md:96–104,250–271`; `SYSTEM.md:103–123,538`.

The slim Fact object is reasonable, but reproducible sources do not require evidence records. The bundle does not provide a normative enforceable join from every fingerprint fact to its exact immutable snapshot and matcher, or from every derived fact to its retrievable input set and execution. A flow version identifies a recipe; an input-set hash identifies content only if that content is actually retained and addressable. Neither alone demonstrates the promised audit/replay path.

**Resolution:** Keep the slim fact if desired, but require a journal provenance edge or execution sidecar containing snapshot/input-set references, model/prompt/raw-response/repair references where applicable, and pinned execution metadata. Carry ancestry eligibility and freshness through derivation; re-computing from stale/candidate inputs must not make them fresh/active.

**Acceptance:** Delete projections and reconstruct every fact's original inputs and eligible lineage using retained journal/blobs alone, including retracted or rebound history.

### A12 — P1: Conflict precedence, lifecycle, and adjudication outcomes are not fully specified

**Evidence:** `generate_structures.py:202–232,776–819`; `data-contracts-and-modules.md:191–205`; mutation results.

The score formula leaves recency_decay, half-life, null priors, weighting across multiple observations, independent-source counting, and numerical tie policy unspecified. Repeated representations of the same upstream evidence must not count as independent corroboration. The schema allows FIRST_DECLARED ties despite the stated abstention rule. The suite-confound disambiguation example decides SUPPRESSED while the adjudication pack says UNRESOLVED. Their semantic purposes differ: evidence insufficiency is not an operational do-not-contact decision.

Several registry types lack typed lifecycle/promotion fields even though “one lifecycle for everything” is claimed. Sample active-source precision/n/gold-set values are not backed by an available evaluation artifact; they are illustrative metadata, not demonstrated calibration. Candidate ancestry must not be promoted implicitly by an active derivation source.

**Resolution:** Define exact scoring and provenance independence; use one typed confound/adjudication representation with reason-code consistency; require recorded release/promotion evidence and distinguish historical pinned authority from present delivery revocation policy.

**Acceptance:** Equivalent upstream evidence cannot increase corroboration merely by duplication; ties abstain; confounds have consistent outcomes; candidate/revoked ancestry blocks production use.

### A13 — P1 for the AI SEO path: AI visibility has conflicting state semantics and no complete experiment contract

**Evidence:** `instances/facts/fact-06.json`; `registry/signal-types.json` SEO_AI_INVISIBLE; `BACKLOG.md` item 4.

The example records a completed probe as OBSERVED with cited:false, but the signal requires the same predicate to be NOT_FOUND across a probe set. Both conventions can be made coherent; the design must select or explicitly transform between them. The AI-visibility mini-spec is already acknowledged as deferred, so this feature should not be described as fully implementation-ready.

**Resolution:** Use completed probe measurements with explicit cited true/false, separate unsuccessful execution as UNKNOWN, and derive a scoped aggregate after declared coverage. Pin engine/model, prompt variants, location/language, timestamp/window, repetitions, citation/entity matching, and the eligible denominator. Keep any copy specific to the tested probes rather than all AI search.

**Acceptance:** A failed provider call cannot become “not cited”; partial or ambiguous probe sets abstain; measured claims can be reproduced from retained model I/O.

### A14 — P2: Cohort statistics and feedback metrics need explicit populations and estimands

**Evidence:** cohort schema/definition and derived examples; `catalog.py` cohort and angle.performance rubrics; `data-contracts-and-modules.md:218,270–278`.

Minimum size alone does not define the valid denominator. The design still needs rules for measured versus unknown members, coverage eligibility, changing membership, cohort version/as-of, ties, percentile conventions, trend windows, and outlier thresholds. Member-specific percentiles/outliers need an account/member reference while preserving their relationship to a cohort. A below-minimum n and an ORG subject on the example cohort fact currently pass validation.

Outcome feedback similarly needs deduplicated send/event IDs, exposure denominators, observation-window maturity, and rules for pending replies, bounces, unsubscribe, and repeated sends. A reply rate among selected recipients is not automatically a causal estimate of an angle's effectiveness.

**Resolution:** Define each statistic's population, measurement eligibility, window, missing-data policy, and consumer scope. Preserve package/angle/recipient/exposure lineage for outcomes and use controlled comparisons before claiming causal performance improvement.

**Acceptance:** UNKNOWN members are not silently counted as negative; small measured samples abstain; repeated webhooks do not inflate rates; pending outcomes are not prematurely classified as failures.

### A15 — P1 before foundational runtime: Journal and release semantics remain narrative contracts

**Evidence:** `data-contracts-and-modules.md:174–205,234–283`; `SYSTEM.md:538–539`; schema inventory.

RunManifest, Snapshot, Subject, the journal envelope, and typed lifecycle/execution events do not have the same normative machine contracts as Fact/Signal. Ontology/crosswalk identifiers likewise lack full concrete registry closure. The journal's hash-chain is optional in the docs, whereas the inventory calls it hash-chained. Canonical serialization, sequence allocation, idempotency, crash recovery, partial writes, concurrent appends, clock use, replay ordering, and schema/release migration remain decisions.

**Resolution:** Define typed foundational contracts before implementing persistence. Pin evaluation time, input snapshot/offset, registry/code/policy releases, and external result references. Define replay as canonical logical-view equality unless physical database byte identity is explicitly required and justified.

**Acceptance:** Crash/retry/replay scenarios preserve exactly the intended observations and lifecycle events; canonical exports match after projection rebuild without live external calls.

### A16 — P2 before operation: Delivery, security, budget, and repair behavior need enforceable boundaries

**Evidence:** `data-contracts-and-modules.md` runtime modules and operational store; `BACKLOG.md` items 1–2; absence of executable implementations in the archive.

These are specification-readiness gaps, not demonstrated deployment bugs. Delivery needs an outbox/idempotency contract, last-moment suppression and authority checks, package invalidation, and retry behavior across CRM/provider synchronization. Budget controls need atomic reservations and charging semantics under concurrency and retries before paid calls. LLM raw-response retention must be complemented by a bounded JSON-repair contract that preserves the original response, repair attempts, schema failures, costs, and terminal abstention; recording raw I/O alone does not implement JSON repair. Untrusted-page/model boundaries, sensitive-data access, retention/deletion versus immutable evidence, and tenant/account isolation also need policies.

**Resolution:** Turn these requirements into typed interfaces and negative acceptance tests at the affected rollout stage. Do not activate provider writes or delivery merely because local packages validate.

**Acceptance:** Duplicate retries cannot double-send; DNC arriving after approval prevents delivery; concurrent requests cannot overspend a declared limit; irreparable model output abstains; repaired content never bypasses claim grounding or authority gates.

### A17 — P1 for integration: The existing runtime needs a versioned compatibility map

**Evidence:** pinned scanner README/runtime tree; pinned Master `runtime/bridged_signal_evaluation.py`.

“No runtime code exists” accurately describes the uploaded target design, not the entire linked codebase. The scanner already has a live crawler, append-only observation events, SQLite projections, research queue, and rule promotion path. Master contains acquisition, orchestration, feature/signals, and outreach runtime. Its inspected bridge audits 223 detector evaluations and emits legacy facts with verdict/resolution/promotion fields, not the new slim Fact contract. Those 223 detectors are not the same counting unit as the new 18 business signals.

The scanner's documented runtime statuses include active_candidate/composite_candidate, whereas the new design requires candidate authority to remain shadow-only. This is an adapter/migration risk, not proof of a new production leak. Legacy bounded artifacts and JSON-LD type extraction also need capability mapping before being treated as full stored-snapshot evidence.

**Resolution:** Map old identifiers, object shapes, statuses, provenance, and capture capabilities to the new release. Mark every capability retained, merged, adapter-backed, deferred, or removed. Quarantine unmapped semantics; do not translate status names blindly.

**Acceptance:** Representative legacy events round-trip through a versioned adapter with original provenance preserved. Unsupported scopes become UNKNOWN, not inferred negatives; candidate status cannot silently become production authority.

### A18 — P3: Inventory, source-of-truth, and workbook portability need correction

**Evidence:** `README.md`, `BACKLOG.md`, `build_workbook.py:1–19`, disk/archive inventory.

There are 25 example JSON instances, not 26. The listed runtime groups sum to 15 components, not 16. `STRUCTURES.md` is referenced but the file is lowercase `structures.md`. README still describes 18 derived rows and 12 examples in older sections despite the actual 23/25. BACKLOG's resolved table still says 22 flows. Schema constants, source samples, and examples live in generate_structures.py, so catalog.py is not literally the only editable source for all artifacts. Direct edits to generated schemas are overwritten. Workbook output is hardcoded to the author's workstation and its styling helper is an external local dependency.

**Resolution:** Generate inventory counts, use correct paths/case, document ownership of each authored artifact, and make workbook output/dependencies portable. Limit the current clean-room assurance to the generated JSON files; independently test workbook regeneration before claiming whole-project portability.

**Acceptance:** Fresh checkout plus declared dependencies can rebuild to a caller-selected output directory; generated-file diffs and counts are checked in CI.

## Resolution sequence

1. **Truth and identity:** A01–A02, A05, A10–A13. Agree what each state and claim means; define account scope, maturity versus offer rung, provenance, and authority inheritance.
2. **Contracts and linker:** A03–A04, A06–A08, A15. Enforce the decisions with typed records, complete reference checks, executable rubrics, and a global dependency model. Convert each counterexample into a permanent regression test.
3. **One safe vertical slice and compatibility:** A09, A17. Stored capture → attributed fact → conservative signal/adjudication → grounded package. Prove an approved path and several abstaining paths before expanding to all predicates and signals.
4. **Controlled operation and expansion:** A14, A16, A18. Complete provider-specific experiments, calibration, outcomes, budgets, delivery, retention, and portability at the stage that uses them.

## Suggested replacement for the handoff claim

> The archive contains a reproducible design-time contract and catalog bundle. Its existing examples validate structurally, but semantic invariants, complete registry linking, executable decision rules, and runtime integration still require the identified fixes and acceptance tests before the design can be treated as implementation-complete.

## Evidence map

- `evidence/baseline_validation.log`: original 59-check run.
- `evidence/independent_validation.json`: schema/instance checks and generation reproducibility.
- `evidence/mutation_results.json`: 40 adversarial/control validation outcomes with injected change and output tail.
- `evidence/supplemental_checks.json`: derived-fact linking and pre-index duplicate membership.
- `evidence/semantic_checks.json`: registry closure, missing inputs/coverage, nine matcher cases, workbook comparison.
- `evidence/source_excerpts.md`: line-numbered excerpts from the uploaded source.
- `evidence/audit_metadata.json`: archive hash, execution versions, and pinned repository commits.
- `tools/`: reproducible audit tools. See README for scope and interpretation.
