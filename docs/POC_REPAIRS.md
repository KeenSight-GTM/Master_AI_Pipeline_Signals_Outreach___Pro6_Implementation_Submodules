# POC and submodule repairs — 2026-09-15

## Scope

This change starts from GitHub `main` at `6ec6640293d41597296b7ba61e91f6e0a586e611`. It repairs the executable requirements in `audits/poc/tests` and `audits/iteration2/tests`, not the full proposed product. Original audit assertions and historical audit documents are retained unchanged.

The collector is now **0.3.0**, with **ScanBundle 1.2**. Canonical schemas remain **4.2.0**; their reference validators and generated code-release hashes are updated. The protocol is still a narrow checker, not an authenticated execution service.

## Repaired standard-usage flows

| Audit | Repair | Contract preserved |
|---|---|---|
| POC-01 | Rule match IDs and error collections use deterministic ordering. Multi-page validation no longer depends on the capture-hash order. | Retain every match and exact report reproduction; don't hide differences by skipping validation. |
| POC-02 | Follow bounded same-origin robots redirects before crawling content. Loops, origin changes, private destinations and exhausted budgets fail closed. | Each network attempt is recorded and counted; robots failures are not ignored. |
| POC-03 | An expired historical 429 does not create a new active cooldown. Explicit failed-GET recovery creates a linked attempt rather than overwriting the old one. | Existing evidence stays immutable; retries require remaining budget and current permission. |
| POC-04 | Parse gzip-compressed sitemaps using an 8 MB decompressed ceiling and existing XML/entry limits. | Retain original compressed bytes. Decode failure or limit exhaustion is PARTIAL, never proof of absence. |
| POC-05 | Apply common stable template ranking to page candidates from anchors, sitemaps and probes. | Keep declared attempt/page budgets; do not improve recall by silently increasing limits. |
| POC-06 | Claims queries include current candidate-rule membership while retaining a separate approval check. | Candidate support stays CANDIDATE and cannot become approved corroboration or a commercial claim. |
| POC-07 | Research views track each capture's evaluated rule release and distinguish unresolved, resolved and historical features. | Rule replay retains observation times; it does not erase research history or refresh TTLs. |
| POC-08 | Claim read models include tenant, subject, scope, origins, observation time and expiry. `claims --subject` filters accounts explicitly. | Multiple accounts/products/scopes remain distinct. |
| POC-09 | Typed semantic comparison treats equal finite numeric values consistently, independently of original JSON spelling. | Do not round, rewrite source bytes, collapse units/windows, or equate booleans with numbers. |

## Repaired submodule boundaries

| Audit | Repair |
|---|---|
| F01 | Binding artifacts and binding locators participate in eligibility/provenance. They do not count as additional substantive corroboration. |
| F02 | Standalone export verifies the template's current ACTIVE authority, implemented renderer and current exact rendering before use. |
| F03 | Publication derives findings exclusively from the validated bundle and reconstructs trusted page evidence. Legacy positional collections are ignored, not trusted. Manifest/findings/research publication remains transactional. |
| F04 | Primitive fact eligibility no longer scans globally for later superseding facts. Supersession is resolved inside the explicitly selected historical or current claim group. |
| F05 | One artifact-availability resolver accepts pinned external inputs or outputs of a unique successful earlier producer in the same run. Full and completion validation use it. |
| F06 | Information-losing lxml ERROR/FATAL recovery marks dependent DOM extractors PARTIAL. Benign unknown-tag recovery is distinguished. Raw-byte and header capture remain separate. |
| F07 | Supersession graphs are checked before traversal; self/multinode cycles and missing dependencies produce contract failures rather than uncontrolled recursion. |
| F08 | Requirements and full validation share distinct-substantive-origin counting. Without an origin resolver, a helper cannot establish multi-origin corroboration merely by counting rows. |
| F09 | Imported runs pin their subject. Mixed-subject captures are rejected before appending them to an incompatible run. |
| F10 | Current research queues exclude revoked, incomplete, expired and unavailable capture support while preserving explicit historical counts. |
| F11 | Command invocations have stable IDs, attempt identity and operator context; duplicate or contradictory terminal outcomes for one invocation are rejected. |
| F12 | Acquisition attempts preserve immutable start metadata and terminal fields together. Even no-byte runs publish a self-identifying zero-output evaluation manifest. |
| F13 | Failed/cancelled operations may record truthful terminal diagnostics after their deadline. Late positive output or success remains invalid. |
| F14 | Collector region classification labels aside content ANCILLARY and excludes it consistently with the narrow canonical presence matcher. |
| F15 | The installed protocol signature rejects unsupported modes and reported forbidden network effects. Actual effect prevention still requires the future runtime runner. |

F16 was a separately documented valid-time policy question, not a failing test. It is **not** represented as completed: announcements, license validity and reporting windows require predicate-specific temporal policies.

