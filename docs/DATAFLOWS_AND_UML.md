# Editable E2E dataflows and UML

Rendered offline views are in `DIAGRAM_BOOK.html`. Sequence and class diagrams describe proposed architecture unless a node/class is explicitly marked implemented. Diagrams are not execution test results.

## Entire product lifecycle and valid terminal products

[Rendered SVG](diagrams/01-product-lifecycle.svg)

```mermaid
flowchart TD
    p["Program / offer<br/>GTM-01"]
    s["Account sourcing<br/>GTM-02"]
    i["Subject / scope<br/>KN-01"]
    a["Acquisition<br/>ING / FP / AI"]
    k["Admitted facts + claims<br/>KN-02 / KN-03"]
    r["Research / signals<br/>RE"]
    o["Opportunity + contacts<br/>COM-01 / AUD-01"]
    m["Grounded content + review<br/>COM-02 / COM-03"]
    c["Campaign / enrollment<br/>CAM"]
    g["Current-use / send gates<br/>COM-04"]
    d["Dispatch / reconciliation<br/>COM-05"]
    e["Replies / CRM<br/>ENG-01 / CRM-01"]
    q["Measured outcomes / quality<br/>COM-06 / QA-01"]
    knowledge["Knowledge + diagnostics<br/>valid terminal output"]
    preview["Reviewed no-send export<br/>valid terminal output"]
    p -->|"approved program"| s
    s -->|"seeds"| i
    i -->|"bounded targets"| a
    a -->|"evidence-backed candidates"| k
    k -->|"no opportunity required"| knowledge
    k -->|"pinned resolved inputs"| r
    r -->|"signals + internal context"| o
    o -->|"eligible proof"| m
    m -->|"export gate"| preview
    m -->|"separate campaign approval"| c
    c -->|"due step"| g
    g -->|"fresh permission"| d
    d -->|"verified reply"| e
    e -->|"attributed outcomes"| q
    q -->|"reviewed future revision"| p
```

## Capture, surface completeness, deduplication and atomic publication

[Rendered SVG](diagrams/02-capture-publication.svg)

```mermaid
flowchart TD
    r["Bounded request + attempt"]
    c["Trusted Capture metadata<br/>+ original blob"]
    x["17 extractor results<br/>complete / partial / failed"]
    m["All rule matches<br/>semantic rule digest"]
    o["Observation + support<br/>one captured claim/value"]
    v["Validate full bundle<br/>rederive surfaces / reports / score"]
    t["One SQLite transaction<br/>evaluation + findings + selection"]
    f["Failure diagnostics<br/>no supported publication"]
    re["Replay selected original captures"]
    r -->|"bytes or no-byte failure"| c
    c -->|"verified read"| x
    x -->|"required capabilities"| m
    m -->|"preserve every support"| o
    o -->|"draft outputs"| v
    v -->|"success"| t
    v -->|"reject"| f
    t -->|"recorded selection"| re
    re -->|"new execution; original observation time"| x
```

## Account proof versus product/industry context

[Rendered SVG](diagrams/03-knowledge-context.svg)

```mermaid
flowchart LR
    a["Account direct observations"]
    p["Product / industry reports"]
    ad["Canonical fact admission"]
    pr["Sample + numerator + denominator"]
    cl["Complete account claim group"]
    co["Research prior<br/>subject stays product / industry"]
    join["Declared context join"]
    si["Signal / opportunity evaluation"]
    copy["Eligible factual clauses"]
    a -->|"evidence + bindings"| ad
    p -->|"attributed reports"| ad
    ad -->|"account facts"| cl
    ad -->|"research records"| pr
    pr -->|"sample-bound measurement"| co
    co -->|"prior"| join
    cl -->|"explicit membership/product link"| join
    join -->|"internal context only"| si
    cl -->|"account condition inputs"| si
    cl -->|"outward proof"| copy
    si -->|"approved question/template selection"| copy
```

## Model call: sealed external inputs and run-produced I/O (proposed live path)

[Rendered SVG](diagrams/04-model-execution.svg)

```mermaid
sequenceDiagram
    participant r as Runner
    participant s as Record store
    participant g as Model gateway
    participant p as Provider
    participant a as Fact admission
    r->>s: 1. Seal external artifact/fact manifest
    r->>g: 2. Task + exact input refs + budget
    g->>s: 3. Retain request under producing execution
    g->>p: 4. Authorized bounded invocation
    p->>g: 5. Response or failure
    g->>s: 6. Retain raw response before parse
    g->>g: 7. Validate; bounded repair or terminal abstention
    g->>s: 8. Commit producer status + produced-artifact refs
    g->>a: 9. Typed output with substantive source locators
    a->>s: 10. Admit only successful eligible output
    r->>s: 11. Resolve generated output after producer completion
```

## Historical evaluation, exact review and current-use export

[Rendered SVG](diagrams/05-review-export.svg)

