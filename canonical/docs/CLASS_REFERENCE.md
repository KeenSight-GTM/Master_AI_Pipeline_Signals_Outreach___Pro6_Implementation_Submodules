# Full class reference

Every exported schema and its complete fields. JSON Schema files are normative; tables below are generated.

## AcquisitionAttempt

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `attempt_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `intake_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `source_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `source_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `adapter_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `target` | `Object` | yes | {"required": ["resource_uri", "subject_id"], "additionalProperties": false} |
| `scope_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `request_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `operation_key` | `string` | yes | {"minLength": 1} |
| `started_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `finished_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `status` | `enum` | yes | {"enum": ["SUCCEEDED", "EMPTY_RESULT", "PARTIAL", "TIMEOUT", "FAILED", "POLICY_DENIED", "BUDGET_DENIED", "CANCELLED"]} |
| `artifact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `terminal_reason` | `Optional~enum~` | yes | {"anyOf": [{"enum": ["TIMEOUT", "POLICY_DENIED", "BUDGET_DENIED", "CANCELLED", "PROVIDER_ERROR", "PARTIAL_RESPONSE", "NO_RESULTS"]}, {"type": "null"}]} |
| `pagination` | `enum` | yes | {"enum": ["NOT_APPLICABLE", "EXHAUSTED", "INCOMPLETE", "UNKNOWN"]} |
| `truncated` | `bool` | yes |  |
| `max_requests` | `int` | yes | {"minimum": 1} |
| `requests_made` | `int` | yes | {"minimum": 0} |
| `timeout_seconds` | `int` | yes | {"minimum": 1} |
| `body_limit_bytes` | `int` | yes | {"minimum": 1} |
| `cost_status` | `enum` | yes | {"enum": ["KNOWN", "UNKNOWN", "NOT_CHARGED"]} |
| `cost_minor` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `currency` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Z]{3}$"}, {"type": "null"}]} |
| `execution_mode` | `enum` | yes | {"enum": ["REPLAY_IMPORT", "LIVE_CAPTURE"]} |

## ActorGrant

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `actor_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `permissions` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `fixture_only` | `bool` | yes |  |
| `active` | `bool` | yes |  |

## Artifact

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `artifact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `source_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `scope_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `resource_uri` | `string` | yes | {"format": "uri"} |
| `media_type` | `string` | yes | {"minLength": 1} |
| `content_ref` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `content_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `byte_count` | `int` | yes | {"minimum": 0} |
| `captured_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `published_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `status` | `enum` | yes | {"enum": ["OK", "ERROR", "TIMEOUT", "POLICY_DENIED"]} |
| `truncated` | `bool` | yes |  |
| `retained_until` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `retention_state` | `enum` | yes | {"enum": ["RETAINED", "DELETED", "EXPIRED", "REFERENCE_ONLY"]} |
| `classification` | `enum` | yes | {"enum": ["PUBLIC_BUSINESS", "PERSONAL", "CONFIDENTIAL", "SENSITIVE"]} |
| `origin_namespace` | `string` | yes | {"minLength": 1} |
| `origin_record_id` | `string` | yes | {"minLength": 1} |
| `origin_revision` | `string` | yes | {"minLength": 1} |
| `independence_group` | `string` | yes | {"minLength": 1} |
| `parent_artifact_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## AttributedStatementValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `statement_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `text` | `string` | yes | {"minLength": 1} |
| `topic_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `modality` | `enum` | yes | {"enum": ["CURRENT_STATE", "REQUIREMENT", "ASPIRATION", "NEGATED", "UNCERTAIN"]} |

## BatchRun

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `mode` | `enum` | yes | {"enum": ["DESIGN_TEST", "PRODUCTION"]} |
| `as_of` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `created_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `code_release` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `registry_release` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `profile_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `input_artifact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `input_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `binding_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `status` | `enum` | yes | {"enum": ["OPEN", "COMPLETE", "PARTIAL", "FAILED"]} |
| `approval_policy_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `knowledge_cutoff` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `sealed_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `sample_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `resolution_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `target_results` | `List~TargetResult~` | yes | {"minItems": 1} |
| `produced_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `imported_execution_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `intake_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |

## CalibrationRecord

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `calibration_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `target_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `target_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `evaluation_dataset_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `true_positives` | `int` | yes | {"minimum": 0} |
| `false_positives` | `int` | yes | {"minimum": 0} |
| `measured_precision` | `number` | yes | {"minimum": 0, "maximum": 1} |
| `report_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `fixture_only` | `bool` | yes |  |
| `review_ref` | `string` | yes | {"minLength": 1} |

## CallEventValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `call_key` | `string` | yes | {"minLength": 1} |
| `started_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `direction` | `enum` | yes | {"enum": ["INBOUND", "OUTBOUND"]} |
| `status` | `enum` | yes | {"enum": ["ANSWERED", "MISSED", "ABANDONED", "VOICEMAIL", "UNKNOWN"]} |
| `duration_seconds` | `Optional~number~` | yes | {"anyOf": [{"type": "number", "minimum": 0}, {"type": "null"}]} |
| `callback_of` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |

## CandidateRecord

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `candidate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `artifact_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `proposed_predicate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `proposed_value` | `PredicateValue` | yes |  |
| `reason` | `enum` | yes | {"enum": ["UNREGISTERED_TYPE", "INVALID_VALUE", "UNRESOLVED_BINDING", "UNKNOWN_TAXONOMY"]} |
| `production_eligible` | `bool` | yes | {"const": false} |
| `attempt_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## CapabilityProfile

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `profile_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `production_enabled` | `bool` | yes |  |
| `capture_source_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `fact_predicate_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `execute_function_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `signal_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `template_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `research_context_enabled` | `bool` | yes |  |
| `delivery_enabled` | `bool` | yes | {"const": false} |
| `product_boundary` | `enum` | yes | {"enum": ["KNOWLEDGE", "PREVIEW", "REVIEWED_HANDOFF"]} |
| `export_enabled` | `bool` | yes |  |

## CaseStudyOutcomeValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `case_id` | `string` | yes | {"minLength": 1} |
| `outcome_id` | `string` | yes | {"minLength": 1} |
| `publisher` | `string` | yes | {"minLength": 1} |
| `source_url` | `string` | yes | {"format": "uri"} |
| `reported_quote` | `string` | yes | {"minLength": 1} |
| `metric_name` | `string` | yes | {"minLength": 1} |
| `reported_value` | `number` | yes |  |
| `unit` | `string` | yes | {"minLength": 1} |
| `baseline_value` | `Optional~number~` | yes | {"anyOf": [{"type": "number"}, {"type": "null"}]} |
| `comparison_kind` | `enum` | yes | {"enum": ["ABSOLUTE", "ABSOLUTE_CHANGE", "RELATIVE_CHANGE", "UNSPECIFIED"]} |
| `measurement_window` | `Optional~Object~` | yes | {"anyOf": [{"type": "object", "properties": {"start": {"type": "string", "format": "date-time", "pattern": "Z$"}, "end": {"type": "string", "format": "date-time", "pattern": "Z$"}}, "required": ["start", "end"], "additionalProperties": false}, {"type": "null"}]} |
| `sample_size` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 1}, {"type": "null"}]} |
| `method_description` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `attribution` | `string` | yes | {"const": "PUBLISHER_REPORTED_NOT_CAUSALLY_VERIFIED"} |
| `transfer_to_target_allowed` | `bool` | yes | {"const": false} |

## ChangeRecord

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `change_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `kind` | `enum` | yes | {"enum": ["RETRACTION", "BINDING_CORRECTION", "AUTHORITY_CHANGE", "POLICY_REVOCATION", "ARTIFACT_DELETION"]} |
| `target_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `effective_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `reason` | `string` | yes | {"minLength": 1} |
| `replacement_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## ClaimResolution

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `resolution_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `predicate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `scope_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `target` | `Object` | yes |  |
| `observation_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `accepted_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `status` | `enum` | yes | {"enum": ["KNOWN", "CONFLICT", "UNKNOWN"]} |
| `policy_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `as_of` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `resolved_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |

## ConfidenceAssessment

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `value` | `number` | yes | {"minimum": 0, "maximum": 1} |
| `meaning` | `enum` | yes | {"enum": ["UNCALIBRATED_MODEL_SCORE", "CALIBRATED_PRECISION", "DETERMINISTIC_MATCH"]} |
| `calibration_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## ContextAssessment

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `context_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `account_subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `context_subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `join_rule_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `link_fact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `context_fact_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `relationship_strength` | `enum` | yes | {"enum": ["FOOTPRINT", "PROVIDER_REPORT", "MEMBERSHIP"]} |
| `purpose` | `string` | yes | {"const": "INTERNAL_RESEARCH"} |
| `company_claim_allowed` | `bool` | yes | {"const": false} |
| `status` | `enum` | yes | {"enum": ["ELIGIBLE", "ABSTAINED"]} |

## ContextJoinRule

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `join_rule_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `link_predicate` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `link_object_path` | `string` | yes | {"minLength": 1} |
| `context_predicate` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `target_kinds` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `link_kind` | `enum` | yes | {"enum": ["FOOTPRINT", "PROVIDER_REPORT", "MEMBERSHIP"]} |
| `purpose` | `string` | yes | {"const": "INTERNAL_RESEARCH"} |
| `maximum_hops` | `int` | yes | {"const": 1} |
| `company_claim_allowed` | `bool` | yes | {"const": false} |

## CoverageCheck

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `resource` | `string` | yes | {"minLength": 1} |
| `artifact_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `result` | `enum` | yes | {"enum": ["OK", "ERROR", "TIMEOUT", "DENIED", "NOT_VISITED"]} |

## CoverageFamilyPlan

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `section` | `int` | yes | {"minimum": 1, "maximum": 11} |
| `title` | `string` | yes | {"minLength": 1} |
| `predicate_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `metric_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `contract_status` | `string` | yes | {"const": "SCHEMA_DEFINED"} |
| `live_adapter_status` | `string` | yes | {"const": "NOT_IMPLEMENTED"} |

## CoverageRecord

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `coverage_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `scope_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `source_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `predicate_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `target` | `Object` | yes |  |
| `planned_resources` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `checked` | `List~Object~` | yes | {"minItems": 1} |
| `status` | `enum` | yes | {"enum": ["COMPLETE", "INCOMPLETE"]} |
| `checked_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `detector_release` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `scope_limitations` | `string` | yes | {"minLength": 1} |
| `attempt_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `detector_execution_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |

## DataAccessPolicy

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `policy_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `review_status` | `enum` | yes | {"enum": ["UNREVIEWED", "APPROVED", "REVOKED"]} |
| `fixture_only` | `bool` | yes |  |
| `approval_ref` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `terms_ref` | `string` | yes | {"format": "uri"} |
| `reviewed_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `valid_until` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `purposes` | `List~enum~` | yes | {"minItems": 0, "uniqueItems": true} |
| `max_raw_retention_seconds` | `int` | yes | {"minimum": 0} |
| `max_derived_retention_seconds` | `int` | yes | {"minimum": 0} |
| `attribution_text` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `allow_personal_data` | `bool` | yes |  |
| `allow_sensitive_data` | `bool` | yes |  |
| `deletion_cascades` | `bool` | yes |  |

## DestinationDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `destination_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `mapping_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `kind` | `enum` | yes | {"enum": ["LOCAL_PREVIEW", "CONTACT_HANDOFF"]} |
| `fixture_only` | `bool` | yes |  |
| `enabled` | `bool` | yes |  |
| `automatic_sending` | `bool` | yes | {"const": false} |

## DiscussionRecordValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `post_key` | `string` | yes | {"minLength": 1} |
| `community` | `string` | yes | {"minLength": 1} |
| `thread_key` | `string` | yes | {"minLength": 1} |
| `published_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `text` | `string` | yes | {"minLength": 1} |
| `language` | `string` | yes | {"minLength": 1} |
| `role` | `enum` | yes | {"enum": ["POST", "COMMENT"]} |

## EconomicHypothesisValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `currency` | `string` | yes | {"pattern": "^[A-Z]{3}$"} |
| `estimated_amount_minor` | `int` | yes | {"minimum": 0} |
| `assumptions` | `List~string~` | yes | {"minItems": 1} |
| `limitations` | `List~string~` | yes | {"minItems": 1} |

## EvidenceLocator

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `locator_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `artifact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `kind` | `enum` | yes | {"enum": ["TEXT_SPAN", "JSON_POINTER", "WHOLE_ARTIFACT"]} |
| `start` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `end` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `pointer` | `Optional~string~` | yes | {"anyOf": [{"type": "string"}, {"type": "null"}]} |
| `quote` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |

## EvidenceSet

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `evidence_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `locator_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `input_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `execution_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `coverage_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `directness` | `enum` | yes | {"enum": ["RAW", "DERIVED", "DIAGNOSTIC"]} |
| `attempt_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `sample_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |

## ExecutionRecord

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `execution_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `function_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `function_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `input_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `input_artifact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `output_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `input_set_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `parameters` | `Object` | yes |  |
| `started_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `finished_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `status` | `enum` | yes | {"enum": ["COMPLETE", "ABSTAINED", "FAILED"]} |
| `model_call_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `input_sample_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `sample_set_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `terminal_reason` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |

## ExportReceipt

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `export_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `package` | `Object` | yes | {"required": ["package_id", "revision", "content_hash"], "additionalProperties": false} |
| `gate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `destination_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `mapping_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `actor_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `recipient_key` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `payload_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `payload_ref` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `idempotency_key` | `string` | yes | {"minLength": 1} |
| `requested_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `completed_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `status` | `enum` | yes | {"enum": ["PREPARED", "CONFIRMED", "UNKNOWN", "FAILED"]} |
| `external_reference` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `automatic_sending` | `bool` | yes | {"const": false} |

## Exposure

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `exposure_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `package_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `business_send_key` | `string` | yes | {"minLength": 1} |
| `provider_message_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `recipient_key` | `string` | yes | {"minLength": 1} |
| `accepted_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `status` | `enum` | yes | {"enum": ["PROVIDER_ACCEPTED", "UNKNOWN_DELIVERY", "FAILED", "BOUNCED"]} |

## ExternalIdentifier

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `namespace` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `value` | `string` | yes | {"minLength": 1} |

