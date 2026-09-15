# Dataflows, UML and complete class reference

All 75 exported contract/value-object classes appear exactly once in the full class partitions. 22 proposed code interfaces are separate. 
Primitive and object payloads are selected by the PredicateDefinition registry: 213 predicates do not require 213 classes or database tables. Payload-family boxes show reusable shapes; individual predicate schemas remain normative.
Association labels denote logical references, not separate services. `..>` is a dependency; `o--` aggregation; `*--` composition. Method bodies on proposed interfaces are not implemented runtime code.
SVGs were rendered locally with Graphviz from the same model as the Mermaid class/flow sources. The state view is rendered through Graphviz; the sequence view uses a local SVG renderer over its message declarations. Mermaid CLI parsing was not run.

## Broad facts, verified handoffs and reviewed local export

```mermaid
flowchart TB
  A["Broad catalog: 11 areas plus 52 ledger placements"]
  T["Intake: known or provisional target and purpose"]
  B["Enabled callable closure and source policy"]
  C["Bounded acquisition attempt: import or live capture"]
  D["Retained artifacts and acquisition completion"]
  Z["Zero-byte failure: attempt-backed UNKNOWN"]
  E["Extraction and scoped detector execution"]
  F["Successful producer, required coverage, lineage and binding admission"]
  Q["Quarantined or rejected candidates"]
  G["Reusable fact store"]
  H["Pinned target inputs and claim resolutions"]
  I["Successful enabled derivations"]
  J["Complete research sample: support, unclassified and exclusions"]
  K["Usable explicit context join"]
  L["Signal requirements over resolved claims"]
  M["Evidence-bound template"]
  N["Completed preview package"]
  R["Authorized review of exact revision and hash"]
  U["Fresh purpose and destination gate"]
  O["Idempotent LOCAL PREVIEW export and receipt"]
  P["Live delivery disabled"]
  A -->|"definitions not automatic activation"| B
  T --> B
  B -->|"authorized capability"| C
  C -->|"capture or import succeeds"| D
  C -->|"no bytes; no business absence"| Z
  D --> E
  E --> F
  F -->|"invalid / failed / ambiguous"| Q
  F -->|"admitted"| G
  G -->|"exact facts and bindings"| H
  H -->|"reject conflicting inputs"| I
  G -->|"exact sample dependency closure"| J
  H -->|"account link"| K
  J -->|"matching product or industry"| K
  I --> L
  K -->|"internal context only"| L
  L -->|"usable condition"| M
  H -->|"eligible account evidence"| M
  M -->|"whole message validates"| N
  N --> R
  R -->|"historical approval not current permission"| U
  U -->|"ALLOW; no sending"| O
  U -->|"not enabled in this profile"| P
```

## Research context is not account-specific proof

```mermaid
flowchart TB
  A["Account: eligible product footprint and binding"]
  B["Canonical software product subject"]
  C["Permitted review or discussion records"]
  D["Exact quoted classifications with stance and sentiment"]
  E["ResearchSample: all retrieved eligible, excluded and unclassified records"]
  P["Versioned support policy: pain versus workflow mention"]
  F["Prior: scoped numerator and full denominator"]
  G["Pinned matching context join: USABLE required"]
  H["Internal investigation or neutral question selection"]
  I["Separate account evidence for outward claims"]
  X["No transfer of reported product pain into company fact"]
  V["Deletion, expiry or rights change to any denominator input blocks current use"]
  A -->|"explicit relationship"| B
  C --> D
  D -->|"one decision per retrieved record"| E
  P -->|"stance and sentiment semantics"| F
  E -->|"deduplicated record denominator"| F
  B --> G
  F --> G
  G -->|"no ABSTAINED context"| H
  H -->|"investigate; do not assert pain"| I
  G -->|"hard boundary"| X
  E -->|"all dependencies retained"| V
```

## Batch evaluation sequence

```mermaid
sequenceDiagram
    participant B as BatchRunner
    participant A as Acquisition
    participant F as FactAdmission
    participant DB as FactRepository
    participant S as Reasoning
    participant R as ReviewService
    participant G as CurrentUseGate
    participant X as PreviewExporter
    B->>A: Validated intake, enabled profile, bounded attempt
    alt No bytes captured
        A-->>B: Failed attempt plus diagnostic UNKNOWN; no NOT_FOUND
    else Capture or approved replay import
        A->>F: Artifacts, extraction results and executed detector coverage
        F->>DB: Admit only successful, attributable, lineage-closed facts
    end
    B->>DB: Pin inputs, sample records, bindings and target completion
    DB-->>B: Exact input set and resolved claim views
    B->>S: Evaluate enabled functions, usable context and signals
    alt Conflicting, failed or insufficient evidence
        S-->>B: Abstained or unresolved target; no approved positive output
    else Eligible supported result
        S->>DB: Publish completed preview with exact dependencies
        R->>DB: Record authorized review of package revision and hash
        G->>DB: Recheck current evidence, policies and restrictions
        alt Gate permits exact destination and purpose
            G->>X: ALLOW with current state hash and expiry
            X->>DB: Record local preview receipt with payload hash
        else Current use blocked
            G->>DB: Record BLOCK; historical review remains
        end
    end
    Note over G,X: A repeated local export key reuses identical bytes; changed payload fails
    Note over B,X: No remote export, automatic sending or production authentication is implemented
```