```mermaid
sequenceDiagram
    participant r as Reasoning
    participant k as Knowledge
    participant m as Renderer
    participant h as Reviewer
    participant g as Use gate
    participant e as Exporter
    r->>k: 1. Consume frozen claim/input snapshot
    r->>m: 2. Eligible conditions + template
    m->>k: 3. Check account proof and ancestry
    m->>h: 4. Exact content revision/hash + evidence
    h->>g: 5. Authorized review for exact revision
    g->>k: 6. Query complete CURRENT claims/rights/restrictions
    k->>g: 7. Conflict or current eligible inputs
    g->>e: 8. ALLOW exact destination/payload or BLOCK
    e->>e: 9. Prepare durable idempotent intent
    e->>g: 10. Recheck before external effect
    e->>e: 11. Write receipt / retain uncertainty
```

## Proposed send, uncertain acceptance, reply stop and CRM retry

[Rendered SVG](diagrams/06-send-reply-crm.svg)

```mermaid
sequenceDiagram
    participant c as Enrollment
    participant g as Send gate
    participant s as Dispatcher
    participant p as Provider
    participant i as Reply ingress
    participant crm as CRM sync
    c->>g: 1. Due step + stable business-effect identity
    g->>s: 2. Current permit or HOLD
    s->>p: 3. Exact reviewed message
    p->>s: 4. Ambiguous timeout
    s->>s: 5. Record UNKNOWN; do not blind resend
    s->>p: 6. Reconcile by provider/operation identity
    p->>s: 7. Original acceptance located
    p->>i: 8. Signed/correlated inbound event
    i->>c: 9. Commit immediate contact/enrollment STOP
    i->>crm: 10. Human follow-up / sales handoff
    crm->>crm: 11. Retry CRM write only; never resend
```

## Execution and publication state machine

[Rendered SVG](diagrams/07-execution-state.svg)

```mermaid
flowchart LR
    n["NEW"]
    v["VALIDATING"]
    r["RUNNING"]
    s["STAGED"]
    c["COMMITTED"]
    f["FAILED"]
    x["CANCELLED"]
    k["SKIPPED"]
    n -->|"validate inputs / signature"| v
    v -->|"allowed + dependencies"| r
    v -->|"not enabled / not applicable"| k
    v -->|"bad contract"| f
    r -->|"draft outputs"| s
    s -->|"validate + atomic publish"| c
    s -->|"rollback"| f
    r -->|"error / timeout"| f
    r -->|"cancel before commit"| x
    c -->|"idempotent same-request reuse"| c
```

## Proposed delivery state machine: uncertainty is not retry permission

[Rendered SVG](diagrams/08-delivery-state.svg)

```mermaid
flowchart LR
    p["PREPARED"]
    g["GATED"]
    s["DISPATCHING"]
    a["ACCEPTED"]
    u["UNKNOWN_ACCEPTANCE"]
    r["RECONCILING"]
    f["DEFINITIVE_FAILURE"]
    h["HELD / CANCELLED"]
    p -->|"current checks"| g
    g -->|"restriction / expiry"| h
    g -->|"permitted"| s
    s -->|"receipt"| a
    s -->|"timeout after possible acceptance"| u
    u -->|"provider lookup"| r
    r -->|"original accepted"| a
    r -->|"definitively rejected"| f
    r -->|"cannot resolve; operator hold"| h
    f -->|"new attempt only under same effect policy"| p
```

## Proposed deployment groups (logical until extracted)

[Rendered SVG](diagrams/09-service-deployment.svg)

```mermaid
flowchart LR
    s0["S0 Control and programs<br/>GTM-01, GTM-02, CTL-01, CTL-02, CTL-03"]
    s1["S1 Capture and fingerprints<br/>ING-02, ING-03, ING-04, ING-05, FP-01, FP-02, FP-03"]
    s2["S2 Canonical knowledge<br/>KN-01, KN-02, KN-03, KN-04, PLAT-01, PLAT-02"]
    s3["S3 Enrichment and model tasks<br/>ING-01, AI-01"]
    s4["S4 Research and intelligence<br/>RE-01, RE-02, RE-03, RE-04, RE-05, COM-01, QA-01"]
    s5["S5 Audience and reviewed content<br/>AUD-01, COM-02, COM-03, COM-04"]
    s6["S6 Engagement and sales handoff<br/>CAM-01, CAM-02, COM-05, COM-06, ENG-01, CRM-01"]
    s7["S7 Operator workspace<br/>UX-01, PLAT-03"]
    s0 -->|"authorized capture request"| s1
    s1 -->|"verified ScanBundle admission"| s2
    s0 -->|"approved enrichment/model task"| s3
    s3 -->|"typed outputs + artifacts"| s2
    s2 -->|"immutable input refs / queries"| s4
    s4 -->|"opportunity / context / proof"| s5
    s5 -->|"reviewed exact content"| s6
    s6 -->|"restricted mutations / outcomes"| s2
    s6 -->|"mature measurements"| s4
    s7 -->|"authorized commands"| s0
    s7 -->|"authorized evidence queries"| s2
    s7 -->|"operator actions"| s6
```

