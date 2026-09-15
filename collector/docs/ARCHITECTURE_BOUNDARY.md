# Integration boundary with v4.1

This release is the Scrapling-first collector, not a new universal Fact Service.
The original v4.1 architecture bundle remains unchanged.

## Handoff

`ScanBundle` contains pinned rule content/digest; retained captures; all extraction
surfaces; all rule matches; per-capture observations; every support edge; deduplicated
claim projections; command results; and resource dispositions. Sending is always false.

The next application stage must resolve/validate the requested subject, source and
rule authority, source-use/retention permissions, current restrictions and exact
producer/execution provenance before constructing canonical v4.1 Fact/EvidenceSet/
ExecutionRecord records. Collector observations are NOT directly inserted as those
canonical records, and `handoff.requires_fact_service_admission` is always true.

The CLI's `--subject` is explicit operator-provided identity, not automated proof of
company ownership of a domain. A canonical tag does not rebind that identity.

## Duplicate-fact handoff recommendation

Promote one admitted canonical observation per collector observation ID and mapping
version. Preserve the evidence-support relation, including rule versions and original
capture time. A canonical claim projection can combine eligible observations without
rewriting them. Never translate each overlapping match into a new independent fact.

## Correctness retained locally

Original bytes and capture timestamps; explicit per-command failures; no business
absence from missing or failed checks; narrow presence versus literal mentions;
separate technical observations and commercial qualification; candidate isolation;
full support edges; no confidence inflation; tenant-keyed persistence; no send path;
current rule allowlisting and capture revocation for stored views.

The batch command records are collector diagnostics, not a claim to implement all
v4.1 producer, current-use, review, import and execution authorization contracts.
The previously unclosed global ChangeRecord F is not solved by the local store's
owner-only revoke method. Hosted authentication, audit authorization, legal/source
rights enforcement and canonical entity binding still need their planned work.

## Graph and storage

Dependencies are fixed batch calls; there is no distributed graph scheduler.
Fingerprint qualification depends on the current page/host evidence set, so it is
an evaluation result, not an immutable field of a raw rule match. The same raw match
can remain identical when a newly captured page supplies an additional guard.

SQLite records raw matches, observations and supports transactionally. Original blobs
are finalized before reference insertion. Abandoned unreferenced blobs may remain
after failure; an orphan-cleanup/retention worker is not included. Full event-sourced
replay, remote delivery, API source suites, cohorts, research priors and outcome
analytics are outside this collector release.

## Minimal next gates

1. Install the pinned SDK in CI and pass the real local HTTP integration test.
2. Implement and test bounded, egress-isolated browser acquisition before enabling
   FETCH_STEALTH; it is not safe to treat DNS preflight as browser egress isolation.
3. Characterize complete donor/operator coverage and production fixture reviews.
4. Bind ScanBundle to the canonical Fact Service with A–H enforcement and authenticated
   tenant/change operations before production downstream use.
