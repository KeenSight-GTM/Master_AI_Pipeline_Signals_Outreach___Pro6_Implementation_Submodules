# Dataflows, UML and complete class reference

All 58 exported contract/value-object classes appear exactly once in the full class partitions. 19 proposed code interfaces are separate. 
Primitive and object payloads are selected by the PredicateDefinition registry: 197 predicates do not require 197 classes or database tables. Payload-family boxes show reusable shapes; individual predicate schemas remain normative.
Association labels denote logical references, not separate services. `..>` is a dependency; `o--` aggregation; `*--` composition. Method bodies on proposed interfaces are not implemented runtime code.
SVGs were rendered locally with Graphviz from the same model as the Mermaid class/flow sources. The state view is rendered through Graphviz; the sequence view uses a local SVG renderer over its message declarations. Mermaid CLI parsing was not run.

## Broad facts, narrow activation, simple batch execution

```mermaid
flowchart TB
  A["Broad capability catalog: all 11 domains"]
  B["Source and purpose approval"]
  C["Optional capture adapters"]
  D["Retained artifacts and coverage"]
  E["Deterministic or bounded model extraction"]
  F["Typed admission and subject binding"]
  Q["Quarantined candidates"]
  G["Reusable fact store"]
  H["Pinned account input set"]
  I["Enabled selectors and derivations"]
  J["Product / industry research facts"]
  K["Explicit context join"]
  L["Signals and confounds"]
  M["Evidence-bound template"]
  N["Validated preview package"]
  O["Human review / current-use export gate"]
  P["Future delivery: disabled"]
  A --> B
  B -->|"authorized"| C
  C --> D
  D --> E
  E --> F
  F -->|"unregistered / ambiguous / invalid"| Q
  F -->|"admitted"| G
  G --> H
  H --> I
  G -->|"separate subjects"| J
  H -->|"account link"| K
  J -->|"research prior"| K
  I -->|"eligible facts"| L
  K -->|"context only"| L
  L -->|"usable opportunity"| M
  H -->|"eligible account evidence"| M
  M -->|"whole-message validation"| N
  N --> O
  O -->|"only after future safeguards"| P
```

## Research context is not account-specific proof

```mermaid
flowchart TB
  A["Account: observed product footprint"]
  B["Software product subject"]
  C["Approved product reviews / forum records"]
  D["Attributed statements and classifications"]
  E["Bounded sample with deduplication and denominator"]
  F["Product-level prior"]
  G["Explicit same-tenant context join"]
  H["Internal investigation or question selection"]
  I["Account-specific facts for outward claims"]
  X["No transfer of product pain into company fact"]
  A -->|"references product identity"| B
  C --> D
  D --> E
  E --> F
  B -->|"relationship evidence"| G
  F -->|"same product only"| G
  G -->|"non-company-claim context"| H
  H -->|"request additional evidence"| I
  G -->|"hard boundary"| X
```

## Batch evaluation sequence