## Full class partition 01: AcquisitionAttempt, ActorGrant, Artifact, AttributedStatementValue, BatchRun, CalibrationRecord

[Rendered SVG](diagrams/classes-01.svg)

```mermaid
classDiagram
    class AcquisitionAttempt {
        adapter_version
        artifact_ids
        attempt_id
        body_limit_bytes
        cost_minor
        cost_status
        currency
        execution_mode
        finished_at
        intake_id
        max_requests
        operation_key
        pagination
        request_hash
        requests_made
        scope_id
        source_id
        source_version
        started_at
        status
        target
        tenant_id
        terminal_reason
        timeout_seconds
        truncated
    }
    class ActorGrant {
        active
        actor_id
        fixture_only
        permissions
        tenant_id
    }
    class Artifact {
        artifact_id
        byte_count
        captured_at
        classification
        content_hash
        content_ref
        independence_group
        media_type
        origin_namespace
        origin_record_id
        origin_revision
        parent_artifact_id
        published_at
        resource_uri
        retained_until
        retention_state
        scope_id
        source_id
        status
        tenant_id
        truncated
    }
    class AttributedStatementValue {
        modality
        statement_id
        text
        topic_id
    }
    class BatchRun {
        approval_policy_version
        as_of
        binding_ids
        code_release
        created_at
        imported_execution_ids
        input_artifact_ids
        input_fact_ids
        intake_id
        knowledge_cutoff
        mode
        produced_artifact_ids
        produced_fact_ids
        profile_id
        registry_release
        resolution_ids
        run_id
        sample_ids
        sealed_at
        status
        target_results
        tenant_id
    }
    class CalibrationRecord {
        calibration_id
        evaluation_dataset_id
        false_positives
        fixture_only
        measured_precision
        report_hash
        review_ref
        target_id
        target_version
        true_positives
    }
```

## Full class partition 02: CallEventValue, CandidateRecord, CapabilityProfile, CaseStudyOutcomeValue, ChangeRecord, ClaimResolution

[Rendered SVG](diagrams/classes-02.svg)

```mermaid
classDiagram
    class CallEventValue {
        call_key
        callback_of
        direction
        duration_seconds
        started_at
        status
    }
    class CandidateRecord {
        artifact_id
        attempt_id
        candidate_id
        production_eligible
        proposed_predicate_id
        proposed_value
        reason
        tenant_id
    }
    class CapabilityProfile {
        capture_source_ids
        delivery_enabled
        execute_function_ids
        export_enabled
        fact_predicate_ids
        product_boundary
        production_enabled
        profile_id
        research_context_enabled
        signal_ids
        template_ids
        version
    }
    class CaseStudyOutcomeValue {
        attribution
        baseline_value
        case_id
        comparison_kind
        measurement_window
        method_description
        metric_name
        outcome_id
        publisher
        reported_quote
        reported_value
        sample_size
        source_url
        transfer_to_target_allowed
        unit
    }
    class ChangeRecord {
        actor_id
        change_id
        effective_at
        kind
        reason
        recorded_at
        replacement_id
        target_id
        target_type
        tenant_id
    }
    class ClaimResolution {
        accepted_fact_ids
        as_of
        observation_ids
        policy_version
        predicate_id
        resolution_id
        resolved_at
        run_id
        scope_id
        status
        subject_id
        target
        tenant_id
    }
```

## Full class partition 03: ConfidenceAssessment, ContextAssessment, ContextJoinRule, CoverageCheck, CoverageFamilyPlan, CoverageRecord

[Rendered SVG](diagrams/classes-03.svg)

```mermaid
classDiagram
    class ConfidenceAssessment {
        calibration_id
        meaning
        value
    }
    class ContextAssessment {
        account_subject_id
        company_claim_allowed
        context_fact_ids
        context_id
        context_subject_id
        join_rule_id
        link_fact_id
        purpose
        relationship_strength
        run_id
        status
        tenant_id
    }
    class ContextJoinRule {
        company_claim_allowed
        context_predicate
        join_rule_id
        link_kind
        link_object_path
        link_predicate
        maximum_hops
        purpose
        target_kinds
        version
    }
    class CoverageCheck {
        artifact_id
        resource
        result
    }
    class CoverageFamilyPlan {
        contract_status
        live_adapter_status
        metric_ids
        predicate_ids
        section
        title
    }
    class CoverageRecord {
        attempt_ids
        checked
        checked_at
        coverage_id
        detector_execution_id
        detector_release
        planned_resources
        predicate_ids
        scope_id
        scope_limitations
        source_id
        status
        target
        tenant_id
    }
```

## Full class partition 04: DataAccessPolicy, DestinationDefinition, DiscussionRecordValue, EconomicHypothesisValue, EvidenceLocator, EvidenceSet

