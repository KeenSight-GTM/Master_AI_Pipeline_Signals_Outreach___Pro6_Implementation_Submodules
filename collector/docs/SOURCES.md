# Source basis and implementation changes

## User-owned inputs

The architecture v4.1 archive and Scrapling-first handoff are the contract/design basis.
The 38 command names and their extraction/matching roles preserve the supplied workbook.
The command transcription was reused from the already inspected handoff; this release
is not a fresh validation of every workbook cell. Input hashes are in
`reports/verification.json`.

## Connected donor repository

Pinned commit: `KeenSight-GTM/SEO-FingerPrint-Scanner-Basic@66358454c98addb8fe297cb5192a32e2bd98f732`.
Inspected through the GitHub connection: `runtime_fingerprints.py`, rule schema/manifest,
and the first six lines of `seo_scanner/data/fingerprints/rules/discovered_2026_09_01.jsonl`.
The retained-evidence design replaces first-hit category/key/value deduplication with
separate match, observation, and claim identities. The donor-shaped examples in this
release are explicitly synthetic; they are not an export of the upstream library.

## Primary dependency source

Scrapling tag `v0.4.15`, official `D4Vinci/Scrapling` repository:
- `scrapling/fetchers/requests.py`
- `scrapling/engines/static.py`, source lines 1-180 and 225-435

These were inspected through the GitHub connector to verify FetcherSession, request
argument forwarding, retry semantics, and the private `_curl_session` extension point.
This is source inspection, not successful installation or execution of the dependency.

The HTTP adapter is deliberately pinned and fail-closed. Its DNS pinning relies on that
private extension point; the included actual-SDK integration test must pass before live
use or any version change. Native browser support is not inferred from static support.

## New implementation choices

Local lxml extraction, strict JSON/typed rules, layered stable IDs, support-edge storage,
conservative non-inflating claim views, per-origin scope, current-rule filtering, local
revocation, a subset donor importer, and no business absence are deliberate first-release
choices. They are described in `DEDUPLICATION.md`, `DONOR_INTEGRATION.md`, and
`ARCHITECTURE_BOUNDARY.md`, rather than claimed to be already implemented by the donor.
