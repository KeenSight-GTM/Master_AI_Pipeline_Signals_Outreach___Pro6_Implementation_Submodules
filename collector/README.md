> **Current collector: 0.3.0; ScanBundle 1.2.** The earlier narrative below is historical. See `../docs/POC_REPAIRS.md` for resolved audits, explicit `scan --retry-failed`, `claims --subject`, release-aware `candidates --rules --as-of --include-resolved`, compatibility, and test scope. Native browser remains disabled; actual SDK verification is a separate gate.

> **Review-and-repair 2026-09-15:** This subpackage is patched. Use the package-root README and `verification/REPAIR_REPORT.md` for current status, compatibility, tests, and remaining work. The historical narrative below is retained for context.

# KeenSight Scrapling Ingestion — 0.1.0

First local collector implementation. It retains every fingerprint match, creates
one observation per claim/value/capture, and presents one claim view across
captures. Multiple overlapping detectors never become independent votes.

**Release boundary:** deterministic parsing, matching, SQLite persistence,
resumable acquisition orchestration, donor import, research harvesting, and replay
are implemented and tested. A real Scrapling 0.4.15 static adapter is included,
but its SDK integration test was skipped in the build environment because that
dependency could not be installed over the unavailable network. The bounded native
browser implementation is NOT delivered; `FETCH_STEALTH` is a disabled extension
point. This is not all-38 production sign-off, the full donor library, a canonical
Fact Service, or a hosted/multi-tenant production release.

## Install

Python 3.11 or later:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[live,test]"
python -m pytest -q
```

For offline analysis only, install `.[test]` instead of `.[live,test]`. Core parsing
uses lxml explicitly. Live HTTP acquisition uses Scrapling; there is no hidden
requests/urllib fallback. Enabling `live` does not enable browser crawling.

## Start with the reproducible demo

```bash
ks-scan demo --output ./demo-output
ks-scan check ./demo-output/scan-bundle.json --store ./demo-output
```

The demo uses synthetic HTML, synthetic approval metadata, a deterministic clock,
and an explicit fixture transport. It makes **zero network requests**.

Expected findings: **7 rule matches → 2 capture observations → 1 claim**.
Five matches are approved within this design fixture and two are candidate-only.
Three distinct element evidence points are retained across the two pages.
The source-group count is one. The combined confidence is `null`/`NOT_COMBINED`.

## Analyze your own retained HTML immediately

```bash
ks-scan analyze-file \
  --html ./examples/page.html \
  --url https://example.test/ \
  --observed-at 2026-09-14T12:00:00Z \
  --tenant local --subject account:example --run imported-001 \
  --rules ./examples/demo-rules.json \
  --store ./imported-output --output ./imported-output/scan-bundle.json
```

The collection timestamp and subject are user-supplied assertions in this mode,
not verified live acquisition or canonical organization binding. Source provenance
is explicitly `source:user-provided-snapshot`.

## Live static scan (requires the live extra)

```bash
ks-scan scan https://example.com/ \
  --tenant local --subject account:example --run scan-001 \
  --rules ./examples/live-candidates.json \
  --store ./scan-output --output ./scan-output/scan-bundle.json \
  --max-attempts 8 --max-pages 5
```

The supplied live rule example is candidate-only and not a calibrated production
library. The approved demo pack is rejected for live scans. Source permission,
retention suitability, and canonical subject binding remain operator/application
responsibilities. The scanner never logs in, submits forms, sends outreach, or
uses rate-limit bypass as browser escalation.

The runner checks robots before content. Every attempt, redirect, metadata fetch,
failed request, and optional probe consumes the same bounded top-level budget.
429 stops subsequent capture for the target; a failed robots fetch fails closed.
Redirects and canonical tags do not silently widen the permitted origin or merge
companies. Cross-origin/www redirects need a future explicitly bound redirect
policy; this initial version declines them.

Reusing an identical run/config resumes its persisted attempts. A changed release
or configuration requires a new run ID. An interrupted PENDING request is
reported, not blindly retried. Use a new run after investigating that diagnostic.

## Stored-evidence replay

```bash
ks-scan replay --store ./demo-output --tenant demo \
  --capture-run demo-capture-1 --evaluation-run replay-001 \
  --as-of 2026-09-14T13:00:00Z \
  --rules ./examples/demo-rules.json --output ./demo-output/replay.json
```

Replay performs no fetching. It verifies retained body hashes, reruns extraction
and matching, and retains original capture timestamps and expiry. A new release
can append new support to existing observation IDs. No retrospective network,
DNS, or private-system evidence is invented.

Query historical observations through a current rule allowlist:

```bash
ks-scan claims --store ./demo-output --tenant demo \
  --rules ./examples/demo-rules.json --as-of 2026-09-14T13:00:00Z
```

## Existing SEO fingerprinter import

```bash
ks-scan import-donor \
  --input ./examples/donor-shaped.jsonl \
  --vendor-map ./examples/vendor-map.json \
  --output ./imported-candidates.json --report ./import-report.json
```

Supported donor operators are documented in `docs/DONOR_INTEGRATION.md`.
Imported entries always remain candidates and conservatively emit `vendor.mentioned`.
Unknown/composite operators, unsupported scopes, ambiguous cardinality, and missing
product mappings remain fully represented in quarantine. There is no automatic
status upgrade, silent dropping, or first-ID-wins conflict resolution.

The examples are donor-shaped synthetic fixtures, NOT the full upstream corpus.
The separately referenced `99_MASTER_ALL` workbook and 2,500-signature library are
not in this release.

## Unknown-feature research

```bash
ks-scan candidates --store ./scan-output --tenant local --min-hosts 3
```

The technical index counts observed origins and capture identities. It does not
claim distinct businesses or statistically independent confirmations. Research
features contain normalized hosts/cookie names rather than URL query secrets.
No automatic rule generation or promotion is implemented.

## Architecture

```text
URL / permitted snapshot
  → budgeted acquisition attempt
  → immutable capture + original bytes
  → 17 extraction functions with exact element locators
  → typed rules, retaining every matching rule/branch/surface
  → observation + many support links
  → deduplicated claim view
  → collector ScanBundle
  → future Fact Service admission and canonical binding
```

The module's `Observation` is a **collector record**, not a schema-compatible
v4.1 `Fact` ready for direct production insertion. `handoff.requires_fact_service_admission`
is always true. See `docs/ARCHITECTURE_BOUNDARY.md`.

## Main modules

| Module | Responsibility |
|---|---|
| `core.py` | Typed records, strict JSON, stable identity, UTC/TTL utilities |
| `transport.py` | Pinned Scrapling adapter, synthetic transport, disabled browser boundary |
| `urls.py`, `discovery.py` | URL/origin rules, DNS policy, robots, sitemap and template discovery |
| `extraction.py` | Seventeen deterministic extraction commands |
| `rules.py` | Closed rule compilation, exact host/regex/region/image matching |
| `claims.py` | Observation/support creation and non-inflating claim views |
| `storage.py` | Content-addressed blobs, SQLite, attempts, support history, research index |
| `importer.py` | Conservative donor JSON/JSONL adapter and quarantine report |
| `pipeline.py` | Batch capture/evaluation/replay orchestration |
| `validation.py` | Bundle schema, input references, rerun matching, derived-view checks |
| `commands.py`, `cli.py` | All 38 IDs, CLI commands and atomic JSON output |

See `docs/COMMAND_COVERAGE.md` for implemented, SDK-unverified and deferred boundaries.