[Rendered SVG](diagrams/classes-04.svg)

```mermaid
classDiagram
    class DataAccessPolicy {
        allow_personal_data
        allow_sensitive_data
        approval_ref
        attribution_text
        deletion_cascades
        fixture_only
        max_derived_retention_seconds
        max_raw_retention_seconds
        policy_id
        purposes
        review_status
        reviewed_at
        tenant_ids
        terms_ref
        valid_until
        version
    }
    class DestinationDefinition {
        automatic_sending
        destination_id
        enabled
        fixture_only
        kind
        mapping_version
        tenant_id
    }
    class DiscussionRecordValue {
        community
        language
        post_key
        published_at
        role
        text
        thread_key
    }
    class EconomicHypothesisValue {
        assumptions
        currency
        estimated_amount_minor
        limitations
    }
    class EvidenceLocator {
        artifact_id
        end
        kind
        locator_id
        pointer
        quote
        start
    }
    class EvidenceSet {
        attempt_id
        coverage_id
        directness
        evidence_id
        execution_id
        input_fact_ids
        locator_ids
        sample_ids
        tenant_id
    }
```

## Full class partition 05: ExecutionRecord, ExportReceipt, Exposure, ExternalIdentifier, Fact, FactRequirement

[Rendered SVG](diagrams/classes-05.svg)

```mermaid
classDiagram
    class ExecutionRecord {
        execution_id
        finished_at
        function_id
        function_version
        input_artifact_ids
        input_fact_ids
        input_sample_ids
        input_set_hash
        model_call_id
        output_artifact_ids
        output_fact_ids
        parameters
        run_id
        sample_set_hash
        started_at
        status
        subject_id
        tenant_id
        terminal_reason
    }
    class ExportReceipt {
        actor_id
        automatic_sending
        completed_at
        destination_id
        export_id
        external_reference
        gate_id
        idempotency_key
        mapping_version
        package
        payload_hash
        payload_ref
        recipient_key
        requested_at
        status
        tenant_id
    }
    class Exposure {
        accepted_at
        business_send_key
        exposure_id
        package_id
        provider_message_id
        recipient_key
        status
        tenant_id
    }
    class ExternalIdentifier {
        namespace
        value
    }
    class Fact {
        binding_id
        confidence
        effective_at
        evidence_id
        execution_id
        expires_at
        fact_id
        nature
        object
        observed_at
        predicate_id
        reason
        recorded_at
        run_id
        schema_version
        scope_id
        source_id
        state
        subject_id
        supersedes_fact_id
        target
        tenant_id
        window
    }
    class FactRequirement {
        allowed_natures
        counting_unit
        minimum
        predicate_id
        state
    }
```

## Full class partition 06: FingerprintDefinition, FunctionDefinition, GroundedClause, HypothesisValue, IntakeRequest, IntakeTarget

[Rendered SVG](diagrams/classes-06.svg)

```mermaid
classDiagram
    class FingerprintDefinition {
        authority
        calibration_ref
        capture_mode
        emits
        fingerprint_id
        fixture_only
        implementation_status
        match_value
        negative_fixtures
        operator
        positive_fixtures
        product_subject_id
        version
    }
    class FunctionDefinition {
        authority
        cross_subject_rule
        detector_contract
        entrypoint
        fixture_only
        function_id
        implementation_status
        input_predicates
        output_predicates
        parameter_schema
        processor
        version
    }
    class GroundedClause {
        clause_id
        evidence_roles
        fact_ids
        template_id
        text
    }
    class HypothesisValue {
        alternatives
        conclusion
        hypothesis_id
        limitations
        verification_question
    }
    class IntakeRequest {
        idempotency_key
        intake_id
        profile_id
        purpose
        received_at
        request_hash
        requester_id
        targets
        tenant_id
    }
    class IntakeTarget {
        resource_uri
        subject_id
    }
```

## Full class partition 07: JobPostingValue, LookalikeMatch, MeasurementValue, MetricDefinition, ModelCall, ObjectReferenceRule

[Rendered SVG](diagrams/classes-07.svg)

```mermaid
classDiagram
    class JobPostingValue {
        department
        employment_type
        namespace
        posting_id
        published_at
        title
        url
    }
    class LookalikeMatch {
        comparison_subject_id
        corpus_release
        differences
        implementation_status
        index_version
        input_fact_ids
        match_id
        missing_features
        outcome_transfer_allowed
        representation_version
        run_id
        similarity_score
        target_subject_id
        tenant_id
        use
    }
    class MeasurementValue {
        denominator
        dimensions
        method_version
        metric_id
        numerator
        reporting_timezone
        sample_size
        uncertainty
        unit
        value
    }
    class MetricDefinition {
        aggregation
        allowed_natures
        description
        dimensions_schema
        metric_id
        requires_denominator
        section_ids
        subject_kinds
        unit
        value_schema
    }
    class ModelCall {
        call_id
        input_artifact_ids
        max_repair_attempts
        model
        output_schema_id
        policy_ids
        prompt_hash
        provider
        request_artifact_id
        response_artifact_id
        status
        task_version
        tenant_id
        terminal_reason
    }
    class ObjectReferenceRule {
        container
        path
        subject_kinds
        target_type
    }
```

