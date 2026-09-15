from pathlib import Path
import json,re,shutil,hashlib,html
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]
probe=json.loads((ROOT/'reports/probe-results.json').read_text())
P={x['id']:x for x in probe['probes']}
findings=[]
def finding(id,title,severity,kind,probes,modules,refs,observed,impact,fix,accept,journeys):
 findings.append(dict(id=id,title=title,priority=severity,classification=kind,probe_ids=probes,modules=modules,source_ranges=refs,observed=observed,impact=impact,proposed_repair=fix,acceptance=accept,journeys=journeys,patched_in_this_review=False))
C='collector/src/keensight_scrapling/';A='canonical/keensight_contracts/'
finding('F01','Identity-binding evidence is outside eligibility/provenance closure','P0','FULL_VALIDATOR_ACCEPTS_INVALID_BOUNDARY',['R2-A01'],['KN-01','KN-02','KN-03','COM-04'],[(A+'validation.py',65,118),(A+'validation.py',123,172),(A+'validation.py',297,303),(A+'completion.py',149,161)],
 'A binding is changed to depend exclusively on a DELETED artifact. The account fact remains current-eligible, and full bundle validation passes. The binding artifact is not in roots(fact).',
 'A fact can lose the evidence establishing whose website or record it is while still supporting account-specific copy. Pinning a binding ID does not pin or preserve its supporting artifacts.',
 'Include accepted binding decisions, their exact evidence locators/artifacts and permitted source state in dependency closure. Separate substantive corroboration from this mandatory identity support. Admit/resolve bindings before dependent facts and invalidate current use when required binding evidence becomes unusable.',
 'Deleted, expired, revoked, unpinned, or foreign binding support must block affected current claims. A valid alternative accepted binding should be an explicit new decision rather than an automatic guessed fallback.', ['J07','J11','J17'])
finding('F02','Demoted templates pass the standalone current-use/export boundary','P0','LOCAL_REFERENCE_EXPORTER_GAP',['R2-A02'],['COM-02','COM-03','COM-04'],[(A+'completion.py',298,377),(A+'handoff.py',19,43),(A+'validation.py',408,422)],
 'After an existing template is demoted from ACTIVE to CANDIDATE and the current version vector is refreshed, LocalPreviewExporter writes the preview. The full bundle validator rejects the same state with MISSING_APPROVAL.',
 'Calling the local gate/export method independently has weaker authority rules than validating the whole bundle. This is a local fixture boundary, not a tested live sender bypass.',
 'Make current-use eligibility explicitly check the current template/renderer, offer where applicable, source and reviewed-release authority. Bind review to immutable historical bytes but perform current vetoes at export. Keep shared validation logic rather than relying on callers to rerun the entire fixture bundle.',
 'Template demotion/retirement must block a new export without erasing the historic review. Existing permitted byte-identical exports retain their receipt; a fresh gate must not restore authority just by recomputing a hash.', ['J07','J13','J17'])
finding('F03','Publication validates one payload and can persist a different argument set','P0','INTERNAL_API_CONTRACT_SPLIT',['R2-C06'],['FP-02','PLAT-01'],[(C+'storage.py',211,258),(C+'pipeline.py',231,246)],
 'Store.publish_evaluation receives a valid bundle describing one observation and separately receives empty match/observation/support arguments. It commits a successful manifest with one observation but zero observation rows.',
 'The normal Scanner passes consistent arguments; the defect is the public local-owner publication API. A future wrapper or refactor can commit an internally contradictory database even though the manifest validated.',
 'Accept one validated publication object and derive all database rows from it, or compare all separate arguments byte-for-byte before beginning the transaction. Re-extract trusted capture evidence at the boundary that owns admission; do not merely validate a sibling object.',
 'Mismatch must reject before any findings or successful manifest commit. Add matching, missing, added and altered-row cases plus rollback fault injection.', ['J03','J11','J19'])
finding('F04','Later supersession leaks into an earlier sealed evaluation','P1','HISTORICAL_QUERY_INCONSISTENCY',['R2-A06'],['KN-03','KN-04','RE-01'],[(A+'validation.py',123,144),(A+'completion.py',170,199),(A+'engine.py',86,98)],
 'The old run pins f.tech. A replacement recorded after its knowledge cutoff, but before its logical as_of, is not in that run. Historical resolution nevertheless becomes UNKNOWN because usable() searches every fact in the bundle for supersession.',
 'Reproducing an old result depends on later database contents. This is distinct from the intended current-use check, which should see newly recorded evidence.',
 'Give historical eligibility an explicit permitted input set/knowledge cutoff and snapshot-specific changes. Keep current-use eligibility as a different operation. Route supersession lookup through the same visibility context rather than scanning all rows.',
 'Adding later observations/corrections must leave sealed historical results unchanged; a current view and use gate must still reflect those changes.', ['J04','J07','J17'])
finding('F05','Generated-artifact handoff is accepted by one validator and rejected by another','P1','INCOMPATIBLE_VALIDATOR_LAYERS',['R2-A03'],['AI-01','RE-01','CTL-02','KN-02'],[(A+'completion.py',425,458),(A+'validation.py',340,356)],
 'A model response is correctly declared as a run-produced artifact, with a successful earlier producer. A later declared execution consumes it. validate_completion passes; Bundle.validate rejects ARTIFACT_OUTSIDE_RUN because an older loop still requires every execution artifact to be in input_artifact_ids.',
 'The repaired manifest can represent generated model I/O, but a downstream consumer cannot consistently use it in the same run.',
 'Use one available-artifact resolver in all validators. It must admit sealed external inputs or eligible prior outputs, enforce chronology and producer ownership, and reject self-consumption. Do not copy a generated response into the external-input list to satisfy the older check.',
 'A two-stage generated-output→consumer path must pass both validators; unfinished, future, self-produced or undeclared inputs must fail.', ['J07','J12'])
finding('F06','HTML recovery can silently truncate the parse while reporting complete detection','P1','EXECUTED_COLLECTOR_DEFECT',['R2-C05'],['ING-04','FP-01'],[(C+'extraction.py',54,67),(C+'extraction.py',96,110),(C+'rules.py',158,191)],
 'A retained page with 400 nested div elements and a later product script triggers parser recovery. Script extraction reports COMPLETE with zero surfaces, and its rules report NO_MATCH. The retained bytes do contain the marker.',
 'The previous fix handles explicit item/text caps, but not structural information discarded by the parser. No absence fact is emitted today; coverage/reporting is nevertheless wrong.',
 'Inspect parser diagnostics and classify information-losing recovery or depth/resource limits. Propagate an explicit partial capability state to all affected extractors and match evaluations. Harmless HTML repairs need a documented policy rather than blanket success or blanket failure.',
 'Deeply nested, truncated and malformed inputs must not produce a complete negative when evidence was dropped. Ordinary recoverable pages should retain deterministic extraction.', ['J02','J03','J09'])
finding('F07','A self-superseding fact raises RecursionError before semantic rejection','P1','UNCONTROLLED_INVALID_INPUT_FAILURE',['R2-A04'],['KN-02','KN-03'],[(A+'validation.py',123,130),(A+'validation.py',485,489),(A+'completion.py',183,199)],
 'Setting f.tech.supersedes_fact_id to f.tech causes full validation to raise RecursionError, rather than the intended ordered-supersession ContractError.',
 'The data does not become accepted, but an ordinary malformed record escapes the controlled contract-failure path and can abort a batch or obscure the actual invalid field.',
 'Validate supersession identity, ordering and acyclicity before eligibility recursion. Add an explicit recursion/visited guard to public read helpers so malformed unadmitted data cannot exhaust the stack.',
 'Self and multi-record cycles receive stable diagnostic codes and no publication; valid historical chains remain queryable.', ['J06','J07','J11'])
