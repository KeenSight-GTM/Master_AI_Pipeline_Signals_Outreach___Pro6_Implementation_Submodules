# KeenSight end-to-end closure — dataflows and UML

Proposed additions to v4, September 14, 2026. These diagrams accompany `KeenSight_End_to_End_Completion_Spec.md`. They show **proposed contracts**, not new implemented services or an updated validated v4 schema set. Mermaid source is supplied; these new diagrams have not been rendered or CLI-validated in this review. The original 58-class v4 diagrams remain in the baseline archive.

## 1. Complete product flow, with independently useful knowledge ingestion

```mermaid
flowchart TD
    I["Intake: accounts, locations, products, industries, resources"] --> L["Validate profile and resolve targets"]
    L --> P["Plan approved bounded acquisition"]
    P --> A["Attempt capture or authorized import"]
    A -->|"No bytes, denied or failed"| FAIL["Attempt diagnostic; unknown result"]
    A -->|"Permitted bytes"| E["Retained artifacts and coverage evidence"]
    E --> X["Parse, extract, bind and validate"]
    X -->|"Unresolved or invalid"| Q["Candidate and binding review"]
    Q -->|"Corrected in a new operation"| X
    X --> F["Broad fact store and queryable evidence"]
    F --> K["Knowledge report: facts, failures, limitations"]
    F --> R["Pinned input sets and claim resolution"]
    R --> D["Eligible selectors, derivations and research priors"]
    D --> C["Explicit eligible product/industry context"]
    D --> S["Business-rule verdicts"]
    C -->|"Internal context only"| S
    S --> O["Reviewed opportunity and template mapping"]
    R -->|"Eligible account claim support"| T["Whole-message grounded rendering"]
    O --> T
    T --> V["Machine validation and human review"]
    V --> G["Current-use gate for exact revision/destination"]
    G -->|"Allow"| H["Export intent and receipt"]
    G -->|"Block"| W["Withheld or historical output"]
    H -.->|"Only with delivery profile enabled"| SEND["Send and reconcile acceptance"]
    SEND --> EVENT["Deduplicate and attribute outcomes"]
    EVENT --> STATS["Mature descriptive performance"]
    STATS -.->|"Later evaluation only"| R
    CHANGE["Rights, DNC, retractions, bindings, expiry, deletion"] --> G
    CHANGE -->|"Conservative reevaluation"| R
```

All roots remain reusable even when no signal/template is enabled. Research context is not an account fact. The knowledge path and the handoff path have separate completion conditions.

## 2. Operational contract additions around existing classes

```mermaid
classDiagram
    class IntakeRequest {
        +id intake_id
        +id tenant_id
        +PrincipalRef requested_by
        +VersionRef profile_ref
        +TargetRef[] targets
        +string input_origin
        +string[] requested_purposes
        +hash request_hash
        +string idempotency_key
        +datetime submitted_at
        +IntakeStatus status
    }
    class AcquisitionAttempt {
        +id attempt_id
        +id tenant_id
        +id intake_id
        +TargetRef target_ref
        +VersionRef source_release
        +VersionRef adapter_release
        +hash request_hash
        +string operation_key
        +PolicyDecisionRef policy_decision_ref
        +AttemptStatus status
        +id[] artifact_ids
        +datetime started_at
        +datetime finished_at
        +PaginationState pagination_state
        +string terminal_reason
        +CostRecord cost
    }
    class BatchRun {
        <<existing extended>>
        +id run_id
        +id target_evaluation_id
        +datetime as_of
        +datetime knowledge_cutoff
        +datetime sealed_at
        +VersionRef[] pinned_releases
        +RecordRef[] pinned_inputs
        +TargetStatus status
        +hash result_hash
    }
    class Artifact {
        <<existing>>
    }
    class EvidenceSet {
        <<existing extended>>
        +AttemptRef operational_attempt_ref
        +RecordRef[] full_dependency_refs
    }
    class ExecutionRecord {
        <<existing extended>>
        +ExecutionStatus status
        +RecordRef[] exact_inputs
        +RecordRef[] exact_outputs
        +string terminal_reason
    }
    class ReviewDecision {
        +id review_id
        +id tenant_id
        +PrincipalRef reviewer_id
        +TypedTargetRef target_ref
        +hash target_hash
        +ReviewAction action
        +string reason
        +datetime decided_at
        +VersionRef policy_version
    }
    class UseGateDecision {
        +id gate_id
        +id tenant_id
        +PackageRef package_ref
        +hash content_hash
        +Purpose purpose
        +DestinationRef destination_ref
        +RecipientRef recipient_ref
        +datetime evaluated_at
        +datetime valid_until
        +VersionVector current_versions
        +GateDecision decision
        +string[] reasons
    }
    class ExportReceipt {
        +id export_id
        +id tenant_id
        +PackageRef package_ref
        +DestinationRef destination_ref
        +VersionRef mapping_version
        +hash payload_hash
        +id gate_id
        +string idempotency_key
        +ExportStatus status
        +string external_reference
    }
    class OutreachPackage {
        <<existing extended>>
        +id package_id
        +int revision
        +hash content_hash
        +id review_id
        +id target_evaluation_id
    }
    IntakeRequest "1" --> "0..*" AcquisitionAttempt : plans
    AcquisitionAttempt "1" --> "0..*" Artifact : optionally_captures
    EvidenceSet "0..*" --> "0..1" AcquisitionAttempt : diagnostic_only
    EvidenceSet "0..*" --> "0..*" Artifact : actual_evidence
    BatchRun "1" --> "0..*" ExecutionRecord : executes
    BatchRun "1" --> "0..*" EvidenceSet : pins
    BatchRun "1" --> "0..*" OutreachPackage : produces
    ReviewDecision "0..*" --> "1" OutreachPackage : binds_exact_revision
    UseGateDecision "0..*" --> "1" OutreachPackage : gates_current_use
    UseGateDecision "0..*" --> "0..1" ReviewDecision : requires_for_handoff
    ExportReceipt "0..*" --> "1" UseGateDecision : authorized_by
    ExportReceipt "0..*" --> "1" OutreachPackage : exports_exact_revision
```

