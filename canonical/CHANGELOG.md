# v4.1

- Implemented selected end-to-end audit A–E/G/H in reference validation and local preview-export code.
- Added intake/attempt, per-target completion, support-policy/sample-decision, review/current-use/export contracts.
- Closed failed-producer, undeclared-consumption, unresolved-claim, omitted-denominator and incomplete-detection paths.
- Preserved no-byte failures as diagnostics/UNKNOWN, not fabricated business facts.
- Added 16 ledger-derived fact families, for 213 predicates total; retained 89 metrics.
- Classified every original ledger row, separating source facts from algorithms, hypotheses and copy strategies.
- Left F/E07 explicitly unfixed; preserved unchanged v4/v3 baselines.
- Changed the retrospective-computation regression fixture to move all newly required dependent timestamps, while retaining the original semantic test.
