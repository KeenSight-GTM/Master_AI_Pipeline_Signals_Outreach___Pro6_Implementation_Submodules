# Known issues and POC blockers

**These bugs are not fixed by repackaging.** The root launcher keeps the failing acceptance requirements executable against the delivered code.

## Standard usage — latest POC review

| ID | Issue | Test suite |
|---|---|---|
| POC-01 | Multi-page validation depends on capture hash/list ordering | audits/poc/tests/test_poc_requirements.py |
| POC-02 | Same-origin robots redirect is not followed | Same |
| POC-03 | Resumed old 429 response misrepresents an expired cooldown and prevents recovery | Same |
| POC-04 | Compressed sitemap handling missing | Same |
| POC-05 | Sitemap discoveries bypass useful-page prioritization | Same |
| POC-06 | Candidate state disagrees between scan and claims query | Same |
| POC-07 | Resolved fingerprints remain in unknown-feature research view | Same |
| POC-08 | Multi-account claim report lacks usable account/scope identity | Same |
| POC-09 | Numerically equal metric values can conflict because byte spelling differs | Same |

## Submodule safety review

Open requirements also cover binding-evidence dependency closure; current template authority at export; one authoritative publication payload; historical visibility; generated-artifact availability; parser recovery/completeness; supersession cycles; support-count units; imported run identity; revoked candidate support; command invocation identity; no-byte diagnostic manifests; truthful late failure reports; matcher-region parity; and operation effect/mode restrictions. A separate temporal-policy question concerns predicate-specific effective-time meaning.

Read the complete [submodule audit](audits/iteration2/AUDIT.md) and [POC audit](audits/poc/REPORT.md). Some failed POC tests specify capabilities rather than regressions. The reports preserve that distinction.

## Invocation

```bash
python tools/workspace.py audit poc
python tools/workspace.py audit iteration2
```

Both commands expose genuine failures and return nonzero until repaired. Do not use xfail or remove them to claim POC completion.

## Minimum next implementation work

1. Repair scan ordering, trustworthy publication, parser completeness, bounded discovery and retrieval recovery.
2. Verify real Scrapling on controlled HTTP fixtures; retain disabled browser behavior until bounded and tested.
3. Repair canonical binding/current-use/historical availability inconsistencies and implement actual collector admission.
4. Demonstrate one capture-to-reviewed, no-send preview using the admitted collector facts, not unrelated synthetic canonical fixtures.
5. Only then expand the remaining source, contact, campaign, delivery and CRM runtime.