finding('F08','Requirement minimum means fact count in the helper but origin count in validation','P1','REFERENCE_FUNCTION_CONTRACT_MISMATCH',['R2-A08'],['RE-05','KN-03'],[(A+'engine.py',143,150),(A+'validation.py',399,407)],
 'evaluate_requirements resolves minimum=2 from two eligible fact rows backed by the same substantive origin. The full signal validator requires two distinct substantive artifact origins.',
 'The allowlisted rule helper can compute a result that its consuming validator rejects. This is a helper-level comparison, not a claim that a fully admitted forged signal passed.',
 'Name the unit explicitly (observations, evidence elements, origins, independent corroboration) in the requirement contract. Share one support-selection/evaluation function between the rule and the validator. Multiple records from one origin cannot satisfy an origin threshold.',
 'Duplicate rows/origins must not increase the selected unit. Independent eligible origins should satisfy a properly configured threshold.', ['J07','J12','J13'])
finding('F09','Retained-file import does not pin subject identity in run configuration','P1','EXECUTED_CLI_IDENTITY_DEFECT',['R2-C07'],['CTL-02','ING-02','FP-02'],[(C+'cli.py',103,114),(C+'storage.py',59,67),(C+'pipeline.py',248,256)],
 'Two analyze-file calls use the same tenant, run, URL, observation time and rules but different subjects. Both return exit 0. The resulting run contains both subjects, and replay fails with Cross-subject/tenant/origin host rollup forbidden.',
 'Independent CLI invocations can create a run that the replay contract cannot consume. The import path pins fewer identity fields than the live scan path.',
 'Use one immutable ScanPlan/run identity for live and imported capture. Include subject, input mode, code/parser version, source and content/import manifest. A single-target run rejects subject changes; a multi-target run requires explicit partitions.',
 'The second changed-subject invocation must fail without appending its capture. A deliberate new run should work and replay independently.', ['J02','J04'])
finding('F10','Current candidate discovery counts unlabelled revoked evidence','P1','RESEARCH_INDEX_ELIGIBILITY_GAP',['R2-C04'],['FP-03','PLAT-02'],[(C+'storage.py',164,215)],
 'After the only supporting capture is revoked, candidates(tenant,min_hosts=1) returns the same current candidate and prevalence counts. The query does not join revocation state.',
 'An operator can prioritize or export a research candidate without seeing that its support is no longer eligible. This probe concerns derived metadata, not continued export of the original revoked bytes.',
 'Separate historical occurrence counts from eligible support counts and expose both with an as_of/policy identity. Filter or flag revoked/expired support in current candidate selection; keep audit history according to policy.',
 'Revoking all support must remove current eligibility or display an explicit unsupported/historical state. New eligible support can restore candidacy without erasing prior history.', ['J05','J17'])
finding('F11','Contradictory duplicate command outcomes are accepted','P1','COMMAND_REPORT_IDENTITY_GAP',['R2-C10'],['FP-01','FP-02','PLAT-03'],[(C+'pipeline.py',211,218),(C+'validation.py',60,72),(C+'core.py',100,111)],
 'Appending a FAILED MATCH_HOST_SUFFIX record with the same inputs alongside valid COMPLETE records still passes validate_bundle. The matcher check accepts any matching correct row; CommandResult has no invocation identity.',
 'A timeline cannot tell whether this is a retry, another operator using the same command name, or a contradiction. The baseline already has multiple COMPLETE rows because host_equals and host_suffix map to the same command.',
 'Assign command_execution_id, operator/version, target and attempt identifiers. Validate exactly one terminal outcome per invocation. Aggregate command-family status separately without discarding individual executions.',
 'Contradictory terminal states for the same invocation fail. Legitimate distinct operators/attempts remain representable and inspectable.', ['J03','J06','J19'])
finding('F12','No-byte failures lose invocation details and have no persisted evaluation manifest','P1','DIAGNOSTIC_AND_COMPLETENESS_GAP',['R2-C01','R2-C09'],['ING-03','CTL-02','PLAT-01','PLAT-03'],[(C+'pipeline.py',46,60),(C+'pipeline.py',76,126),(C+'storage.py',69,94),(C+'storage.py',214,236)],
 'finish_attempt replaces the reserved request payload; after timeout, started_at, command_id and mode are gone. A no-byte scan emits a bundle with no top-level tenant/subject/run identity (only evaluation_id), no captures, and no stored evaluation row.',
 'The attempts table retains tenant/run and run configuration separately, so identity is not wholly lost in the store. But the exported failure is not self-identifying and cannot produce a complete attempt timeline or durable failed-target evaluation.',
 'Keep immutable request metadata and append/merge the terminal outcome without deleting start fields. Require explicit evaluation tenant, target and run identity independently of artifacts. Persist zero-output success/failure/abstention manifests as first-class results.',
 'Two failed targets with the same human run label remain distinguishable. Start/end/command/mode survive timeout and resume, without manufacturing bytes or positive facts.', ['J06','J09','J19'])
finding('F13','Protocol rejects an honest timeout failure reported after its deadline','P1','FAILURE_REPORT_CONTRACT_GAP',['R2-P01'],['CTL-02','PLAT-03'],[('protocol/validate_protocol.py',92,151)],
 'A FAILED result with no positive outputs and an explicit timeout diagnostic, finalized one second after deadline, is rejected as Operation finished beyond deadline.',
 'The system needs to deny late success/effects while still recording the real end time and failed outcome. Otherwise a worker must lie about finish time or lose its failure report.',
 'Separate execution deadline, cancellation/timeout outcome, report completion and late-effect handling. Accept truthful terminal diagnostics after a deadline without allowing success publication or new side effects.',
 'Late FAILED/CANCELLED reports with appropriate reasons are admissible; a late success without approved semantics remains rejected and any uncertain side effect is reconciled.', ['J06','J08','J19'])
finding('F14','Collector and canonical matcher disagree on aside-region semantics','P1','CROSS_MODULE_MATCHER_POLICY_MISMATCH',['R2-C08'],['ING-04','FP-01','KN-02'],[(C+'extraction.py',23,35),(C+'rules.py',163,169),(A+'engine.py',117,138)],
 'For the same script in an aside element, the collector supports vendor.present; canonical fingerprint_hosts returns no match because it excludes aside.',
 'A future bridge can reject a collector finding that looked valid, or change its meaning. This review does not assert that every aside must be ignored or accepted.',
 'Choose and version one attribution/region policy; share a matcher/evidence representation or run parity fixtures through both implementations. Do not silently map the two predicate contracts as equivalent.',
 'Identical content and the declared same rule policy yield compatible results across collection and admission; differences require explicit policy/version labels.', ['J02','J03','J11'])
finding('F15','The protocol fixture does not constrain mode/effects against operation parameters','P2','DRAFT_CHECKER_INCOMPLETENESS',['R2-P02'],['CTL-01','CTL-03','PLAT-03'],[('protocol/validate_protocol.py',51,131)],
 'The complete fixture payload check accepts FP-01.match in CAPTURE mode reporting five network attempts even though its validated parameters say allow_network=false.',
 'No network was performed; this is a checker-consistency test. The enforcing runner still does not exist, so the current envelope cannot be advertised as enforcing effect permissions.',
 'Extend trusted operation signatures with allowed modes, effect classes and budget policies; compare reported usage to those constraints and enforce them before execution through capability-limited dependencies. Diagnostics must remain truthful when policy is violated.',
 'Offline matching cannot be authorized to capture; reported forbidden effects trigger a policy failure and alert rather than a successful eligible output.', ['J08','J19'])