## Domain identity, facts and corrections

```mermaid
classDiagram
direction LR
class Subject {
  +string subject_id
  +string tenant_id
  +enum kind
  +string display_name
  +List~Object~ external_ids
}
class Scope {
  +string scope_id
  +string tenant_id
  +string subject_id
  +enum kind
  +List~string~ resources
  +enum capture_mode
  +string population_description
  +string stable_scope_key
}
class SubjectBinding {
  +string binding_id
  +string tenant_id
  +string subject_id
  +string scope_id
  +List~string~ artifact_ids
  +enum role
  +enum status
  +string method
  +string decided_at
  +List~string~ evidence_locator_ids
}
class PredicateDefinition {
  +string predicate_id
  +string version
  +string family
  +string description
  +List~enum~ subject_kinds
  +Object target_schema
  +Object value_schema
  +List~enum~ allowed_natures
  +List~enum~ allowed_processors
  +bool absence_allowed
  +enum temporal_mode
  +enum copy_policy
  +List~Object~ reference_rules
  +List~int~ section_ids
  +string value_class
  +enum origin
  +Object example_target
  +PredicateValue example_value
}
class Fact {
  +string schema_version
  +string fact_id
  +string tenant_id
  +string subject_id
  +string predicate_id
  +Object target
  +string scope_id
  +enum state
  +PredicateValue object
  +enum nature
  +string source_id
  +Optional~string~ binding_id
  +string evidence_id
  +Optional~string~ execution_id
  +string run_id
  +string observed_at
  +string recorded_at
  +Optional~string~ effective_at
  +Optional~Object~ window
  +Optional~enum~ reason
  +string expires_at
  +Optional~Object~ confidence
  +Optional~string~ supersedes_fact_id
}
class ClaimResolution {
  +string resolution_id
  +string tenant_id
  +string subject_id
  +string predicate_id
  +string scope_id
  +Object target
  +List~string~ observation_ids
  +List~string~ accepted_fact_ids
  +enum status
  +string policy_version
  +string as_of
  +string run_id
  +string resolved_at
}
class CandidateRecord {
  +string candidate_id
  +string tenant_id
  +Optional~string~ artifact_id
  +string proposed_predicate_id
  +PredicateValue proposed_value
  +enum reason
  +bool production_eligible
  +Optional~string~ attempt_id
}
class ChangeRecord {
  +string change_id
  +string tenant_id
  +enum kind
  +string target_id
  +string effective_at
  +string reason
  +Optional~string~ replacement_id
}
class IntakeRequest {
  +string intake_id
  +string tenant_id
  +string requester_id
  +string profile_id
  +enum purpose
  +List~Object~ targets
  +string received_at
  +string request_hash
  +string idempotency_key
}
class ActorGrant {
  +string actor_id
  +string tenant_id
  +List~enum~ permissions
  +bool fixture_only
  +bool active
}
Scope "*" --> "1" Subject : describes
SubjectBinding "*" --> "1" Subject : attributes
SubjectBinding "*" --> "1" Scope : binds
Fact "*" --> "1" Subject : concerns
Fact "*" --> "1" PredicateDefinition : conforms_to
Fact "*" --> "1" Scope : scoped_by
Fact "*" --> "0..1" SubjectBinding : raw_attribution
ClaimResolution "1" o-- "1..*" Fact : projects
ChangeRecord "*" ..> "0..1" Fact : can_retract
CandidateRecord "*" ..> "0..1" Fact : admit_only_after_validation
```

## Evidence acquisition, rights and coverage