```mermaid
sequenceDiagram
    participant B as BatchRunner
    participant R as RegistryLinker
    participant A as AcquisitionService
    participant F as FactAdmission
    participant DB as FactRepository
    participant C as ContextJoiner
    participant S as SignalEngine
    participant P as PackageValidator
    B->>R: Validate enabled dependency closure and pin release
    opt Capture enabled and source policy approved
        B->>A: Bounded capture request
        A->>F: Retained artifacts, coverage, extraction candidates
        F->>DB: Append typed facts or quarantine invalid candidates
    end
    B->>DB: Select exact account inputs at as_of
    DB-->>B: Facts, versions, bindings and evidence references
    B->>C: Join eligible account link to product or industry prior
    C-->>B: Internal ContextAssessment, never company pain proof
    B->>S: Evaluate enabled rules in validated order
    alt Missing, stale, conflicted or ineligible evidence
        S-->>B: UNRESOLVED or SUPPRESSED
    else Supported condition
        S-->>B: RESOLVED with exact inputs
        B->>P: Render reviewed template and recheck full message
        P->>DB: Publish completed preview atomically per account
    end
    Note over B,DB: Retries are idempotent; a new evidence selection creates a new evaluation
    Note over B,P: No automatic sending or feedback optimization in this profile
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
}
class CandidateRecord {
  +string candidate_id
  +string tenant_id
  +string artifact_id
  +string proposed_predicate_id
  +PredicateValue proposed_value
  +enum reason
  +bool production_eligible
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
}
SourceDefinition "*" --> "1" DataAccessPolicy : governed_by
ProviderBlueprint "1" ..> "0..*" SourceDefinition : requires_implementation_and_approval
Artifact "*" --> "1" SourceDefinition : obtained_from
EvidenceLocator "*" --> "1" Artifact : locates
EvidenceSet "1" o-- "0..*" EvidenceLocator : cites
EvidenceSet "*" --> "0..1" CoverageRecord : absence_proof
CoverageRecord "1" --> "1..*" Artifact : completed_capture_refs
Artifact "*" --> "0..1" Artifact : transformed_from
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
MeasurementValue "*" --> "1" MetricDefinition : unit_dimensions_and_bounds
ResearchPriorValue "*" --> "1" ResearchSample : denominator_and_selection
ThemeClassificationValue "*" --> "1" TaxonomyTerm : classified_theme
ResearchPriorValue "*" --> "1" TaxonomyTerm : summarized_theme
ReviewRecordValue "1" ..> "0..*" ThemeClassificationValue : input_to_classifier
DiscussionRecordValue "1" ..> "0..*" ThemeClassificationValue : input_to_classifier
ResearchPriorValue "1" o-- "1..*" ThemeClassificationValue : support_fact_references
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
  +string response_artifact_id
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
}
ContextAssessment "*" --> "1" ContextJoinRule : explicit_one_hop_join
SignalEvaluation "1" --> "0..*" ContextAssessment : internal_context_only
SignalEvaluation "*" --> "1" SignalDefinition : conforms_to
OutreachPackage "1" --> "0..*" SignalEvaluation : eligible_results
OutreachPackage "1" *-- "1..*" GroundedClause : contains
OutreachPackage "*" --> "1" TemplateDefinition : reviewed_template
GroundedClause "*" --> "1" TemplateDefinition : deterministic_rendering
OutreachPackage "1" --> "0..*" ContextAssessment : not_copy_evidence
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
  +run(profile_id, account_ids) List~OutreachPackage~
}
class RegistryLinker {
  <<Interface>>
  +load_release(release_id) void
  +validate_closure(profile) void
  +execution_order(profile) List~FunctionDefinition~
}
class SourceAdapter {
  <<Interface>>
  +capture(scope) List~Artifact~
}
class AcquisitionService {
  <<Interface>>
  +SourceAdapter adapter
  +RightsGate rights
  +ContentRepository content
  +collect(scope) CoverageRecord
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

## Evidence-to-preview lifecycle

```mermaid
stateDiagram-v2
    [*] --> CapturedArtifact
    CapturedArtifact --> Candidate: extract
    Candidate --> Quarantined: invalid shape, unknown predicate or ambiguous binding
    Candidate --> AdmittedFact: shape, references, source and attribution pass
    AdmittedFact --> EligibleInput: current-use checks pass
    AdmittedFact --> HistoricalOnly: expired, retracted or rights revoked
    EligibleInput --> Unresolved: missing prerequisites or conflicts
    EligibleInput --> ResolvedSignal: declared condition holds
    ResolvedSignal --> PreviewPackage: reviewed template and eligible account evidence
    PreviewPackage --> Withheld: copy or policy check fails
    PreviewPackage --> ApprovedPreview: whole-message check passes
    ApprovedPreview --> HistoricalOnly: supporting evidence changes
    ApprovedPreview --> [*]: human review or controlled export
    Quarantined --> Candidate: reviewed definition or binding correction
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
