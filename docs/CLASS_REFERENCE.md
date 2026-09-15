# Complete class and field reference

119 class/record entries. These combine actual reference contracts, implemented collector dataclasses, common envelope drafts and explicitly proposed product records; they are not 119 deployed services.

## AcquisitionAttempt

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/AcquisitionAttempt.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| adapter_version | string | yes |
| artifact_ids | list[string] | yes |
| attempt_id | string | yes |
| body_limit_bytes | integer | yes |
| cost_minor | integer \| null | yes |
| cost_status | enum(KNOWN, UNKNOWN, NOT_CHARGED) | yes |
| currency | string \| null | yes |
| execution_mode | enum(REPLAY_IMPORT, LIVE_CAPTURE) | yes |
| finished_at | string | yes |
| intake_id | string | yes |
| max_requests | integer | yes |
| operation_key | string | yes |
| pagination | enum(NOT_APPLICABLE, EXHAUSTED, INCOMPLETE, UNKNOWN) | yes |
| request_hash | string | yes |
| requests_made | integer | yes |
| scope_id | string \| null | yes |
| source_id | string | yes |
| source_version | string | yes |
| started_at | string | yes |
| status | enum(SUCCEEDED, EMPTY_RESULT, PARTIAL, TIMEOUT, FAILED, POLICY_DENIED, BUDGET_DENIED, CANCELLED) | yes |
| target | closed object | yes |
| tenant_id | string | yes |
| terminal_reason | enum(TIMEOUT, POLICY_DENIED, BUDGET_DENIED, CANCELLED, PROVIDER_ERROR, PARTIAL_RESPONSE, NO_RESULTS) \| null | yes |
| timeout_seconds | integer | yes |
| truncated | boolean | yes |

## ActorGrant

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ActorGrant.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| active | boolean | yes |
| actor_id | string | yes |
| fixture_only | boolean | yes |
| permissions | list[enum(INTAKE, REVIEW_PACKAGE, USE_GATE, EXPORT, RESTRICT, CHANGE_FACT, CHANGE_BINDING, CHANGE_ARTIFACT, CHANGE_REGISTRY)] | yes |
| tenant_id | string | yes |

## Artifact

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/Artifact.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| artifact_id | string | yes |
| byte_count | integer | yes |
| captured_at | string | yes |
| classification | enum(PUBLIC_BUSINESS, PERSONAL, CONFIDENTIAL, SENSITIVE) | yes |
| content_hash | string | yes |
| content_ref | string \| null | yes |
| independence_group | string | yes |
| media_type | string | yes |
| origin_namespace | string | yes |
| origin_record_id | string | yes |
| origin_revision | string | yes |
| parent_artifact_id | string \| null | yes |
| published_at | string \| null | yes |
| resource_uri | string | yes |
| retained_until | string | yes |
| retention_state | enum(RETAINED, DELETED, EXPIRED, REFERENCE_ONLY) | yes |
| scope_id | string | yes |
| source_id | string | yes |
| status | enum(OK, ERROR, TIMEOUT, POLICY_DENIED) | yes |
| tenant_id | string | yes |
| truncated | boolean | yes |

## AttributedStatementValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/AttributedStatementValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| modality | enum(CURRENT_STATE, REQUIREMENT, ASPIRATION, NEGATED, UNCERTAIN) | yes |
| statement_id | string | yes |
| text | string | yes |
| topic_id | string | yes |

## BatchRun

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/BatchRun.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| approval_policy_version | string | yes |
| as_of | string | yes |
| binding_ids | list[string] | yes |
| code_release | string | yes |
| created_at | string | yes |
| imported_execution_ids | list[string] | yes |
| input_artifact_ids | list[string] | yes |
| input_fact_ids | list[string] | yes |
| intake_id | string | yes |
| knowledge_cutoff | string | yes |
| mode | enum(DESIGN_TEST, PRODUCTION) | yes |
| produced_artifact_ids | list[string] | yes |
| produced_fact_ids | list[string] | yes |
| profile_id | string | yes |
| registry_release | string | yes |
| resolution_ids | list[string] | yes |
| run_id | string | yes |
| sample_ids | list[string] | yes |
| sealed_at | string | yes |
| status | enum(OPEN, COMPLETE, PARTIAL, FAILED) | yes |
| target_results | list[TargetResult] | yes |
| tenant_id | string | yes |

## CalibrationRecord

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CalibrationRecord.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| calibration_id | string | yes |
| evaluation_dataset_id | string | yes |
| false_positives | integer | yes |
| fixture_only | boolean | yes |
| measured_precision | number | yes |
| report_hash | string | yes |
| review_ref | string | yes |
| target_id | string | yes |
| target_version | string | yes |
| true_positives | integer | yes |

## CallEventValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CallEventValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| call_key | string | yes |
| callback_of | string \| null | yes |
| direction | enum(INBOUND, OUTBOUND) | yes |
| duration_seconds | number \| null | yes |
| started_at | string | yes |
| status | enum(ANSWERED, MISSED, ABANDONED, VOICEMAIL, UNKNOWN) | yes |

## CandidateRecord

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CandidateRecord.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| artifact_id | string \| null | yes |
| attempt_id | string \| null | yes |
| candidate_id | string | yes |
| production_eligible | const False | yes |
| proposed_predicate_id | string | yes |
| proposed_value | constrained value | yes |
| reason | enum(UNREGISTERED_TYPE, INVALID_VALUE, UNRESOLVED_BINDING, UNKNOWN_TAXONOMY) | yes |
| tenant_id | string | yes |

## CapabilityProfile

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CapabilityProfile.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| capture_source_ids | list[string] | yes |
| delivery_enabled | const False | yes |
| execute_function_ids | list[string] | yes |
| export_enabled | boolean | yes |
| fact_predicate_ids | list[string] | yes |
| product_boundary | enum(KNOWLEDGE, PREVIEW, REVIEWED_HANDOFF) | yes |
| production_enabled | boolean | yes |
| profile_id | string | yes |
| research_context_enabled | boolean | yes |
| signal_ids | list[string] | yes |
| template_ids | list[string] | yes |
| version | string | yes |

## CaseStudyOutcomeValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CaseStudyOutcomeValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| attribution | const PUBLISHER_REPORTED_NOT_CAUSALLY_VERIFIED | yes |
| baseline_value | number \| null | yes |
| case_id | string | yes |
| comparison_kind | enum(ABSOLUTE, ABSOLUTE_CHANGE, RELATIVE_CHANGE, UNSPECIFIED) | yes |
| measurement_window | closed object \| null | yes |
| method_description | string \| null | yes |
| metric_name | string | yes |
| outcome_id | string | yes |
| publisher | string | yes |
| reported_quote | string | yes |
| reported_value | number | yes |
| sample_size | integer \| null | yes |
| source_url | string | yes |
| transfer_to_target_allowed | const False | yes |
| unit | string | yes |

## ChangeRecord

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ChangeRecord.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| actor_id | string | yes |
| change_id | string | yes |
| effective_at | string | yes |
| kind | enum(RETRACTION, BINDING_CORRECTION, AUTHORITY_CHANGE, POLICY_REVOCATION, ARTIFACT_DELETION) | yes |
| reason | string | yes |
| recorded_at | string | yes |
| replacement_id | string \| null | yes |
| target_id | string | yes |
| target_type | enum(facts, bindings, sources, policies, artifacts, fingerprints, functions) | yes |
| tenant_id | string | yes |

## ClaimResolution

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ClaimResolution.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| accepted_fact_ids | list[string] | yes |
| as_of | string | yes |
| observation_ids | list[string] | yes |
| policy_version | string | yes |
| predicate_id | string | yes |
| resolution_id | string | yes |
| resolved_at | string | yes |
| run_id | string | yes |
| scope_id | string | yes |
| status | enum(KNOWN, CONFLICT, UNKNOWN) | yes |
| subject_id | string | yes |
| target | object | yes |
| tenant_id | string | yes |

## ConfidenceAssessment

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ConfidenceAssessment.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| calibration_id | string \| null | yes |
| meaning | enum(UNCALIBRATED_MODEL_SCORE, CALIBRATED_PRECISION, DETERMINISTIC_MATCH) | yes |
| value | number | yes |