## Full class partition 08: OutcomeEvent, OutreachPackage, PackageReference, PredicateDefinition, ProviderBlueprint, PublishedRecordValue

[Rendered SVG](diagrams/classes-08.svg)

```mermaid
classDiagram
    class OutcomeEvent {
        attribution_status
        event_id
        evidence_id
        exposure_id
        kind
        occurred_at
        provider
        provider_event_id
        received_at
        tenant_id
    }
    class OutreachPackage {
        approved_at
        clauses
        context_ids
        maturity_fact_id
        package_id
        rendered_text
        review_id
        revision
        run_id
        send_allowed
        signal_ids
        status
        subject_id
        template_id
        tenant_id
    }
    class PackageReference {
        content_hash
        package_id
        revision
    }
    class PredicateDefinition {
        absence_allowed
        allowed_natures
        allowed_processors
        copy_policy
        description
        example_target
        example_value
        family
        origin
        predicate_id
        reference_rules
        section_ids
        subject_kinds
        target_schema
        temporal_mode
        value_class
        value_schema
        version
    }
    class ProviderBlueprint {
        adapter_implemented
        approval_required
        blueprint_id
        families
        methods
        notes
        provider
        section_ids
        terms_url
    }
    class PublishedRecordValue {
        namespace
        published_at
        publisher
        record_id
        record_type
        text
        title
        url
    }
```

## Full class partition 09: QuotedTextResult, RegistryRecordValue, RepairAttempt, ResearchPriorValue, ResearchSample, ResearchSupportPolicy

[Rendered SVG](diagrams/classes-09.svg)

```mermaid
classDiagram
    class QuotedTextResult {
        text
    }
    class RegistryRecordValue {
        effective_at
        filed_at
        issuer
        jurisdiction
        namespace
        record_id
        record_status
    }
    class RepairAttempt {
        attempt_id
        call_id
        input_response_artifact_id
        method
        ordinal
        output_response_artifact_id
        status
        validation_errors
    }
    class ResearchPriorValue {
        classified_eligible_count
        contradicting_fact_ids
        denominator_definition
        eligible_count
        population_claim
        sample_id
        sample_share
        support_count
        support_policy_id
        supporting_fact_ids
        theme_id
        unclassified_count
    }
    class ResearchSample {
        complete_population
        created_at
        dedupe_policy_version
        eligible_artifact_ids
        excluded_artifact_ids
        limitations
        policy_ids
        population_size
        record_decisions
        retrieved_artifact_ids
        sample_id
        sampling_frame
        scope_id
        selection_method
        subject_id
        support_policy_id
        tenant_id
        theme_id
        window
    }
    class ResearchSupportPolicy {
        allowed_sentiments
        allowed_stances
        counting_unit
        denominator_rule
        meaning
        support_policy_id
        unclassified_policy
        version
    }
```

## Full class partition 10: ReviewDecision, ReviewRecordValue, SalaryValue, SampleRecordDecision, ScenarioEstimate, Scope

[Rendered SVG](diagrams/classes-10.svg)

```mermaid
classDiagram
    class ReviewDecision {
        action
        decided_at
        package
        policy_version
        reason
        review_id
        reviewer_id
        tenant_id
    }
    class ReviewRecordValue {
        edited
        language
        platform
        published_at
        rating
        rating_scale_max
        review_key
        text
    }
    class SalaryValue {
        basis
        currency
        maximum_minor
        minimum_minor
        minor_unit_exponent
        period
    }
    class SampleRecordDecision {
        artifact_id
        classification_fact_ids
        reason
        status
    }
    class ScenarioEstimate {
        assumptions
        currency
        formula_version
        implementation_status
        limitations
        lower_minor
        observed_input_fact_ids
        scenario_id
        subject_id
        tenant_id
        time_period
        upper_minor
        verified_loss
    }
    class Scope {
        capture_mode
        kind
        population_description
        resources
        scope_id
        stable_scope_key
        subject_id
        tenant_id
    }
```

## Full class partition 11: SignalDefinition, SignalEvaluation, SourceDefinition, Subject, SubjectBinding, SurfaceObservationValue

[Rendered SVG](diagrams/classes-11.svg)

