# Implementation dataflows and scanner UML

These are proposed implementation views, not diagrams of a newly deployed runtime. The 75 existing v4.1 contract classes remain in the supplied baseline diagram book; this document focuses on the scanner and integration interfaces to implement next.

## 1. Phase dependencies

```mermaid
flowchart LR
  P0["P0: baseline and thin contracts"] --> P1["P1: first Scrapling collector"]
  P1 --> P2["P2: all 38 commands"]
  P2 --> P3["P3: dynamic rule learning and replay"]
  P3 --> P4["P4: persistent facts and authorization"]
  P4 --> P5["P5: broad approved source suites"]
  P4 --> P6["P6: reasoning and research context"]
  P5 -. "Only required source capabilities gate a feature" .-> P6
  P6 --> P7["P7: reviewed no-send intelligence"]
  P7 --> P8["P8: remote handoff and optional delivery"]
  P8 --> P9["P9: outcomes and operating scale"]
```

## 2. End-to-end dataflow

```mermaid
flowchart TD
  REG["Pinned contracts, command implementations and rule release"] --> PLAN["Direct URLs / target intake and source policy"]
  PLAN --> BUD["Bounded origin/request plan"]
  BUD --> HTTP["Scrapling static request"]
  HTTP -->|Usable response| CAP["Original artifact and attempt"]
  HTTP -->|Permitted render needed| BR["Browser fallback with independent resource caps"]
  BR --> CAP
  HTTP -->|Denied / failed / budget exhausted| DIAG["Attempt diagnostics; no fabricated body"]
  CAP --> EX["All applicable extraction surfaces"]
  EX --> FOLLOW["Bounded same-host discovery/probe loop"]
  FOLLOW --> HTTP
  EX --> IDX["Page and host evidence index with locators"]
  IDX --> MATCH["Typed rule matching"]
  MATCH --> QUAL["Vertical/schema checks and separate priority"]
  QUAL --> OUT["ScanBundle and HostResult/Hit projections"]
  DIAG --> OUT

  IDX --> UNKNOWN["Unknown feature normalization and research queue"]
  UNKNOWN --> REVIEW["Candidate export and reviewed rule proposal"]
  REVIEW --> TEST["Fixtures, mutations, shadow comparison and approval"]
  TEST --> REL["Immutable next rule release"]
  REL --> REPLAY["Replay compatible artifacts or request recapture"]
  REPLAY --> MATCH

  OUT --> ADM["Canonical fact admission and claim resolution"]
  ADM --> SEARCH["Broad knowledge search"]
  ADM --> THINK["Enabled derivations, signals and confounds"]
  EXT["Approved ATS/API/review/registry/publication sources"] --> ADM
  ADM --> PRIORS["Sample-bound product/industry research"]
  PRIORS --> CTX["Explicit internal context join"]
  CTX --> THINK
  THINK --> PACK["Supported templates and exact-revision review"]
  PACK --> USE["Current-use gate and export receipt"]
  USE -->|Separate permission| SEND["Optional delivery and reconciliation"]
  SEND --> OUTCOMES["Deduplicated outcomes and mature measurement"]
```

The feedback arrows are bounded acquisition/review workflows, not same-evaluation recursive fact derivation. A scan pins its release; learned rules enter a later run/replay.

## 3. Scanner interface and record classes