finding('F16','effective_at is stored but its decision semantics are undefined/unused','P2','POLICY_DECISION_REQUIRED',['R2-A05'],['KN-02','KN-03','RE-05'],[(A+'engine.py',37,44),(A+'validation.py',123,171),(A+'validation.py',452,493)],
 'A fact with effective_at a month after the use gate remains current-eligible and passes full validation. The gate time, observed_at and recorded_at are distinct, but effective_at is not consulted.',
 'Some records describe future events and are valid observations now; others must not be interpreted as a currently effective status. The generic contract does not say which rule applies. This is separately reported, not an assumed universal failing requirement.',
 'Define per-predicate temporal semantics: observation of an announcement, asserted valid-time state, reporting period, and validity interval. Test the permitted language and signal conditions separately rather than universally dropping future-dated records.',
 'A future license effective date cannot prove currently effective licensure; a supported statement that the record announces a future effective date remains possible.', ['J11','J12','J13'])
(ROOT/'findings.json').write_text(json.dumps(findings,indent=2))

# Exact retained-source excerpts for the audit.
ex=['# Iteration 2 — numbered source evidence','', 'Source: the unchanged September 15 repaired package. Line numbers are local source-file line numbers. No remote source was fetched.','']
for f in findings:
 ex+=['## '+f['id']+' — '+f['title'],'']
 for path,start,end in f['source_ranges']:
  lines=(BASE/path).read_text().splitlines();end=min(end,len(lines))
  ex += [f'### `{path}:{start}–{end}`','', '```text']+[f'{i:4}: {lines[i-1]}' for i in range(start,end+1)]+['```','']
(ROOT/'SOURCE_EXCERPTS.md').write_text('\n'.join(ex))

intro='''# Iteration 2: submodule audit and implementation decisions

## Verdict and scope

The repaired local source still passes its existing test suites, but several adjacent boundaries remain inconsistent. This is a **new audit, reproducible safety tests, and walkthrough addendum**, not a new runtime release. Collector 0.2.0, canonical reference 4.2.0, the draft protocol checker and product design remain unchanged.

The baseline's integrity verifier confirms all 438 manifest-listed packaged files. This review did not modify GitHub, contact providers, crawl public sites, send messages, or run CRM mutations. All injected records and exports are synthetic local fixtures.

## Executed evidence

| Verification | Result | Meaning |
|---|---|---|
| Collector original suite | 183 passed, 1 skipped | Actual Scrapling dependency is absent; native browser is still disabled. |
| Canonical original suite | 609 passed | Reference contracts and retained fixture tests. |
| Protocol original suite | 42 passed | Fixture signature/payload checker, not a general runner. |
| New probes | 23 executed | 16 concrete contract counterexamples, 1 separately classified temporal-policy question, 6 passing controls. |
| Required-behavior suite | 16 failed, 6 passed | Failures deliberately express unimplemented repairs; no xfail/skip hides them. |
| Walkthrough smoke run | 8 journeys; 20 subprocesses | Offline local commands/reference fixtures; all expected exit codes and assertions passed. |

The 16 safety counterexamples are grouped into **15 code/contract findings** because two probes describe different parts of the same diagnostic gap. F16 is a separate temporal-policy decision. Passing the 834 original tests is not evidence that the new failing cases are safe. The local walkthroughs exercise narrow working paths, not a complete deployed business workflow.

## Priority convention

P0 means close before trusting autonomous outward use or a shared admission/publication boundary. P1 means close before completing the corresponding user journey or service extraction. P2 means a reference/interface design gap that must be settled before enabling that operation. These are review priorities, not externally scored security ratings.

## Summary

| ID | Priority | Finding | Boundary |
|---|---|---|---|
'''
for f in findings:intro+=f"| {f['id']} | {f['priority']} | {f['title']} | {f['classification']} |\n"
intro+='\n## Detailed findings\n\n'
for f in findings:
 intro+=f"### {f['id']} — {f['title']}\n\n**Priority:** {f['priority']}. **Owners:** {', '.join(f['modules'])}. **Probes:** {', '.join(f['probe_ids'])}.\n\n**Observed:** {f['observed']}\n\n**Impact and scope:** {f['impact']}\n\n**Proposed repair:** {f['proposed_repair']}\n\n**Acceptance condition:** {f['acceptance']}\n\n**Affected journeys:** {', '.join(f['journeys'])}.\n\n**Source:** "+'; '.join(f'`{p}:{lo}–{hi}`' for p,lo,hi in f['source_ranges'])+'. Numbered excerpts are in `SOURCE_EXCERPTS.md`; actual observations are in `reports/probe-results.json`.\n\n'
intro+='''## Existing repairs that still hold

Six controls passed: changed capture metadata is rejected; duplicate evaluation input does not publish findings; compatible rule-release replay succeeds; an unresolved binding blocks use; a cross-tenant ChangeRecord cannot veto the other tenant's fact; and an undeclared protocol input is rejected. These results distinguish residual gaps from blanket claims that previous repairs failed.

## Repair sequence

1. **One trusted decision dependency closure:** binding evidence, sealed versus current visibility, current template authority (F01, F02, F04). Keep the historical view separate from the current-use veto.
2. **One publication payload and invocation identity:** atomic persistence from the validated object, self-identifying zero-output evaluations, immutable attempts and command execution IDs (F03, F11, F12).
3. **Collector completeness and identity parity:** parser-loss diagnostics, shared region policy, run-subject identity and eligible research support (F06, F09, F10, F14).
4. **Canonical execution consistency:** one artifact-availability resolver, guarded supersession and shared requirement-counting logic (F05, F07, F08).
5. **Service protocol:** allow honest late failure reports and constrain operation modes/effects before exposing network workers (F13, F15). Decide predicate-specific effective-time behavior (F16).
6. Re-run the old suites, these safety tests, and the linked journeys. Only then broaden the capture→canonical→preview integration.

## Incompleteness remains explicit

There is no executable collector-to-canonical production admission bridge, persistent authenticated canonical service, general module runner, full donor-rule promotion service, native bounded browser, broad production connector suite, contact/campaign/enrollment implementation, sender, inbound conversation processor or CRM synchronization service in this baseline. The design provides module names, contracts and intended ownership. The feature map records these as proposed, not as callable endpoints.

The request in this iteration is to identify bugs and add critique/invocation walkthroughs. No application behavior has been patched. A local helper was added solely to run and log the documented offline journeys; it is not the proposed execution middleware.

## Reproduction

From this review package's root:

```bash
# Existing baseline; dependency installation may need network access in your environment.
python -m pip install -e './baseline/collector[test]'
python -m pip install -r ./baseline/canonical/requirements.txt
python baseline/verify_integrity.py
(cd baseline/collector && python -m pytest -q)
(cd baseline/canonical && python generate.py --check && python validate.py && python -m pytest -q)
(cd baseline/protocol && python validate_protocol.py && python -m pytest -q)

# New audit: expected to identify the documented defects against this unchanged baseline.
python audit_probes.py --output ./audit-output.json
python -m pytest -q tests/test_required_behaviour.py

# Narrow working user paths: offline and no-send, not full-system sign-off.
python walkthroughs/run_local_journeys.py --output ./journey-output --journey all-local
```

The failing safety suite should remain separate from the original passing-test count until patches intentionally change the expected outcomes. No defect is proven merely by a higher test count.
'''
(ROOT/'AUDIT.md').write_text(intro)