`TargetRef`, `PrincipalRef`, `PackageRef`, `CostRecord` and similar items above are typed value objects/identifiers to be encoded with the schema delta. They are not implemented new classes in the baseline. Successful evidence and operational failure references deliberately have different roles.

## 3. Failure-safe acquisition to reviewed export sequence

```mermaid
sequenceDiagram
    actor User as Authorized operator
    participant B as BatchRunner
    participant A as AcquisitionService
    participant X as Extraction and admission
    participant R as FactRepository
    participant C as Claim and rule evaluation
    participant V as Review and use gate
    participant D as Export destination

    User->>B: Submit targets and enabled profile
    B->>B: Link implementations and validate dependency closure
    B->>A: Execute approved bounded acquisition plan
    alt Denied, timeout, or no retained bytes
        A->>R: Persist diagnostic AcquisitionAttempt
        B->>R: Complete target report with unknown/failed stage
    else Retained evidence available
        A->>R: Persist artifacts and attempt/coverage references
        B->>X: Extract, attribute, validate
        X->>R: Append admitted facts or quarantine candidates
        B->>R: Seal exact target input set
        B->>C: Resolve claims and run enabled computations
        alt Conflict, failed producer, or insufficient inputs
            C->>R: Record unknown/error; do not publish approved copy
        else Supported opportunity
            C->>R: Commit completed target result and draft revision
            User->>V: Review exact content hash
            V->>R: Record ReviewDecision
            B->>V: Recheck current use and destination
            alt Current rights/restrictions block
                V->>R: Record blocked UseGateDecision
            else Current use allowed
                V->>R: Commit export intent and applicable gate
                B->>D: Handoff stable export identity
                alt Confirmed
                    D-->>B: Destination reference
                    B->>R: Confirm ExportReceipt
                else Acceptance uncertain
                    B->>R: Mark export UNKNOWN
                    B->>D: Reconcile before any retry
                end
            end
        end
    end
```

## 4. Research prior dependency closure

```mermaid
flowchart LR
    M["Sample frame, window, selection and dedup policy"] --> P["Versioned prior computation"]
    N["Supporting records and classifications"] --> P
    D["All denominator records and eligibility results"] --> P
    E["Exclusions, unknowns and contradictions"] --> P
    V["Explicit stance/sentiment support policy"] --> P
    P --> PRIOR["Descriptive product or industry prior"]
    PRIOR --> JOIN["Explicit eligible account link"]
    JOIN --> CONTEXT["Internal ContextAssessment"]
    CURRENT["Current rights, retention, revocations"] --> PRIOR
    CURRENT --> CONTEXT
    CONTEXT --> QUESTION["Investigation/question selection"]
    FACT["Eligible account-specific fact"] --> COPY["Outward factual clause"]
    QUESTION --> COPY
```

A numerator-only provenance graph is insufficient. Deleting a denominator record can change the statistic and therefore its eligibility. An abstained context is visible only as an audit result.

## 5. Separate computation, review and action state

```mermaid
stateDiagram-v2
    [*] --> Collected
    Collected --> Quarantined: invalid or ambiguous
    Collected --> Admitted: validated evidence and attribution
    Admitted --> Evaluated: sealed inputs and completed producer
    Evaluated --> NoOpportunity: NO_MATCH or UNKNOWN or ERROR
    Evaluated --> Draft: supported opportunity
    Draft --> Rejected: review rejects
    Draft --> Reviewed: machine checks and authorized review
    Reviewed --> Blocked: current restrictions or evidence loss
    Reviewed --> ExportPrepared: current-use gate allows exact revision
    ExportPrepared --> ExportConfirmed: destination confirms
    ExportPrepared --> ExportUnknown: acceptance uncertain
    ExportUnknown --> ExportConfirmed: reconciliation confirms
    ExportUnknown --> ExportPrepared: reconciliation proves no prior acceptance
    ExportConfirmed --> [*]
    Blocked --> Draft: new evidence or revised content, new evaluation
```

Delivery is outside this core state diagram. Enabling it adds its own PENDING/DISPATCHING/ACCEPTED/UNKNOWN_DELIVERY/FAILED/CANCELLED intent states and a separately enforced gate. An exported preview does not itself grant permission to send.
