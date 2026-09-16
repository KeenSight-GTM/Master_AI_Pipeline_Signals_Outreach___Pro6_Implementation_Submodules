# KeenSight — AI signals and outreach source workspace

**Current repair: collector 0.3.0, canonical reference 4.2.0, and the protocol checker.** The nine POC failures and 16 iteration-2 submodule failures have been repaired. Both audit suites are now mandatory regression gates in `verify`; none of their assertions was removed or marked xfail.

This is not a claim that the complete product is implemented or production-ready. Live SDK acquisition requires its separate integration gate, browser capture stays disabled, and the persistent collector-to-canonical bridge and engagement runtimes remain unimplemented.

Start with [POC repairs and invocation changes](docs/POC_REPAIRS.md), [current status](STATUS.md), and [remaining work](KNOWN_ISSUES.md).

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
| `audits/iteration2/` | Submodule safety probes and unresolved requirements | Historical reproductions; repaired acceptance tests run as regression gates |
| `audits/poc/` | Standard-usage POC probes and repair checklist | Historical reproductions; repaired acceptance tests run as regression gates |
| `sources/` | Original 38-command workbook and 52-idea business ledger | Supplied inputs, not verified provider access or performance claims |
| `tools/` | Workspace launcher and source-integrity checks | Local development tooling only |
| `provenance/` | Source archive hashes, byte-identical component inventory, path-adaptation log | Reproducible assembly record |
| `verification/` | Earlier repair evidence plus current assembly logs/report | Read the dated scope of each result |

There are **no `.gitmodules` Git submodules**: all delivered component code is included in this one repository.

## Regression gates, including the repaired defects

`python tools/workspace.py verify` now runs all component/workspace tests **and both audit suites**. They can also be invoked separately:

```bash
python tools/workspace.py audit poc --output ../keensight-poc-audit
python tools/workspace.py audit iteration2 --output ../keensight-safety-audit
```

Both now return zero. The original audit reports and their historical output logs remain unchanged, so old reports still show the original failures. Current results and remaining implementation limits are in [STATUS.md](STATUS.md) and [the repair report](verification/POC_REPAIR_VALIDATION.md).

Probe-only commands remain available. A successful probe process means it ran, not that an observed behavior necessarily met its requirement.

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
python tools/verify_manifest.py --strict
```

The default manifest covers the current Git-tracked source snapshot, excluding itself. Runtime databases, caches, environments, and archive outputs are not source files and are not included.

`python tools/verify_manifest.py --components` intentionally compares against the **original pre-repair component import** in `provenance/`. It reports changed files after these repairs; this historical comparison is not the current verification gate. Those original manifests are retained rather than rewritten as proof of unchanged source.

Historical component READMEs, audit reports and `docs/history/` preserve earlier results. **The root README, STATUS.md, docs/POC_REPAIRS.md and verification/POC_REPAIR_VALIDATION.md describe this repair.** In archived examples, `baseline/collector` and `baseline/canonical` refer to the corresponding workspace roots; use the root launcher for relocated tests.

The commands above do not deploy services or authorize provider actions. No sender is enabled.