## ContextAssessment

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ContextAssessment.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| account_subject_id | string | yes |
| company_claim_allowed | const False | yes |
| context_fact_ids | list[string] | yes |
| context_id | string | yes |
| context_subject_id | string | yes |
| join_rule_id | string | yes |
| link_fact_id | string | yes |
| purpose | const INTERNAL_RESEARCH | yes |
| relationship_strength | enum(FOOTPRINT, PROVIDER_REPORT, MEMBERSHIP) | yes |
| run_id | string | yes |
| status | enum(ELIGIBLE, ABSTAINED) | yes |
| tenant_id | string | yes |

## ContextJoinRule

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ContextJoinRule.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| company_claim_allowed | const False | yes |
| context_predicate | string | yes |
| join_rule_id | string | yes |
| link_kind | enum(FOOTPRINT, PROVIDER_REPORT, MEMBERSHIP) | yes |
| link_object_path | string | yes |
| link_predicate | string | yes |
| maximum_hops | const 1 | yes |
| purpose | const INTERNAL_RESEARCH | yes |
| target_kinds | list[enum(SOFTWARE_PRODUCT, INDUSTRY)] | yes |
| version | string | yes |

## CoverageCheck

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CoverageCheck.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| artifact_id | string \| null | yes |
| resource | string | yes |
| result | enum(OK, ERROR, TIMEOUT, DENIED, NOT_VISITED) | yes |

## CoverageFamilyPlan

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CoverageFamilyPlan.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| contract_status | const SCHEMA_DEFINED | yes |
| live_adapter_status | const NOT_IMPLEMENTED | yes |
| metric_ids | list[string] | yes |
| predicate_ids | list[string] | yes |
| section | integer | yes |
| title | string | yes |

## CoverageRecord

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/CoverageRecord.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| attempt_ids | list[string] | yes |
| checked | list[closed object] | yes |
| checked_at | string | yes |
| coverage_id | string | yes |
| detector_execution_id | string | yes |
| detector_release | string | yes |
| planned_resources | list[string] | yes |
| predicate_ids | list[string] | yes |
| scope_id | string | yes |
| scope_limitations | string | yes |
| source_id | string | yes |
| status | enum(COMPLETE, INCOMPLETE) | yes |
| target | object | yes |
| tenant_id | string | yes |

## DataAccessPolicy

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/DataAccessPolicy.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| allow_personal_data | boolean | yes |
| allow_sensitive_data | boolean | yes |
| approval_ref | string \| null | yes |
| attribution_text | string \| null | yes |
| deletion_cascades | boolean | yes |
| fixture_only | boolean | yes |
| max_derived_retention_seconds | integer | yes |
| max_raw_retention_seconds | integer | yes |
| policy_id | string | yes |
| purposes | list[enum(CAPTURE, RETAIN, DERIVE, LLM_PROCESS, INTERNAL_RESEARCH, OUTREACH, EXPORT)] | yes |
| review_status | enum(UNREVIEWED, APPROVED, REVOKED) | yes |
| reviewed_at | string | yes |
| tenant_ids | list[string] | yes |
| terms_ref | string | yes |
| valid_until | string | yes |
| version | string | yes |

## DestinationDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/DestinationDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| automatic_sending | const False | yes |
| destination_id | string | yes |
| enabled | boolean | yes |
| fixture_only | boolean | yes |
| kind | enum(LOCAL_PREVIEW, CONTACT_HANDOFF) | yes |
| mapping_version | string | yes |
| tenant_id | string | yes |

## DiscussionRecordValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/DiscussionRecordValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| community | string | yes |
| language | string | yes |
| post_key | string | yes |
| published_at | string | yes |
| role | enum(POST, COMMENT) | yes |
| text | string | yes |
| thread_key | string | yes |

## EconomicHypothesisValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/EconomicHypothesisValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| assumptions | list[string] | yes |
| currency | string | yes |
| estimated_amount_minor | integer | yes |
| limitations | list[string] | yes |

## EvidenceLocator

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/EvidenceLocator.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| artifact_id | string | yes |
| end | integer \| null | yes |
| kind | enum(TEXT_SPAN, JSON_POINTER, WHOLE_ARTIFACT) | yes |
| locator_id | string | yes |
| pointer | string \| null | yes |
| quote | string \| null | yes |
| start | integer \| null | yes |

## EvidenceSet

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/EvidenceSet.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| attempt_id | string \| null | yes |
| coverage_id | string \| null | yes |
| directness | enum(RAW, DERIVED, DIAGNOSTIC) | yes |
| evidence_id | string | yes |
| execution_id | string \| null | yes |
| input_fact_ids | list[string] | yes |
| locator_ids | list[string] | yes |
| sample_ids | list[string] | yes |
| tenant_id | string | yes |

## ExecutionRecord

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ExecutionRecord.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| execution_id | string | yes |
| finished_at | string | yes |
| function_id | string | yes |
| function_version | string | yes |
| input_artifact_ids | list[string] | yes |
| input_fact_ids | list[string] | yes |
| input_sample_ids | list[string] | yes |
| input_set_hash | string | yes |
| model_call_id | string \| null | yes |
| output_artifact_ids | list[string] | yes |
| output_fact_ids | list[string] | yes |
| parameters | object | yes |
| run_id | string | yes |
| sample_set_hash | string | yes |
| started_at | string | yes |
| status | enum(COMPLETE, ABSTAINED, FAILED) | yes |
| subject_id | string | yes |
| tenant_id | string | yes |
| terminal_reason | string \| null | yes |

## ExportReceipt

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ExportReceipt.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| actor_id | string | yes |
| automatic_sending | const False | yes |
| completed_at | string \| null | yes |
| destination_id | string | yes |
| export_id | string | yes |
| external_reference | string \| null | yes |
| gate_id | string | yes |
| idempotency_key | string | yes |
| mapping_version | string | yes |
| package | closed object | yes |
| payload_hash | string | yes |
| payload_ref | string \| null | yes |
| recipient_key | string \| null | yes |
| requested_at | string | yes |
| status | enum(PREPARED, CONFIRMED, UNKNOWN, FAILED) | yes |
| tenant_id | string | yes |

## Exposure

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/Exposure.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| accepted_at | string \| null | yes |
| business_send_key | string | yes |
| exposure_id | string | yes |
| package_id | string | yes |
| provider_message_id | string \| null | yes |
| recipient_key | string | yes |
| status | enum(PROVIDER_ACCEPTED, UNKNOWN_DELIVERY, FAILED, BOUNCED) | yes |
| tenant_id | string | yes |

## ExternalIdentifier

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ExternalIdentifier.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| namespace | string | yes |
| value | string | yes |

## Fact

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/Fact.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| binding_id | string \| null | yes |
| confidence | closed object \| null | yes |
| effective_at | string \| null | yes |
| evidence_id | string | yes |
| execution_id | string \| null | yes |
| expires_at | string | yes |
| fact_id | string | yes |
| nature | enum(DIRECT_OBSERVATION, FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT, PROVIDER_ESTIMATE, REGISTRY_RECORD, INFERENCE, DERIVED_MEASUREMENT) | yes |
| object | constrained value | yes |
| observed_at | string | yes |
| predicate_id | string | yes |
| reason | enum(NOT_DETECTED_IN_SCOPE, NOT_CHECKED, FETCH_FAILED, POLICY_BLOCKED, INSUFFICIENT_EVIDENCE, CONFLICT, AMBIGUOUS_ATTRIBUTION, EXTRACTION_FAILED) \| null | yes |
| recorded_at | string | yes |
| run_id | string | yes |
| schema_version | const 4.2.0 | yes |
| scope_id | string | yes |
| source_id | string | yes |
| state | enum(OBSERVED, NOT_FOUND, UNKNOWN) | yes |
| subject_id | string | yes |
| supersedes_fact_id | string \| null | yes |
| target | object | yes |
| tenant_id | string | yes |
| window | closed object \| null | yes |

## FactRequirement

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/FactRequirement.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| allowed_natures | list[enum(DIRECT_OBSERVATION, FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT, PROVIDER_ESTIMATE, REGISTRY_RECORD, INFERENCE, DERIVED_MEASUREMENT)] | yes |
| counting_unit | const DISTINCT_ORIGIN | yes |
| minimum | integer | yes |
| predicate_id | string | yes |
| state | enum(OBSERVED, NOT_FOUND) | yes |

## FingerprintDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/FingerprintDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| authority | enum(CANDIDATE, ACTIVE, DEPRECATED) | yes |
| calibration_ref | string \| null | yes |
| capture_mode | enum(RAW_HTML, RENDERED_DOM, NETWORK_TRACE, DNS, CERTIFICATE_LOG, API_BODY) | yes |
| emits | string | yes |
| fingerprint_id | string | yes |
| fixture_only | boolean | yes |
| implementation_status | enum(REFERENCE_IMPLEMENTED, DESIGN_ONLY) | yes |
| match_value | string | yes |
| negative_fixtures | list[string] | yes |
| operator | enum(SCRIPT_HOST, IFRAME_HOST, FORM_HOST, COOKIE_NAME, HEADER_VALUE, DNS_TARGET, JSON_VALUE, ATTRIBUTE_VALUE) | yes |
| positive_fixtures | list[string] | yes |
| product_subject_id | string | yes |
| version | string | yes |

## FunctionDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/FunctionDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| authority | enum(CANDIDATE, ACTIVE, DEPRECATED) | yes |
| cross_subject_rule | enum(SAME_SUBJECT, SAME_RESEARCH_TARGET, EXPLICIT_RELATION, CONTEXT_ONLY) | yes |
| detector_contract | closed object \| null | yes |
| entrypoint | string \| null | yes |
| fixture_only | boolean | yes |
| function_id | string | yes |
| implementation_status | enum(REFERENCE_IMPLEMENTED, DESIGN_ONLY) | yes |
| input_predicates | list[string] | yes |
| output_predicates | list[string] | yes |
| parameter_schema | object | yes |
| processor | enum(DETERMINISTIC, LLM, HUMAN_REVIEW, DERIVATION) | yes |
| version | string | yes |

## GroundedClause

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/GroundedClause.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| clause_id | string | yes |
| evidence_roles | list[enum(DIRECT, ATTRIBUTED, SCOPED_ABSENCE)] | yes |
| fact_ids | list[string] | yes |
| template_id | string | yes |
| text | string | yes |

## HypothesisValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/HypothesisValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| alternatives | list[string] | yes |
| conclusion | string | yes |
| hypothesis_id | string | yes |
| limitations | list[string] | yes |
| verification_question | string | yes |

## IntakeRequest

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/IntakeRequest.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| idempotency_key | string | yes |
| intake_id | string | yes |
| profile_id | string | yes |
| purpose | enum(KNOWLEDGE, REVIEWED_HANDOFF) | yes |
| received_at | string | yes |
| request_hash | string | yes |
| requester_id | string | yes |
| targets | list[closed object] | yes |
| tenant_id | string | yes |

## IntakeTarget

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/IntakeTarget.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| resource_uri | string | yes |
| subject_id | string \| null | yes |

## JobPostingValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/JobPostingValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| department | string \| null | yes |
| employment_type | enum(FULL_TIME, PART_TIME, CONTRACT, TEMPORARY, INTERNSHIP, OTHER) \| null | yes |
| namespace | string | yes |
| posting_id | string | yes |
| published_at | string \| null | yes |
| title | string | yes |
| url | string | yes |

## LookalikeMatch

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/LookalikeMatch.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| comparison_subject_id | string | yes |
| corpus_release | string | yes |
| differences | list[string] | yes |
| implementation_status | const DESIGN_ONLY | yes |
| index_version | string | yes |
| input_fact_ids | list[string] | yes |
| match_id | string | yes |
| missing_features | list[string] | yes |
| outcome_transfer_allowed | const False | yes |
| representation_version | string | yes |
| run_id | string | yes |
| similarity_score | number | yes |
| target_subject_id | string | yes |
| tenant_id | string | yes |
| use | const INTERNAL_RANKING | yes |

## MeasurementValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/MeasurementValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| denominator | integer \| null | yes |
| dimensions | object | yes |
| method_version | string | yes |
| metric_id | string | yes |
| numerator | integer \| null | yes |
| reporting_timezone | string | yes |
| sample_size | integer \| null | yes |
| uncertainty | closed object \| null | yes |
| unit | string | yes |
| value | number | yes |

## MetricDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/MetricDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| aggregation | enum(COUNT, SUM, MEAN, RATE, RANK, ESTIMATE, DISTRIBUTION, DESCRIPTIVE) | yes |
| allowed_natures | list[enum(DIRECT_OBSERVATION, FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT, PROVIDER_ESTIMATE, REGISTRY_RECORD, INFERENCE, DERIVED_MEASUREMENT)] | yes |
| description | string | yes |
| dimensions_schema | object | yes |
| metric_id | string | yes |
| requires_denominator | boolean | yes |
| section_ids | list[integer] | yes |
| subject_kinds | list[enum(ORG, LOCATION, PERSON, BRAND, WEBSITE, SOFTWARE_PRODUCT, INDUSTRY, JOB_POSTING, APPLICATION, LISTING, COHORT, ANGLE)] | yes |
| unit | string | yes |
| value_schema | object | yes |

## ModelCall

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ModelCall.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| call_id | string | yes |
| input_artifact_ids | list[string] | yes |
| max_repair_attempts | integer | yes |
| model | string | yes |
| output_schema_id | string | yes |
| policy_ids | list[string] | yes |
| prompt_hash | string | yes |
| provider | string | yes |
| request_artifact_id | string | yes |
| response_artifact_id | string \| null | yes |
| status | enum(PARSED, ABSTAINED, FAILED) | yes |
| task_version | string | yes |
| tenant_id | string | yes |
| terminal_reason | string \| null | yes |

## ObjectReferenceRule

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ObjectReferenceRule.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| container | enum(target, object) | yes |
| path | string | yes |
| subject_kinds | list[enum(ORG, LOCATION, PERSON, BRAND, WEBSITE, SOFTWARE_PRODUCT, INDUSTRY, JOB_POSTING, APPLICATION, LISTING, COHORT, ANGLE)] | yes |
| target_type | enum(SUBJECT, FACT, ARTIFACT, LOCATOR) | no |

## OutcomeEvent

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/OutcomeEvent.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| attribution_status | enum(MATCHED, QUARANTINED) | yes |
| event_id | string | yes |
| evidence_id | string | yes |
| exposure_id | string \| null | yes |
| kind | enum(REPLY, MEETING, BOUNCE, UNSUBSCRIBE, DELIVERY_UPDATE) | yes |
| occurred_at | string | yes |
| provider | string | yes |
| provider_event_id | string | yes |
| received_at | string | yes |
| tenant_id | string | yes |

## OutreachPackage

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/OutreachPackage.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| approved_at | string \| null | yes |
| clauses | list[GroundedClause] | yes |
| context_ids | list[string] | yes |
| maturity_fact_id | string \| null | yes |
| package_id | string | yes |
| rendered_text | string | yes |
| review_id | string \| null | yes |
| revision | integer | yes |
| run_id | string | yes |
| send_allowed | const False | yes |
| signal_ids | list[string] | yes |
| status | enum(DRAFT, DESIGN_TEST_APPROVED, APPROVED, WITHHELD) | yes |
| subject_id | string | yes |
| template_id | string | yes |
| tenant_id | string | yes |

## PackageReference

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/PackageReference.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| content_hash | string | yes |
| package_id | string | yes |
| revision | integer | yes |

## PredicateDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/PredicateDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| absence_allowed | boolean | yes |
| allowed_natures | list[enum(DIRECT_OBSERVATION, FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT, PROVIDER_ESTIMATE, REGISTRY_RECORD, INFERENCE, DERIVED_MEASUREMENT)] | yes |
| allowed_processors | list[enum(DETERMINISTIC, LLM, HUMAN_REVIEW, DERIVATION)] | yes |
| copy_policy | enum(DIRECT_SCOPED, ATTRIBUTED_ONLY, ESTIMATE_ATTRIBUTED, REGISTRY_ATTRIBUTED, INTERNAL_ONLY, CONTEXT_ONLY) | yes |
| description | string | yes |
| example_target | object | yes |
| example_value | constrained value | yes |
| family | string | yes |
| origin | enum(V3_RETAINED, V3_REVISED, V4_ADDED) | yes |
| predicate_id | string | yes |
| reference_rules | list[closed object] | yes |
| section_ids | list[integer] | yes |
| subject_kinds | list[enum(ORG, LOCATION, PERSON, BRAND, WEBSITE, SOFTWARE_PRODUCT, INDUSTRY, JOB_POSTING, APPLICATION, LISTING, COHORT, ANGLE)] | yes |
| target_schema | object | yes |
| temporal_mode | enum(POINT, EVENT, PERIOD) | yes |
| value_class | string | yes |
| value_schema | object | yes |
| version | string | yes |

