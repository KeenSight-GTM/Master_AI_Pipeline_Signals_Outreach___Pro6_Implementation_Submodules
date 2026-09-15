# Proposed product contract field reference

These are conceptual DTOs, not new JSON Schemas. They complement the retained protocol and current v4.1 domain records. No runtime consumer is declared compatible by this document alone.

## ProgramDefinition

**Owning module:** GTM-01

**Minimum fields:** `program_id`, `tenant_id`, `revision`, `objectives`, `audience_ref`, `offer_refs`, `capability_profile_ref`, `acquisition_limits`, `outreach_policy_ref`, `owner`, `approval_state`.

**Invariant:** Program configuration does not assert that accounts satisfy it.

## AudienceDefinition

**Owning module:** GTM-01

**Minimum fields:** `audience_id`, `revision`, `account_filters`, `permitted_geographies`, `excluded_segments`, `membership_as_of_policy`, `selection_reason_codes`.

**Invariant:** Selections record their input snapshot; broad facts persist even for rejected targets.

## OfferDefinition

**Owning module:** GTM-01

**Minimum fields:** `offer_id`, `revision`, `service_line`, `supported_problem_classes`, `prerequisites`, `allowed_template_refs`, `persona_rules`, `restrictions`.

**Invariant:** Named service/offer policy; not proof of prospect pain or an implemented automation playbook catalog.

## AccountSeed

**Owning module:** GTM-02

**Minimum fields:** `seed_id`, `tenant_id`, `program_id`, `discovery_source_ref`, `original_record_ref`, `resource_uri`, `provisional_external_ids`, `discovered_at`, `normalization_decision`.

**Invariant:** Unresolved seeds remain provisional; neither a redirect nor source label proves domain ownership.

## LeadSelection

**Owning module:** GTM-02

**Minimum fields:** `selection_id`, `program_id`, `account_ref`, `input_snapshot_ref`, `fit_decision`, `reasons`, `exclusion_state_refs`, `selected_at`.

**Invariant:** Fit and exclusion decisions are not evidence strength or source authority.

## ResearchPlan

**Owning module:** GTM-02

**Minimum fields:** `plan_id`, `account_ref`, `intended_predicates`, `existing_coverage_refs`, `permitted_source_refs`, `acquisition_limits`, `priority_reasons`, `stopping_rules`.

**Invariant:** Missing evidence results in a bounded plan or explicit defer, never a fabricated fact.

## ContactProfile

**Owning module:** AUD-01

**Minimum fields:** `contact_profile_id`, `tenant_id`, `person_subject_ref`, `account_relationship_ref`, `endpoint_refs`, `source_evidence_refs`, `role_effective_window`, `verified_at`, `retention_policy_ref`.

**Invariant:** Identifiers, evidence, and operational view remain separate; KN-01 owns canonical identity.

## ContactAssessment

**Owning module:** AUD-01

**Minimum fields:** `assessment_id`, `contact_profile_ref`, `opportunity_ref`, `role_fit`, `employer_binding_status`, `endpoint_verification`, `source_use_state`, `restrictions_refs`, `checked_at`, `reasons`.

**Invariant:** Deliverable endpoint does not imply appropriate recipient or outreach permission.

## MessageArtifact

**Owning module:** COM-02

**Minimum fields:** `message_id`, `revision`, `package_ref`, `channel`, `subject_or_title`, `body_ref`, `required_footer_ref`, `rendered_content_digest`, `renderer_version`, `permitted_transformations`.

**Invariant:** Exact recipient-visible factual content must be reviewed. Channel rendering cannot add unsupported assertions after package review.

## CampaignDefinition

**Owning module:** CAM-01

**Minimum fields:** `campaign_id`, `revision`, `program_ref`, `route_ref`, `ordered_step_definitions`, `template_refs`, `schedule_owner`, `send_window_policy`, `timezone_policy`, `sender_constraints`, `stop_policy`, `frequency_caps`.

**Invariant:** Exactly one scheduler owns progression; campaign activation is separate from creation or review.

## CampaignApproval