# Feature map. Status is per feature, not inherited from a diagram/module name.
features=[]
def feature(fid,title,actor,status,modules,journeys,entry,output,limits):
 features.append(dict(feature_id=fid,title=title,actor=actor,status=status,modules=modules.split(','),journeys=journeys.split(','),invocation=entry,expected_output=output,limits=limits))
feature('FM01','Define program, audience and offer','Growth lead','PROPOSED','GTM-01','J10',None,'Versioned ProgramDefinition/AudienceDefinition/OfferDefinition','No program CLI, API or UI exists.')
feature('FM02','Discover and select account seeds','Research operator','PROPOSED','GTM-02','J10',None,'AccountSeed, LeadSelection, ResearchPlan','The collector accepts a URL; it does not discover the complete prospect universe or import Harvest automatically.')
feature('FM03','Validate rules, contracts and release metadata','Engineer','REFERENCE','CTL-01,CTL-03','J08','reference-checks','Validation reports and fixture signature checks','No unified release compiler or effect-enforcing runner.')
feature('FM04','Run the synthetic scanner demonstration','Engineer','LOCAL','CTL-02,ING-02,ING-03,FP-02','J01','demo','ScanBundle and deduplicated claim view','Synthetic transport and fixture authority; no real Scrapling call.')
feature('FM05','Analyze retained HTML','Research engineer','LOCAL','ING-02,ING-04,FP-01,FP-02','J02','analyze-file','Stored capture, evidence, matches, observations and ScanBundle','Operator asserts source/time/subject; use a unique run per target. F09.')
feature('FM06','Capture an authorized website with Scrapling','Collection operator','SDK_UNVERIFIED','ING-02,ING-03','J09','scan (dependency-gated)','Artifacts, attempts, bundle or diagnostics','SDK unavailable in the audit environment; no live integration claim.')
feature('FM07','Render JavaScript/browser/network evidence','Collection operator','DISABLED','ING-03','J09',None,'Proposed rendered Capture and network artifacts','FETCH_STEALTH is a disabled extension point. No public browser runtime.')
feature('FM08','Extract the 17 surfaces as an independent process','Debugger','LOCAL','ING-04','J03','extract','PageEvidence with per-extractor reports','Parser-loss completeness and aside-region parity need F06/F14.')
feature('FM09','Match pinned rules as an independent process','Rule engineer','LOCAL','FP-01','J03','match','StandaloneMatchResult','Not canonical facts; no output publication to canonical store.')
feature('FM10','Inspect duplicate support and collector claim views','Analyst','LOCAL','FP-02','J01,J03,J04','resolve / claims','One view per claim with all support links','Historical collector view, not a current commercial use gate.')
feature('FM11','Verify bundle, metadata and original bytes','Debugger','LOCAL','PLAT-01,FP-02','J03,J06','check','Valid response or nonzero rejection','Offline structural-only check without --store is weaker; use trusted store verification.')
feature('FM12','Replay retained evidence under a selected rule release','Rule engineer','LOCAL','ING-05','J04','replay','New evaluation with original observation dates','Compatible release replay verified; no recapture, model call or TTL refresh.')
feature('FM13','Import the supported donor-rule subset','Rule curator','LOCAL','FP-03','J05','import-donor','Candidate rule pack and quarantine report','No inherited approval or complete donor-corpus integration.')
feature('FM14','Inspect recurring unknown technical features','Rule curator','LOCAL','FP-03','J05','candidates','Candidate/prevalence rows','Revoked support is not filtered from current counts: F10.')
feature('FM15','Promote and distribute reviewed rules','Rule reviewer','PROPOSED','FP-03,QA-01','J05,J18',None,'Reviewed immutable fingerprint release','No complete promotion/calibration/distribution runtime.')
feature('FM16','Resolve production subject identity','Research analyst','PROPOSED','KN-01','J11',None,'Accepted binding with exact identity evidence','Fixture bindings exist; real resolver and admission workflow do not.')
feature('FM17','Admit collector output as canonical facts','Knowledge engineer','PROPOSED','KN-02','J11',None,'Fact/Evidence/Execution plus admission report','Executable bridge and persistent canonical repository absent.')
feature('FM18','Check canonical claim resolution and samples','Knowledge engineer','REFERENCE','KN-03,KN-04','J07','canonical validate / Python fixture API','Reference validation and decision results','Not a hosted query API; sealed/current semantics need F04.')
feature('FM19','Capture broad third-party source families','Research operator','PROPOSED','ING-01,CTL-03','J12',None,'Approved artifacts and source-specific fact drafts','213 predicate definitions are not 213 implemented collectors.')
feature('FM20','Run bounded live model extraction and repair','Research engineer','PROPOSED','AI-01','J12',None,'ModelCall, artifacts, repair chain, typed output','Reference checks only; generated-output consumer bug F05.')
feature('FM21','Compute research priors and explicit context joins','Research analyst','REFERENCE','RE-02,RE-03','J07,J12','canonical fixture validation / Python helpers','Sample-bound priors and internal ContextAssessment','No live-source research job; context is not outward company proof.')
feature('FM22','Find comparable cases and rank lookalikes','Strategy analyst','PROPOSED','RE-04','J12',None,'Comparison and LookalikeMatch','No vector service/index or verified causal transfer.')
feature('FM23','Evaluate derivations and business conditions','Analyst','REFERENCE','RE-01,RE-05','J07,J12','reference functions, not a product CLI','Derived drafts and signal decisions','Minimum-support units disagree: F08. Production selectors absent.')
feature('FM24','Choose a supported commercial opportunity','Growth operator','PROPOSED','COM-01','J13',None,'OpportunitySelection','A detected tool does not automatically prove pain or offer fit.')
feature('FM25','Assess contact, role, endpoint and permission','Sales researcher','PROPOSED','AUD-01','J13',None,'ContactProfile and ContactAssessment','No contact enrichment/verification runtime.')
feature('FM26','Render existing reference packages','Content reviewer','REFERENCE','COM-02','J07','Bundle.render(existing_package)','Grounded text from delivered fixture templates','No arbitrary-prose proof engine or all-channel renderer.')
feature('FM27','Approve exact content through an authenticated workspace','Reviewer','PROPOSED','COM-03,UX-01','J13',None,'ReviewDecision tied to exact revision/hash','Synthetic reviews and actor grants are fixtures, not human auth/UI.')
feature('FM28','Export a local reference preview with idempotency','Reference tester','REFERENCE','COM-04','J07','LocalPreviewExporter via walkthrough helper','Local JSON preview; repeated key reuses bytes','No remote CRM export or send; current template veto F02.')
feature('FM29','Configure campaigns and sequence ownership','Sales operations','PROPOSED','CAM-01','J14',None,'CampaignDefinition/Approval/Readiness','No campaign manager or provider configuration mutation.')
feature('FM30','Enroll a contact and schedule/stop steps','Sales operations','PROPOSED','CAM-02','J14',None,'Enrollment, StepEligibility, DeliveryIntent','No durable enrollment/scheduler runtime.')
feature('FM31','Dispatch and reconcile an exact authorized message','Sales operations','PROPOSED','COM-05','J15',None,'Attempt, receipt, Exposure','No sender; preview/export gates do not authorize sending.')
feature('FM32','Route replies and immediate stop requests','Sales representative','PROPOSED','ENG-01,COM-06','J16',None,'Conversation, assessment, stop control, follow-up','No authenticated webhook/mailbox integration.')
feature('FM33','Synchronize sales handoff with CRM','Sales owner','PROPOSED','CRM-01','J16',None,'CRMSyncIntent/Receipt and linked handoff','No connected CRM mutations performed or implemented in this package.')
feature('FM34','Measure outcomes, experiments and calibration','Analyst/QA','PROPOSED','COM-06,QA-01','J18',None,'Attributable measurements and reviewed promotion proposals','Tests and schemas exist; no full exposure/attribution/experiment pipeline.')
feature('FM35','Govern evidence, bindings, changes and retention','Administrator','REFERENCE','PLAT-02,KN-03','J17','Store.revoke or Bundle.validate_change (local/reference only)','Revocation/change validation','No hosted auth, real retention worker or restore service. F01/F10 remain.')
feature('FM36','Inspect/debug individual modules and service boundaries','Engineer/operator','LOCAL','PLAT-01,PLAT-03,UX-01','J03,J06,J08,J19','ks-module and offline walkthrough harness','JSON outputs and per-process logs','No operator UI, distributed trace backend or general ModuleRequest runner.')
allmodules={x['module_id'] for x in json.loads((BASE/'product-design/module_catalog.json').read_text())['modules']}
assert {m for f in features for m in f['modules']}==allmodules
(ROOT/'feature-map.json').write_text(json.dumps(features,indent=2))
fm='''# E2E feature map and invocation boundaries

This map covers all 39 logical module IDs through 36 user-facing feature areas. It is grounded in collector 0.2.0, canonical reference 4.2.0 and the supplied product design. Features are not declared implemented merely because a schema, diagram or module name exists.

## Readiness legend

- **LOCAL:** a narrow local operation is implemented and exercised by the offline journeys; not production sign-off.
- **REFERENCE:** only synthetic/reference functions or validation are executable; no real product workflow is implied.
- **SDK_UNVERIFIED:** a real adapter exists but its dependency/integration could not be run here.
- **DISABLED:** the delivered entrypoint deliberately refuses the capability.
- **PROPOSED:** design/contract only; no working invocation exists.

`walkthroughs/run_local_journeys.py` is a test/documentation harness, not a replacement execution engine. It makes no network requests or sends.

| Feature | User | Readiness | Modules | Journey / callable boundary |
|---|---|---|---|---|
'''
for f in features:fm+=f"| {f['feature_id']} — {f['title']} | {f['actor']} | {f['status']} | {', '.join(f['modules'])} | {', '.join(f['journeys'])}: {f['invocation'] or 'Not implemented; no command/API to invoke'} |\n"
fm+='\n## Feature outputs and limitations\n\n'
for f in features:
 fm+=f"### {f['feature_id']} — {f['title']}\n\n**Expected output:** {f['expected_output']}.\n\n**Boundary:** {f['limits']}\n\n"