## ProviderBlueprint

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ProviderBlueprint.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| adapter_implemented | const False | yes |
| approval_required | const True | yes |
| blueprint_id | string | yes |
| families | list[string] | yes |
| methods | list[enum(HTTP_CAPTURE, API, DNS, CERTIFICATE_LOG, AUTHORIZED_EXPORT, HUMAN_UPLOAD, DERIVATION)] | yes |
| notes | string | yes |
| provider | string | yes |
| section_ids | list[integer] | yes |
| terms_url | string | yes |

## PublishedRecordValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/PublishedRecordValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| namespace | string | yes |
| published_at | string \| null | yes |
| publisher | string | yes |
| record_id | string | yes |
| record_type | string | yes |
| text | string | yes |
| title | string | yes |
| url | string | yes |

## QuotedTextResult

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/QuotedTextResult.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| text | string | yes |

## RegistryRecordValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/RegistryRecordValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| effective_at | string \| null | yes |
| filed_at | string \| null | yes |
| issuer | string | yes |
| jurisdiction | string | yes |
| namespace | string | yes |
| record_id | string | yes |
| record_status | string | yes |

## RepairAttempt

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/RepairAttempt.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| attempt_id | string | yes |
| call_id | string | yes |
| input_response_artifact_id | string | yes |
| method | enum(DETERMINISTIC_JSON_REPAIR, BOUNDED_MODEL_REPAIR) | yes |
| ordinal | integer | yes |
| output_response_artifact_id | string | yes |
| status | enum(VALID, INVALID) | yes |
| validation_errors | list[string] | yes |

## ResearchPriorValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ResearchPriorValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| classified_eligible_count | integer | yes |
| contradicting_fact_ids | list[string] | yes |
| denominator_definition | const ELIGIBLE_RETRIEVED_RECORDS_INCLUDING_UNCLASSIFIED | yes |
| eligible_count | integer | yes |
| population_claim | const False | yes |
| sample_id | string | yes |
| sample_share | number | yes |
| support_count | integer | yes |
| support_policy_id | string | yes |
| supporting_fact_ids | list[string] | yes |
| theme_id | string | yes |
| unclassified_count | integer | yes |

## ResearchSample

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ResearchSample.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| complete_population | boolean | yes |
| created_at | string | yes |
| dedupe_policy_version | string | yes |
| eligible_artifact_ids | list[string] | yes |
| excluded_artifact_ids | list[string] | yes |
| limitations | list[string] | yes |
| policy_ids | list[string] | yes |
| population_size | integer \| null | yes |
| record_decisions | list[SampleRecordDecision] | yes |
| retrieved_artifact_ids | list[string] | yes |
| sample_id | string | yes |
| sampling_frame | string | yes |
| scope_id | string | yes |
| selection_method | enum(CENSUS, PROVIDER_SAMPLE, QUERY_SAMPLE, CURATED_SAMPLE) | yes |
| subject_id | string | yes |
| support_policy_id | string | yes |
| tenant_id | string | yes |
| theme_id | string | yes |
| window | closed object | yes |

## ResearchSupportPolicy

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ResearchSupportPolicy.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| allowed_sentiments | list[string] | yes |
| allowed_stances | list[string] | yes |
| counting_unit | const DISTINCT_ORIGIN | yes |
| denominator_rule | const ELIGIBLE_RETRIEVED_RECORDS | yes |
| meaning | enum(REPORTED_NEGATIVE_EXPERIENCE, WORKFLOW_MENTION) | yes |
| support_policy_id | string | yes |
| unclassified_policy | const RETAIN_AS_UNMEASURED_NOT_NEGATIVE | yes |
| version | string | yes |

## ReviewDecision

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ReviewDecision.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| action | enum(APPROVE, REJECT, REQUEST_CHANGE) | yes |
| decided_at | string | yes |
| package | closed object | yes |
| policy_version | string | yes |
| reason | string | yes |
| review_id | string | yes |
| reviewer_id | string | yes |
| tenant_id | string | yes |

## ReviewRecordValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ReviewRecordValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| edited | boolean | yes |
| language | string | yes |
| platform | string | yes |
| published_at | string | yes |
| rating | number \| null | yes |
| rating_scale_max | number \| null | yes |
| review_key | string | yes |
| text | string | yes |

## SalaryValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/SalaryValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| basis | enum(BASE, TOTAL_COMPENSATION, UNSPECIFIED) | yes |
| currency | string | yes |
| maximum_minor | integer \| null | yes |
| minimum_minor | integer \| null | yes |
| minor_unit_exponent | integer | yes |
| period | enum(HOUR, DAY, WEEK, MONTH, YEAR, PROJECT) | yes |

## SampleRecordDecision

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/SampleRecordDecision.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| artifact_id | string | yes |
| classification_fact_ids | list[string] | yes |
| reason | string \| null | yes |
| status | enum(SUPPORT, CONTRADICT, NO_THEME, UNCLASSIFIED, EXCLUDED) | yes |

## ScenarioEstimate

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ScenarioEstimate.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| assumptions | list[closed object] | yes |
| currency | string | yes |
| formula_version | string | yes |
| implementation_status | const DESIGN_ONLY | yes |
| limitations | list[string] | yes |
| lower_minor | integer | yes |
| observed_input_fact_ids | list[string] | yes |
| scenario_id | string | yes |
| subject_id | string | yes |
| tenant_id | string | yes |
| time_period | string | yes |
| upper_minor | integer | yes |
| verified_loss | const False | yes |

## Scope

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/Scope.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| capture_mode | enum(RAW_HTML, RENDERED_DOM, NETWORK_TRACE, DNS, CERTIFICATE_LOG, API_BODY, DOCUMENT, HUMAN_RECORD, DERIVED) | yes |
| kind | enum(ELEMENT, PAGE, WEBSITE, PROVIDER_QUERY, AUTHORIZED_SYSTEM, RESEARCH_SAMPLE, REGISTRY_RECORD, OPERATIONS) | yes |
| population_description | string | yes |
| resources | list[string] | yes |
| scope_id | string | yes |
| stable_scope_key | string | yes |
| subject_id | string | yes |
| tenant_id | string | yes |

## SignalDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/SignalDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| context_allowed | boolean | yes |
| description | string | yes |
| function_id | string | yes |
| required_facts | list[closed object] | yes |
| signal_type_id | string | yes |
| status | enum(REFERENCE_IMPLEMENTED, DESIGN_ONLY) | yes |
| version | string | yes |

## SignalEvaluation

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/SignalEvaluation.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| context_ids | list[string] | yes |
| evaluated_at | string | yes |
| input_fact_ids | list[string] | yes |
| reason | enum(THIN_DATA, CONFLICT, POLICY, DNC, CANDIDATE_SOURCE) \| null | yes |
| run_id | string | yes |
| signal_id | string | yes |
| signal_type_id | string | yes |
| status | enum(RESOLVED, UNRESOLVED, SUPPRESSED, CANDIDATE) | yes |
| subject_id | string | yes |
| tenant_id | string | yes |

## SourceDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/SourceDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| acquisition_method | enum(HTTP_CAPTURE, API, DNS, CERTIFICATE_LOG, AUTHORIZED_EXPORT, HUMAN_UPLOAD, DERIVATION) | yes |
| adapter_status | enum(FIXTURE_ONLY, DESIGN_ONLY, IMPLEMENTED) | yes |
| allowed_natures | list[enum(DIRECT_OBSERVATION, FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT, PROVIDER_ESTIMATE, REGISTRY_RECORD, INFERENCE, DERIVED_MEASUREMENT)] | yes |
| authority | enum(CANDIDATE, ACTIVE, DEPRECATED) | yes |
| emits | list[string] | yes |
| fixture_only | boolean | yes |
| freshness_seconds | integer | yes |
| policy_id | string | yes |
| provider | string | yes |
| source_id | string | yes |
| upstream_namespace | string | yes |
| version | string | yes |