```mermaid
classDiagram
direction LR
class SourceDefinition {
  +string source_id
  +string version
  +string provider
  +enum acquisition_method
  +enum authority
  +bool fixture_only
  +string policy_id
  +List~string~ emits
  +List~enum~ allowed_natures
  +int freshness_seconds
  +enum adapter_status
  +string upstream_namespace
}
class DataAccessPolicy {
  +string policy_id
  +List~string~ tenant_ids
  +string version
  +enum review_status
  +bool fixture_only
  +Optional~string~ approval_ref
  +string terms_ref
  +string reviewed_at
  +string valid_until
  +List~enum~ purposes
  +int max_raw_retention_seconds
  +int max_derived_retention_seconds
  +Optional~string~ attribution_text
  +bool allow_personal_data
  +bool allow_sensitive_data
  +bool deletion_cascades
}
class ProviderBlueprint {
  +string blueprint_id
  +string provider
  +List~int~ section_ids
  +List~string~ families
  +List~enum~ methods
  +string terms_url
  +bool approval_required
  +bool adapter_implemented
  +string notes
}
class Artifact {
  +string artifact_id
  +string tenant_id
  +string source_id
  +string scope_id
  +string resource_uri
  +string media_type
  +Optional~string~ content_ref
  +string content_hash
  +int byte_count
  +string captured_at
  +Optional~string~ published_at
  +enum status
  +bool truncated
  +string retained_until
  +enum retention_state
  +enum classification
  +string origin_namespace
  +string origin_record_id
  +string origin_revision
  +string independence_group
  +Optional~string~ parent_artifact_id
}
class EvidenceLocator {
  +string locator_id
  +string artifact_id
  +enum kind
  +Optional~int~ start
  +Optional~int~ end
  +Optional~string~ pointer
  +Optional~string~ quote
}
class EvidenceSet {
  +string evidence_id
  +string tenant_id
  +List~string~ locator_ids
  +List~string~ input_fact_ids
  +Optional~string~ execution_id
  +Optional~string~ coverage_id
  +enum directness
  +Optional~string~ attempt_id
  +List~string~ sample_ids
}
class CoverageRecord {
  +string coverage_id
  +string tenant_id
  +string scope_id
  +string source_id
  +List~string~ predicate_ids
  +Object target
  +List~string~ planned_resources
  +List~Object~ checked
  +enum status
  +string checked_at
  +string detector_release
  +string scope_limitations
  +List~string~ attempt_ids
  +string detector_execution_id
}
class AcquisitionAttempt {
  +string attempt_id
  +string tenant_id
  +string intake_id
  +string source_id
  +string source_version
  +string adapter_version
  +Object target
  +Optional~string~ scope_id
  +string request_hash
  +string operation_key
  +string started_at
  +string finished_at
  +enum status
  +List~string~ artifact_ids
  +Optional~enum~ terminal_reason
  +enum pagination
  +bool truncated
  +int max_requests
  +int requests_made
  +int timeout_seconds
  +int body_limit_bytes
  +enum cost_status
  +Optional~int~ cost_minor
  +Optional~string~ currency
  +enum execution_mode
}
SourceDefinition "*" --> "1" DataAccessPolicy : governed_by
ProviderBlueprint "1" ..> "0..*" SourceDefinition : requires_implementation_and_approval
Artifact "*" --> "1" SourceDefinition : obtained_from
EvidenceLocator "*" --> "1" Artifact : locates
EvidenceSet "1" o-- "0..*" EvidenceLocator : cites
EvidenceSet "*" --> "0..1" CoverageRecord : absence_proof
CoverageRecord "1" --> "1..*" Artifact : completed_capture_refs
Artifact "*" --> "0..1" Artifact : transformed_from
AcquisitionAttempt "1" --> "0..*" Artifact : can_have_no_bytes
CoverageRecord "1" --> "1..*" AcquisitionAttempt : completed_acquisition
```

## Typed payload examples: tooling, hiring and workflow

```mermaid
classDiagram
direction LR
class TechnologyValue {
  +string product_id
  +Optional~string~ version
  +enum surface
  +string matched_value
  +string fingerprint_id
  +string deployment_claim
}
class TechnologyReportValue {
  +string product_id
  +string provider
  +Optional~string~ provider_detected_at
  +Optional~string~ reported_version
}
class JobPostingValue {
  +string posting_id
  +string namespace
  +string url
  +string title
  +Optional~string~ department
  +Optional~string~ published_at
  +Optional~enum~ employment_type
}
class SalaryValue {
  +Optional~int~ minimum_minor
  +Optional~int~ maximum_minor
  +string currency
  +int minor_unit_exponent
  +enum period
  +enum basis
}
class AttributedStatementValue {
  +string statement_id
  +string text
  +string topic_id
  +enum modality
}
class SurfaceObservationValue {
  +string surface_key
  +string observed_value
}
class HypothesisValue {
  +string hypothesis_id
  +string conclusion
  +List~string~ alternatives
  +List~string~ limitations
  +string verification_question
}
class QuotedTextResult {
  +string text
}
class PublishedRecordValue {
  +string namespace
  +string record_id
  +string url
  +string publisher
  +Optional~string~ published_at
  +string record_type
  +string title
  +string text
}
class CaseStudyOutcomeValue {
  +string case_id
  +string outcome_id
  +string publisher
  +string source_url
  +string reported_quote
  +string metric_name
  +number reported_value
  +string unit
  +Optional~number~ baseline_value
  +enum comparison_kind
  +Optional~Object~ measurement_window
  +Optional~int~ sample_size
  +Optional~string~ method_description
  +string attribution
  +bool transfer_to_target_allowed
}
JobPostingValue "1" ..> "0..*" SalaryValue : separate_fact_by_posting_key
JobPostingValue "1" ..> "0..*" AttributedStatementValue : may_support_extracted_statements
QuotedTextResult "1" ..> "0..1" AttributedStatementValue : requires_quote_and_binding_checks
AttributedStatementValue "*" ..> "0..*" HypothesisValue : inputs_not_proof_of_conclusion
SurfaceObservationValue "*" ..> "0..*" TechnologyValue : detector_evidence
TechnologyReportValue "*" ..> "*" TechnologyValue : distinct_epistemic_channels
```