fm+='''## Execution boundaries that must remain explicit

A call to `canonical/validate.py` checks the supplied fixture bundle. It does not run account research, create a canonical service, execute all derivations, or perform identity resolution. `protocol/validate_protocol.py` checks its shipped example and signature; it does not accept arbitrary runtime requests or provide an HTTP endpoint. `ks-module` calls are separate processes around collector functions, not the proposed ModuleRequest transport. The local reference exporter does not create review decisions or send messages.

Raw observations and product/industry context stay broad. Feature activation controls what can be computed or used, not whether the schema catalog must shrink to the initial few signals.
'''
(ROOT/'FEATURE_MAP.md').write_text(fm)

journeys=[]
def journey(id,title,actor,status,stages,steps,inputs,outputs,failure,invocation,accept):
 journeys.append(dict(journey_id=id,title=title,actor=actor,status=status,stages=stages,steps=steps,inputs=inputs,outputs=outputs,failure_branch=failure,invocation=invocation,acceptance=accept))

def local(id):return f'python walkthroughs/run_local_journeys.py --output ./journey-output --journey {id}'
journey('J01','First offline run: see duplicate fingerprints become one claim','Engineer','LOCAL','F03–F07',[
 'List the 38 registered command IDs; this is an inventory, not all-38 live sign-off.',
 'Run the synthetic two-page demonstration with fixture transport.',
 'Inspect all 7 match records, 2 observations and 1 claim; keep the support links.',
 'Check the bundle against its trusted metadata and original blobs.'],
 'The included collector examples and installed core parser dependencies. No credentials.',
 'demo-store/scan-bundle.json, claims.json, scanner.sqlite3 and retained fixture blobs.',
 'A dependency or contract error produces nonzero exit. No LLM, provider, campaign or sender is called.',local('J01'),
 'The shipped synthetic result is 7 matches → 2 observations → 1 claim, with no combined confidence. This count is an example, not a business scoring policy.')
journey('J02','Analyze an already-retained page','Research engineer','LOCAL','F02,F05–F07',[
 'Confirm your right to retain/process the page and record the actual collection time separately from today.',
 'Choose explicit tenant and subject identifiers and a new single-target run ID.',
 'Call analyze-file; the source is marked user-provided-snapshot.',
 'Inspect the capture, extraction reports and observation support; run the trusted-store bundle check.'],
 'HTML bytes, page URL, asserted collection timestamp, explicit subject/tenant, selected rule release.',
 'imported-store/scan-bundle.json and original-content store.',
 'The importer does not verify legal company ownership. F09 means a reused run can currently mix subjects: do not reuse a run across targets. F06 affects deep/malformed HTML.',local('J02'),
 'No network calls. Supported observations trace to the supplied bytes; user-supplied timestamps are not independently authenticated.')
journey('J03','Debug extraction, matching and resolution as separate processes','Debugger','LOCAL','F06–F07,F26',[
 'Select a capture_id from observations or evaluated_capture_ids, not an arbitrary robots response.',
 'Run ks-module extract and inspect PageEvidence and every extractor status.',
 'Run ks-module match against those evidence records and a pinned rule pack.',
 'Run check for the whole bundle; run resolve for its historical claim view.',
 'Use IDs to follow claim → observation → support → match → surface → capture.'],
 'An existing trusted collector store and ScanBundle.',
 'page-evidence.json, matches.json, checked.json, resolved.json plus per-process logs.',
 'Do not equate standalone match output with canonical Fact admission. F11 means a command-family timeline is not yet unambiguous; F03 is the publication API issue.',local('J03'),
 'Each process uses stored bytes and returns parseable JSON or an explicit nonzero failure. No service deployment is implied.')
journey('J04','Replay retained evidence and compare before/after','Rule engineer','LOCAL','F07–F08,F11',[
 'Keep the original capture run unchanged.',
 'Choose an evaluation ID and rule release; the replay uses no transport.',
 'Run replay and compare matches, observations, rule release and capture time.',
 'Query historical collector claims under an explicit currently selected rule allowlist.'],
 'Original store, original capture-run ID, evaluation-run ID, rule pack and evaluation as_of.',
 'replay.json; all original observations retain their captured timestamps.',
 'Missing capture modalities require recapture; they cannot be reconstructed. F04 is a separate canonical historical-visibility defect, not a failure of this passing collector replay example.',local('J04'),
 'The smoke test asserts identical observations for unchanged evidence/rules. A separate control verifies a compatible changed release replays successfully.')