## Subject

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/Subject.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| display_name | string | yes |
| external_ids | list[closed object] | yes |
| kind | enum(ORG, LOCATION, PERSON, BRAND, WEBSITE, SOFTWARE_PRODUCT, INDUSTRY, JOB_POSTING, APPLICATION, LISTING, COHORT, ANGLE) | yes |
| subject_id | string | yes |
| tenant_id | string | yes |

## SubjectBinding

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/SubjectBinding.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| artifact_ids | list[string] | yes |
| binding_id | string | yes |
| decided_at | string | yes |
| evidence_locator_ids | list[string] | yes |
| method | string | yes |
| role | enum(FIRST_PARTY, REVIEW_TARGET, REGISTRY_SUBJECT, RESEARCH_TARGET, AGENCY, MENTION_ONLY, UNRESOLVED) | yes |
| scope_id | string | yes |
| status | enum(ACCEPTED, REJECTED, UNRESOLVED) | yes |
| subject_id | string | yes |
| tenant_id | string | yes |

## SurfaceObservationValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/SurfaceObservationValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| observed_value | string | yes |
| surface_key | string | yes |

## TargetResult

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/TargetResult.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| completed_at | string | yes |
| reason | string \| null | yes |
| status | enum(COMPLETE, FAILED, ABSTAINED) | yes |
| subject_id | string | yes |

## TaxonomyTerm

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/TaxonomyTerm.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| label | string | yes |
| parent_id | string \| null | yes |
| scheme_id | string | yes |
| scheme_version | string | yes |
| term_id | string | yes |

## TechnologyReportValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/TechnologyReportValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| product_id | string | yes |
| provider | string | yes |
| provider_detected_at | string \| null | yes |
| reported_version | string \| null | yes |

## TechnologyValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/TechnologyValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| deployment_claim | const PUBLIC_FOOTPRINT_ONLY | yes |
| fingerprint_id | string | yes |
| matched_value | string | yes |
| product_id | string | yes |
| surface | enum(SCRIPT, IFRAME, FORM, NETWORK, COOKIE, HEADER, CSP, DNS, CERTIFICATE, SUBDOMAIN, JSON_LD, ATTRIBUTE) | yes |
| version | string \| null | yes |

## TemplateDefinition

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/TemplateDefinition.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| allowed_natures | list[enum(DIRECT_OBSERVATION, FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT, PROVIDER_ESTIMATE, REGISTRY_RECORD, INFERENCE, DERIVED_MEASUREMENT)] | yes |
| authority | enum(CANDIDATE, ACTIVE, DEPRECATED) | yes |
| maturity_required | boolean | yes |
| mode | enum(OBSERVATION_QUESTION, MATURITY_OFFER) | yes |
| offered_rung | enum(L1, L2, L3) \| null | yes |
| question | string | yes |
| renderer | enum(observed_product_v1, attributed_job_statement_v1, scoped_absence_v1) | yes |
| required_predicate | string | yes |
| review_ref | string | yes |
| template_id | string | yes |
| version | string | yes |

## ThemeClassificationValue

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/ThemeClassificationValue.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| record_key | string | yes |
| sentiment | enum(POSITIVE, NEGATIVE, NEUTRAL, MIXED) | yes |
| stance | enum(EXPERIENCED, ASKED, NEGATED, QUOTED, UNCERTAIN) | yes |
| support_locator_ids | list[string] | yes |
| theme_id | string | yes |

## TimeWindow

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/TimeWindow.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| end | string | yes |
| start | string | yes |

## UseGateDecision

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/UseGateDecision.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| actor_id | string | yes |
| decision | enum(ALLOW, BLOCK) | yes |
| destination_id | string | yes |
| evaluated_at | string | yes |
| gate_id | string | yes |
| package | closed object | yes |
| purpose | enum(PREVIEW_EXPORT, CONTACT_EXPORT) | yes |
| reasons | list[string] | yes |
| recipient_key | string \| null | yes |
| review_id | string | yes |
| tenant_id | string | yes |
| valid_until | string | yes |
| version_vector | string | yes |

## UseRestriction

