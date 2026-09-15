# POC implementation checklist

This checklist proposes the first integrated proof of concept. The audit does not implement these changes.

## Keep the first finish line narrow

Single local operator; explicitly approved static website targets; immutable evidence; typed observations; one canonical binding/admission path; one supported observation-led message; manual exact-revision review; no-send export. Retain the broad knowledge catalog without enabling unfinished capabilities.

## Work package 1 — Reliable collector

- [ ] POC-01: canonicalize set-like rule report fields before both publication and validation; preserve separate execution chronology.
- [ ] POC-02: budgeted same-origin robots redirects with loop/unsafe-destination rejection.
- [ ] POC-03: distinguish past 429 from current cooldown; add an explicit bounded retry attempt with immutable `retry_of` history.
- [ ] Every run/target ends as completed, partial, blocked, or failed; zero claims is not a universal success label.
- [ ] Resolve exact-origin alias policy for the POC: operator-supplied canonical seeds or reviewed alias handling.

## Work package 2 — Discovery and research

- [ ] POC-04: safe bounded gzip sitemap parsing, or declared unsupported-capability outcome.
- [ ] POC-05: rank sitemap and anchor discoveries through one frontier.
- [ ] POC-06: retain candidate state in read models without approved eligibility.
- [ ] POC-07: reconcile known-versus-unknown features against the selected release and current evidence policy.
- [ ] POC-08: account/scope/time-attributed reports plus subject filter and support inspection.
- [ ] Explicitly document one-file import scope; add a manifest only if multi-file same-run import is required.

## Work package 3 — Actual capture-to-preview integration

- [ ] Execute the real pinned Scrapling SDK against controlled HTTP cases and a permitted live sample.
- [ ] Do not unblock the browser merely to make a test green; its egress/capture limits remain a separate gate.
- [ ] Implement collector Observation/SupportLink/Match → canonical Fact/EvidenceSet/ExecutionRecord admission, with subject/source mapping.
- [ ] Resolve historical versus current claim views through shared helpers.
- [ ] POC-09: normalized numeric equality separate from raw content hashing.
- [ ] Close the prior binding-evidence, template-authority, publication-object and generated-artifact defects needed by the slice.
- [ ] One real observation-led template produces supported copy from admitted collector data, not pre-authored fixture facts.
- [ ] Review/export tests include stale evidence, conflict, template demotion, restrictions, and duplicate-export identity.

## Demonstration cases

| Case | Expected result |
|---|---|
| Same vendor on two pages, overlapping rules | One claim; all supports retained; no combined confidence |
| Same pages under changed run ID or traversal order | Equivalent successful semantic evaluation |
| No target marker on complete selected pages | No detection with explicit checked scope; no claim of missing private capability |
| Same-origin redirect of robots | Follow safely within budget, then honor retrieved rules |
| Rate limit followed by recovery | Hold during cooldown; explicit bounded retry after it |
| Compressed sitemap and low-priority noise | Correct discovery and declared page-role selection |
| Candidate imported definition | Candidate-only result in both bundle and report |
| Newly approved definition replay | No repeat unresolved research item for fully recognized evidence |
| Two accounts in one store | Every reported claim retains account/scope identity |
| Equal numeric spellings | Agreement, not false conflict |
| New contradiction after review | Block new outward use without rewriting historical evaluation |
| Capture fails before bytes | Honest diagnostic and failed/blocked status, not fabricated absence |

## Defer without deleting design material

Provider integrations not needed by the selected signal, all eight compound-signal implementations, full case-study matching, cohort statistics, browser capture, sending, contacts/campaign state machines, replies, CRM, and service deployment. Maintain disabled profiles and explicit status for each.

## How to verify this audit package

```bash
python baseline/verify_integrity.py
python poc_probes.py
python -m pytest tests -q --tb=short
```

The last command is currently expected to exit nonzero with nine unmet POC requirements and five passing controls. Remove no tests just to produce a green count. Update an explicitly policy-dependent acceptance case only alongside an approved design decision.
