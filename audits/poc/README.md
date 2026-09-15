> Workspace relocation: the original nested `baseline/` is now the repository root. Run `python tools/workspace.py audit poc` from the root. The source and historical test findings are unchanged; this archive does not contain post-audit fixes.

# KeenSight POC-readiness review

This is an additional audit of **ordinary feature usage** over the unmodified source supplied with Iteration 2. It is not a new runtime release.

Start with `REPORT.md`, then `POC_CHECKLIST.md`. Exact outputs are in `reports/poc-probe-results.json`, and executable requirements are in `tests/test_poc_requirements.py`. `poc_probes.py` uses the supported fixture transport and actual local/reference code; it performs no public network, model, CRM or send operations.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e './baseline/collector[test]'
python -m pip install -r baseline/canonical/requirements.txt
python baseline/verify_integrity.py
python poc_probes.py
python -m pytest tests -q --tb=short
```

Installation may access your package index. Test/probe execution is offline. Pinned Scrapling installation could not be resolved in this environment; the actual SDK test remains skipped and browser transport disabled.

- Existing suites: 183 collector + 609 canonical + 42 protocol tests passed; one SDK test skipped.
- New probes: 17; nine finding scenarios, three separate policy/scope limits, five controls.
- POC requirement tests: nine fail and five pass on the supplied baseline. They are intentionally not xfailed.
- All 438 baseline manifest entries are unchanged.

The complete source baseline is included to make reproductions self-contained. Its older documentation is not a statement that later audits have been fixed. No repository or application behavior was modified in this pass.
