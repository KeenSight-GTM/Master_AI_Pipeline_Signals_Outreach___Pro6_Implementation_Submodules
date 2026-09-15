# Collector 0.1.0 validation report

## Delivered scope

A real, locally executable Python package implementing evidence-preserving fingerprint
matching and claim deduplication, deterministic extraction, SQLite persistence, scan
orchestration, retained-input replay, and conservative donor-rule import. A pinned
Scrapling HTTP adapter is included. This release does not change the v4.1 baseline.

## Executed verification

| Check | Result |
|---|---|
| Source-tree tests | **155 passed, 1 skipped** |
| Installed-wheel tests, outside source tree | **155 passed, 1 skipped** |
| Python compilation | Pass |
| CLI demo | Pass; synthetic transport, zero network requests |
| Schema/reference/recomputed matching and claim validation | Pass |
| Original stored bytes rehashed and re-extracted | Pass |
| Retained-HTML command | Pass |
| Replay | Pass; original observation records and timestamps unchanged |
| Donor-shaped fixture import | 2 input rows; 1 candidate; 1 explicit quarantine; 0 approvals |

The installed-wheel check used a separate virtual environment and pre-existing core
dependencies supplied through a .pth path. The package itself loaded from the installed
wheel, not the project source directory. This is a packaging check, not proof of a clean
internet dependency installation or compatibility across all supported Python versions.

## Duplicate demonstration

Seven rule matches on two HTML pages produce two capture observations and one claim.
Five matches are eligible under synthetic fixture approval; two remain candidates.
Three element evidence points and one source-origin group are retained. Confidence is
null/NOT_COMBINED. A source group is provenance bookkeeping, not statistical independence.

The full scan also retains metadata/probe captures; the two observations refer specifically
to the evidence-containing HTML pages, not the count of all requests or captures.

## Tests cover

Overlapping rules and alias mapping; candidate isolation; repeated scans and retries;
replay without refreshed TTL; current rule allowlists; revoked/stale/partial capture;
conflicting values; tenant/subject/product/predicate/origin/mode isolation; exact parsed
host boundaries; footer/blog/comment/template false positives; all 17 extraction
functions; rule compilation and regex limits; robots, URL/DNS checks, redirects, 429,
request limits and resumability; malformed JSON and XML; blob corruption; complete
support references; bundle tampering; and CLI/wheel operation.

## Explicit verification gaps

**The real Scrapling integration test was skipped because Scrapling could not be
installed in this environment.** The adapter was written against the 0.4.15 source
and its control flow was exercised with a fake SDK boundary. That is not a real SDK
or HTTP roundtrip. The included CI definition requires importing the exact SDK before
running tests; CI has not been executed remotely.

**FETCH_STEALTH is disabled and native bounded browser acquisition is not implemented.**
All 38 command IDs are retained, but that does not establish all-38 production readiness.
GATE_SCHEMA is advisory type support rather than canonical company binding. The legacy
HostResult/Hit file formats are not implemented verbatim.

The full 739-definition donor library, missing master signature catalog, hosted approvals,
calibrated production rules, canonical FactService admission, full A-H runtime contracts,
retention worker, cross-origin redirect authorization, and sending remain outside this
release. Candidate research harvesting and a subset importer are implemented; automatic
rule proposal/promotion is not.

## Reproduce

```bash
python -m pip install -e ".[test]"
python -m pytest -q
ks-scan demo --output ./demo-output
ks-scan check ./demo-output/scan-bundle.json --store ./demo-output
```

To test actual static HTTP acquisition in an environment with package access:

```bash
python -m pip install -e ".[live,test]"
python -m pytest -q tests/test_live_integration.py
```

See `reports/verification.json` for machine-readable results, environment package
versions, and input hashes. JUnit reports and pytest logs are included alongside it.