## Reviews, research samples and dimensional measurements

```mermaid
classDiagram
direction LR
class MetricDefinition {
  +string metric_id
  +string description
  +string unit
  +Object value_schema
  +Object dimensions_schema
  +bool requires_denominator
  +enum aggregation
  +List~enum~ allowed_natures
  +List~enum~ subject_kinds
  +List~int~ section_ids
}
class MeasurementValue {
  +string metric_id
  +number value
  +string unit
  +Object dimensions
  +string method_version
  +string reporting_timezone
  +Optional~int~ numerator
  +Optional~int~ denominator
  +Optional~int~ sample_size
  +Optional~Object~ uncertainty
}
class TaxonomyTerm {
  +string term_id
  +string scheme_id
  +string scheme_version
  +string label
  +Optional~string~ parent_id
}
class ResearchSample {
  +string sample_id
  +string tenant_id
  +string subject_id
  +string scope_id
  +Object window
  +string sampling_frame
  +enum selection_method
  +List~string~ retrieved_artifact_ids
  +List~string~ eligible_artifact_ids
  +List~string~ excluded_artifact_ids
  +string dedupe_policy_version
  +Optional~int~ population_size
  +bool complete_population
  +List~string~ limitations
  +List~string~ policy_ids
  +string support_policy_id
  +string theme_id
  +List~SampleRecordDecision~ record_decisions
  +string created_at
}
class ResearchPriorValue {
  +string sample_id
  +string theme_id
  +List~string~ supporting_fact_ids
  +List~string~ contradicting_fact_ids
  +int support_count
  +int eligible_count
  +number sample_share
  +bool population_claim
  +string support_policy_id
  +int classified_eligible_count
  +int unclassified_count
  +string denominator_definition
}
class ReviewRecordValue {
  +string review_key
  +string platform
  +string published_at
  +Optional~number~ rating
  +Optional~number~ rating_scale_max
  +string text
  +string language
  +bool edited
}
class DiscussionRecordValue {
  +string post_key
  +string community
  +string thread_key
  +string published_at
  +string text
  +string language
  +enum role
}
class ThemeClassificationValue {
  +string theme_id
  +string record_key
  +enum sentiment
  +enum stance
  +List~string~ support_locator_ids
}
class ResearchSupportPolicy {
  +string support_policy_id
  +string version
  +enum meaning
  +List~string~ allowed_stances
  +List~string~ allowed_sentiments
  +string counting_unit
  +string denominator_rule
  +string unclassified_policy
}
class SampleRecordDecision {
  +string artifact_id
  +enum status
  +List~string~ classification_fact_ids
  +Optional~string~ reason
}
class LookalikeMatch {
  +string match_id
  +string run_id
  +string tenant_id
  +string target_subject_id
  +string comparison_subject_id
  +List~string~ input_fact_ids
  +string corpus_release
  +string representation_version
  +string index_version
  +number similarity_score
  +List~string~ missing_features
  +List~string~ differences
  +bool outcome_transfer_allowed
  +string use
  +string implementation_status
}
class ScenarioEstimate {
  +string scenario_id
  +string tenant_id
  +string subject_id
  +List~string~ observed_input_fact_ids
  +List~Object~ assumptions
  +string formula_version
  +string currency
  +int lower_minor
  +int upper_minor
  +string time_period
  +List~string~ limitations
  +bool verified_loss
  +string implementation_status
}
MeasurementValue "*" --> "1" MetricDefinition : unit_dimensions_and_bounds
ResearchPriorValue "*" --> "1" ResearchSample : denominator_and_selection
ThemeClassificationValue "*" --> "1" TaxonomyTerm : classified_theme
ResearchPriorValue "*" --> "1" TaxonomyTerm : summarized_theme
ReviewRecordValue "1" ..> "0..*" ThemeClassificationValue : input_to_classifier
DiscussionRecordValue "1" ..> "0..*" ThemeClassificationValue : input_to_classifier
ResearchPriorValue "1" o-- "1..*" ThemeClassificationValue : support_fact_references
ResearchSample "1" *-- "1..*" SampleRecordDecision : complete_denominator
ResearchSample "*" --> "1" ResearchSupportPolicy : counting_rule
```

## Registry, authorized call and future outcome payloads

