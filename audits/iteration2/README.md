> Workspace relocation: the original nested `baseline/` is now the repository root. Run `python tools/workspace.py audit iteration2` from the root. The source and historical test findings are unchanged; this archive does not contain post-audit fixes.

# KeenSight — iteration 2 audit, feature map and user journeys

**Read-only review of the repaired September 15 source, not a new runtime release.**

Collector **0.2.0**, canonical reference **4.2.0**, the draft protocol checker and product-design records are retained under `baseline/`. No application behavior is patched in this package. Proposed repairs are described with reproducible failures and acceptance requirements.

## Read in this order

1. `REVIEW_NAVIGATOR.html` — offline feature/journey/stage review navigator.
2. `AUDIT.md` — 15 code/contract findings and one separately classified temporal-policy question.
3. `FEATURE_MAP.md` — 36 user-facing features mapped to all 39 module IDs.
4. `USER_JOURNEYS.md` — 19 user journeys with actors, steps, outputs, failure branches and real invocation commands where supported.
5. `UPDATED_STAGE_WALKTHROUGHS.md` — all 27 existing F00–F26 stage cards, enriched with feature, journey and finding links.
6. `SUBMODULE_TRACEABILITY.md` and `SOURCE_EXCERPTS.md` — exact submodule ownership and numbered source evidence.

There is **no invented endpoint** for proposed contacts, campaigns, sending or CRM functionality. The eight executable walkthroughs use local synthetic fixtures/reference helpers, not live accounts. The collector-to-canonical bridge and enforcing generic module runner remain unimplemented. Original diagrams and service-extraction designs are retained under `baseline/docs/`; the new navigator does not claim new service deployments.

## Install the local test dependencies

From the unpacked package root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e './baseline/collector[test]'
python -m pip install -r ./baseline/canonical/requirements.txt
```

Use the corresponding virtual-environment activation command on Windows. These installation commands may access a package index; the walkthrough execution itself uses no network or sending. The actual Scrapling SDK is an optional separate integration prerequisite, described in J09; the test remains unverified here, and native browser capture is disabled.

## Execute the tested walkthroughs

```bash
python walkthroughs/run_local_journeys.py --output ./journey-output --journey all-local
```

Or select a journey such as independent extraction/matching/resolution:

```bash
python walkthroughs/run_local_journeys.py --output ./journey-J03 --journey J03
```

The harness launches separate Python processes and saves arguments, working directory, exit code, stdout and stderr. It is **not** the proposed general module runner. Use a fresh output directory so previous logs are not overwritten. Fixed synthetic evaluation timestamps are intentional; they do not grant current real-world permission.

## Audit and verification

```bash
# Verify every manifest-listed file in the unchanged source baseline.
python baseline/verify_integrity.py

# Cross-check this review's feature, journey, finding and evidence indexes.
python verify_review.py

# Rerun all read-only probes. Each uses temporary stores/synthetic copies.
python audit_probes.py --output ./probe-results-new.json

# Deliberately failing safety requirements against the unchanged baseline.
python -m pytest tests -q --tb=short
```

The last command is expected to exit **1** until the repairs are implemented: **16 failed, 6 passed** in this review. The separately unresolved effective-time policy is not imposed as an assumed universal failing assertion. `audit_probes.py` also accepts `--select R2-A01 R2-A03`; set `KEENSIGHT_BASELINE` before invocation to test another explicitly compatible source directory.

Baseline suites are separate:

```bash
(cd baseline/collector && python -m pytest -q)
(cd baseline/canonical && python -m pytest -q)
(cd baseline/protocol && python -m pytest -q)
```

Observed baseline: **834 passed, one skipped** across the three suites. New probes: **23**, comprising 16 safety counterexamples, one temporal-policy question and six passing controls. Working smoke journeys: **8**, with **20** separate invocations. See `reports/` for the actual outputs. Do not add these different counts together as a single runtime-coverage score.

## Repairs to prioritize

1. Identity-evidence closure, current template authority, and a single publication payload.
2. Consistent historical snapshots, generated-artifact availability, and support-count semantics.
3. Parsing completeness, immutable import identity, candidate eligibility and invocation-level diagnostics.
4. Shared matching/attribution policy and a genuinely enforcing module runner before service extraction.

Keep historical decisions separate from current-use vetoes. Keep all provenance but count only qualifying independent substantive support. Splitting code into services does not repair an inconsistent boundary; pass each operation's contract tests locally first.
