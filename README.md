# KeenSight — AI signals and outreach source workspace

**Complete consolidated source and documentation from the latest supplied local implementation.** This is not a claim that the full proposed product is implemented or POC-ready.

The authoritative code is **collector 0.2.0 + canonical reference 4.2.0 + the protocol checker**. Later audit archives contained the same application source, not additional repairs. This workspace retains that code without changing application behavior, and includes the known-failing acceptance requirements, feature map, user journeys, and full E2E design.

## Start here

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e './collector[test]'

python tools/workspace.py check
python tools/workspace.py test
python tools/workspace.py demo --output ../keensight-demo
python tools/workspace.py journeys --output ../keensight-journeys
```

On Windows use `.venv\Scripts\Activate.ps1` instead of the activation command above. The commands also run from source without an editable install when their Python dependencies are already available. `make` targets are optional; the Python commands are cross-platform.

Output directories must be outside this source tree. Use a fresh output directory for a clean walkthrough. The eight journeys run local synthetic fixtures/reference helpers only; J07 does **not** exercise the missing collector-to-canonical admission bridge.

## What's in the codebase

| Directory | Purpose | Status |
|---|---|---|
| `collector/` | Scrapling adapter, extraction, matching, deduplication, storage, replay, standalone commands, tests | Local prototype; actual SDK integration unverified in the assembly environment, browser disabled |
| `canonical/` | Broad fact/metric catalogs, 75 schemas, semantic validators, narrow reference calculations and no-send exporter | Contract/reference implementation, not a persistent production service |
| `protocol/` | Shared request/result envelopes, exact fixture operation validation, tests | Reference checker, not a general enforcing runner |
| `product-design/` | Entire 39-module product, field-level proposed contracts, workflow plans | Design only |
| `implementation/` | Scrapling-first phases, modules/submodules, 38-command traceability, source reuse plan | Implementation handoff |
| `docs/` | E2E stage cards, 31 offline diagrams, service extraction, class reference, features/journeys | Architecture and review documents |
| `walkthroughs/` | Eight executable local fixture journeys | Runs commands in separate subprocesses |
| `audits/iteration2/` | Submodule safety probes and unresolved requirements | Intentionally failing acceptance tests retained |
| `audits/poc/` | Standard-usage POC probes and repair checklist | Intentionally failing acceptance tests retained |
| `sources/` | Original 38-command workbook and 52-idea business ledger | Supplied inputs, not verified provider access or performance claims |
| `tools/` | Workspace launcher and source-integrity checks | Local development tooling only |
| `provenance/` | Source archive hashes, byte-identical component inventory, path-adaptation log | Reproducible assembly record |
| `verification/` | Earlier repair evidence plus current assembly logs/report | Read the dated scope of each result |

There are **no `.gitmodules` Git submodules**: all delivered component code is included in this one repository.

## The defects are included, not hidden

Passing the existing regression suite does not mean POC sign-off. These independent suites preserve the additional requirements that the current implementation still fails:

```bash
python tools/workspace.py audit poc --output ../keensight-poc-audit
python tools/workspace.py audit iteration2 --output ../keensight-safety-audit
```

Both currently return a nonzero exit code. Their failures are not marked xfail, discarded, or included in the successful regression count. Read [KNOWN_ISSUES.md](KNOWN_ISSUES.md) before using the prototype with real data.

Run observations without asserting those requirements:

```bash
python tools/workspace.py audit poc --probes-only --output ../keensight-poc-probes
python tools/workspace.py audit iteration2 --probes-only --output ../keensight-safety-probes
```

A successful probe process means the probe executed, **not** that the observed system behavior was correct.

## Actual SDK verification is a separate gate

```bash
python -m pip install -e './collector[live,test]'
python tools/workspace.py live-check --output ../keensight-sdk-check
```

This fails explicitly when the pinned Scrapling SDK cannot import; it does not silently count a skip as verified acquisition. The current SDK integration test uses a controlled local HTTP fixture. Native browser capture remains disabled. No production rule approval is implied by the synthetic example rule pack.

## Documentation navigation

- [Current status and limitations](STATUS.md)
- [Feature map](docs/FEATURE_MAP.md)
- [User journeys and exact local commands](docs/USER_JOURNEYS.md)
- [Updated F00–F26 stage walkthroughs](docs/UPDATED_STAGE_WALKTHROUGHS.md)
- [Interactive feature/journey navigator](docs/FEATURE_AND_JOURNEY_REVIEW.html)
- [E2E UML diagram book](docs/DIAGRAM_BOOK.html) — open locally in a browser
- [Editable dataflows and UML](docs/DATAFLOWS_AND_UML.md)
- [Class reference](docs/CLASS_REFERENCE.md)
- [Submodule ownership and contracts](docs/SUBMODULE_TRACEABILITY.md)
- [Standalone operations and service extraction](docs/SERVICE_EXTRACTION.md)
- [Full product architecture](product-design/DESIGN.md)
- [Implementation phases](implementation/IMPLEMENTATION_PHASES.md)
- [All 38 collector commands](implementation/SCRAPLING_38_COMMANDS.md)
- [POC readiness checklist](audits/poc/POC_CHECKLIST.md)
- [Assembly validation](verification/ASSEMBLY_VALIDATION.md)

## Source and packaging integrity

```bash
python tools/verify_manifest.py --components
python tools/verify_manifest.py --strict
```

`--components` compares imported implementation files with the supplied repaired source. The default manifest compares this complete distributed snapshot. Once you intentionally edit code, an integrity mismatch is expected; this is not a runtime security or authentication system.

Older component READMEs and `docs/history/` preserve their original version narratives and test counts. **This root README, STATUS.md, and the current assembly validation report determine what is delivered now.** In historical audit commands, `baseline/collector`, `baseline/canonical`, etc. refer to the corresponding root directories in this workspace. Use the root launcher for relocated tests.

No GitHub push or hosted deployment is performed by these commands. See [repository handoff](docs/REPOSITORY_HANDOFF.md) for the optional local Git-bundle workflow.