```mermaid
classDiagram
direction LR
class RegistryRecordValue {
  +string namespace
  +string record_id
  +string issuer
  +string jurisdiction
  +Optional~string~ effective_at
  +Optional~string~ filed_at
  +string record_status
}
class CallEventValue {
  +string call_key
  +string started_at
  +enum direction
  +enum status
  +Optional~number~ duration_seconds
  +Optional~string~ callback_of
}
class EconomicHypothesisValue {
  +string currency
  +int estimated_amount_minor
  +List~string~ assumptions
  +List~string~ limitations
}
class Exposure {
  +string exposure_id
  +string tenant_id
  +string package_id
  +string business_send_key
  +Optional~string~ provider_message_id
  +string recipient_key
  +Optional~string~ accepted_at
  +enum status
}
class OutcomeEvent {
  +string event_id
  +string tenant_id
  +string provider
  +string provider_event_id
  +Optional~string~ exposure_id
  +string occurred_at
  +string received_at
  +enum kind
  +enum attribution_status
  +string evidence_id
}
CallEventValue "*" ..> "0..*" EconomicHypothesisValue : inputs_plus_explicit_assumptions
OutcomeEvent "*" --> "0..1" Exposure : matched_or_quarantined
```

## Batch execution, versioning and bounded model tasks

```mermaid
classDiagram
direction LR
class BatchRun {
  +string run_id
  +string tenant_id
  +enum mode
  +string as_of
  +string created_at
  +string code_release
  +string registry_release
  +string profile_id
  +List~string~ input_artifact_ids
  +List~string~ input_fact_ids
  +List~string~ binding_ids
  +enum status
  +string approval_policy_version
  +string knowledge_cutoff
  +string sealed_at
  +List~string~ sample_ids
  +List~string~ resolution_ids
  +List~TargetResult~ target_results
  +List~string~ produced_fact_ids
  +List~string~ imported_execution_ids
  +string intake_id
}
class CapabilityProfile {
  +string profile_id
  +string version
  +bool production_enabled
  +List~string~ capture_source_ids
  +List~string~ fact_predicate_ids
  +List~string~ execute_function_ids
  +List~string~ signal_ids
  +List~string~ template_ids
  +bool research_context_enabled
  +bool delivery_enabled
  +enum product_boundary
  +bool export_enabled
}
class FunctionDefinition {
  +string function_id
  +string version
  +enum processor
  +enum authority
  +bool fixture_only
  +List~string~ input_predicates
  +List~string~ output_predicates
  +Object parameter_schema
  +enum cross_subject_rule
  +enum implementation_status
  +Optional~string~ entrypoint
  +Optional~Object~ detector_contract
}
class ExecutionRecord {
  +string execution_id
  +string tenant_id
  +string run_id
  +string function_id
  +string function_version
  +string subject_id
  +List~string~ input_fact_ids
  +List~string~ input_artifact_ids
  +List~string~ output_fact_ids
  +string input_set_hash
  +Object parameters
  +string started_at
  +string finished_at
  +enum status
  +Optional~string~ model_call_id
  +List~string~ input_sample_ids
  +string sample_set_hash
  +Optional~string~ terminal_reason
}
class ModelCall {
  +string call_id
  +string tenant_id
  +string task_version
  +string provider
  +string model
  +string prompt_hash
  +string output_schema_id
  +List~string~ input_artifact_ids
  +string request_artifact_id
  +Optional~string~ response_artifact_id
  +List~string~ policy_ids
  +int max_repair_attempts
  +enum status
  +Optional~string~ terminal_reason
}
class RepairAttempt {
  +string attempt_id
  +string call_id
  +int ordinal
  +string input_response_artifact_id
  +string output_response_artifact_id
  +enum method
  +enum status
  +List~string~ validation_errors
}
class FingerprintDefinition {
  +string fingerprint_id
  +string version
  +enum authority
  +bool fixture_only
  +string product_subject_id
  +string emits
  +enum capture_mode
  +enum operator
  +string match_value
  +List~string~ positive_fixtures
  +List~string~ negative_fixtures
  +Optional~string~ calibration_ref
  +enum implementation_status
}
class CalibrationRecord {
  +string calibration_id
  +string target_id
  +string target_version
  +string evaluation_dataset_id
  +int true_positives
  +int false_positives
  +number measured_precision
  +string report_hash
  +bool fixture_only
  +string review_ref
}
class CoverageFamilyPlan {
  +int section
  +string title
  +List~string~ predicate_ids
  +List~string~ metric_ids
  +string contract_status
  +string live_adapter_status
}
class TargetResult {
  +string subject_id
  +enum status
  +string completed_at
  +Optional~string~ reason
}
BatchRun "*" --> "1" CapabilityProfile : pins
ExecutionRecord "*" --> "1" BatchRun : belongs_to
ExecutionRecord "*" --> "1" FunctionDefinition : versioned_function
ExecutionRecord "1" --> "0..1" ModelCall : bounded_model_step
ModelCall "1" o-- "0..2" RepairAttempt : bounded_repair_history
FingerprintDefinition "1" --> "0..1" CalibrationRecord : does_not_self_calibrate
CapabilityProfile "1" --> "0..*" FunctionDefinition : enabled_dependency_closure
CoverageFamilyPlan "*" ..> "*" CapabilityProfile : breadth_is_not_activation
```

