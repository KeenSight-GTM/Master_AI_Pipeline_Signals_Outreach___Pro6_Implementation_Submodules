# Safety and operating limitations

Local, single-machine prototype for operator-approved sources. Not a hosted service.
There is no arbitrary-code registry dispatch, LLM provider, login, form submission,
CRM mutation or outbound messaging. Browser acquisition is disabled by default.

Static HTTP validates schemes, userinfo, origins, ports and all DNS answers. It rejects
non-public/multicast/reserved destinations and configures libcurl RESOLVE on the pinned
Scrapling session. It disables environment proxies, automatic redirects, hidden retries,
and adaptive parsing. A decoded-body callback aborts at its configured byte ceiling.
Actual SDK execution of those controls remains a CI gate, not verified here.

DNS resolution itself currently uses the system resolver; its latency is not hard-
bounded by a separate process supervisor. Header handling and process-wide CPU/memory
budgets also require production characterization. Use network isolation when deploying
untrusted-input fetchers. Do not enable the test-only loopback policy in production.

Robots is not a license or privacy permission. Check source-specific capture, retention,
model-processing and redistribution rights before use. This module does not automate
legal access review or privacy deletion. It stores raw evidence in owner-restricted
local blobs; raw HTML and URLs may contain personal data or secrets. Use an appropriately
restricted volume and retention policy. Cookie values and arbitrary sensitive header
values are not retained in ordinary response-header metadata.

Rule-pack APPROVED metadata is trusted local configuration, not authenticated user
approval or proof of calibrated precision. The bundled approved example is synthetic
and fixture-only. Native browser use, hosted ChangeRecord authorization, canonical
Fact admission, current-use gates and production release signing remain separate gates.

The exporter writes local JSON only. It has no path that activates or sends a campaign.