## Fact

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `schema_version` | `string` | yes | {"const": "4.1.0"} |
| `fact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `predicate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `target` | `Object` | yes |  |
| `scope_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `state` | `enum` | yes | {"enum": ["OBSERVED", "NOT_FOUND", "UNKNOWN"]} |
| `object` | `PredicateValue` | yes |  |
| `nature` | `enum` | yes | {"enum": ["DIRECT_OBSERVATION", "FIRST_PARTY_STATEMENT", "THIRD_PARTY_REPORT", "PROVIDER_ESTIMATE", "REGISTRY_RECORD", "INFERENCE", "DERIVED_MEASUREMENT"]} |
| `source_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `binding_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `evidence_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `execution_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `observed_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `recorded_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `effective_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `window` | `Optional~Object~` | yes | {"anyOf": [{"type": "object", "properties": {"start": {"type": "string", "format": "date-time", "pattern": "Z$"}, "end": {"type": "string", "format": "date-time", "pattern": "Z$"}}, "required": ["start", "end"], "additionalProperties": false}, {"type": "null"}]} |
| `reason` | `Optional~enum~` | yes | {"anyOf": [{"enum": ["NOT_DETECTED_IN_SCOPE", "NOT_CHECKED", "FETCH_FAILED", "POLICY_BLOCKED", "INSUFFICIENT_EVIDENCE", "CONFLICT", "AMBIGUOUS_ATTRIBUTION", "EXTRACTION_FAILED"]}, {"type": "null"}]} |
| `expires_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `confidence` | `Optional~Object~` | yes | {"anyOf": [{"type": "object", "properties": {"value": {"type": "number", "minimum": 0, "maximum": 1}, "meaning": {"enum": ["UNCALIBRATED_MODEL_SCORE", "CALIBRATED_PRECISION", "DETERMINISTIC_MATCH"]}, "calibration_id": {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]}}, "required": ["value", "meaning", "calibration_id"], "additionalProperties": false}, {"type": "null"}]} |
| `supersedes_fact_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## FactRequirement

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `predicate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `allowed_natures` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `state` | `enum` | yes | {"enum": ["OBSERVED", "NOT_FOUND"]} |
| `minimum` | `int` | yes | {"minimum": 1} |
| `counting_unit` | `string` | yes | {"const": "DISTINCT_ORIGIN"} |

## FingerprintDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `fingerprint_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `authority` | `enum` | yes | {"enum": ["CANDIDATE", "ACTIVE", "DEPRECATED"]} |
| `fixture_only` | `bool` | yes |  |
| `product_subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `emits` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `capture_mode` | `enum` | yes | {"enum": ["RAW_HTML", "RENDERED_DOM", "NETWORK_TRACE", "DNS", "CERTIFICATE_LOG", "API_BODY"]} |
| `operator` | `enum` | yes | {"enum": ["SCRIPT_HOST", "IFRAME_HOST", "FORM_HOST", "COOKIE_NAME", "HEADER_VALUE", "DNS_TARGET", "JSON_VALUE", "ATTRIBUTE_VALUE"]} |
| `match_value` | `string` | yes | {"minLength": 1} |
| `positive_fixtures` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `negative_fixtures` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `calibration_ref` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `implementation_status` | `enum` | yes | {"enum": ["REFERENCE_IMPLEMENTED", "DESIGN_ONLY"]} |

## FunctionDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `function_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `processor` | `enum` | yes | {"enum": ["DETERMINISTIC", "LLM", "HUMAN_REVIEW", "DERIVATION"]} |
| `authority` | `enum` | yes | {"enum": ["CANDIDATE", "ACTIVE", "DEPRECATED"]} |
| `fixture_only` | `bool` | yes |  |
| `input_predicates` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `output_predicates` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `parameter_schema` | `Object` | yes |  |
| `cross_subject_rule` | `enum` | yes | {"enum": ["SAME_SUBJECT", "SAME_RESEARCH_TARGET", "EXPLICIT_RELATION", "CONTEXT_ONLY"]} |
| `implementation_status` | `enum` | yes | {"enum": ["REFERENCE_IMPLEMENTED", "DESIGN_ONLY"]} |
| `entrypoint` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `detector_contract` | `Optional~Object~` | yes | {"anyOf": [{"type": "object", "properties": {"capture_modes": {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1, "uniqueItems": true}, "predicate_ids": {"type": "array", "items": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, "minItems": 1, "uniqueItems": true}, "operator": {"type": "string", "minLength": 1}}, "required": ["capture_modes", "predicate_ids", "operator"], "additionalProperties": false}, {"type": "null"}]} |

## GroundedClause

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `clause_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `fact_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `template_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `text` | `string` | yes | {"minLength": 1} |
| `evidence_roles` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |

## HypothesisValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `hypothesis_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `conclusion` | `string` | yes | {"minLength": 1} |
| `alternatives` | `List~string~` | yes | {"minItems": 1} |
| `limitations` | `List~string~` | yes | {"minItems": 1} |
| `verification_question` | `string` | yes | {"minLength": 1} |

## IntakeRequest

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `intake_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `requester_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `profile_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `purpose` | `enum` | yes | {"enum": ["KNOWLEDGE", "REVIEWED_HANDOFF"]} |
| `targets` | `List~Object~` | yes | {"minItems": 1} |
| `received_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `request_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `idempotency_key` | `string` | yes | {"minLength": 1} |

## IntakeTarget

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `resource_uri` | `string` | yes | {"format": "uri"} |
| `subject_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## JobPostingValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `posting_id` | `string` | yes | {"minLength": 1} |
| `namespace` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `url` | `string` | yes | {"format": "uri"} |
| `title` | `string` | yes | {"minLength": 1} |
| `department` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `published_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `employment_type` | `Optional~enum~` | yes | {"anyOf": [{"enum": ["FULL_TIME", "PART_TIME", "CONTRACT", "TEMPORARY", "INTERNSHIP", "OTHER"]}, {"type": "null"}]} |

## LookalikeMatch

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `match_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `target_subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `comparison_subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `input_fact_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `corpus_release` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `representation_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `index_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `similarity_score` | `number` | yes |  |
| `missing_features` | `List~string~` | yes | {"minItems": 0} |
| `differences` | `List~string~` | yes | {"minItems": 1} |
| `outcome_transfer_allowed` | `bool` | yes | {"const": false} |
| `use` | `string` | yes | {"const": "INTERNAL_RANKING"} |
| `implementation_status` | `string` | yes | {"const": "DESIGN_ONLY"} |

## MeasurementValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `metric_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `value` | `number` | yes |  |
| `unit` | `string` | yes | {"minLength": 1} |
| `dimensions` | `Object` | yes |  |
| `method_version` | `string` | yes | {"minLength": 1} |
| `reporting_timezone` | `string` | yes | {"minLength": 1} |
| `numerator` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `denominator` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `sample_size` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `uncertainty` | `Optional~Object~` | yes | {"anyOf": [{"type": "object", "properties": {"lower": {"type": "number"}, "upper": {"type": "number"}, "method": {"type": "string", "minLength": 1}}, "required": ["lower", "upper", "method"], "additionalProperties": false}, {"type": "null"}]} |

## MetricDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `metric_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `description` | `string` | yes | {"minLength": 1} |
| `unit` | `string` | yes | {"minLength": 1} |
| `value_schema` | `Object` | yes |  |
| `dimensions_schema` | `Object` | yes |  |
| `requires_denominator` | `bool` | yes |  |
| `aggregation` | `enum` | yes | {"enum": ["COUNT", "SUM", "MEAN", "RATE", "RANK", "ESTIMATE", "DISTRIBUTION", "DESCRIPTIVE"]} |
| `allowed_natures` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `subject_kinds` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `section_ids` | `List~int~` | yes | {"minItems": 1, "uniqueItems": true} |

## ModelCall

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `call_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `task_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `provider` | `string` | yes | {"minLength": 1} |
| `model` | `string` | yes | {"minLength": 1} |
| `prompt_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `output_schema_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `input_artifact_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `request_artifact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `response_artifact_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `policy_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `max_repair_attempts` | `int` | yes | {"minimum": 0, "maximum": 2} |
| `status` | `enum` | yes | {"enum": ["PARSED", "ABSTAINED", "FAILED"]} |
| `terminal_reason` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |

## ObjectReferenceRule

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `container` | `enum` | yes | {"enum": ["target", "object"]} |
| `path` | `string` | yes | {"minLength": 1} |
| `subject_kinds` | `List~enum~` | yes | {"minItems": 0, "uniqueItems": true} |
| `target_type` | `enum` | no | {"enum": ["SUBJECT", "FACT", "ARTIFACT", "LOCATOR"]} |

## OutcomeEvent

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `event_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `provider` | `string` | yes | {"minLength": 1} |
| `provider_event_id` | `string` | yes | {"minLength": 1} |
| `exposure_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `occurred_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `received_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `kind` | `enum` | yes | {"enum": ["REPLY", "MEETING", "BOUNCE", "UNSUBSCRIBE", "DELIVERY_UPDATE"]} |
| `attribution_status` | `enum` | yes | {"enum": ["MATCHED", "QUARANTINED"]} |
| `evidence_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |

## OutreachPackage

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `package_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `revision` | `int` | yes | {"minimum": 1} |
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `template_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `clauses` | `List~GroundedClause~` | yes | {"minItems": 1} |
| `signal_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `context_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `maturity_fact_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `status` | `enum` | yes | {"enum": ["DRAFT", "DESIGN_TEST_APPROVED", "APPROVED", "WITHHELD"]} |
| `rendered_text` | `string` | yes | {"minLength": 1} |
| `approved_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `send_allowed` | `bool` | yes | {"const": false} |
| `review_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## PackageReference

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `package_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `revision` | `int` | yes | {"minimum": 1} |
| `content_hash` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |

## PredicateDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `predicate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `family` | `string` | yes | {"minLength": 1} |
| `description` | `string` | yes | {"minLength": 1} |
| `subject_kinds` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `target_schema` | `Object` | yes |  |
| `value_schema` | `Object` | yes |  |
| `allowed_natures` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `allowed_processors` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `absence_allowed` | `bool` | yes |  |
| `temporal_mode` | `enum` | yes | {"enum": ["POINT", "EVENT", "PERIOD"]} |
| `copy_policy` | `enum` | yes | {"enum": ["DIRECT_SCOPED", "ATTRIBUTED_ONLY", "ESTIMATE_ATTRIBUTED", "REGISTRY_ATTRIBUTED", "INTERNAL_ONLY", "CONTEXT_ONLY"]} |
| `reference_rules` | `List~Object~` | yes | {"minItems": 0} |
| `section_ids` | `List~int~` | yes | {"minItems": 0, "uniqueItems": true} |
| `value_class` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `origin` | `enum` | yes | {"enum": ["V3_RETAINED", "V3_REVISED", "V4_ADDED"]} |
| `example_target` | `Object` | yes |  |
| `example_value` | `PredicateValue` | yes |  |

## ProviderBlueprint

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `blueprint_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `provider` | `string` | yes | {"minLength": 1} |
| `section_ids` | `List~int~` | yes | {"minItems": 1, "uniqueItems": true} |
| `families` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `methods` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `terms_url` | `string` | yes | {"format": "uri"} |
| `approval_required` | `bool` | yes | {"const": true} |
| `adapter_implemented` | `bool` | yes | {"const": false} |
| `notes` | `string` | yes | {"minLength": 1} |

## PublishedRecordValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `namespace` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `record_id` | `string` | yes | {"minLength": 1} |
| `url` | `string` | yes | {"format": "uri"} |
| `publisher` | `string` | yes | {"minLength": 1} |
| `published_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `record_type` | `string` | yes | {"minLength": 1} |
| `title` | `string` | yes | {"minLength": 1} |
| `text` | `string` | yes | {"minLength": 1} |

## QuotedTextResult

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `text` | `string` | yes | {"minLength": 1} |

## RegistryRecordValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `namespace` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `record_id` | `string` | yes | {"minLength": 1} |
| `issuer` | `string` | yes | {"minLength": 1} |
| `jurisdiction` | `string` | yes | {"minLength": 1} |
| `effective_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `filed_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `record_status` | `string` | yes | {"minLength": 1} |