## Scoped research joins, signal evaluation and grounded previews

```mermaid
classDiagram
direction LR
class ContextJoinRule {
  +string join_rule_id
  +string version
  +string link_predicate
  +string link_object_path
  +string context_predicate
  +List~enum~ target_kinds
  +enum link_kind
  +string purpose
  +int maximum_hops
  +bool company_claim_allowed
}
class ContextAssessment {
  +string context_id
  +string tenant_id
  +string run_id
  +string account_subject_id
  +string context_subject_id
  +string join_rule_id
  +string link_fact_id
  +List~string~ context_fact_ids
  +enum relationship_strength
  +string purpose
  +bool company_claim_allowed
  +enum status
}
class SignalDefinition {
  +string signal_type_id
  +string version
  +List~Object~ required_facts
  +string function_id
  +bool context_allowed
  +string description
  +enum status
}
class SignalEvaluation {
  +string signal_id
  +string run_id
  +string tenant_id
  +string subject_id
  +string signal_type_id
  +List~string~ input_fact_ids
  +List~string~ context_ids
  +enum status
  +Optional~enum~ reason
  +string evaluated_at
}
class TemplateDefinition {
  +string template_id
  +string version
  +enum authority
  +enum mode
  +string required_predicate
  +List~enum~ allowed_natures
  +enum renderer
  +string question
  +bool maturity_required
  +Optional~enum~ offered_rung
  +string review_ref
}
class GroundedClause {
  +string clause_id
  +List~string~ fact_ids
  +string template_id
  +string text
  +List~enum~ evidence_roles
}
class OutreachPackage {
  +string package_id
  +int revision
  +string run_id
  +string tenant_id
  +string subject_id
  +string template_id
  +List~GroundedClause~ clauses
  +List~string~ signal_ids
  +List~string~ context_ids
  +Optional~string~ maturity_fact_id
  +enum status
  +string rendered_text
  +Optional~string~ approved_at
  +bool send_allowed
  +Optional~string~ review_id
}
class ReviewDecision {
  +string review_id
  +string tenant_id
  +string reviewer_id
  +Object package
  +enum action
  +string reason
  +string decided_at
  +string policy_version
}
class UseRestriction {
  +string restriction_id
  +string tenant_id
  +string subject_id
  +Optional~string~ recipient_key
  +enum kind
  +string actor_id
  +string effective_at
  +Optional~string~ released_at
  +Optional~string~ released_by
  +string reason
}
class UseGateDecision {
  +string gate_id
  +string tenant_id
  +Object package
  +string review_id
  +string actor_id
  +enum purpose
  +string destination_id
  +Optional~string~ recipient_key
  +string evaluated_at
  +string valid_until
  +string version_vector
  +enum decision
  +List~string~ reasons
}
class DestinationDefinition {
  +string destination_id
  +string tenant_id
  +string mapping_version
  +enum kind
  +bool fixture_only
  +bool enabled
  +bool automatic_sending
}
class ExportReceipt {
  +string export_id
  +string tenant_id
  +Object package
  +string gate_id
  +string destination_id
  +string mapping_version
  +string actor_id
  +Optional~string~ recipient_key
  +string payload_hash
  +Optional~string~ payload_ref
  +string idempotency_key
  +string requested_at
  +Optional~string~ completed_at
  +enum status
  +Optional~string~ external_reference
  +bool automatic_sending
}
ContextAssessment "*" --> "1" ContextJoinRule : explicit_one_hop_join
SignalEvaluation "1" --> "0..*" ContextAssessment : internal_context_only
SignalEvaluation "*" --> "1" SignalDefinition : conforms_to
OutreachPackage "1" --> "0..*" SignalEvaluation : eligible_results
OutreachPackage "1" *-- "1..*" GroundedClause : contains
OutreachPackage "*" --> "1" TemplateDefinition : reviewed_template
GroundedClause "*" --> "1" TemplateDefinition : deterministic_rendering
OutreachPackage "1" --> "0..*" ContextAssessment : not_copy_evidence
ReviewDecision "*" --> "1" OutreachPackage : exact_revision_hash
UseGateDecision "*" --> "1" ReviewDecision : current_use_not_just_review
UseGateDecision "*" --> "0..*" UseRestriction : non_expiring_DNC_check
ExportReceipt "*" --> "1" UseGateDecision : must_allow_at_dispatch
ExportReceipt "*" --> "1" DestinationDefinition : versioned_mapping
```

## Shared value objects and requirement records