## Invocation examples

Install the local deterministic core from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e './collector[test]'
python tools/workspace.py verify --output ../repair-verification
python tools/workspace.py journeys --output ../repair-journeys
```

The verification command includes both audit suites. Independent equivalents remain:

```bash
python tools/workspace.py audit poc --output ../poc-regression
python tools/workspace.py audit iteration2 --output ../submodule-regression
```

### Explicit recovery versus replay

For an already authorized live static scan with the same run/configuration, request one retry per original failed GET after any cooldown:

```bash
ks-scan scan https://example.com/ \
  --tenant local --subject account:example --run scan-001 \
  --rules ./collector/examples/live-candidates.json \
  --store ../scan-store --output ../scan-store/recovered.json \
  --max-attempts 8 --max-pages 5 --retry-failed
```

The original attempt is retained. A retry records `retry_of`, request key, ordinal, original command/mode, start, and completion. Success is reused rather than repeated. PENDING/crash-uncertain attempts, non-retryable HTTP failures, changed run identity and exhausted budgets are not retried. This policy is for bounded GET acquisition, **not** sends, form submissions, or arbitrary provider effects.

Without `--retry-failed`, resume retains the old result. An old expired 429 is labelled retained failed evidence rather than an active cooldown. `replay` never performs new acquisition.

### Account-labelled claims and research state

```bash
ks-scan claims --store ../demo-store --tenant demo \
  --subject account:demo --rules ./collector/examples/demo-rules.json \
  --as-of 2026-09-14T13:00:00Z

ks-scan candidates --store ../demo-store --tenant demo --min-hosts 1 \
  --rules ./collector/examples/demo-rules.json \
  --as-of 2026-09-14T13:00:00Z --include-resolved
```

Demo rule approvals/timestamps are synthetic, not current permission. Without `--include-resolved`, the candidate queue returns only unresolved eligible features meeting the origin threshold. Without `--rules`, it uses the latest evaluated release for each capture. Supplying a new unevaluated release does not silently apply it; replay first. Expired/revoked support can appear as HISTORICAL in the explicit history view but cannot populate an eligible queue.

### Actual SDK gate

```bash
python -m pip install -e './collector[live,test]'
python tools/workspace.py live-check --output ../scrapling-sdk-check
```

Unlike a test-suite skip, `live-check` fails when the exact Scrapling 0.4.15 dependency cannot import. Its request is to an explicitly permitted loopback fixture; it does not contact a prospect. Native browser capture stays disabled.

## Schema-format portability

Canonical and protocol schema validation now register local strict `date-time` and `uri` format checks instead of relying on optional `jsonschema` format extras. Invalid calendar dates therefore fail consistently in a minimal CI environment as well as a developer environment. Type validation remains in the schema; the local format checker only supplies deterministic format semantics.

## Compatibility and data ownership

- ScanBundle 1.2 requires tenant, subject and capture-run IDs even when no artifact exists. Command executions add IDs and attempts; claim views add account/scope/time metadata; surfaces add ANCILLARY context.
- Command identity is scoped by its containing tenant/run/evaluation. It does not claim to be a global remote execution identity. A future ModuleRequest runner must use the outer execution protocol too.
- Old v1.1 bundles are not auto-relabelled. Re-extract and evaluate the trusted stored captures to get a v1.2 bundle; never fabricate collection time or subject identity. Code-version changes require new acquisition runs. Stored capture replay remains a distinct operation.
- SQLite adds release-aware research tables using non-destructive `CREATE TABLE IF NOT EXISTS`. Old occurrences without an evaluation state are conservatively unresolved. Original observations/support/captures are not dropped.
- Canonical semantic comparison changes value interpretation, not artifact/content digests. Distinct values still conflict and different dimensions remain different claim identities.
- Historical evaluation sees its selected input claim group; the current-use path intentionally checks the current group and current restrictions. This is not a claim that a complete bitemporal database has been implemented.
- `publish_evaluation` remains a trusted local-owner boundary. Hosted authorization, record-service permissions and multi-tenant deployment are not supplied by a `tenant_id` field.
- The fixture protocol validates *reported* effects against its signature. It does not sandbox plugins or certify that an arbitrary plugin accurately reported I/O.

## Acceptance and next step

The original POC and iteration-2 assertions run unchanged. Thirty additional component tests cover decompression limits, redirect safety, explicit retry lineage and cooldown, release-aware research, parser recovery, source identity, current/historical decisions, numeric types and protocol timing/effects.

Keep the 213-predicate knowledge breadth. The next executable product milestone is **actual Scrapling capture → admitted canonical facts → one supported reviewed no-send preview**. The admission bridge, hosted authentication, broad live connectors, contact/campaign state machines, sending/replies/CRM, and native browser are not implemented by this repair.
