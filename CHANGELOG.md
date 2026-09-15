# Workspace changelog

## 2026-09-15-local-assembly.1

- Consolidated the supplied collector 0.2.0, canonical reference 4.2.0, protocol and full product design into one ordinary source repository.
- Retained all 311 imported component files byte-identically. No post-audit application fixes are asserted.
- Removed duplicate nested source trees from the two latest audit packages; adapted their imports to the shared workspace.
- Included all eight local journeys, the 19-journey user map, feature/submodule traceability, 31 detailed E2E diagrams, and the Scrapling-first implementation handoff.
- Added root install/check/test/demo/journey/audit commands, explicit offline versus SDK gate separation, 14 workspace tests, and source integrity manifests.
- Included the original workbook and ledger as source inputs; retained earlier narrative under docs/history.
- Preserved unresolved iteration-2 and POC requirements as genuinely failing tests. Normal regression CI is not advertised as POC sign-off.

For the application changes in the earlier repair, see verification/REPAIR_REPORT.md. For subsequent problems, see audits/iteration2/AUDIT.md and audits/poc/REPORT.md.
