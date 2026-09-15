# KeenSight v4 validation report

Verification date: September 14, 2026. Scope: the delivered local architecture/contract/reference bundle, not production operations or the old repositories.

## Results actually executed

| Check | Result |
|---|---|
| Python regression suite | **471 passed**, zero failed, zero errors. |
| Exported Draft-07 schema checks | **58** schemas valid. |
| Predicate target/value specimens | **197** typed definitions checked; all 87 v3 identifiers retained. |
| Metric contract/specimen checks | **89** definitions checked. |
| Coverage records | All **11** requested domain mappings resolve. |
| Full cross-record fixture validation | **144** synthetic records, including **27 facts** and **3 approved DESIGN_TEST previews**. |
| Schema-instance calls in full validator | **962** calls, including dynamic predicate/metric dispatch; this is not 962 independent tests. |
| Regeneration check | **95** generated files match the delivered release. |
| Clean-room generation | Removed generated outputs; regenerated from authoring/reference inputs in a separate directory; all **95 files byte-identical**. |
| Original archive preservation | v3 archive copy is byte-identical to the provided original. |
| Full class diagrams | All **58** contract/value-object classes and every exported field appear in the full class partitions. |
| Proposed code interfaces | **19** separately labeled proposed ports; method bodies are not implemented services. |
| Diagram artifacts | **14** editable Mermaid views and **14** well-formed SVGs; Graphviz/source-model rendering plus a local sequence renderer. |

## What the test count includes

58 schema-definition cases, 197 predicate-specimen cases, 89 metric-definition cases, 11 domain-coverage cases, and 116 additional reference/negative/integration-boundary cases. These categories total 471. The number is not an estimate of production accuracy or completeness.

Representative rejected cases include wrong account/tenant/product, wrong subject binding, dangling evidence, unknown taxonomy, unsupported source/processor, estimates relabeled as direct observations, nonexistent/incorrect quoted text, unproven absence, incomplete or truncated capture, mismatched metric dimensions/units, invalid salary/rating ranges, zero denominators, stale/candidate/retired source ancestry, inappropriate maturity mode, unsupported fixed copy, incorrect product/industry joins, source-purpose/tenant/retention violations, unknown enabled implementations, code/request pin mismatch, and invalid state or graph cycles.

Current-use tests include source policy revocation. Temporal tests distinguish a logical as_of from later wall-clock computation. Confidence metadata does not grant production authority.

## Example and implementation limits

The 27 facts exercise linked evidence across all eleven areas, but the remaining predicate specimens validate shape rather than every possible real-world extraction/relationship. Source fixtures, product names, observations, classified themes, approvals and model responses are synthetic. No live API, real LLM, licensed review corpus or prospect scan was executed.

There is one narrow SCRIPT_HOST fingerprint with six synthetic fixtures, not a 2,500-signature library. Reference classification examples are DESIGN_ONLY; no measured precision/recall or gold-set calibration is claimed. Exact-quote checks validate text support for supplied renderers, not arbitrary semantic entailment.

No database crash/retry/concurrency test, production current-state service, cost reservation, source license approval, privacy erasure job, outreach export or delivery operation was implemented or verified. Those are proposed runtime gates. The original 18 signals and 23 numerical kernels are preserved in the reference archive, not automatically integrated or retested as v4 runtime features.

The original user table provided aggregate counts and representative categories, not all 424 catalog rows. Coverage here is family-level, not a fabricated item-by-item audit of an unavailable catalog.

## Rendering verification

All SVGs parsed successfully as XML. The main flow, context/classes and sequence views were rasterized locally and visually inspected; the sequence labels were corrected during review. Mermaid CLI parsing was not run. A Chromium full-page screenshot attempt timed out, so no browser screenshot success is claimed. The self-contained HTML book embeds the actual SVGs and editable source; it does not depend on a web renderer.

## Environment

Python 3.13.5; jsonschema 4.26.0; pytest 9.0.2; referencing 0.37.0. dot - graphviz version 2.42.4 (0).

```bash
python -m pip install -r requirements.txt
python generate.py --check
python validate.py
python -m pytest -q
# Optional: requires Graphviz dot on PATH.
python build_diagrams.py
```

Machine-readable evidence is in `reports/validation.json`, `reports/reproducibility.json` and `reports/pytest.xml`; the console summary is in `reports/pytest.log`.