## RepairAttempt

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `attempt_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `call_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `ordinal` | `int` | yes | {"minimum": 1, "maximum": 2} |
| `input_response_artifact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `output_response_artifact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `method` | `enum` | yes | {"enum": ["DETERMINISTIC_JSON_REPAIR", "BOUNDED_MODEL_REPAIR"]} |
| `status` | `enum` | yes | {"enum": ["VALID", "INVALID"]} |
| `validation_errors` | `List~string~` | yes | {"minItems": 0} |

## ResearchPriorValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `sample_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `theme_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `supporting_fact_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `contradicting_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `support_count` | `int` | yes | {"minimum": 0} |
| `eligible_count` | `int` | yes | {"minimum": 1} |
| `sample_share` | `number` | yes | {"minimum": 0, "maximum": 1} |
| `population_claim` | `bool` | yes | {"const": false} |
| `support_policy_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `classified_eligible_count` | `int` | yes | {"minimum": 0} |
| `unclassified_count` | `int` | yes | {"minimum": 0} |
| `denominator_definition` | `string` | yes | {"const": "ELIGIBLE_RETRIEVED_RECORDS_INCLUDING_UNCLASSIFIED"} |

## ResearchSample

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `sample_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `scope_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `window` | `Object` | yes | {"required": ["start", "end"], "additionalProperties": false} |
| `sampling_frame` | `string` | yes | {"minLength": 1} |
| `selection_method` | `enum` | yes | {"enum": ["CENSUS", "PROVIDER_SAMPLE", "QUERY_SAMPLE", "CURATED_SAMPLE"]} |
| `retrieved_artifact_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `eligible_artifact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `excluded_artifact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `dedupe_policy_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `population_size` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `complete_population` | `bool` | yes |  |
| `limitations` | `List~string~` | yes | {"minItems": 1} |
| `policy_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `support_policy_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `theme_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `record_decisions` | `List~SampleRecordDecision~` | yes | {"minItems": 1} |
| `created_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |

## ResearchSupportPolicy

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `support_policy_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `meaning` | `enum` | yes | {"enum": ["REPORTED_NEGATIVE_EXPERIENCE", "WORKFLOW_MENTION"]} |
| `allowed_stances` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `allowed_sentiments` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `counting_unit` | `string` | yes | {"const": "DISTINCT_ORIGIN"} |
| `denominator_rule` | `string` | yes | {"const": "ELIGIBLE_RETRIEVED_RECORDS"} |
| `unclassified_policy` | `string` | yes | {"const": "RETAIN_AS_UNMEASURED_NOT_NEGATIVE"} |

## ReviewDecision

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `review_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `reviewer_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `package` | `Object` | yes | {"required": ["package_id", "revision", "content_hash"], "additionalProperties": false} |
| `action` | `enum` | yes | {"enum": ["APPROVE", "REJECT", "REQUEST_CHANGE"]} |
| `reason` | `string` | yes | {"minLength": 1} |
| `decided_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `policy_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |

## ReviewRecordValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `review_key` | `string` | yes | {"minLength": 1} |
| `platform` | `string` | yes | {"minLength": 1} |
| `published_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `rating` | `Optional~number~` | yes | {"anyOf": [{"type": "number", "minimum": 0}, {"type": "null"}]} |
| `rating_scale_max` | `Optional~number~` | yes | {"anyOf": [{"type": "number", "minimum": 0}, {"type": "null"}]} |
| `text` | `string` | yes | {"minLength": 1} |
| `language` | `string` | yes | {"minLength": 1} |
| `edited` | `bool` | yes |  |

## SalaryValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `minimum_minor` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `maximum_minor` | `Optional~int~` | yes | {"anyOf": [{"type": "integer", "minimum": 0}, {"type": "null"}]} |
| `currency` | `string` | yes | {"pattern": "^[A-Z]{3}$"} |
| `minor_unit_exponent` | `int` | yes | {"minimum": 0, "maximum": 4} |
| `period` | `enum` | yes | {"enum": ["HOUR", "DAY", "WEEK", "MONTH", "YEAR", "PROJECT"]} |
| `basis` | `enum` | yes | {"enum": ["BASE", "TOTAL_COMPENSATION", "UNSPECIFIED"]} |

## SampleRecordDecision

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `artifact_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `status` | `enum` | yes | {"enum": ["SUPPORT", "CONTRADICT", "NO_THEME", "UNCLASSIFIED", "EXCLUDED"]} |
| `classification_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `reason` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |

## ScenarioEstimate

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `scenario_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `observed_input_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `assumptions` | `List~Object~` | yes | {"minItems": 1} |
| `formula_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `currency` | `string` | yes | {"pattern": "^[A-Z]{3}$"} |
| `lower_minor` | `int` | yes | {"minimum": 0} |
| `upper_minor` | `int` | yes | {"minimum": 0} |
| `time_period` | `string` | yes | {"minLength": 1} |
| `limitations` | `List~string~` | yes | {"minItems": 1} |
| `verified_loss` | `bool` | yes | {"const": false} |
| `implementation_status` | `string` | yes | {"const": "DESIGN_ONLY"} |

