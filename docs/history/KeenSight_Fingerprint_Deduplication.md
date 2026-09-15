# Fingerprints that duplicate the same fact

## Decision

Deduplicate the **claim view**, not the evidence trail. For a single capture,
coalesce identical semantic observations and attach all distinct rule-match supports.
Preserve observations from different captures as separate history.

## Identity layers

| Layer | Identity basis | Result |
|---|---|---|
| Content blob | Tenant + SHA-256 of original retained bytes | Identical bytes can share storage without sharing observations. |
| Capture | Tenant + subject + acquisition run + URL + captured time + mode | A later scan is a new observation opportunity even if the bytes are identical. |
| Underlying evidence point | Capture + DOM/header locator | Two rules matching one script element share one evidence point. |
| Rule evidence | Rule definition digest + capture + surface + matching alternative | Stable across releases that retain the same definition. |
| Audited match | Rule digest + release digest + capture + surface + alternative | Exact same replay is idempotent; a different release is auditable. |
| Claim | Tenant + subject + predicate + nature + scope + canonical target + window | Does NOT include rule ID, detector confidence, or competing object value. |
| Observation | Claim + capture + source + state + object value | Same capture/claim/value produces one observation even with many detectors. |
| Support link | Observation + audited match | All successful match provenance is retained without duplicating the observation. |

For the collector's technology claims, scope is the exact sampled origin and
capture mode; target is the canonical product ID. There is no fuzzy vendor merge.
Aliases are explicit release content, checked for cycles. A generic vendor family
and a distinct product must not be merged merely because their names are similar.

`vendor.present` here means a qualifying narrowly detected footprint on the sampled
public origin. It does not mean every employee uses the product, the account pays
for it, or a private integration exists. `vendor.mentioned` remains a different
predicate and therefore a different claim.

## Demonstration

On the homepage, an exact-host script rule, a suffix-host rule, an iframe rule,
and a candidate script rule match Calendly. On the contact page, the two script
rules and the candidate script rule match it again.

| Quantity | Result |
|---|---:|
| All audited matches | 7 |
| Approved fixture supports | 5 |
| Candidate-only supports | 2 |
| Underlying eligible element evidence points | 3 |
| Capture observations | 2 |
| Current claim rows | 1 |
| Source-origin groups | 1 |
| Calculated probability | None |

Four rules, two pages, or repeated monthly crawls are not four/two/new independent
corroborating sources. This implementation does not sum, average, maximize, or
apply noisy-OR to authored rule confidence values. It retains those values on the
match as metadata and exposes `confidence: null` and `NOT_COMBINED` on the claim.
A source group is provenance bookkeeping, not proof of statistical independence.

## Changes and conflicts

A newly added rule produces additional support without changing the old observation
identity or refreshing its timestamp/TTL. Removing an approved rule from the current
allowlist removes its eligible support, not its historical matches. Other eligible
support can continue to substantiate the claim. Candidate support cannot substitute
for a removed approved rule. Revoked captures are excluded at view time.

Different eligible values for the same claim produce CONFLICT. The module does not
choose the newest/highest-confidence convenient value. The scanner deliberately
does not emit negative business facts: NO_MATCH is detector output, not NOT_FOUND.
Formal absence admission still requires the full scope/coverage/authority contracts.

Rule-level duplicate IDs fail compilation. Two differently identified rules that
happen to match the same evidence are both auditable and converge at the observation
and claim layers. Deduplication is not a substitute for cleaning up redundant rules.

## Cross-boundary isolation

Tenant, subject, predicate, canonical target, nature, origin/mode scope, and reporting
window cannot be removed from identity to improve apparent deduplication. In particular,
the same captured product marker on two accounts never becomes one account fact.
