# Current implementation status

Snapshot: **2026-09-15-local-assembly.1**. Machine-readable counterpart: [STATUS.json](STATUS.json).

## This delivery

The previous GitHub upload attempt did not establish a verified full-code push. This delivery is the full source workspace **here**, with no remote write required. The repaired collector 0.2.0, canonical reference 4.2.0, and protocol are preserved byte-for-byte. All three later source archives carried the identical repair baseline; no unseen post-audit fix is assumed.

New work in this assembly consists of a consistent repository layout, local command launcher, source manifests, CI configuration, onboarding, and workspace tests. Audit and walkthrough imports are adjusted to reference the one shared source tree. These path adaptations are recorded in provenance/IMPORTS.json.

## Operational boundaries

- The deterministic collector and its local operations exist, with known defects in multi-page ordering, recovery, discovery, candidate projections and reporting.
- The actual Scrapling dependency is unavailable in this assembly environment. There is no claim that live SDK acquisition passed. Browser capture is disabled.
- Canonical admission/resolution/rendering includes runnable **reference validators and fixtures**, but no persistent authenticated canonical service or executable collector bridge.
- Correction authorization F was tightened in reference code. That is not a hosted identity/role administration system; later binding and current-use gaps remain documented.
- The broad catalog, 52-idea integration, 38-command inventory and 39-module product architecture are retained. Definitions are not implementations of all connectors, matchers, service endpoints or business rules.
- No automated sending, contacts/campaign state machines, CRM integration, or generic ModuleRequest execution middleware is delivered as implemented functionality.
- Eight supplied journeys exercise local commands and synthetic/reference fixtures. They do not demonstrate the complete business lifecycle or production data.

## Known defects are part of the handoff

The latest two acceptance suites remain independent of the original regression tests and currently fail. Do not interpret a green existing-suite workflow as POC readiness. [KNOWN_ISSUES.md](KNOWN_ISSUES.md) identifies the repair priorities and reproducible tests.

## Version precedence

1. This status document and verification/ASSEMBLY_VALIDATION.md describe this assembled delivery.
2. audits/poc and audits/iteration2 describe the still-open behavior.
3. verification/REPAIR_REPORT.md describes the earlier implemented fixes.
4. Older component narrative and docs/history are retained historical records, not later release claims.