**Status:** REFERENCE CONTRACT v4.2. **Source:** `canonical/schemas/UseRestriction.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| actor_id | string | yes |
| effective_at | string | yes |
| kind | enum(DNC, HOLD) | yes |
| reason | string | yes |
| recipient_key | string \| null | yes |
| released_at | string \| null | yes |
| released_by | string \| null | yes |
| restriction_id | string | yes |
| subject_id | string | yes |
| tenant_id | string | yes |

## ProgramDefinition

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| program_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| revision | Proposed field; exact schema/cardinality to implement | see source |
| objectives | Proposed field; exact schema/cardinality to implement | see source |
| audience_ref | Proposed field; exact schema/cardinality to implement | see source |
| offer_refs | Proposed field; exact schema/cardinality to implement | see source |
| capability_profile_ref | Proposed field; exact schema/cardinality to implement | see source |
| acquisition_limits | Proposed field; exact schema/cardinality to implement | see source |
| outreach_policy_ref | Proposed field; exact schema/cardinality to implement | see source |
| owner | Proposed field; exact schema/cardinality to implement | see source |
| approval_state | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Program configuration does not assert that accounts satisfy it.

## AudienceDefinition

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| audience_id | Proposed field; exact schema/cardinality to implement | see source |
| revision | Proposed field; exact schema/cardinality to implement | see source |
| account_filters | Proposed field; exact schema/cardinality to implement | see source |
| permitted_geographies | Proposed field; exact schema/cardinality to implement | see source |
| excluded_segments | Proposed field; exact schema/cardinality to implement | see source |
| membership_as_of_policy | Proposed field; exact schema/cardinality to implement | see source |
| selection_reason_codes | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Selections record their input snapshot; broad facts persist even for rejected targets.

## OfferDefinition

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| offer_id | Proposed field; exact schema/cardinality to implement | see source |
| revision | Proposed field; exact schema/cardinality to implement | see source |
| service_line | Proposed field; exact schema/cardinality to implement | see source |
| supported_problem_classes | Proposed field; exact schema/cardinality to implement | see source |
| prerequisites | Proposed field; exact schema/cardinality to implement | see source |
| allowed_template_refs | Proposed field; exact schema/cardinality to implement | see source |
| persona_rules | Proposed field; exact schema/cardinality to implement | see source |
| restrictions | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Named service/offer policy; not proof of prospect pain or an implemented automation playbook catalog.

## AccountSeed

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| seed_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| program_id | Proposed field; exact schema/cardinality to implement | see source |
| discovery_source_ref | Proposed field; exact schema/cardinality to implement | see source |
| original_record_ref | Proposed field; exact schema/cardinality to implement | see source |
| resource_uri | Proposed field; exact schema/cardinality to implement | see source |
| provisional_external_ids | Proposed field; exact schema/cardinality to implement | see source |
| discovered_at | Proposed field; exact schema/cardinality to implement | see source |
| normalization_decision | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Unresolved seeds remain provisional; neither a redirect nor source label proves domain ownership.

## LeadSelection

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| selection_id | Proposed field; exact schema/cardinality to implement | see source |
| program_id | Proposed field; exact schema/cardinality to implement | see source |
| account_ref | Proposed field; exact schema/cardinality to implement | see source |
| input_snapshot_ref | Proposed field; exact schema/cardinality to implement | see source |
| fit_decision | Proposed field; exact schema/cardinality to implement | see source |
| reasons | Proposed field; exact schema/cardinality to implement | see source |
| exclusion_state_refs | Proposed field; exact schema/cardinality to implement | see source |
| selected_at | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Fit and exclusion decisions are not evidence strength or source authority.

## ResearchPlan

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| plan_id | Proposed field; exact schema/cardinality to implement | see source |
| account_ref | Proposed field; exact schema/cardinality to implement | see source |
| intended_predicates | Proposed field; exact schema/cardinality to implement | see source |
| existing_coverage_refs | Proposed field; exact schema/cardinality to implement | see source |
| permitted_source_refs | Proposed field; exact schema/cardinality to implement | see source |
| acquisition_limits | Proposed field; exact schema/cardinality to implement | see source |
| priority_reasons | Proposed field; exact schema/cardinality to implement | see source |
| stopping_rules | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Missing evidence results in a bounded plan or explicit defer, never a fabricated fact.

## ContactProfile

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| contact_profile_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| person_subject_ref | Proposed field; exact schema/cardinality to implement | see source |
| account_relationship_ref | Proposed field; exact schema/cardinality to implement | see source |
| endpoint_refs | Proposed field; exact schema/cardinality to implement | see source |
| source_evidence_refs | Proposed field; exact schema/cardinality to implement | see source |
| role_effective_window | Proposed field; exact schema/cardinality to implement | see source |
| verified_at | Proposed field; exact schema/cardinality to implement | see source |
| retention_policy_ref | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Identifiers, evidence, and operational view remain separate; KN-01 owns canonical identity.

## ContactAssessment

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| assessment_id | Proposed field; exact schema/cardinality to implement | see source |
| contact_profile_ref | Proposed field; exact schema/cardinality to implement | see source |
| opportunity_ref | Proposed field; exact schema/cardinality to implement | see source |
| role_fit | Proposed field; exact schema/cardinality to implement | see source |
| employer_binding_status | Proposed field; exact schema/cardinality to implement | see source |
| endpoint_verification | Proposed field; exact schema/cardinality to implement | see source |
| source_use_state | Proposed field; exact schema/cardinality to implement | see source |
| restrictions_refs | Proposed field; exact schema/cardinality to implement | see source |
| checked_at | Proposed field; exact schema/cardinality to implement | see source |
| reasons | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Deliverable endpoint does not imply appropriate recipient or outreach permission.

## MessageArtifact

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| message_id | Proposed field; exact schema/cardinality to implement | see source |
| revision | Proposed field; exact schema/cardinality to implement | see source |
| package_ref | Proposed field; exact schema/cardinality to implement | see source |
| channel | Proposed field; exact schema/cardinality to implement | see source |
| subject_or_title | Proposed field; exact schema/cardinality to implement | see source |
| body_ref | Proposed field; exact schema/cardinality to implement | see source |
| required_footer_ref | Proposed field; exact schema/cardinality to implement | see source |
| rendered_content_digest | Proposed field; exact schema/cardinality to implement | see source |
| renderer_version | Proposed field; exact schema/cardinality to implement | see source |
| permitted_transformations | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Exact recipient-visible factual content must be reviewed. Channel rendering cannot add unsupported assertions after package review.

## CampaignDefinition

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| campaign_id | Proposed field; exact schema/cardinality to implement | see source |
| revision | Proposed field; exact schema/cardinality to implement | see source |
| program_ref | Proposed field; exact schema/cardinality to implement | see source |
| route_ref | Proposed field; exact schema/cardinality to implement | see source |
| ordered_step_definitions | Proposed field; exact schema/cardinality to implement | see source |
| template_refs | Proposed field; exact schema/cardinality to implement | see source |
| schedule_owner | Proposed field; exact schema/cardinality to implement | see source |
| send_window_policy | Proposed field; exact schema/cardinality to implement | see source |
| timezone_policy | Proposed field; exact schema/cardinality to implement | see source |
| sender_constraints | Proposed field; exact schema/cardinality to implement | see source |
| stop_policy | Proposed field; exact schema/cardinality to implement | see source |
| frequency_caps | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Exactly one scheduler owns progression; campaign activation is separate from creation or review.

## CampaignApproval

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| approval_id | Proposed field; exact schema/cardinality to implement | see source |
| campaign_id | Proposed field; exact schema/cardinality to implement | see source |
| revision | Proposed field; exact schema/cardinality to implement | see source |
| definition_hash | Proposed field; exact schema/cardinality to implement | see source |
| authorized_actor | Proposed field; exact schema/cardinality to implement | see source |
| allowed_mode | Proposed field; exact schema/cardinality to implement | see source |
| approved_at | Proposed field; exact schema/cardinality to implement | see source |
| policy_ref | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Does not substitute for a package ReviewDecision or per-effect current-use/send authorization.

## CampaignReadiness

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| readiness_id | Proposed field; exact schema/cardinality to implement | see source |
| campaign_ref | Proposed field; exact schema/cardinality to implement | see source |
| sender_snapshot_refs | Proposed field; exact schema/cardinality to implement | see source |
| provider_state_refs | Proposed field; exact schema/cardinality to implement | see source |
| compatibility_checks | Proposed field; exact schema/cardinality to implement | see source |
| checked_at | Proposed field; exact schema/cardinality to implement | see source |
| decision | Proposed field; exact schema/cardinality to implement | see source |
| reasons | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Readiness is time-sensitive; provider drift can block dispatch despite prior approval.

## Enrollment

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| enrollment_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| campaign_ref | Proposed field; exact schema/cardinality to implement | see source |
| account_ref | Proposed field; exact schema/cardinality to implement | see source |
| contact_ref | Proposed field; exact schema/cardinality to implement | see source |
| enrollment_policy_ref | Proposed field; exact schema/cardinality to implement | see source |
| state | Proposed field; exact schema/cardinality to implement | see source |
| next_step_id | Proposed field; exact schema/cardinality to implement | see source |
| state_revision | Proposed field; exact schema/cardinality to implement | see source |
| enrolled_at | Proposed field; exact schema/cardinality to implement | see source |
| last_event_ref | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Same recipient/account can be constrained across campaigns. State changes use expected revisions and event identities.

## StepEligibility

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| eligibility_id | Proposed field; exact schema/cardinality to implement | see source |
| enrollment_ref | Proposed field; exact schema/cardinality to implement | see source |
| step_id | Proposed field; exact schema/cardinality to implement | see source |
| due_at | Proposed field; exact schema/cardinality to implement | see source |
| timezone_basis | Proposed field; exact schema/cardinality to implement | see source |
| package_ref | Proposed field; exact schema/cardinality to implement | see source |
| contact_assessment_ref | Proposed field; exact schema/cardinality to implement | see source |
| cap_reservation_ref | Proposed field; exact schema/cardinality to implement | see source |
| state_revision | Proposed field; exact schema/cardinality to implement | see source |
| decision | Proposed field; exact schema/cardinality to implement | see source |
| reasons | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Scheduling eligibility is not SendGateDecision; final current restrictions are checked again before dispatch.

## DeliveryIntent

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| intent_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| enrollment_ref | Proposed field; exact schema/cardinality to implement | see source |
| step_id | Proposed field; exact schema/cardinality to implement | see source |
| recipient_binding_ref | Proposed field; exact schema/cardinality to implement | see source |
| channel | Proposed field; exact schema/cardinality to implement | see source |
| reviewed_message_ref | Proposed field; exact schema/cardinality to implement | see source |
| logical_effect_key | Proposed field; exact schema/cardinality to implement | see source |
| execution_owner | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Stable business intent across retries and code upgrades; altered payload under same effect is an error.

## SendGateDecision

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| gate_id | Proposed field; exact schema/cardinality to implement | see source |
| intent_ref | Proposed field; exact schema/cardinality to implement | see source |
| message_ref | Proposed field; exact schema/cardinality to implement | see source |
| review_ref | Proposed field; exact schema/cardinality to implement | see source |
| campaign_approval_ref | Proposed field; exact schema/cardinality to implement | see source |
| readiness_ref | Proposed field; exact schema/cardinality to implement | see source |
| recipient_ref | Proposed field; exact schema/cardinality to implement | see source |
| current_restriction_vector | Proposed field; exact schema/cardinality to implement | see source |
| current_contact_vector | Proposed field; exact schema/cardinality to implement | see source |
| evaluated_at | Proposed field; exact schema/cardinality to implement | see source |
| valid_until | Proposed field; exact schema/cardinality to implement | see source |
| decision | Proposed field; exact schema/cardinality to implement | see source |
| reasons | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** New proposed family. Existing UseGateDecision supports export purposes only. Recheck immediately before effect; no indefinite gate caching.

## SenderCapabilitySnapshot

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| snapshot_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| sender_account_ref | Proposed field; exact schema/cardinality to implement | see source |
| provider | Proposed field; exact schema/cardinality to implement | see source |
| channel | Proposed field; exact schema/cardinality to implement | see source |
| verified_capabilities | Proposed field; exact schema/cardinality to implement | see source |
| live_state | Proposed field; exact schema/cardinality to implement | see source |
| checked_at | Proposed field; exact schema/cardinality to implement | see source |
| configuration_digest | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Secrets remain protected references; do not assume a provider supports idempotency, cancellation, or exact content preservation.

## DeliveryAttempt

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| attempt_id | Proposed field; exact schema/cardinality to implement | see source |
| intent_ref | Proposed field; exact schema/cardinality to implement | see source |
| gate_ref | Proposed field; exact schema/cardinality to implement | see source |
| request_digest | Proposed field; exact schema/cardinality to implement | see source |
| started_at | Proposed field; exact schema/cardinality to implement | see source |
| finished_at | Proposed field; exact schema/cardinality to implement | see source |
| transport_status | Proposed field; exact schema/cardinality to implement | see source |
| acceptance_status | Proposed field; exact schema/cardinality to implement | see source |
| external_message_ref | Proposed field; exact schema/cardinality to implement | see source |
| error_ref | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Transport completion and remote acceptance are separate; ambiguous acceptance requires reconciliation, not resend.

## Conversation

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| conversation_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| account_ref | Proposed field; exact schema/cardinality to implement | see source |
| contact_refs | Proposed field; exact schema/cardinality to implement | see source |
| provider_account_ref | Proposed field; exact schema/cardinality to implement | see source |
| external_thread_ref | Proposed field; exact schema/cardinality to implement | see source |
| event_refs | Proposed field; exact schema/cardinality to implement | see source |
| enrollment_links | Proposed field; exact schema/cardinality to implement | see source |
| current_owner | Proposed field; exact schema/cardinality to implement | see source |
| state | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Reply chains link exposures without guessing causal attribution for analytics; unmatched events remain visible.

## ReplyAssessment

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| assessment_id | Proposed field; exact schema/cardinality to implement | see source |
| inbound_event_ref | Proposed field; exact schema/cardinality to implement | see source |
| classification_kind | Proposed field; exact schema/cardinality to implement | see source |
| literal_support_refs | Proposed field; exact schema/cardinality to implement | see source |
| producer_execution_ref | Proposed field; exact schema/cardinality to implement | see source |
| confidence_metadata | Proposed field; exact schema/cardinality to implement | see source |
| human_review_state | Proposed field; exact schema/cardinality to implement | see source |
| recommended_action | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Model labels are inferences; pause/opt-out controls do not wait on or take permission from model confidence.

## EnrollmentControl

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| control_id | Proposed field; exact schema/cardinality to implement | see source |
| target_enrollment_refs | Proposed field; exact schema/cardinality to implement | see source |
| cause_event_ref | Proposed field; exact schema/cardinality to implement | see source |
| desired_transition | Proposed field; exact schema/cardinality to implement | see source |
| scope | Proposed field; exact schema/cardinality to implement | see source |
| created_at | Proposed field; exact schema/cardinality to implement | see source |
| expected_state_refs | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** ENG-01 requests stops; CAM-02 applies them idempotently. Authorized restrictions are written separately by PLAT-02.

## FollowUpTask

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| task_id | Proposed field; exact schema/cardinality to implement | see source |
| conversation_ref | Proposed field; exact schema/cardinality to implement | see source |
| assigned_owner | Proposed field; exact schema/cardinality to implement | see source |
| task_kind | Proposed field; exact schema/cardinality to implement | see source |
| due_at | Proposed field; exact schema/cardinality to implement | see source |
| source_event_ref | Proposed field; exact schema/cardinality to implement | see source |
| state | Proposed field; exact schema/cardinality to implement | see source |
| authorization_requirements | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Creating a human task is not authorizing an automated follow-up, referral send, or calendar action.

## SalesHandoff

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| handoff_id | Proposed field; exact schema/cardinality to implement | see source |
| account_ref | Proposed field; exact schema/cardinality to implement | see source |
| contact_ref | Proposed field; exact schema/cardinality to implement | see source |
| conversation_ref | Proposed field; exact schema/cardinality to implement | see source |
| exposure_refs | Proposed field; exact schema/cardinality to implement | see source |
| qualification_notes_refs | Proposed field; exact schema/cardinality to implement | see source |
| intended_owner | Proposed field; exact schema/cardinality to implement | see source |
| meeting_or_next_action | Proposed field; exact schema/cardinality to implement | see source |
| created_at | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** A positive reply is not a confirmed meeting, won sale, or permission to invent additional factual qualifications.

## CRMMapping

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| mapping_id | Proposed field; exact schema/cardinality to implement | see source |
| provider | Proposed field; exact schema/cardinality to implement | see source |
| schema_version | Proposed field; exact schema/cardinality to implement | see source |
| field_ownership | Proposed field; exact schema/cardinality to implement | see source |
| inbound_outbound_transforms | Proposed field; exact schema/cardinality to implement | see source |
| idempotency_policy | Proposed field; exact schema/cardinality to implement | see source |
| suppression_rules | Proposed field; exact schema/cardinality to implement | see source |
| loop_prevention | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Each field has one authority or an explicit merge policy; use versions/receipts, not unrestricted last-write-wins.

## CRMAccountView

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| view_id | Proposed field; exact schema/cardinality to implement | see source |
| account_ref | Proposed field; exact schema/cardinality to implement | see source |
| external_record_links | Proposed field; exact schema/cardinality to implement | see source |
| owner | Proposed field; exact schema/cardinality to implement | see source |
| lifecycle_stage | Proposed field; exact schema/cardinality to implement | see source |
| customer_or_open_deal_state | Proposed field; exact schema/cardinality to implement | see source |
| restriction_observations | Proposed field; exact schema/cardinality to implement | see source |
| provider_version | Proposed field; exact schema/cardinality to implement | see source |
| fetched_at | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Imported pipeline data is a current provider report. Stale critical exclusions cause refresh or hold, not automatic reactivation.

## CRMSyncIntent

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| sync_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| mapping_ref | Proposed field; exact schema/cardinality to implement | see source |
| entity_link | Proposed field; exact schema/cardinality to implement | see source |
| desired_fields | Proposed field; exact schema/cardinality to implement | see source |
| source_record_refs | Proposed field; exact schema/cardinality to implement | see source |
| expected_remote_version | Proposed field; exact schema/cardinality to implement | see source |
| idempotency_key | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** No delivery commands in CRM write retries; emit approved record mutations only.

## CRMSyncReceipt

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| receipt_id | Proposed field; exact schema/cardinality to implement | see source |
| sync_intent_ref | Proposed field; exact schema/cardinality to implement | see source |
| external_record_ref | Proposed field; exact schema/cardinality to implement | see source |
| payload_hash | Proposed field; exact schema/cardinality to implement | see source |
| status | Proposed field; exact schema/cardinality to implement | see source |
| provider_version | Proposed field; exact schema/cardinality to implement | see source |
| confirmed_at | Proposed field; exact schema/cardinality to implement | see source |
| reconciliation_ref | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Record ambiguous writes and reconcile without duplicating tasks or deals; missing data cannot release DNC.

## ExperimentDefinition

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| experiment_id | Proposed field; exact schema/cardinality to implement | see source |
| hypothesis | Proposed field; exact schema/cardinality to implement | see source |
| eligible_population | Proposed field; exact schema/cardinality to implement | see source |
| randomization_or_observational_design | Proposed field; exact schema/cardinality to implement | see source |
| treatment_refs | Proposed field; exact schema/cardinality to implement | see source |
| holdout_policy | Proposed field; exact schema/cardinality to implement | see source |
| outcome_definition | Proposed field; exact schema/cardinality to implement | see source |
| maturity_window | Proposed field; exact schema/cardinality to implement | see source |
| stopping_rule | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Label observational versus randomized designs explicitly; no promised causal conclusions.

## ExperimentAssignment

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| assignment_id | Proposed field; exact schema/cardinality to implement | see source |
| experiment_ref | Proposed field; exact schema/cardinality to implement | see source |
| unit_ref | Proposed field; exact schema/cardinality to implement | see source |
| assigned_variant | Proposed field; exact schema/cardinality to implement | see source |
| assignment_rule_version | Proposed field; exact schema/cardinality to implement | see source |
| assigned_at | Proposed field; exact schema/cardinality to implement | see source |
| exposure_links | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Pin before exposure; deduplicate and track cross-campaign contamination.

## QualityAssessment

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| assessment_id | Proposed field; exact schema/cardinality to implement | see source |
| evaluated_release_refs | Proposed field; exact schema/cardinality to implement | see source |
| gold_set_ref | Proposed field; exact schema/cardinality to implement | see source |
| eligible_sample | Proposed field; exact schema/cardinality to implement | see source |
| observed_metrics | Proposed field; exact schema/cardinality to implement | see source |
| errors | Proposed field; exact schema/cardinality to implement | see source |
| uncertainty | Proposed field; exact schema/cardinality to implement | see source |
| limitations | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Quality outcomes do not alter source authority by themselves; preserve fixture versus live-evaluation distinction.

## PromotionProposal

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| proposal_id | Proposed field; exact schema/cardinality to implement | see source |
| target_definition_ref | Proposed field; exact schema/cardinality to implement | see source |
| assessed_release_ref | Proposed field; exact schema/cardinality to implement | see source |
| quality_assessment_refs | Proposed field; exact schema/cardinality to implement | see source |
| intended_change | Proposed field; exact schema/cardinality to implement | see source |
| reasons | Proposed field; exact schema/cardinality to implement | see source |
| review_requirements | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Proposal only. Authorized governance and release compiler publish a new immutable release for later runs.

## WorkspaceView

**Status:** PROPOSED PRODUCT RECORD. **Source:** `product-design/proposed_product_contracts.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| view_id | Proposed field; exact schema/cardinality to implement | see source |
| tenant_id | Proposed field; exact schema/cardinality to implement | see source |
| view_kind | Proposed field; exact schema/cardinality to implement | see source |
| permitted_record_refs | Proposed field; exact schema/cardinality to implement | see source |
| as_of | Proposed field; exact schema/cardinality to implement | see source |
| redaction_policy_ref | Proposed field; exact schema/cardinality to implement | see source |
| completeness_notes | Proposed field; exact schema/cardinality to implement | see source |

