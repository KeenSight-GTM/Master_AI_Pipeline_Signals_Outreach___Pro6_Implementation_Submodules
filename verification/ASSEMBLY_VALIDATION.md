# Consolidated source — verification

Date: **September 15, 2026**. Scope: the generated local workspace, not a hosted or production E2E deployment.

## Source provenance

The three supplied repaired/audit archives carry the same 439-entry repair baseline. The 311 files in collector/, canonical/, protocol/ and product-design/ are byte-identical to that supplied source. This assembly changes repository organization, onboarding, audit path defaults and root tooling—not application behavior.

## Executed checks

| Suite | Passed | Failed | Skipped |
|---|---:|---:|---:|
| Existing collector | 183 | 0 | 1 |
| Existing canonical reference | 609 | 0 | 0 |
| Existing protocol checker | 42 | 0 | 0 |
| New workspace tooling | 14 | 0 | 0 |

**834 existing component tests + 14 workspace tests = 848 passing regression tests; one SDK-dependent test skipped.**

Canonical generation matches all 116 generated files; canonical bundle validation, protocol fixture validation, full-product design validation, and the 38-command implementation-plan validator pass. The root `tools/workspace.py verify` command completed successfully.

Eight offline fixture/reference journeys completed through 20 subprocess invocations with the expected exit codes. A separate demo/check completed with zero actual network requests. This demonstrates independent local commands, not network services or the missing collector-to-canonical bridge.

## Known requirements remain unsatisfied

| Separate acceptance suite | Failed | Passed |
|---|---:|---:|
| Latest POC usage requirements | 9 | 5 |
| Iteration-2 submodule requirements | 16 | 6 |

These are genuine failures, not xfails. The launcher preserves their nonzero exit status. Their tests and reports are retained under audits/. A successful probe command only means observations were recorded; it does not mean all observed behavior was correct.

## Explicitly not verified or delivered

- Scrapling 0.4.15 HTTP SDK operation: dependency absent here; the controlled live test is skipped.
- Native bounded browser: disabled.
- Full donor corpus, complete signature target, live enrichment/model providers, or data-access rights.
- A persistent authenticated canonical service or collector admission bridge.
- General ModuleRequest middleware, contacts/campaign/enrollment runtimes, sender, replies or CRM.
- Remote GitHub CI, push, merge, service deployment, or production correctness.

See current/SUMMARY.json for machine-readable counts, current/regression/ for logs/JUnit, current/journeys/ for invocation logs, and the two current/audit-* folders for explicit failure outputs. Earlier verification files remain historical evidence.

The distributed source manifest is independently checkable after extraction. A separate external package-verification record accompanies the final download so its checksum can cover the finished archive without a circular self-reference.