```mermaid
classDiagram
    class SignalDefinition {
        context_allowed
        description
        function_id
        required_facts
        signal_type_id
        status
        version
    }
    class SignalEvaluation {
        context_ids
        evaluated_at
        input_fact_ids
        reason
        run_id
        signal_id
        signal_type_id
        status
        subject_id
        tenant_id
    }
    class SourceDefinition {
        acquisition_method
        adapter_status
        allowed_natures
        authority
        emits
        fixture_only
        freshness_seconds
        policy_id
        provider
        source_id
        upstream_namespace
        version
    }
    class Subject {
        display_name
        external_ids
        kind
        subject_id
        tenant_id
    }
    class SubjectBinding {
        artifact_ids
        binding_id
        decided_at
        evidence_locator_ids
        method
        role
        scope_id
        status
        subject_id
        tenant_id
    }
    class SurfaceObservationValue {
        observed_value
        surface_key
    }
```

## Full class partition 12: TargetResult, TaxonomyTerm, TechnologyReportValue, TechnologyValue, TemplateDefinition, ThemeClassificationValue

[Rendered SVG](diagrams/classes-12.svg)

```mermaid
classDiagram
    class TargetResult {
        completed_at
        reason
        status
        subject_id
    }
    class TaxonomyTerm {
        label
        parent_id
        scheme_id
        scheme_version
        term_id
    }
    class TechnologyReportValue {
        product_id
        provider
        provider_detected_at
        reported_version
    }
    class TechnologyValue {
        deployment_claim
        fingerprint_id
        matched_value
        product_id
        surface
        version
    }
    class TemplateDefinition {
        allowed_natures
        authority
        maturity_required
        mode
        offered_rung
        question
        renderer
        required_predicate
        review_ref
        template_id
        version
    }
    class ThemeClassificationValue {
        record_key
        sentiment
        stance
        support_locator_ids
        theme_id
    }
```

## Full class partition 13: TimeWindow, UseGateDecision, UseRestriction, ProgramDefinition, AudienceDefinition, OfferDefinition

[Rendered SVG](diagrams/classes-13.svg)

```mermaid
classDiagram
    class TimeWindow {
        end
        start
    }
    class UseGateDecision {
        actor_id
        decision
        destination_id
        evaluated_at
        gate_id
        package
        purpose
        reasons
        recipient_key
        review_id
        tenant_id
        valid_until
        version_vector
    }
    class UseRestriction {
        actor_id
        effective_at
        kind
        reason
        recipient_key
        released_at
        released_by
        restriction_id
        subject_id
        tenant_id
    }
    class ProgramDefinition {
        program_id
        tenant_id
        revision
        objectives
        audience_ref
        offer_refs
        capability_profile_ref
        acquisition_limits
        outreach_policy_ref
        owner
        approval_state
    }
    class AudienceDefinition {
        audience_id
        revision
        account_filters
        permitted_geographies
        excluded_segments
        membership_as_of_policy
        selection_reason_codes
    }
    class OfferDefinition {
        offer_id
        revision
        service_line
        supported_problem_classes
        prerequisites
        allowed_template_refs
        persona_rules
        restrictions
    }
```

## Full class partition 14: AccountSeed, LeadSelection, ResearchPlan, ContactProfile, ContactAssessment, MessageArtifact

[Rendered SVG](diagrams/classes-14.svg)

```mermaid
classDiagram
    class AccountSeed {
        seed_id
        tenant_id
        program_id
        discovery_source_ref
        original_record_ref
        resource_uri
        provisional_external_ids
        discovered_at
        normalization_decision
    }
    class LeadSelection {
        selection_id
        program_id
        account_ref
        input_snapshot_ref
        fit_decision
        reasons
        exclusion_state_refs
        selected_at
    }
    class ResearchPlan {
        plan_id
        account_ref
        intended_predicates
        existing_coverage_refs
        permitted_source_refs
        acquisition_limits
        priority_reasons
        stopping_rules
    }
    class ContactProfile {
        contact_profile_id
        tenant_id
        person_subject_ref
        account_relationship_ref
        endpoint_refs
        source_evidence_refs
        role_effective_window
        verified_at
        retention_policy_ref
    }
    class ContactAssessment {
        assessment_id
        contact_profile_ref
        opportunity_ref
        role_fit
        employer_binding_status
        endpoint_verification
        source_use_state
        restrictions_refs
        checked_at
        reasons
    }
    class MessageArtifact {
        message_id
        revision
        package_ref
        channel
        subject_or_title
        body_ref
        required_footer_ref
        rendered_content_digest
        renderer_version
        permitted_transformations
    }
```

## Full class partition 15: CampaignDefinition, CampaignApproval, CampaignReadiness, Enrollment, StepEligibility, DeliveryIntent

[Rendered SVG](diagrams/classes-15.svg)