```mermaid
classDiagram
direction LR
class TimeWindow {
  +string start
  +string end
}
class ExternalIdentifier {
  +string namespace
  +string value
}
class ConfidenceAssessment {
  +number value
  +enum meaning
  +Optional~string~ calibration_id
}
class ObjectReferenceRule {
  +enum container
  +string path
  +List~enum~ subject_kinds
  +enum target_type
}
class CoverageCheck {
  +string resource
  +Optional~string~ artifact_id
  +enum result
}
class FactRequirement {
  +string predicate_id
  +List~enum~ allowed_natures
  +enum state
  +int minimum
  +string counting_unit
}
class PackageReference {
  +string package_id
  +int revision
  +string content_hash
}
class IntakeTarget {
  +string resource_uri
  +Optional~string~ subject_id
}
```

## Proposed application interfaces, not deployed services

```mermaid
classDiagram
direction LR
class BatchRunner {
  <<Interface>>
  +RegistryLinker registry
  +FactRepository facts
  +run(intake_id) BatchRun
}
class RegistryLinker {
  <<Interface>>
  +load_release(release_id) void
  +validate_closure(profile) void
  +execution_order(profile) List~FunctionDefinition~
}
class SourceAdapter {
  <<Interface>>
  +capture(target, scope) AcquisitionAttempt
}
class AcquisitionService {
  <<Interface>>
  +SourceAdapter adapter
  +RightsGate rights
  +ContentRepository content
  +collect(intake, scope) AcquisitionAttempt
}
class RightsGate {
  <<Interface>>
  +assert_use(policy_ids, purpose, as_of) void
  +retention_deadline(policy_ids) datetime
}
class ContentRepository {
  <<Interface>>
  +put_immutable(bytes, policy) Artifact
  +read_verified(artifact_id) bytes
  +delete(artifact_id) ChangeRecord
}
class SubjectResolver {
  <<Interface>>
  +bind(artifact, subject, locators) SubjectBinding
}
class ExtractionService {
  <<Interface>>
  +BoundedModelGateway model
  +extract(artifact, definition) List~CandidateRecord~
}
class BoundedModelGateway {
  <<Interface>>
  +call(task, artifacts) ModelCall
  +repair_or_abstain(call) QuotedTextResult
}
class FactAdmission {
  <<Interface>>
  +RightsGate rights
  +RegistryLinker registry
  +validate(candidate, evidence, binding) Fact
  +quarantine(candidate, reason) CandidateRecord
}
class FactRepository {
  <<Interface>>
  +append_idempotent(fact) Fact
  +select_inputs(subject, as_of) List~Fact~
  +record_change(change) void
}
class AccountInputSelector {
  <<Interface>>
  +FactRepository facts
  +freeze_account_inputs(subject, as_of) BatchRun
}
class DerivationRunner {
  <<Interface>>
  +evaluate(function, inputs, parameters) ExecutionRecord
}
class ContextJoiner {
  <<Interface>>
  +join(rule, account_facts, context_facts) ContextAssessment
}
class SignalEngine {
  <<Interface>>
  +evaluate(definition, facts, contexts) SignalEvaluation
}
class TemplateRenderer {
  <<Interface>>
  +render(template, eligible_facts) List~GroundedClause~
}
class PackageValidator {
  <<Interface>>
  +RightsGate rights
  +approve_preview(package, as_of) OutreachPackage
  +revalidate_for_export(package, as_of) void
}
class RetentionService {
  <<Interface>>
  +ContentRepository content
  +FactRepository facts
  +apply_policy(policy, as_of) List~ChangeRecord~
}
class UnitOfWork {
  <<Interface>>
  +begin() void
  +commit_account_result() void
  +rollback() void
}
class ReviewService {
  <<Interface>>
  +review(exact_package_revision, principal) ReviewDecision
}
class UseGate {
  <<Interface>>
  +evaluate(package, destination, principal, current_time) UseGateDecision
}
class LocalPreviewExporter {
  <<Interface>>
  +export(gate_id, principal_id, at, idempotency_key) LocalExportResult
}
BatchRunner ..> ReviewService : review_exact_revision
BatchRunner ..> UseGate : current_permission
UseGate ..> LocalPreviewExporter : allow_local_export_only
BatchRunner ..> RegistryLinker : uses
BatchRunner ..> AcquisitionService : optional_capture
BatchRunner ..> AccountInputSelector : pins_inputs
BatchRunner ..> DerivationRunner : sequential_plan
BatchRunner ..> ContextJoiner : context_join
BatchRunner ..> SignalEngine : evaluate
BatchRunner ..> TemplateRenderer : compose
BatchRunner ..> PackageValidator : approve_preview
BatchRunner ..> UnitOfWork : publish_atomically_per_account
AcquisitionService ..> SourceAdapter : port
AcquisitionService ..> ContentRepository : persist
AcquisitionService ..> RightsGate : before_capture
ExtractionService ..> SubjectResolver : attribution
ExtractionService ..> BoundedModelGateway : optional
ExtractionService ..> FactAdmission : no_direct_promotion
FactAdmission ..> FactRepository : append
FactAdmission ..> RightsGate : permitted_derivation
AccountInputSelector ..> FactRepository : select
PackageValidator ..> RightsGate : current_use_check
RetentionService ..> ContentRepository : delete_or_expire
RetentionService ..> FactRepository : record_changes
```