**Owning module:** CAM-01

**Minimum fields:** `approval_id`, `campaign_id`, `revision`, `definition_hash`, `authorized_actor`, `allowed_mode`, `approved_at`, `policy_ref`.

**Invariant:** Does not substitute for a package ReviewDecision or per-effect current-use/send authorization.

## CampaignReadiness

**Owning module:** CAM-01

**Minimum fields:** `readiness_id`, `campaign_ref`, `sender_snapshot_refs`, `provider_state_refs`, `compatibility_checks`, `checked_at`, `decision`, `reasons`.

**Invariant:** Readiness is time-sensitive; provider drift can block dispatch despite prior approval.

## Enrollment

**Owning module:** CAM-02

**Minimum fields:** `enrollment_id`, `tenant_id`, `campaign_ref`, `account_ref`, `contact_ref`, `enrollment_policy_ref`, `state`, `next_step_id`, `state_revision`, `enrolled_at`, `last_event_ref`.

**Invariant:** Same recipient/account can be constrained across campaigns. State changes use expected revisions and event identities.

## StepEligibility

**Owning module:** CAM-02

**Minimum fields:** `eligibility_id`, `enrollment_ref`, `step_id`, `due_at`, `timezone_basis`, `package_ref`, `contact_assessment_ref`, `cap_reservation_ref`, `state_revision`, `decision`, `reasons`.

**Invariant:** Scheduling eligibility is not SendGateDecision; final current restrictions are checked again before dispatch.

## DeliveryIntent

**Owning module:** CAM-02

**Minimum fields:** `intent_id`, `tenant_id`, `enrollment_ref`, `step_id`, `recipient_binding_ref`, `channel`, `reviewed_message_ref`, `logical_effect_key`, `execution_owner`.

**Invariant:** Stable business intent across retries and code upgrades; altered payload under same effect is an error.

## SendGateDecision

**Owning module:** COM-04

**Minimum fields:** `gate_id`, `intent_ref`, `message_ref`, `review_ref`, `campaign_approval_ref`, `readiness_ref`, `recipient_ref`, `current_restriction_vector`, `current_contact_vector`, `evaluated_at`, `valid_until`, `decision`, `reasons`.

**Invariant:** New proposed family. Existing UseGateDecision supports export purposes only. Recheck immediately before effect; no indefinite gate caching.

## SenderCapabilitySnapshot

**Owning module:** COM-05

**Minimum fields:** `snapshot_id`, `tenant_id`, `sender_account_ref`, `provider`, `channel`, `verified_capabilities`, `live_state`, `checked_at`, `configuration_digest`.

**Invariant:** Secrets remain protected references; do not assume a provider supports idempotency, cancellation, or exact content preservation.

## DeliveryAttempt

**Owning module:** COM-05

**Minimum fields:** `attempt_id`, `intent_ref`, `gate_ref`, `request_digest`, `started_at`, `finished_at`, `transport_status`, `acceptance_status`, `external_message_ref`, `error_ref`.

**Invariant:** Transport completion and remote acceptance are separate; ambiguous acceptance requires reconciliation, not resend.

## Conversation

**Owning module:** ENG-01

**Minimum fields:** `conversation_id`, `tenant_id`, `account_ref`, `contact_refs`, `provider_account_ref`, `external_thread_ref`, `event_refs`, `enrollment_links`, `current_owner`, `state`.

**Invariant:** Reply chains link exposures without guessing causal attribution for analytics; unmatched events remain visible.

## ReplyAssessment

**Owning module:** ENG-01

**Minimum fields:** `assessment_id`, `inbound_event_ref`, `classification_kind`, `literal_support_refs`, `producer_execution_ref`, `confidence_metadata`, `human_review_state`, `recommended_action`.

**Invariant:** Model labels are inferences; pause/opt-out controls do not wait on or take permission from model confidence.

## EnrollmentControl

**Owning module:** ENG-01

**Minimum fields:** `control_id`, `target_enrollment_refs`, `cause_event_ref`, `desired_transition`, `scope`, `created_at`, `expected_state_refs`.