## Scope

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `scope_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `kind` | `enum` | yes | {"enum": ["ELEMENT", "PAGE", "WEBSITE", "PROVIDER_QUERY", "AUTHORIZED_SYSTEM", "RESEARCH_SAMPLE", "REGISTRY_RECORD", "OPERATIONS"]} |
| `resources` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `capture_mode` | `enum` | yes | {"enum": ["RAW_HTML", "RENDERED_DOM", "NETWORK_TRACE", "DNS", "CERTIFICATE_LOG", "API_BODY", "DOCUMENT", "HUMAN_RECORD", "DERIVED"]} |
| `population_description` | `string` | yes | {"minLength": 1} |
| `stable_scope_key` | `string` | yes | {"minLength": 1} |

## SignalDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `signal_type_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `required_facts` | `List~Object~` | yes | {"minItems": 1} |
| `function_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `context_allowed` | `bool` | yes |  |
| `description` | `string` | yes | {"minLength": 1} |
| `status` | `enum` | yes | {"enum": ["REFERENCE_IMPLEMENTED", "DESIGN_ONLY"]} |

## SignalEvaluation

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `signal_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `run_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `signal_type_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `input_fact_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `context_ids` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |
| `status` | `enum` | yes | {"enum": ["RESOLVED", "UNRESOLVED", "SUPPRESSED", "CANDIDATE"]} |
| `reason` | `Optional~enum~` | yes | {"anyOf": [{"enum": ["THIN_DATA", "CONFLICT", "POLICY", "DNC", "CANDIDATE_SOURCE"]}, {"type": "null"}]} |
| `evaluated_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |

## SourceDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `source_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `provider` | `string` | yes | {"minLength": 1} |
| `acquisition_method` | `enum` | yes | {"enum": ["HTTP_CAPTURE", "API", "DNS", "CERTIFICATE_LOG", "AUTHORIZED_EXPORT", "HUMAN_UPLOAD", "DERIVATION"]} |
| `authority` | `enum` | yes | {"enum": ["CANDIDATE", "ACTIVE", "DEPRECATED"]} |
| `fixture_only` | `bool` | yes |  |
| `policy_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `emits` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `allowed_natures` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `freshness_seconds` | `int` | yes | {"minimum": 1} |
| `adapter_status` | `enum` | yes | {"enum": ["FIXTURE_ONLY", "DESIGN_ONLY", "IMPLEMENTED"]} |
| `upstream_namespace` | `string` | yes | {"minLength": 1} |

## Subject

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `kind` | `enum` | yes | {"enum": ["ORG", "LOCATION", "PERSON", "BRAND", "WEBSITE", "SOFTWARE_PRODUCT", "INDUSTRY", "JOB_POSTING", "APPLICATION", "LISTING", "COHORT", "ANGLE"]} |
| `display_name` | `string` | yes | {"minLength": 1} |
| `external_ids` | `List~Object~` | yes | {"minItems": 0, "uniqueItems": true} |

## SubjectBinding

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `binding_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `scope_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `artifact_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |
| `role` | `enum` | yes | {"enum": ["FIRST_PARTY", "REVIEW_TARGET", "REGISTRY_SUBJECT", "RESEARCH_TARGET", "AGENCY", "MENTION_ONLY", "UNRESOLVED"]} |
| `status` | `enum` | yes | {"enum": ["ACCEPTED", "REJECTED", "UNRESOLVED"]} |
| `method` | `string` | yes | {"minLength": 1} |
| `decided_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `evidence_locator_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |

## SurfaceObservationValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `surface_key` | `string` | yes | {"minLength": 1} |
| `observed_value` | `string` | yes | {"minLength": 1} |

## TargetResult

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `status` | `enum` | yes | {"enum": ["COMPLETE", "FAILED", "ABSTAINED"]} |
| `completed_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `reason` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |

## TaxonomyTerm

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `term_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `scheme_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `scheme_version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `label` | `string` | yes | {"minLength": 1} |
| `parent_id` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |

## TechnologyReportValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `product_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `provider` | `string` | yes | {"minLength": 1} |
| `provider_detected_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `reported_version` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |

## TechnologyValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `product_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `surface` | `enum` | yes | {"enum": ["SCRIPT", "IFRAME", "FORM", "NETWORK", "COOKIE", "HEADER", "CSP", "DNS", "CERTIFICATE", "SUBDOMAIN", "JSON_LD", "ATTRIBUTE"]} |
| `matched_value` | `string` | yes | {"minLength": 1} |
| `fingerprint_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `deployment_claim` | `string` | yes | {"const": "PUBLIC_FOOTPRINT_ONLY"} |

## TemplateDefinition

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `template_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `version` | `string` | yes | {"pattern": "^\\d+\\.\\d+\\.\\d+$"} |
| `authority` | `enum` | yes | {"enum": ["CANDIDATE", "ACTIVE", "DEPRECATED"]} |
| `mode` | `enum` | yes | {"enum": ["OBSERVATION_QUESTION", "MATURITY_OFFER"]} |
| `required_predicate` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `allowed_natures` | `List~enum~` | yes | {"minItems": 1, "uniqueItems": true} |
| `renderer` | `enum` | yes | {"enum": ["observed_product_v1", "attributed_job_statement_v1", "scoped_absence_v1"]} |
| `question` | `string` | yes | {"minLength": 1} |
| `maturity_required` | `bool` | yes |  |
| `offered_rung` | `Optional~enum~` | yes | {"anyOf": [{"enum": ["L1", "L2", "L3"]}, {"type": "null"}]} |
| `review_ref` | `string` | yes | {"minLength": 1} |