**Invariant:** Read model only; user actions must route through authenticated owning operations.

## Common

**Status:** DRAFT COMMON ENVELOPE. **Source:** `protocol/schemas/Common.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|

## Diagnostic

**Status:** DRAFT COMMON ENVELOPE. **Source:** `protocol/schemas/Diagnostic.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| cause_execution_id | string \| null | yes |
| code | string | yes |
| diagnostic_id | string | yes |
| field_path | string \| null | yes |
| message | string | yes |
| record_refs | list[RecordRef] | yes |
| restricted_details_ref | RecordRef \| null | yes |
| severity | enum(INFO, WARNING, ERROR) | yes |
| suggested_action | enum(NONE, FIX_INPUT, FIX_CONFIGURATION, RETRY_AFTER_POLICY, RECAPTURE, REVIEW, RECONCILE, REAUTHORIZE) | yes |

## ModuleRequest

**Status:** DRAFT COMMON ENVELOPE. **Source:** `protocol/schemas/ModuleRequest.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| attempt | integer | yes |
| budget_reservation_ref | RecordRef \| null | yes |
| context | Context | yes |
| deadline_at | string | yes |
| execution_id | string | yes |
| idempotency_key | string | yes |
| input_refs | list[RecordRef] | yes |
| module_id | string | yes |
| operation | string | yes |
| parameters_ref | RecordRef \| null | yes |
| protocol_version | const 1.0.0-draft.1 | yes |
| release_lock_ref | RecordRef \| null | yes |
| request_id | string | yes |
| trace | Trace | yes |

## ModuleResult

**Status:** DRAFT COMMON ENVELOPE. **Source:** `protocol/schemas/ModuleResult.schema.json`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| consumed_refs | list[RecordRef] | yes |
| context | Context | yes |
| diagnostic_record_refs | list[RecordRef] | yes |
| diagnostics | list[urn:keensight:module-protocol:1.0.0-draft.1:Diagnostic] | yes |
| execution_id | string | yes |
| execution_status | enum(SUCCEEDED, FAILED, SKIPPED, CANCELLED) | yes |
| finished_at | string | yes |
| module_id | string | yes |
| operation | string | yes |
| output_refs | list[RecordRef] | yes |
| protocol_version | const 1.0.0-draft.1 | yes |
| request_digest | string | yes |
| request_id | string | yes |
| reused_execution_id | string \| null | yes |
| started_at | string | yes |
| trace | Trace | yes |
| usage | ResourceUsage | yes |

## CollectorCapture

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| capture_id | See typed dataclass | see source |
| tenant_id | See typed dataclass | see source |
| subject_id | See typed dataclass | see source |
| run_id | See typed dataclass | see source |
| url | See typed dataclass | see source |
| observed_at | See typed dataclass | see source |
| mode | See typed dataclass | see source |
| status_code | See typed dataclass | see source |
| body_sha256 | See typed dataclass | see source |
| body_path | See typed dataclass | see source |
| headers | See typed dataclass | see source |
| complete | See typed dataclass | see source |
| source_id | See typed dataclass | see source |
| limitations | See typed dataclass | see source |
| source_ttl_seconds | See typed dataclass | see source |

## CollectorSurface

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| surface_id | See typed dataclass | see source |
| capture_id | See typed dataclass | see source |
| command_id | See typed dataclass | see source |
| kind | See typed dataclass | see source |
| locator | See typed dataclass | see source |
| value | See typed dataclass | see source |
| context | See typed dataclass | see source |
| attributes | See typed dataclass | see source |

## CollectorCommandResult

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| command_id | See typed dataclass | see source |
| status | See typed dataclass | see source |
| input_ids | See typed dataclass | see source |
| output_ids | See typed dataclass | see source |
| limitations | See typed dataclass | see source |
| details | See typed dataclass | see source |

## CollectorPageEvidence

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| capture | See typed dataclass | see source |
| surfaces | See typed dataclass | see source |
| commands | See typed dataclass | see source |

## CollectorMatch

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| match_id | See typed dataclass | see source |
| rule_id | See typed dataclass | see source |
| rule_digest | See typed dataclass | see source |
| release_digest | See typed dataclass | see source |
| authority | See typed dataclass | see source |
| capture_id | See typed dataclass | see source |
| surface_id | See typed dataclass | see source |
| branch | See typed dataclass | see source |
| predicate | See typed dataclass | see source |
| product_id | See typed dataclass | see source |
| object_value | See typed dataclass | see source |
| evidence_key | See typed dataclass | see source |
| rule_evidence_key | See typed dataclass | see source |
| authored_confidence | See typed dataclass | see source |

## CollectorObservation

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| observation_id | See typed dataclass | see source |
| claim_key | See typed dataclass | see source |
| tenant_id | See typed dataclass | see source |
| subject_id | See typed dataclass | see source |
| predicate | See typed dataclass | see source |
| target | See typed dataclass | see source |
| scope_id | See typed dataclass | see source |
| nature | See typed dataclass | see source |
| state | See typed dataclass | see source |
| object_value | See typed dataclass | see source |
| capture_id | See typed dataclass | see source |
| source_id | See typed dataclass | see source |
| source_group | See typed dataclass | see source |
| observed_at | See typed dataclass | see source |
| expires_at | See typed dataclass | see source |

## CollectorSupportLink

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| observation_id | See typed dataclass | see source |
| match_id | See typed dataclass | see source |

## CollectorClaimView

**Status:** IMPLEMENTED DATACLASS (COLLECTOR). **Source:** `collector/src/keensight_scrapling/core.py`.

| Field | Declared type / interpretation | Required |
|---|---|---|
| claim_key | See typed dataclass | see source |
| predicate | See typed dataclass | see source |
| target | See typed dataclass | see source |
| status | See typed dataclass | see source |
| object_value | See typed dataclass | see source |
| observation_ids | See typed dataclass | see source |
| supporting_match_ids | See typed dataclass | see source |
| eligible_match_ids | See typed dataclass | see source |
| rule_ids | See typed dataclass | see source |
| capture_count | See typed dataclass | see source |
| source_group_count | See typed dataclass | see source |
| evidence_count | See typed dataclass | see source |
| confidence | See typed dataclass | see source |
| confidence_policy | See typed dataclass | see source |