## Evidence-to-reviewed-local-export lifecycle

```mermaid
stateDiagram-v2
    [*] --> Intake
    Intake --> Attempt: approved profile and purpose
    Attempt --> DiagnosticUnknown: failure without captured bytes
    Attempt --> CapturedArtifact: permitted capture or import
    CapturedArtifact --> Candidate: extract
    Candidate --> Quarantined: invalid, failed producer or ambiguous binding
    Candidate --> AdmittedFact: all admission checks pass
    AdmittedFact --> EligibleInput: pinned lineage and claim resolution pass
    AdmittedFact --> HistoricalOnly: expired, retracted or rights revoked
    EligibleInput --> Unresolved: missing prerequisites or conflict
    EligibleInput --> ResolvedSignal: enabled condition holds
    ResolvedSignal --> PreviewPackage: supported deterministic template
    PreviewPackage --> ReviewedRevision: authorized exact-hash review
    ReviewedRevision --> UseGate: fresh checks for exact purpose and destination
    UseGate --> Blocked: restrictions, stale evidence or changed inputs
    UseGate --> LocalExport: ALLOW and idempotent file write
    LocalExport --> [*]: no sending
    DiagnosticUnknown --> [*]: retained diagnostic
    Quarantined --> Candidate: explicit corrected extraction
```

## Cross-partition domain relationships — selected fields only

```mermaid
classDiagram
direction LR
class Subject {
  +string subject_id
  +string tenant_id
}
class PredicateDefinition {
  +string predicate_id
}
class Fact {
  +string fact_id
  +string tenant_id
  +string subject_id
  +string predicate_id
  +Object target
  +string scope_id
  +enum state
  +enum nature
  +string source_id
  +Optional~string~ binding_id
  +string evidence_id
  +Optional~string~ execution_id
  +string run_id
  +Optional~Object~ window
  +Optional~string~ supersedes_fact_id
}
class EvidenceSet {
  +string evidence_id
  +string tenant_id
  +Optional~string~ execution_id
  +Optional~string~ coverage_id
  +Optional~string~ attempt_id
}
class Artifact {
  +string artifact_id
  +string tenant_id
  +string source_id
  +string scope_id
  +enum status
  +string origin_record_id
  +Optional~string~ parent_artifact_id
}
class ExecutionRecord {
  +string execution_id
  +string tenant_id
  +string run_id
  +string function_id
  +string subject_id
  +enum status
  +Optional~string~ model_call_id
}
class BatchRun {
  +string run_id
  +string tenant_id
  +string as_of
  +string profile_id
  +enum status
  +string intake_id
}
class ContextAssessment {
  +string context_id
  +string tenant_id
  +string run_id
  +string account_subject_id
  +string context_subject_id
  +string join_rule_id
  +string link_fact_id
  +bool company_claim_allowed
  +enum status
}
class SignalEvaluation {
  +string signal_id
  +string run_id
  +string tenant_id
  +string subject_id
  +string signal_type_id
  +enum status
}
class OutreachPackage {
  +string package_id
  +string run_id
  +string tenant_id
  +string subject_id
  +string template_id
  +Optional~string~ maturity_fact_id
  +enum status
  +Optional~string~ review_id
}
class GroundedClause {
  +string clause_id
  +string template_id
}
class MetricDefinition {
  +string metric_id
}
Fact "*" --> "1" Subject : about
Fact "*" --> "1" PredicateDefinition : typed_by
Fact "*" --> "1" EvidenceSet : supported_by
EvidenceSet "*" --> "0..*" Artifact : through_locators
EvidenceSet "*" --> "0..*" Fact : derived_input_refs
Fact "*" --> "0..1" ExecutionRecord : produced_by
ExecutionRecord "*" --> "1" BatchRun : pinned_run
ExecutionRecord "*" --> "*" Fact : reads_and_produces
Fact "*" --> "0..1" MetricDefinition : measurement_contract
ContextAssessment "*" --> "2..*" Fact : account_link_and_context_fact
SignalEvaluation "*" --> "0..*" Fact : eligible_inputs
SignalEvaluation "*" --> "0..*" ContextAssessment : internal_context
OutreachPackage "*" --> "0..*" SignalEvaluation : based_on
OutreachPackage "1" *-- "1..*" GroundedClause : contains
GroundedClause "*" --> "1..*" Fact : own_account_claim_support
```