journey('J05','Inspect unknown features and import donor candidates','Rule curator','LOCAL/PARTIAL','F08',[
 'Run candidates against the local technical index; the demo lowers min-hosts to 1 only for inspection.',
 'Import donor-shaped JSONL using an explicit vendor map.',
 'Review IMPORTED_CANDIDATE versus QUARANTINED disposition for every input row.',
 'Stop before promotion: no production approval or distribution command is implemented.'],
 'Retained captures, donor rows, canonical vendor mapping, reviewer policies for future promotion.',
 'imported-candidates.json, import-report.json and candidate-query output.',
 'F10 means revoked evidence still affects unlabelled candidate counts. Never treat current output as automatically eligible promotion evidence.',local('J05'),
 'Automatic approvals remain zero and every row is accounted for. This is a subset adapter, not the full 739-definition donor corpus or 2,500-signature catalog.')
journey('J06','Investigate a failed check and preserve diagnostics','Engineer/operator','LOCAL/PARTIAL','F05,F07,F26',[
 'Make a copy of a valid bundle; do not modify original capture bytes or the database.',
 'Change one supplied metadata field in that copy and run check.',
 'Expect exit 2 and inspect stderr; the original bundle must still validate.',
 'For acquisition failures inspect attempts and run configuration with read-only SQL; do not fabricate a capture.',
 'Run the separate required-behavior suite to see the still-failing diagnostic boundaries.'],
 'A valid fixture store and the new audit tests.',
 'tampered-bundle.json, expected rejection logs, valid-after-rejection.json.',
 'F12 currently drops start fields at attempt finalization and omits zero-capture evaluation identity; F13 rejects honest post-deadline timeout reports. These are not repaired by the passing tamper test.',local('J06'),
 'The deliberate tamper must fail, while original data remains valid. New safety tests are intentionally failing until code fixes land.')
journey('J07','Review the canonical reference path and produce a local preview','Reference tester','REFERENCE','F09–F18,F21',[
 'Check canonical generated files and validate the shipped synthetic bundle.',
 'Inspect existing bindings, facts, claim resolutions, sample priors, signals and package evidence.',
 'Use the existing fixture review and gate at their fixed historical timestamps.',
 'Export a local no-send JSON preview; repeat the same idempotency key and confirm reused bytes.'],
 'The shipped canonical fixture bundle, trusted synthetic actor.fixture grant and fixture destination.',
 'reference/reference-preview.json and one idempotent local preview JSON.',
 'This is not capture-to-canonical admission, real review/authentication, contact enrichment or current production permission. F01/F02/F04/F05/F08 remain blockers for the corresponding paths.',local('J07'),
 'Full reference validation passes, repeated export reuses bytes, send_allowed remains false, and no collector data is silently converted to canonical facts.')
journey('J08','Verify the shared protocol and product design inventories','Integration engineer','REFERENCE','F03,F26',[
 'Run the protocol fixture checker.',
 'Inspect the exact registered operation: FP-01.match with example-only payload schemas.',
 'Run the 39-module product-design inventory checker.',
 'Compare desired deployment with the proposed eight ownership groups; do not deploy the checker as a worker.'],
 'protocol/examples and product-design definitions.',
 'Protocol/example consistency and design-inventory reports.',
 'F13/F15 show the checker still lacks correct failure/effect semantics. No arbitrary operation handler, auth server or HTTP endpoint is supplied.',local('J08'),
 'Passing reports explicitly remain fixture/design checks. Unknown implementation names are not treated as supported modules.')
journey('J09','Enable and verify a real permitted static capture','Collection operator','SDK_UNVERIFIED; BROWSER DISABLED','F03–F07',[
 'Install the live extra in an environment that can obtain Scrapling 0.4.15.',
 'Require the SDK import to succeed before running test_live_integration.py; a skipped test is not sign-off.',
 'Run the controlled local HTTP fixture integration before an authorized public target.',
 'Use the candidate-only live rule example; inspect limits, redirects, failures and coverage.',
 'Keep browser capture disabled until egress, cookies, resources and cancellation have their own verified boundary.'],
 'Permitted target, installed pinned SDK, source-purpose approval, bounded ScanConfig and candidate-only rules.',
 'Real attempts, artifacts and scan bundle only after actual integration succeeds.',
 'No live call was made in this iteration. F06/F12/F14 must be understood; never bypass rate limits or source restrictions to make a test green. Browser has no working default.',
 "python -m pip install -e './baseline/collector[live,test]'\npython -c \"from scrapling.fetchers import FetcherSession; from importlib.metadata import version; assert version('scrapling') == '0.4.15'\"\n(cd baseline/collector && python -m pytest -q tests/test_live_integration.py)",
 'Require actual execution (not skip), then real capture within declared policy. User-supplied target identity is still not canonical ownership evidence.')
journey('J10','Set up a sales program and select accounts','Growth lead','PROPOSED','F00–F03',[
 'Define services, audience, geography, exclusions, permitted sources and budgets.',
 'Approve a versioned program and derive a research plan.',
 'Import/discover seeds and deduplicate account identities without turning fit criteria into facts.',
 'Authorize a bounded run with a pinned capability profile.'],
 'Program/audience/offer definitions, seed origin, current account/CRM exclusions and trusted principal.',
 'Program revision, AccountSeed, LeadSelection, ResearchPlan, IntakeRequest and BatchRun.',
 'No program UI or seed-selection handler exists. The one-URL collector is not an account-discovery engine.',None,
 'Implement tests for exclusions, provenance, identity ambiguity, budget denial and zero eligible accounts before enabling this journey.')
journey('J11','Move collector observations into canonical, searchable knowledge','Knowledge engineer','PROPOSED BRIDGE','F02,F09–F11',[
 'Read the complete ScanBundle, not just host priority or one claim row.',
 'Verify successful producers, original captures, subject bindings and typed predicate mappings.',
 'Admit one captured observation with all its supports and exact provenance.',
 'Resolve complete claim groups; separate historical and current visibility.',
 'Publish a searchable knowledge result even when no commercial rule fires.'],
 'Collector observations/support, canonical predicate/source release and accepted identity evidence.',
 'Canonical Fact/Evidence/Execution plus admission report, ClaimResolution and InputSnapshot.',
 'No executable production bridge or persistent canonical API exists. F01/F03/F04/F07/F09/F14 must be closed before the integration is trusted.',None,
 'A real stored capture traverses admission without manual fixture editing; missing identity, stale/candidate/conflicting evidence and zero results are handled honestly.')
journey('J12','Build enriched account research and product/industry context','Research analyst','PROPOSED RUNTIME; REFERENCE CHECKS ONLY','F12–F15',[
 'Select approved source families and capture relevant hiring, technology, review, traffic, registry or publication artifacts.',
 'Run typed extraction; any model task retains original I/O and bounded repair history.',
 'Create samples with explicit eligible, excluded and unclassified members.',
 'Compute priors and join them through declared product/industry links.',
 'Run enabled derivations/signals over pinned complete claim groups.'],
 'Permitted source records, InputSnapshot, versioned functions, sample/support policies and context rules.',
 'Typed facts, sample-bound priors, ContextAssessment, derivations and SignalEvaluation.',
 'The current reference bundle illustrates records but does not execute the broad live flow. F05/F08/F16 require consistent decisions; context cannot become company-specific proof.',None,
 'A product-prior change or deleted denominator changes its eligibility. Failed model calls produce honest uncertainty. Duplicate origins cannot inflate support.')
