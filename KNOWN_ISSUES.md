# Remaining implementation limits and resolved audits

The **nine POC requirements and sixteen previously failing submodule requirements are repaired** in this snapshot. Run `python tools/workspace.py verify` or either audit suite directly. The original audit reports and historical output files remain immutable evidence of the earlier behavior, not statements of present failure.

## Not included in this repair

- Native browser/network capture remains disabled.
- Actual Scrapling 0.4.15 HTTP behavior must pass `live-check` in an environment with the pinned SDK. Local fixture tests are not SDK verification. A separate CI job now requires that gate.
- There is no persistent authenticated collector-to-canonical admission service, broad live provider implementation, or fully integrated capture-to-reviewed-preview business workflow.
- The protocol package is a checker for its declared reference operation, not a sandbox or general execution runner. Reported effects are validated; a future runner must enforce actual I/O.
- Contacts, campaigns, delivery, inbound replies, and CRM remain proposed runtimes. No send path is enabled.
- Predicate-specific `effective_at`/valid-time policy (iteration-2 F16) remains an explicit design decision. An observed announcement about a future event differs from currently effective licensure; no universal time rule was invented in this patch.
- Cross-origin/bare-domain/www redirects remain denied without an explicit binding/policy extension. Robots redirects added here stay same-origin and bounded.
- Conservative footer/template/noscript/inert/aside attribution remains a profile limitation. Collector and narrow canonical matcher now agree on `aside` exclusion.
- Imported snapshot runs pin one subject, URL, release, and observation time. Use separate runs rather than append unrelated snapshots.
- This is not a fully bitemporal database: historical claim selection no longer sees later unpinned supersession, while current-use decisions intentionally inspect current restrictions/evidence.
- Existing v1.1 scan bundles require re-evaluation from their trusted capture store to produce v1.2, not editing or inventing capture identities.

## Next POC milestone

Verify the actual static Scrapling SDK, implement the collector-to-canonical bridge using complete match/support lineage and accepted subject binding, then demonstrate one supported no-send reviewed preview from those actual collector facts. Do not use the separate canonical fixture journey as proof that this bridge exists.

See [repair mapping and invocation guide](docs/POC_REPAIRS.md), [historical POC audit](audits/poc/REPORT.md), and [historical submodule audit](audits/iteration2/AUDIT.md).