**Invariant:** ENG-01 requests stops; CAM-02 applies them idempotently. Authorized restrictions are written separately by PLAT-02.

## FollowUpTask

**Owning module:** ENG-01

**Minimum fields:** `task_id`, `conversation_ref`, `assigned_owner`, `task_kind`, `due_at`, `source_event_ref`, `state`, `authorization_requirements`.

**Invariant:** Creating a human task is not authorizing an automated follow-up, referral send, or calendar action.

## SalesHandoff

**Owning module:** ENG-01

**Minimum fields:** `handoff_id`, `account_ref`, `contact_ref`, `conversation_ref`, `exposure_refs`, `qualification_notes_refs`, `intended_owner`, `meeting_or_next_action`, `created_at`.

**Invariant:** A positive reply is not a confirmed meeting, won sale, or permission to invent additional factual qualifications.

## CRMMapping

**Owning module:** CRM-01

**Minimum fields:** `mapping_id`, `provider`, `schema_version`, `field_ownership`, `inbound_outbound_transforms`, `idempotency_policy`, `suppression_rules`, `loop_prevention`.

**Invariant:** Each field has one authority or an explicit merge policy; use versions/receipts, not unrestricted last-write-wins.

## CRMAccountView

**Owning module:** CRM-01

**Minimum fields:** `view_id`, `account_ref`, `external_record_links`, `owner`, `lifecycle_stage`, `customer_or_open_deal_state`, `restriction_observations`, `provider_version`, `fetched_at`.

**Invariant:** Imported pipeline data is a current provider report. Stale critical exclusions cause refresh or hold, not automatic reactivation.

## CRMSyncIntent

**Owning module:** CRM-01

**Minimum fields:** `sync_id`, `tenant_id`, `mapping_ref`, `entity_link`, `desired_fields`, `source_record_refs`, `expected_remote_version`, `idempotency_key`.

**Invariant:** No delivery commands in CRM write retries; emit approved record mutations only.

## CRMSyncReceipt

**Owning module:** CRM-01

**Minimum fields:** `receipt_id`, `sync_intent_ref`, `external_record_ref`, `payload_hash`, `status`, `provider_version`, `confirmed_at`, `reconciliation_ref`.

**Invariant:** Record ambiguous writes and reconcile without duplicating tasks or deals; missing data cannot release DNC.

## ExperimentDefinition

**Owning module:** QA-01

**Minimum fields:** `experiment_id`, `hypothesis`, `eligible_population`, `randomization_or_observational_design`, `treatment_refs`, `holdout_policy`, `outcome_definition`, `maturity_window`, `stopping_rule`.

**Invariant:** Label observational versus randomized designs explicitly; no promised causal conclusions.

## ExperimentAssignment

**Owning module:** QA-01

**Minimum fields:** `assignment_id`, `experiment_ref`, `unit_ref`, `assigned_variant`, `assignment_rule_version`, `assigned_at`, `exposure_links`.

**Invariant:** Pin before exposure; deduplicate and track cross-campaign contamination.

## QualityAssessment

**Owning module:** QA-01

**Minimum fields:** `assessment_id`, `evaluated_release_refs`, `gold_set_ref`, `eligible_sample`, `observed_metrics`, `errors`, `uncertainty`, `limitations`.

**Invariant:** Quality outcomes do not alter source authority by themselves; preserve fixture versus live-evaluation distinction.

## PromotionProposal

**Owning module:** QA-01

**Minimum fields:** `proposal_id`, `target_definition_ref`, `assessed_release_ref`, `quality_assessment_refs`, `intended_change`, `reasons`, `review_requirements`.

**Invariant:** Proposal only. Authorized governance and release compiler publish a new immutable release for later runs.

## WorkspaceView

**Owning module:** UX-01

**Minimum fields:** `view_id`, `tenant_id`, `view_kind`, `permitted_record_refs`, `as_of`, `redaction_policy_ref`, `completeness_notes`.

**Invariant:** Read model only; user actions must route through authenticated owning operations.