journey('J13','Choose an offer, assess a contact and review supported copy','Growth operator/reviewer','PROPOSED PRODUCT; NARROW RENDERER REFERENCE','F16–F18,F21',[
 'Select a supported service-line opportunity; allow no-opportunity as a valid result.',
 'Resolve relevant person/account relation, role, endpoint status and permission separately.',
 'Render approved clauses using eligible account evidence; context may guide a neutral question only.',
 'Review the exact message revision and hash with an authenticated reviewer.',
 'Obtain a fresh use decision for its specific purpose and destination.'],
 'Opportunity, account proof, contact assessment, approved template and trusted reviewer.',
 'OpportunitySelection, ContactAssessment, GroundedClause, OutreachPackage, ReviewDecision and gate.',
 'Live contacts, opportunity orchestration, review UI and authenticated service are not implemented. Reference preview is J07. Unknown maturity blocks maturity claims, not every neutral question.',None,
 'Changed content invalidates old review; demoted template blocks current use; incomplete contact assessment holds contact-specific export.')
journey('J14','Approve a campaign, enroll and schedule one step','Sales operations','PROPOSED','F19–F20',[
 'Define allowed audience, templates, sequence steps, sender limits, timezone and stop rules.',
 'Choose exactly one scheduling authority: local application or provider.',
 'Approve campaign readiness separately from reviewing one account message.',
 'Enroll an eligible contact with deduplication and cross-campaign frequency limits.',
 'Produce a due DeliveryIntent; do not send just because a package exists.'],
 'Approved program/campaign, assessed contact, reviewed content and restrictions.',
 'CampaignApproval, Enrollment, StepEligibility and stable DeliveryIntent.',
 'No campaign, enrollment or schedule-management CLI/API exists. Do not invent provider campaign IDs or activation commands.',None,
 'Duplicate enrollment is idempotent, step progression has one owner, reply/opt-out/customer exclusions hold subsequent steps.')
journey('J15','Authorize, dispatch and reconcile a message','Sales operations','PROPOSED','F21–F22',[
 'Resolve the exact reviewed message and stable logical send identity.',
 'Check current contact, campaign, enrollment, source rights, restrictions and sender readiness.',
 'Commit intent/outbox state before external dispatch.',
 'Record acceptance, rejection or uncertainty.',
 'Reconcile possible acceptance before retry; do not equate acceptance with inbox delivery.'],
 'DeliveryIntent, exact message, authenticated authority and a dedicated send gate.',
 'Delivery attempt, receipt, Exposure or unresolved reconciliation state.',
 'No sender exists. Current canonical preview/contact export purposes are not send authority. New attempts and CRM retries never authorize duplicate sends.',None,
 'Provider timeout after acceptance results in one reconciled send, not a blind retry. Late restrictions stop subsequent actions with actual chronology retained.')
journey('J16','Handle replies, stop outreach and hand off to sales/CRM','Sales representative','PROPOSED','F23–F24',[
 'Authenticate and deduplicate inbound events; correlate the exposure and conversation.',
 'Apply immediate pause/stop/restriction rules before optional model classification.',
 'Route interest, questions, objections, out-of-office and referrals appropriately.',
 'Create human response/sales-handoff tasks.',
 'Synchronize CRM with field ownership and idempotent receipts; reconcile retries without resending outreach.'],
 'Verified event, permitted content, contact/exposure/enrollment IDs and current restrictions.',
 'Conversation, ReplyAssessment, EnrollmentControl, follow-up/SalesHandoff and CRM sync receipt.',
 'No mailbox/webhook/CRM runtime exists here. An opt-out cannot wait for analytics or a model. Referrals create candidates, not automatic outreach permission.',None,
 'Duplicate events do not duplicate effects; CRM failure retries only the CRM action; uncorrelated events are quarantined without invented exposure links.')
journey('J17','Correct identity or revoke evidence/authority','Administrator','REFERENCE / LOCAL OWNER ONLY','F26',[
 'Identify the exact fact, binding, artifact, template or source and its dependencies.',
 'Authorize the requested correction/revocation with typed target and tenant ownership.',
 'Keep history while blocking current use and invalidating affected projections.',
 'Separate historical reads from current action permission.',
 'Verify all dependent research, identity and content surfaces report the changed state.'],
 'Trusted configured actor (reference only), exact target, reason, effective/recorded chronology and policy.',
 'Reference ChangeRecord validation or local collector capture revocation; production workflow still absent.',
 'F01 binding support, F02 template gate and F10 research candidates are incomplete. Hosted auth/grant management/deletion workers remain unimplemented. Historical metadata retention is policy-specific.',None,
 'Required-behavior tests for F01/F02/F10/F04 must pass before presenting a complete revoke/correct workflow.')
journey('J18','Measure outcomes and improve rules/templates','QA/analyst','PROPOSED','F08,F25',[
 'Join verified outcomes to deduplicated exposures and sample eligible mature windows.',
 'Keep denominator, attribution, exclusions and missingness explicit.',
 'Measure detector/extractor quality separately from outreach conversion.',
 'Evaluate changes on appropriate gold sets or approved experiments.',
 'Review promotion proposals and publish a new immutable release for later runs.'],
 'Valid exposures/outcomes, evaluation sets, release versions and measurement policies.',
 'Descriptive measurement facts, QualityAssessment and PromotionProposal.',
 'No full metric/experiment/promotion runtime exists. Success rates cannot turn weak evidence into truth; observational comparison is not causal proof.',None,
 'Retries, duplicate replies, immature response windows, selection bias and source-origin duplication are covered by acceptance tests before activation.')
journey('J19','Run submodules separately and prepare service extraction','Integration engineer','LOCAL PROCESSES; PROPOSED SERVICES','F03,F26',[
 'Use J03 for extract/match/check/resolve in separate Python processes.',
 'Retain one owner for publication, canonical admission, enrollment/send intent and restrictions.',
 'Add a real enforcing runner and trusted record resolver before remote workers.',
 'Close operation modes/effects, timeout diagnostics, auth, idempotency and transaction boundaries.',
 'Extract a service only for a demonstrated isolation/scaling reason; do not deploy one service per cheap extractor.'],
 'Existing package, typed contract plans, service ownership map, scoped storage and release locks.',
 'Today: standalone JSON artifacts/logs. Later: authorized worker requests/results with tested boundary parity.',
 'There is no HTTP endpoint, broker, distributed tracing backend or generic task dispatcher. Shared SQLite across machines is not a service architecture.',None,
 'Pure outputs agree across in-process and worker execution. F03/F11/F12/F13/F15 must be closed before wrapper behavior is relied on.')
(ROOT/'user-journeys.json').write_text(json.dumps(journeys,indent=2))

