# Cross-system acceptance scenarios to implement

**Status: test specifications, not tests executed in this design continuation.** Each enabled path needs real producer/consumer fixtures and failure assertions. A schema pass, skipped command or diagram is not evidence that the scenario works.

| ID | Scenario | Required outcome |
|---|---|---|
| E2E-01 | Duplicate account imports and discovery aliases | Keep origins; identity review prevents incorrect merge; repeat intake does not duplicate work or enrollment. |
| E2E-02 | Capture denied before any bytes | Attempt/diagnostic records exist; no fake provider response or NOT_FOUND business fact. |
| E2E-03 | Two fingerprint rules match one script | Both matches retained; one capture observation/evidence point; confidence not multiplied. |
| E2E-04 | New rule replayed over old bytes | New execution support, old capture time/TTL, no live requests or action. |
| E2E-05 | Positive and negative eligible observations conflict | Complete claim resolution blocks unsupported signal and outward statement. |
| E2E-06 | Product-prior denominator evidence deleted | Current prior/context and dependent decision are blocked or recomputed; no preserved stale statistic. |
| E2E-07 | Relevant account, no verified appropriate contact | Knowledge/opportunity succeed; enrollment held; no invented email or job role. |
| E2E-08 | Contact verified but DNC or customer exclusion exists | No send; endpoint verification does not override restrictions or audience policy. |
| E2E-09 | Subject/body/footer changed after approval | Message/package revision mismatch blocks export/send until revalidated/reviewed. |
| E2E-10 | Same recipient/account targeted by two campaigns | Declared global cap/exclusivity produces a deterministic allowed/held decision; no independent duplicate dispatch. |
| E2E-11 | Remote sequence and local scheduler both configured | Configuration fails; only one schedule owner may advance the enrollment. |
| E2E-12 | Provider times out after possible acceptance | Intent remains acceptance-unknown, reconciliation precedes retry, no duplicate send. |
| E2E-13 | Reply arrives while next step is due | Verified ingress pauses/stops through state owner before classifier; dispatch rechecks latest local restriction/enrollment revision. Any already accepted external effect is recorded accurately. |
| E2E-14 | Opt-out arrives while model or CRM is unavailable | Restriction and future-step stop do not wait on model, CRM synchronization or metric maturity. |
| E2E-15 | Out-of-office, ambiguous reply or referral | Preserve literal event, pause under policy; only explicit checked action can resume or admit referred contacts. |
| E2E-16 | Positive reply and CRM-write failure | Handoff/task sync retries idempotently; send count does not change. |
| E2E-17 | Duplicate/out-of-order webhooks from different provider accounts | Scoped IDs and state revisions prevent collisions/regression; unmatched messages remain quarantined. |
| E2E-18 | CRM clears a field or reports stale lifecycle | Blank fields do not release restriction; stale exclusion refreshes/holds; field authority is enforced. |
| E2E-19 | Reply counted before its analysis window matures | Correctly excluded/pending denominator status, not counted as failure or inflated success. |
| E2E-20 | Candidate rule performs well in campaign | Quality proposal only; no automatic promotion of source authority or in-flight release mutation. |
| E2E-21 | Unauthorized cross-tenant correction | Reject actor/target/replacement; baseline F must be fixed before enabling hosted mutation. |
| E2E-22 | Offline replay of send/reply/CRM history | Diagnostic simulation only; no message, calendar action, source query, promotion or CRM write. |
| E2E-23 | Restore after write/process crash | Recover records plus byte references and prepared effects; reconcile remote acceptance; no loss/duplication of business actions. |
| E2E-24 | Knowledge-only and research-only runs | Attributable facts/context and coverage/diagnostics complete without requiring a recipient, package, campaign or signal match. |

## Layered gates

For every operation: envelope validation → exact domain schema validation → semantic permission/lineage checks → actual producer behavior → consumer acceptance → failure/retry/restore testing. Technical stages should have local deterministic fixtures; real provider adapters need approved bounded integration tests. Live integration availability is a separate status, never inferred from unit tests.