## ThemeClassificationValue

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `theme_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `record_key` | `string` | yes | {"minLength": 1} |
| `sentiment` | `enum` | yes | {"enum": ["POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED"]} |
| `stance` | `enum` | yes | {"enum": ["EXPERIENCED", "ASKED", "NEGATED", "QUOTED", "UNCERTAIN"]} |
| `support_locator_ids` | `List~string~` | yes | {"minItems": 1, "uniqueItems": true} |

## TimeWindow

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `start` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `end` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |

## UseGateDecision

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `gate_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `package` | `Object` | yes | {"required": ["package_id", "revision", "content_hash"], "additionalProperties": false} |
| `review_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `actor_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `purpose` | `enum` | yes | {"enum": ["PREVIEW_EXPORT", "CONTACT_EXPORT"]} |
| `destination_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `recipient_key` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `evaluated_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `valid_until` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `version_vector` | `string` | yes | {"pattern": "^sha256:[a-f0-9]{64}$"} |
| `decision` | `enum` | yes | {"enum": ["ALLOW", "BLOCK"]} |
| `reasons` | `List~string~` | yes | {"minItems": 0, "uniqueItems": true} |

## UseRestriction

| Field | Type | Required | Constraints / semantics |
|---|---|---|---|
| `restriction_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `tenant_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `subject_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `recipient_key` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]} |
| `kind` | `enum` | yes | {"enum": ["DNC", "HOLD"]} |
| `actor_id` | `string` | yes | {"pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"} |
| `effective_at` | `string` | yes | {"format": "date-time", "pattern": "Z$"} |
| `released_at` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "format": "date-time", "pattern": "Z$"}, {"type": "null"}]} |
| `released_by` | `Optional~string~` | yes | {"anyOf": [{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:@/\\-]*$"}, {"type": "null"}]} |
| `reason` | `string` | yes | {"minLength": 1} |

## BatchRunner — proposed interface

Attributes: `RegistryLinker registry`, `FactRepository facts`.

`run(intake_id) BatchRun`  

## RegistryLinker — proposed interface

Attributes: none specified.

`load_release(release_id) void`  
`validate_closure(profile) void`  
`execution_order(profile) List~FunctionDefinition~`  

## SourceAdapter — proposed interface

Attributes: none specified.

`capture(target, scope) AcquisitionAttempt`  

## AcquisitionService — proposed interface

Attributes: `SourceAdapter adapter`, `RightsGate rights`, `ContentRepository content`.

`collect(intake, scope) AcquisitionAttempt`  

## RightsGate — proposed interface

Attributes: none specified.

`assert_use(policy_ids, purpose, as_of) void`  
`retention_deadline(policy_ids) datetime`  

## ContentRepository — proposed interface

Attributes: none specified.

`put_immutable(bytes, policy) Artifact`  
`read_verified(artifact_id) bytes`  
`delete(artifact_id) ChangeRecord`  

## SubjectResolver — proposed interface

Attributes: none specified.

`bind(artifact, subject, locators) SubjectBinding`  

## ExtractionService — proposed interface

Attributes: `BoundedModelGateway model`.

`extract(artifact, definition) List~CandidateRecord~`  

## BoundedModelGateway — proposed interface

Attributes: none specified.

`call(task, artifacts) ModelCall`  
`repair_or_abstain(call) QuotedTextResult`  

## FactAdmission — proposed interface

Attributes: `RightsGate rights`, `RegistryLinker registry`.

`validate(candidate, evidence, binding) Fact`  
`quarantine(candidate, reason) CandidateRecord`  

## FactRepository — proposed interface

Attributes: none specified.

`append_idempotent(fact) Fact`  
`select_inputs(subject, as_of) List~Fact~`  
`record_change(change) void`  

## AccountInputSelector — proposed interface

Attributes: `FactRepository facts`.

`freeze_account_inputs(subject, as_of) BatchRun`  

## DerivationRunner — proposed interface

Attributes: none specified.

`evaluate(function, inputs, parameters) ExecutionRecord`  

## ContextJoiner — proposed interface

Attributes: none specified.

`join(rule, account_facts, context_facts) ContextAssessment`  

## SignalEngine — proposed interface

Attributes: none specified.

`evaluate(definition, facts, contexts) SignalEvaluation`  

## TemplateRenderer — proposed interface

Attributes: none specified.

`render(template, eligible_facts) List~GroundedClause~`  

## PackageValidator — proposed interface

Attributes: `RightsGate rights`.

`approve_preview(package, as_of) OutreachPackage`  
`revalidate_for_export(package, as_of) void`  

## RetentionService — proposed interface

Attributes: `ContentRepository content`, `FactRepository facts`.

`apply_policy(policy, as_of) List~ChangeRecord~`  

## UnitOfWork — proposed interface

Attributes: none specified.

`begin() void`  
`commit_account_result() void`  
`rollback() void`  

## ReviewService — proposed interface

Attributes: none specified.

`review(exact_package_revision, principal) ReviewDecision`  

## UseGate — proposed interface

Attributes: none specified.

`evaluate(package, destination, principal, current_time) UseGateDecision`  

## LocalPreviewExporter — proposed interface

Attributes: none specified.

`export(gate_id, principal_id, at, idempotency_key) LocalExportResult`  