jd='''# Feature walkthroughs and user journeys

## What can be invoked now

Eight local/reference journeys below were executed in 20 separate subprocesses with expected exit codes. No network/provider operation was enabled. The real static Scrapling path is dependency-gated and unverified here; native browser is disabled. All business journeys without handlers are explicitly marked PROPOSED and have no pretend command or endpoint.

From the unpacked review package root:

```bash
python -m pip install -e './baseline/collector[test]'
python -m pip install -r ./baseline/canonical/requirements.txt
python walkthroughs/run_local_journeys.py --output ./journey-output --journey all-local
```

The harness also works from the source tree through PYTHONPATH without installing CLI entrypoints, provided the core dependencies already exist. It records command argv, working directory, exit code, stdout and stderr under the chosen output directory. Use a new output directory for a new review so old logs are not overwritten. The records use fixed **synthetic September 14, 2026 timestamps**; they do not grant current production permission.

**Artifact inspection loop:** request/command → capture metadata and bytes → surface locators → rule match → observation and support → collector claim. The next canonical admission step is missing and must not be replaced by manual renaming of fields.

| Journey | User goal | Readiness | Stages |
|---|---|---|---|
'''
for j in journeys:jd+=f"| {j['journey_id']} | {j['title']} | {j['status']} | {j['stages']} |\n"
jd+='\n## Step-by-step journey cards\n\n'
for j in journeys:
 fs=[f['feature_id'] for f in features if j['journey_id'] in f['journeys']]
 issues=[f['id'] for f in findings if j['journey_id'] in f['journeys']]
 jd+=f"### {j['journey_id']} — {j['title']}\n\n**Actor:** {j['actor']}. **Readiness:** {j['status']}. **Stages:** {j['stages']}.\n\n**Features:** {', '.join(fs) or 'Cross-cutting journey'}. **Open findings:** {', '.join(issues) or 'See general implementation boundaries'}.\n\n**Preconditions / inputs:** {j['inputs']}\n\n"
 jd+='\n'.join(f'{i}. {s}' for i,s in enumerate(j['steps'],1))+'\n\n'
 jd+=f"**Outputs to inspect:** {j['outputs']}\n\n**Failure/hold path:** {j['failure_branch']}\n\n"
 if j['invocation']:jd+='**Invocation:**\n\n```bash\n'+j['invocation']+'\n```\n\n'
 else:jd+='**Invocation:** No executable product command/API is implemented for this journey. The steps above are implementation acceptance requirements, not a simulated successful run. Related fixture or local checks are identified separately.\n\n'
 jd+=f"**Acceptance:** {j['acceptance']}\n\n"
jd+='''## Direct commands behind J03

After J01 creates `journey-output/demo-store`, these are the actual collector entrypoints (after editable installation). They are separate processes, not services:

```bash
# Select a technical capture that actually supports an observation.
CAPTURE_ID=$(python -c 'import json; print(json.load(open("journey-output/demo-store/scan-bundle.json"))["observations"][0]["capture_id"])')
ks-module extract --tenant demo --capture-id "$CAPTURE_ID" \
  --store ./journey-output/demo-store --output ./journey-output/page-evidence.json
ks-module match --page ./journey-output/page-evidence.json \
  --rules ./baseline/collector/examples/demo-rules.json \
  --store ./journey-output/demo-store --output ./journey-output/matches.json
ks-module check --bundle ./journey-output/demo-store/scan-bundle.json \
  --store ./journey-output/demo-store --output ./journey-output/checked.json
ks-module resolve --bundle ./journey-output/demo-store/scan-bundle.json \
  --as-of 2026-09-14T12:00:00Z --store ./journey-output/demo-store \
  --output ./journey-output/resolved.json
```

For reference validation, use `(cd baseline/canonical && python validate.py)`. It validates the included bundle; it does not accept a collector bundle or run the missing canonical service.

For the protocol, use `(cd baseline/protocol && python validate_protocol.py)`. Only the shipped example operation/signature is registered. There is no working `ks-program`, `ks-enroll`, `ks-send`, generic `--module KN-02`, or HTTP service command in this package.

## Read-only diagnostics for an existing local store

This inspection does not update attempts or claims:

```bash
python - <<'PYREAD'
from pathlib import Path
import sqlite3,json
path=Path('journey-output/demo-store/scanner.sqlite3').resolve()
with sqlite3.connect(path.as_uri()+'?mode=ro',uri=True) as db:
    db.row_factory=sqlite3.Row
    for row in db.execute('SELECT tenant,run_id,request_key,status,payload FROM attempts ORDER BY rowid'):
        r=dict(row);r['payload']=json.loads(r['payload']);print(json.dumps(r))
PYREAD
```

Local filesystem ownership is trusted. These CLI flags and reads are not authentication or multi-tenant authorization.

## Separate-process acceptance versus service deployment

The evidence here verifies local process invocation with a shared local owner. A service must additionally authenticate callers, resolve scoped immutable records, enforce exact operation/effect signatures, preserve successful/failed target manifests, and publish one consistent payload transactionally. The original service extraction document remains in `baseline/docs/SERVICE_EXTRACTION.md`; this audit adds blockers F03, F11, F12, F13 and F15 to its pre-service gate.
'''
(ROOT/'USER_JOURNEYS.md').write_text(jd)

# Enrich every original stage card rather than replacing the original organization.
stages=json.loads((BASE/'docs/stage_cards.json').read_text())
wf=['# Expanded implementation walkthrough: 27 stages with feature/invocation links','',
 'Original F00–F26 titles, owners, inputs and outputs are preserved from the supplied stage_cards.json. New sections below link user-facing features, callable boundaries and this audit. No missing handler is silently treated as implemented.','']
for s in stages:
 ms=re.findall(r'[A-Z]{2,4}-\d{2}',s['owners'])
 fs=[f for f in features if set(ms)&set(f['modules'])]
 js=sorted({j for f in fs for j in f['journeys']})
 issues=[f for f in findings if set(ms)&set(f['modules'])]
 wf += [f"## F{s['step']} — {s['title']}",'',f"**Owners:** {s['owners']}",'',f"**Original stated inputs:** {s['inputs']}",'',f"**Original stated outputs:** {s['outputs']}",'',f"**Processing:** {s['processing']}",'',f"**Transaction:** {s['transaction']}",'',f"**Failure path:** {s['failure']}",'',f"**Identity:** {s['identity']}",'',f"**Original critique question:** {s['critique_question']}",'',
 '| Feature | Actual readiness in this audit | Invocation / journey |','|---|---|---|']
 for f in fs:wf.append(f"| {f['feature_id']}: {f['title']} | {f['status']} | {f['invocation'] or 'No implementation'}; {', '.join(f['journeys'])} |")
 wf += ['', '**User walkthroughs:** '+', '.join(js)+'. See USER_JOURNEYS.md for steps and outputs.','', '**New issues to address:** '+('; '.join(f['id']+' — '+f['title'] for f in issues) or 'No new reproduced issue for this stage; this is not completeness sign-off.'), '', '**Review decision:** Accept / Change / Defer. Owner: ______. Required test evidence: ______.','']
(ROOT/'UPDATED_STAGE_WALKTHROUGHS.md').write_text('\n'.join(wf))

# Module-level traceability, including all original submodule names.
mods=json.loads((BASE/'product-design/module_catalog.json').read_text())['modules']
mm=['# Submodule, feature, invocation and bug traceability','',
 'The original 39 module IDs, names and submodule names are retained. This view does not turn every function into a network service. Feature status is finer grained than module status.','']
for m in mods:
 fs=[f for f in features if m['module_id'] in f['modules']];issues=[f for f in findings if m['module_id'] in f['modules']]
 mm += [f"## {m['module_id']} — {m['name']}",'', '**Submodules:** '+ '; '.join(m['submodules']), '', '**Original inputs:** '+', '.join(m['input_contracts']), '', '**Original outputs:** '+', '.join(m['output_contracts']), '', '**Feature coverage:** '+ '; '.join(f"{f['feature_id']} ({f['status']})" for f in fs), '', '**Invoke:** '+ '; '.join(sorted({f['invocation'] or 'Proposed: no callable product operation' for f in fs})), '', '**Audit:** '+('; '.join(f['id']+' '+f['title'] for f in issues) or 'No new reproduced bug; implementation gaps remain as shown.'), '']
(ROOT/'SUBMODULE_TRACEABILITY.md').write_text('\n'.join(mm))