```mermaid
classDiagram
    class CampaignDefinition {
        campaign_id
        revision
        program_ref
        route_ref
        ordered_step_definitions
        template_refs
        schedule_owner
        send_window_policy
        timezone_policy
        sender_constraints
        stop_policy
        frequency_caps
    }
    class CampaignApproval {
        approval_id
        campaign_id
        revision
        definition_hash
        authorized_actor
        allowed_mode
        approved_at
        policy_ref
    }
    class CampaignReadiness {
        readiness_id
        campaign_ref
        sender_snapshot_refs
        provider_state_refs
        compatibility_checks
        checked_at
        decision
        reasons
    }
    class Enrollment {
        enrollment_id
        tenant_id
        campaign_ref
        account_ref
        contact_ref
        enrollment_policy_ref
        state
        next_step_id
        state_revision
        enrolled_at
        last_event_ref
    }
    class StepEligibility {
        eligibility_id
        enrollment_ref
        step_id
        due_at
        timezone_basis
        package_ref
        contact_assessment_ref
        cap_reservation_ref
        state_revision
        decision
        reasons
    }
    class DeliveryIntent {
        intent_id
        tenant_id
        enrollment_ref
        step_id
        recipient_binding_ref
        channel
        reviewed_message_ref
        logical_effect_key
        execution_owner
    }
```

## Full class partition 16: SendGateDecision, SenderCapabilitySnapshot, DeliveryAttempt, Conversation, ReplyAssessment, EnrollmentControl

[Rendered SVG](diagrams/classes-16.svg)

```mermaid
classDiagram
    class SendGateDecision {
        gate_id
        intent_ref
        message_ref
        review_ref
        campaign_approval_ref
        readiness_ref
        recipient_ref
        current_restriction_vector
        current_contact_vector
        evaluated_at
        valid_until
        decision
        reasons
    }
    class SenderCapabilitySnapshot {
        snapshot_id
        tenant_id
        sender_account_ref
        provider
        channel
        verified_capabilities
        live_state
        checked_at
        configuration_digest
    }
    class DeliveryAttempt {
        attempt_id
        intent_ref
        gate_ref
        request_digest
        started_at
        finished_at
        transport_status
        acceptance_status
        external_message_ref
        error_ref
    }
    class Conversation {
        conversation_id
        tenant_id
        account_ref
        contact_refs
        provider_account_ref
        external_thread_ref
        event_refs
        enrollment_links
        current_owner
        state
    }
    class ReplyAssessment {
        assessment_id
        inbound_event_ref
        classification_kind
        literal_support_refs
        producer_execution_ref
        confidence_metadata
        human_review_state
        recommended_action
    }
    class EnrollmentControl {
        control_id
        target_enrollment_refs
        cause_event_ref
        desired_transition
        scope
        created_at
        expected_state_refs
    }
```

## Full class partition 17: FollowUpTask, SalesHandoff, CRMMapping, CRMAccountView, CRMSyncIntent, CRMSyncReceipt

[Rendered SVG](diagrams/classes-17.svg)

```mermaid
classDiagram
    class FollowUpTask {
        task_id
        conversation_ref
        assigned_owner
        task_kind
        due_at
        source_event_ref
        state
        authorization_requirements
    }
    class SalesHandoff {
        handoff_id
        account_ref
        contact_ref
        conversation_ref
        exposure_refs
        qualification_notes_refs
        intended_owner
        meeting_or_next_action
        created_at
    }
    class CRMMapping {
        mapping_id
        provider
        schema_version
        field_ownership
        inbound_outbound_transforms
        idempotency_policy
        suppression_rules
        loop_prevention
    }
    class CRMAccountView {
        view_id
        account_ref
        external_record_links
        owner
        lifecycle_stage
        customer_or_open_deal_state
        restriction_observations
        provider_version
        fetched_at
    }
    class CRMSyncIntent {
        sync_id
        tenant_id
        mapping_ref
        entity_link
        desired_fields
        source_record_refs
        expected_remote_version
        idempotency_key
    }
    class CRMSyncReceipt {
        receipt_id
        sync_intent_ref
        external_record_ref
        payload_hash
        status
        provider_version
        confirmed_at
        reconciliation_ref
    }
```

## Full class partition 18: ExperimentDefinition, ExperimentAssignment, QualityAssessment, PromotionProposal, WorkspaceView, Common

[Rendered SVG](diagrams/classes-18.svg)

```mermaid
classDiagram
    class ExperimentDefinition {
        experiment_id
        hypothesis
        eligible_population
        randomization_or_observational_design
        treatment_refs
        holdout_policy
        outcome_definition
        maturity_window
        stopping_rule
    }
    class ExperimentAssignment {
        assignment_id
        experiment_ref
        unit_ref
        assigned_variant
        assignment_rule_version
        assigned_at
        exposure_links
    }
    class QualityAssessment {
        assessment_id
        evaluated_release_refs
        gold_set_ref
        eligible_sample
        observed_metrics
        errors
        uncertainty
        limitations
    }
    class PromotionProposal {
        proposal_id
        target_definition_ref
        assessed_release_ref
        quality_assessment_refs
        intended_change
        reasons
        review_requirements
    }
    class WorkspaceView {
        view_id
        tenant_id
        view_kind
        permitted_record_refs
        as_of
        redaction_policy_ref
        completeness_notes
    }
    class Common {
    }
```