```mermaid
classDiagram
  class ScanRunner {
    run(plan) ScanBundle
    resume(run_id) ScanBundle
  }
  class CommandRegistry {
    validate_profile(profile)
    resolve(command_id, version)
  }
  class CommandSpec {
    command_id
    handler_version
    allowed_scope
    argument_schema
    required_capabilities
    fixture_ids
  }
  class CommandExecution {
    execution_id
    command_id
    input_refs
    output_refs
    status
    reason
    counters
  }
  class ScanPlan {
    intake_id
    tenant_id
    targets
    allowed_origins
    release_lock
    budget_profile
  }
  class PolicyGate {
    authorize(target, purpose)
    reserve_request()
    classify_failure(response)
  }
  class ScraplingTransport {
    static_fetch(request) CaptureResult
    browser_fetch(request) CaptureResult
  }
  class CaptureResult {
    attempt_id
    requested_url
    final_url
    actual_mode
    artifact_refs
    truncation
    limitations
  }
  class ExtractionPipeline {
    extract(capture) PageEvidenceIndex
  }
  class PageEvidenceIndex {
    artifact_id
    surface_refs
    subject_binding_refs
    completeness
  }
  class HostEvidenceIndex {
    scope_id
    run_id
    page_refs
    surface_refs
  }
  class RuleEngine {
    match(index, rule_release)
    qualify(matches, index)
  }
  class FingerprintMatch {
    rule_id
    rule_version
    release_hash
    surface_refs
    locator_refs
    capture_mode
    qualification
    limitations
  }
  class ScanBundle {
    manifest
    attempt_refs
    command_execution_refs
    evidence_refs
    match_refs
    coverage_refs
    result_status
  }
  class FactCandidateAdapter {
    map(bundle) CandidateRecords
  }
  class FactAdmission {
    admit(candidate, policy) Fact
  }

  ScanRunner --> ScanPlan
  ScanRunner --> CommandRegistry
  CommandRegistry o-- CommandSpec
  ScanRunner --> CommandExecution
  ScanRunner --> PolicyGate
  ScanRunner --> ScraplingTransport
  ScraplingTransport --> CaptureResult
  CaptureResult --> ExtractionPipeline
  ExtractionPipeline --> PageEvidenceIndex
  HostEvidenceIndex o-- PageEvidenceIndex
  RuleEngine --> HostEvidenceIndex
  RuleEngine --> FingerprintMatch
  ScanBundle o-- CommandExecution
  ScanBundle o-- CaptureResult
  ScanBundle o-- FingerprintMatch
  ScanRunner --> ScanBundle
  FactCandidateAdapter --> ScanBundle
  FactCandidateAdapter --> FactAdmission
```

`CommandExecution` is an operational record for all 38 actions, including actions which produce no fact. A fact-producing command must also satisfy the normative successful-producer/lineage contract. Most new record types can be composed from existing v4.1 values.

## 4. Dynamic fingerprint sequence

```mermaid
sequenceDiagram
  participant C as Collector
  participant B as Blob and evidence store
  participant R as Approved rule runtime
  participant Q as Candidate research index
  participant H as Reviewer
  participant L as Fingerprint library release CI
  participant A as Fact admission

  C->>B: Persist bounded original capture and provenance
  C->>R: Match pinned approved release
  R->>A: All matched supports and mapped candidates
  C->>Q: Unknown normalized surface observations
  Q->>Q: Deduplicate origins and count eligible sites
  Q->>H: Export bounded candidate evidence
  H->>L: Proposed definition and review
  L->>L: Schema, semantics, fixture, mutation and shadow gates
  alt Approved
    L->>R: Publish immutable release for next run
    R->>B: Request eligible stored evidence for replay
    alt Compatible retained modality and permission
      B-->>R: Exact prior capture
      R->>A: New execution using original observation time
    else Required evidence missing or no longer permitted
      R->>Q: Recapture required or unavailable; no false absence
    end
  else Rejected or incomplete
    L->>Q: Keep candidate/rejection history
  end
```

## 5. Repository dependencies

```mermaid
flowchart LR
  GH[".github: CI / release policy"]
  K["knowledge-contracts: types / validation"]
  F["fingerprint-library: data / fixtures / releases"]
  C["scrapling-ingestion: capture / match / replay"]
  P["signals-platform: facts / reasoning / reviewed handoff"]
  K --> F
  K --> C
  K --> P
  F --> C
  C -->|Library call or ScanBundle| P
  GH -.-> F
  GH -.-> C
  GH -.-> P
```

Code flows from shared contracts toward consumers. There is no runtime dependency from the collector back into the Signals app, and no second authoritative fingerprint registry inside that app.