## Full class partition 19: Diagnostic, ModuleRequest, ModuleResult, CollectorCapture, CollectorSurface, CollectorCommandResult

[Rendered SVG](diagrams/classes-19.svg)

```mermaid
classDiagram
    class Diagnostic {
        cause_execution_id
        code
        diagnostic_id
        field_path
        message
        record_refs
        restricted_details_ref
        severity
        suggested_action
    }
    class ModuleRequest {
        attempt
        budget_reservation_ref
        context
        deadline_at
        execution_id
        idempotency_key
        input_refs
        module_id
        operation
        parameters_ref
        protocol_version
        release_lock_ref
        request_id
        trace
    }
    class ModuleResult {
        consumed_refs
        context
        diagnostic_record_refs
        diagnostics
        execution_id
        execution_status
        finished_at
        module_id
        operation
        output_refs
        protocol_version
        request_digest
        request_id
        reused_execution_id
        started_at
        trace
        usage
    }
    class CollectorCapture {
        capture_id
        tenant_id
        subject_id
        run_id
        url
        observed_at
        mode
        status_code
        body_sha256
        body_path
        headers
        complete
        source_id
        limitations
        source_ttl_seconds
    }
    class CollectorSurface {
        surface_id
        capture_id
        command_id
        kind
        locator
        value
        context
        attributes
    }
    class CollectorCommandResult {
        command_id
        status
        input_ids
        output_ids
        limitations
        details
    }
```

## Full class partition 20: CollectorPageEvidence, CollectorMatch, CollectorObservation, CollectorSupportLink, CollectorClaimView

[Rendered SVG](diagrams/classes-20.svg)

```mermaid
classDiagram
    class CollectorPageEvidence {
        capture
        surfaces
        commands
    }
    class CollectorMatch {
        match_id
        rule_id
        rule_digest
        release_digest
        authority
        capture_id
        surface_id
        branch
        predicate
        product_id
        object_value
        evidence_key
        rule_evidence_key
        authored_confidence
    }
    class CollectorObservation {
        observation_id
        claim_key
        tenant_id
        subject_id
        predicate
        target
        scope_id
        nature
        state
        object_value
        capture_id
        source_id
        source_group
        observed_at
        expires_at
    }
    class CollectorSupportLink {
        observation_id
        match_id
    }
    class CollectorClaimView {
        claim_key
        predicate
        target
        status
        object_value
        observation_ids
        supporting_match_ids
        eligible_match_ids
        rule_ids
        capture_count
        source_group_count
        evidence_count
        confidence
        confidence_policy
    }
```

## UML association overview (identifiers resolve through explicit owners)

[Rendered SVG](diagrams/10-core-associations.svg)

```mermaid
classDiagram
    CollectorCapture "1" --> "many" CollectorSurface : extracts
    CollectorSurface "1" --> "many" CollectorMatch : supports
    CollectorObservation "1" --> "many" CollectorSupportLink : retains
    CollectorSupportLink --> CollectorMatch : references
    CollectorObservation ..> Fact : admission adapter required
    Fact --> Subject : attributed to
    Fact --> EvidenceSet : supported by
    EvidenceSet --> ExecutionRecord : derived producer
    ExecutionRecord --> BatchRun : pinned under
    ClaimResolution --> Fact : complete claim group
    ResearchSample --> EvidenceSet : full sample lineage
    ContextAssessment --> ResearchSample : contextual prior
    SignalEvaluation --> ClaimResolution : resolved proof
    SignalEvaluation --> ContextAssessment : internal context
    OutreachPackage --> SignalEvaluation : eligible condition
    OutreachPackage --> Fact : grounded clauses
    ReviewDecision --> OutreachPackage : exact revision hash
    UseGateDecision --> ReviewDecision : current permission
    ExportReceipt --> UseGateDecision : authorized handoff
```

## Implemented software classes and callable boundaries

[Rendered SVG](diagrams/11-implemented-software.svg)

```mermaid
classDiagram
    class Scanner {
        +scan(url, config) ScanBundle
        +evaluate(pages, evaluation_id, as_of) ScanBundle
        +replay(tenant, capture_run_id, evaluation_id, as_of) ScanBundle
    }
    class Store {
        +body(capture) bytes
        +publish_evaluation(data, pages, matches, observations, links)
        +stored_claims(tenant, as_of) ClaimView[]
        +replay_eligible(capture) bool
    }
    class RulePack {
        +compile(data) RulePack
        +load(path) RulePack
    }
    class Transport {
        <<interface>>
        +get(url) FetchResult
    }
    class ScraplingTransport {
        +get(url) FetchResult
    }
    class FixtureTransport {
        +get(url) FetchResult
    }
    Scanner --> Store : reads and publishes
    Scanner --> RulePack : pins
    Scanner --> Transport : invokes
    ScraplingTransport ..|> Transport
    FixtureTransport ..|> Transport
```
