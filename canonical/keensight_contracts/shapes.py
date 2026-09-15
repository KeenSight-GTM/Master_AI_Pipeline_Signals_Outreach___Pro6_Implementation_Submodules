"""Closed, versioned JSON Schema Draft-07 shapes. Generate; never hand-edit schemas/."""
from copy import deepcopy
S = {'type':'string','minLength':1}
ID = {'type':'string','pattern':r'^[A-Za-z0-9][A-Za-z0-9_.:@/\-]*$'}
UTC = {'type':'string','format':'date-time','pattern':'Z$'}
URI = {'type':'string','format':'uri'}
HASH = {'type':'string','pattern':'^sha256:[a-f0-9]{64}$'}
INT = {'type':'integer','minimum':0}
POS = {'type':'integer','minimum':1}
NUM = {'type':'number'}
NONNEG = {'type':'number','minimum':0}
PROB = {'type':'number','minimum':0,'maximum':1}
BOOL = {'type':'boolean'}
VER = {'type':'string','pattern':r'^\d+\.\d+\.\d+$'}
CURRENCY = {'type':'string','pattern':'^[A-Z]{3}$'}
NATURES = ['DIRECT_OBSERVATION','FIRST_PARTY_STATEMENT','THIRD_PARTY_REPORT','PROVIDER_ESTIMATE','REGISTRY_RECORD','INFERENCE','DERIVED_MEASUREMENT']
SUBJECTS = ['ORG','LOCATION','PERSON','BRAND','WEBSITE','SOFTWARE_PRODUCT','INDUSTRY','JOB_POSTING','APPLICATION','LISTING','COHORT','ANGLE']
PURPOSES = ['CAPTURE','RETAIN','DERIVE','LLM_PROCESS','INTERNAL_RESEARCH','OUTREACH','EXPORT']
METHODS = ['HTTP_CAPTURE','API','DNS','CERTIFICATE_LOG','AUTHORIZED_EXPORT','HUMAN_UPLOAD','DERIVATION']
PROCESSORS = ['DETERMINISTIC','LLM','HUMAN_REVIEW','DERIVATION']
AUTH = ['CANDIDATE','ACTIVE','DEPRECATED']
def enum(*xs): return {'enum':list(xs)}
def arr(shape=S, minimum=0, unique=False):
    x={'type':'array','items':deepcopy(shape),'minItems':minimum}
    if unique: x['uniqueItems']=True
    return x
def obj(fields, required=None):
    return {'type':'object','properties':deepcopy(fields),'required':list(fields) if required is None else required,'additionalProperties':False}
def nullable(s): return {'anyOf':[deepcopy(s),{'type':'null'}]}
def ref(name): return {'$ref':f'https://keensight.local/v4.2/{name}.schema.json'}
WINDOW=obj({'start':UTC,'end':UTC})
EXTERNAL=obj({'namespace':ID,'value':S})
SCORE=obj({'value':PROB,'meaning':enum('UNCALIBRATED_MODEL_SCORE','CALIBRATED_PRECISION','DETERMINISTIC_MATCH'),'calibration_id':nullable(ID)})
REFERENCE_RULE=obj({'container':enum('target','object'),'path':S,'subject_kinds':arr(enum(*SUBJECTS),0,True),'target_type':enum('SUBJECT','FACT','ARTIFACT','LOCATOR')},['container','path','subject_kinds'])
SCHEMAS={}
def add(name,shape):
    SCHEMAS[name]={'$schema':'http://json-schema.org/draft-07/schema#','$id':f'https://keensight.local/v4.2/{name}.schema.json','title':name,**shape}

add('Subject',obj({'subject_id':ID,'tenant_id':ID,'kind':enum(*SUBJECTS),'display_name':S,'external_ids':arr(EXTERNAL,0,True)}))
add('Scope',obj({'scope_id':ID,'tenant_id':ID,'subject_id':ID,'kind':enum('ELEMENT','PAGE','WEBSITE','PROVIDER_QUERY','AUTHORIZED_SYSTEM','RESEARCH_SAMPLE','REGISTRY_RECORD','OPERATIONS'),
    'resources':arr(S,1,True),'capture_mode':enum('RAW_HTML','RENDERED_DOM','NETWORK_TRACE','DNS','CERTIFICATE_LOG','API_BODY','DOCUMENT','HUMAN_RECORD','DERIVED'),
    'population_description':S,'stable_scope_key':S}))
add('SubjectBinding',obj({'binding_id':ID,'tenant_id':ID,'subject_id':ID,'scope_id':ID,'artifact_ids':arr(ID,1,True),
    'role':enum('FIRST_PARTY','REVIEW_TARGET','REGISTRY_SUBJECT','RESEARCH_TARGET','AGENCY','MENTION_ONLY','UNRESOLVED'),
    'status':enum('ACCEPTED','REJECTED','UNRESOLVED'),'method':S,'decided_at':UTC,'evidence_locator_ids':arr(ID,1,True)}))
add('DataAccessPolicy',obj({'policy_id':ID,'tenant_ids':arr(ID,1,True),'version':VER,'review_status':enum('UNREVIEWED','APPROVED','REVOKED'),'fixture_only':BOOL,
    'approval_ref':nullable(S),'terms_ref':URI,'reviewed_at':UTC,'valid_until':UTC,'purposes':arr(enum(*PURPOSES),0,True),
    'max_raw_retention_seconds':INT,'max_derived_retention_seconds':INT,'attribution_text':nullable(S),
    'allow_personal_data':BOOL,'allow_sensitive_data':BOOL,'deletion_cascades':BOOL}))
add('SourceDefinition',obj({'source_id':ID,'version':VER,'provider':S,'acquisition_method':enum(*METHODS),'authority':enum(*AUTH),
    'fixture_only':BOOL,'policy_id':ID,'emits':arr(ID,1,True),'allowed_natures':arr(enum(*NATURES),1,True),
    'freshness_seconds':POS,'adapter_status':enum('FIXTURE_ONLY','DESIGN_ONLY','IMPLEMENTED'),'upstream_namespace':S}))
add('Artifact',obj({'artifact_id':ID,'tenant_id':ID,'source_id':ID,'scope_id':ID,'resource_uri':URI,'media_type':S,
    'content_ref':nullable(S),'content_hash':HASH,'byte_count':INT,'captured_at':UTC,'published_at':nullable(UTC),
    'status':enum('OK','ERROR','TIMEOUT','POLICY_DENIED'),'truncated':BOOL,'retained_until':UTC,
    'retention_state':enum('RETAINED','DELETED','EXPIRED','REFERENCE_ONLY'),'classification':enum('PUBLIC_BUSINESS','PERSONAL','CONFIDENTIAL','SENSITIVE'),
    'origin_namespace':S,'origin_record_id':S,'origin_revision':S,'independence_group':S,'parent_artifact_id':nullable(ID)}))
add('EvidenceLocator',obj({'locator_id':ID,'artifact_id':ID,'kind':enum('TEXT_SPAN','JSON_POINTER','WHOLE_ARTIFACT'),
    'start':nullable(INT),'end':nullable(INT),'pointer':nullable({'type':'string'}),'quote':nullable(S)}))
CHECKED=obj({'resource':S,'artifact_id':nullable(ID),'result':enum('OK','ERROR','TIMEOUT','DENIED','NOT_VISITED')})
add('CoverageRecord',obj({'coverage_id':ID,'tenant_id':ID,'scope_id':ID,'source_id':ID,'predicate_ids':arr(ID,1,True),
    'target':{'type':'object'},'planned_resources':arr(S,1,True),'checked':arr(CHECKED,1),'status':enum('COMPLETE','INCOMPLETE'),
    'checked_at':UTC,'detector_release':HASH,'scope_limitations':S}))
add('EvidenceSet',obj({'evidence_id':ID,'tenant_id':ID,'locator_ids':arr(ID,0,True),'input_fact_ids':arr(ID,0,True),
    'execution_id':nullable(ID),'coverage_id':nullable(ID),'directness':enum('RAW','DERIVED')}))
add('PredicateDefinition',obj({'predicate_id':ID,'version':VER,'family':S,'description':S,'subject_kinds':arr(enum(*SUBJECTS),1,True),
    'target_schema':{'type':'object'},'value_schema':{'type':'object'},'allowed_natures':arr(enum(*NATURES),1,True),
    'allowed_processors':arr(enum(*PROCESSORS),1,True),'absence_allowed':BOOL,'temporal_mode':enum('POINT','EVENT','PERIOD'),
    'copy_policy':enum('DIRECT_SCOPED','ATTRIBUTED_ONLY','ESTIMATE_ATTRIBUTED','REGISTRY_ATTRIBUTED','INTERNAL_ONLY','CONTEXT_ONLY'),
    'reference_rules':arr(REFERENCE_RULE),'section_ids':arr({'type':'integer','minimum':0,'maximum':11},0,True),
    'value_class':ID,'origin':enum('V3_RETAINED','V3_REVISED','V4_ADDED'),'example_target':{'type':'object'},'example_value':{}}))
# target and object are deliberately predicate-dispatched; validating this envelope alone is insufficient.
add('Fact',obj({'schema_version':{'const':'4.2.0'},'fact_id':ID,'tenant_id':ID,'subject_id':ID,'predicate_id':ID,
    'target':{'type':'object'},'scope_id':ID,'state':enum('OBSERVED','NOT_FOUND','UNKNOWN'),'object':{},'nature':enum(*NATURES),
    'source_id':ID,'binding_id':nullable(ID),'evidence_id':ID,'execution_id':nullable(ID),'run_id':ID,
    'observed_at':UTC,'recorded_at':UTC,'effective_at':nullable(UTC),'window':nullable(WINDOW),
    'reason':nullable(enum('NOT_DETECTED_IN_SCOPE','NOT_CHECKED','FETCH_FAILED','POLICY_BLOCKED','INSUFFICIENT_EVIDENCE','CONFLICT','AMBIGUOUS_ATTRIBUTION','EXTRACTION_FAILED')),
    'expires_at':UTC,'confidence':nullable(SCORE),'supersedes_fact_id':nullable(ID)}))
SCHEMAS['Fact']['allOf']=[
    {'if':{'properties':{'state':{'const':'OBSERVED'}}},'then':{'properties':{'object':{'not':{'type':'null'}},'reason':{'type':'null'}}}},
    {'if':{'properties':{'state':{'const':'NOT_FOUND'}}},'then':{'properties':{'object':{'type':'null'},'reason':{'const':'NOT_DETECTED_IN_SCOPE'}}}},
    {'if':{'properties':{'state':{'const':'UNKNOWN'}}},'then':{'properties':{'object':{'type':'null'},'reason':{'enum':['NOT_CHECKED','FETCH_FAILED','POLICY_BLOCKED','INSUFFICIENT_EVIDENCE','CONFLICT','AMBIGUOUS_ATTRIBUTION','EXTRACTION_FAILED']}}}}]
add('ClaimResolution',obj({'resolution_id':ID,'tenant_id':ID,'subject_id':ID,'predicate_id':ID,'scope_id':ID,'target':{'type':'object'},
    'observation_ids':arr(ID,1,True),'accepted_fact_ids':arr(ID,0,True),'status':enum('KNOWN','CONFLICT','UNKNOWN'),
    'policy_version':VER,'as_of':UTC}))
add('MetricDefinition',obj({'metric_id':ID,'description':S,'unit':S,'value_schema':{'type':'object'},'dimensions_schema':{'type':'object'},
    'requires_denominator':BOOL,'aggregation':enum('COUNT','SUM','MEAN','RATE','RANK','ESTIMATE','DISTRIBUTION','DESCRIPTIVE'),
    'allowed_natures':arr(enum(*NATURES),1,True),'subject_kinds':arr(enum(*SUBJECTS),1,True),'section_ids':arr({'type':'integer','minimum':1,'maximum':11},1,True)}))
add('MeasurementValue',obj({'metric_id':ID,'value':NUM,'unit':S,'dimensions':{'type':'object'},'method_version':S,'reporting_timezone':S,
    'numerator':nullable(INT),'denominator':nullable(INT),'sample_size':nullable(INT),'uncertainty':nullable(obj({'lower':NUM,'upper':NUM,'method':S}))}))
add('TaxonomyTerm',obj({'term_id':ID,'scheme_id':ID,'scheme_version':VER,'label':S,'parent_id':nullable(ID)}))
add('FingerprintDefinition',obj({'fingerprint_id':ID,'version':VER,'authority':enum(*AUTH),'fixture_only':BOOL,'product_subject_id':ID,'emits':ID,
    'capture_mode':enum('RAW_HTML','RENDERED_DOM','NETWORK_TRACE','DNS','CERTIFICATE_LOG','API_BODY'),
    'operator':enum('SCRIPT_HOST','IFRAME_HOST','FORM_HOST','COOKIE_NAME','HEADER_VALUE','DNS_TARGET','JSON_VALUE','ATTRIBUTE_VALUE'),
    'match_value':S,'positive_fixtures':arr(S,1,True),'negative_fixtures':arr(S,1,True),'calibration_ref':nullable(ID),
    'implementation_status':enum('REFERENCE_IMPLEMENTED','DESIGN_ONLY')}))
add('FunctionDefinition',obj({'function_id':ID,'version':VER,'processor':enum(*PROCESSORS),'authority':enum(*AUTH),'fixture_only':BOOL,
    'input_predicates':arr(ID,0,True),'output_predicates':arr(ID,0,True),'parameter_schema':{'type':'object'},
    'cross_subject_rule':enum('SAME_SUBJECT','SAME_RESEARCH_TARGET','EXPLICIT_RELATION','CONTEXT_ONLY'),
    'implementation_status':enum('REFERENCE_IMPLEMENTED','DESIGN_ONLY'),'entrypoint':nullable(S)}))
add('ExecutionRecord',obj({'execution_id':ID,'tenant_id':ID,'run_id':ID,'function_id':ID,'function_version':VER,'subject_id':ID,
    'input_fact_ids':arr(ID,0,True),'input_artifact_ids':arr(ID,0,True),'output_fact_ids':arr(ID,0,True),
    'input_set_hash':HASH,'parameters':{'type':'object'},'started_at':UTC,'finished_at':UTC,
    'status':enum('COMPLETE','ABSTAINED','FAILED'),'model_call_id':nullable(ID)}))
add('BatchRun',obj({'run_id':ID,'tenant_id':ID,'mode':enum('DESIGN_TEST','PRODUCTION'),'as_of':UTC,'created_at':UTC,
    'code_release':HASH,'registry_release':HASH,'profile_id':ID,'input_artifact_ids':arr(ID,0,True),'input_fact_ids':arr(ID,0,True),
    'binding_ids':arr(ID,0,True),'status':enum('OPEN','COMPLETE','FAILED'),'approval_policy_version':VER}))
add('CapabilityProfile',obj({'profile_id':ID,'version':VER,'production_enabled':BOOL,'capture_source_ids':arr(ID,0,True),
    'fact_predicate_ids':arr(ID,1,True),'execute_function_ids':arr(ID,0,True),'signal_ids':arr(ID,0,True),
    'template_ids':arr(ID,0,True),'research_context_enabled':BOOL,'delivery_enabled':{'const':False}}))
add('ResearchSample',obj({'sample_id':ID,'tenant_id':ID,'subject_id':ID,'scope_id':ID,'window':WINDOW,'sampling_frame':S,
    'selection_method':enum('CENSUS','PROVIDER_SAMPLE','QUERY_SAMPLE','CURATED_SAMPLE'),'retrieved_artifact_ids':arr(ID,1,True),
    'eligible_artifact_ids':arr(ID,0,True),'excluded_artifact_ids':arr(ID,0,True),'dedupe_policy_version':VER,
    'population_size':nullable(INT),'complete_population':BOOL,'limitations':arr(S,1),'policy_ids':arr(ID,1,True)}))
add('ResearchPriorValue',obj({'sample_id':ID,'theme_id':ID,'supporting_fact_ids':arr(ID,1,True),'contradicting_fact_ids':arr(ID,0,True),
    'support_count':INT,'eligible_count':POS,'sample_share':PROB,'population_claim':{'const':False}}))
add('ContextJoinRule',obj({'join_rule_id':ID,'version':VER,'link_predicate':ID,'link_object_path':S,'context_predicate':ID,
    'target_kinds':arr(enum('SOFTWARE_PRODUCT','INDUSTRY'),1,True),'link_kind':enum('FOOTPRINT','PROVIDER_REPORT','MEMBERSHIP'),
    'purpose':{'const':'INTERNAL_RESEARCH'},'maximum_hops':{'const':1},'company_claim_allowed':{'const':False}}))
add('ContextAssessment',obj({'context_id':ID,'tenant_id':ID,'run_id':ID,'account_subject_id':ID,'context_subject_id':ID,
    'join_rule_id':ID,'link_fact_id':ID,'context_fact_ids':arr(ID,1,True),'relationship_strength':enum('FOOTPRINT','PROVIDER_REPORT','MEMBERSHIP'),
    'purpose':{'const':'INTERNAL_RESEARCH'},'company_claim_allowed':{'const':False},'status':enum('ELIGIBLE','ABSTAINED')}))
REQ=obj({'predicate_id':ID,'allowed_natures':arr(enum(*NATURES),1,True),'state':enum('OBSERVED','NOT_FOUND'),'minimum':POS})
add('SignalDefinition',obj({'signal_type_id':ID,'version':VER,'required_facts':arr(REQ,1),'function_id':ID,
    'context_allowed':BOOL,'description':S,'status':enum('REFERENCE_IMPLEMENTED','DESIGN_ONLY')}))
add('SignalEvaluation',obj({'signal_id':ID,'run_id':ID,'tenant_id':ID,'subject_id':ID,'signal_type_id':ID,
    'input_fact_ids':arr(ID,0,True),'context_ids':arr(ID,0,True),'status':enum('RESOLVED','UNRESOLVED','SUPPRESSED','CANDIDATE'),
    'reason':nullable(enum('THIN_DATA','CONFLICT','POLICY','DNC','CANDIDATE_SOURCE'))}))
add('TemplateDefinition',obj({'template_id':ID,'version':VER,'authority':enum(*AUTH),'mode':enum('OBSERVATION_QUESTION','MATURITY_OFFER'),
    'required_predicate':ID,'allowed_natures':arr(enum(*NATURES),1,True),'renderer':enum('observed_product_v1','attributed_job_statement_v1','scoped_absence_v1'),
    'question':S,'maturity_required':BOOL,'offered_rung':nullable(enum('L1','L2','L3')),'review_ref':S}))
add('GroundedClause',obj({'clause_id':ID,'fact_ids':arr(ID,1,True),'template_id':ID,'text':S,'evidence_roles':arr(enum('DIRECT','ATTRIBUTED','SCOPED_ABSENCE'),1,True)}))
add('OutreachPackage',obj({'package_id':ID,'revision':POS,'run_id':ID,'tenant_id':ID,'subject_id':ID,'template_id':ID,
    'clauses':arr(ref('GroundedClause'),1),'signal_ids':arr(ID,0,True),'context_ids':arr(ID,0,True),
    'maturity_fact_id':nullable(ID),'status':enum('DRAFT','DESIGN_TEST_APPROVED','APPROVED','WITHHELD'),
    'rendered_text':S,'approved_at':nullable(UTC),'send_allowed':{'const':False}}))
add('ChangeRecord',obj({'change_id':ID,'tenant_id':ID,'kind':enum('RETRACTION','BINDING_CORRECTION','AUTHORITY_CHANGE','POLICY_REVOCATION','ARTIFACT_DELETION'),
    'target_id':ID,'effective_at':UTC,'reason':S,'replacement_id':nullable(ID)}))
add('ModelCall',obj({'call_id':ID,'tenant_id':ID,'task_version':VER,'provider':S,'model':S,'prompt_hash':HASH,'output_schema_id':ID,
    'input_artifact_ids':arr(ID,1,True),'request_artifact_id':ID,'response_artifact_id':ID,'policy_ids':arr(ID,1,True),
    'max_repair_attempts':{'type':'integer','minimum':0,'maximum':2},'status':enum('PARSED','ABSTAINED','FAILED'),'terminal_reason':nullable(S)}))
add('RepairAttempt',obj({'attempt_id':ID,'call_id':ID,'ordinal':{'type':'integer','minimum':1,'maximum':2},
    'input_response_artifact_id':ID,'output_response_artifact_id':ID,'method':enum('DETERMINISTIC_JSON_REPAIR','BOUNDED_MODEL_REPAIR'),
    'status':enum('VALID','INVALID'),'validation_errors':arr(S)}))
add('Exposure',obj({'exposure_id':ID,'tenant_id':ID,'package_id':ID,'business_send_key':S,'provider_message_id':nullable(S),
    'recipient_key':S,'accepted_at':nullable(UTC),'status':enum('PROVIDER_ACCEPTED','UNKNOWN_DELIVERY','FAILED','BOUNCED')}))
add('OutcomeEvent',obj({'event_id':ID,'tenant_id':ID,'provider':S,'provider_event_id':S,'exposure_id':nullable(ID),
    'occurred_at':UTC,'received_at':UTC,'kind':enum('REPLY','MEETING','BOUNCE','UNSUBSCRIBE','DELIVERY_UPDATE'),
    'attribution_status':enum('MATCHED','QUARANTINED'),'evidence_id':ID}))
add('ProviderBlueprint',obj({'blueprint_id':ID,'provider':S,'section_ids':arr({'type':'integer','minimum':1,'maximum':11},1,True),
    'families':arr(S,1,True),'methods':arr(enum(*METHODS),1,True),'terms_url':URI,'approval_required':{'const':True},
    'adapter_implemented':{'const':False},'notes':S}))

add('CoverageFamilyPlan',obj({'section':{'type':'integer','minimum':1,'maximum':11},'title':S,'predicate_ids':arr(ID,1,True),'metric_ids':arr(ID,0,True),'contract_status':{'const':'SCHEMA_DEFINED'},'live_adapter_status':{'const':'NOT_IMPLEMENTED'}}))

add('CalibrationRecord',obj({'calibration_id':ID,'target_id':ID,'target_version':VER,'evaluation_dataset_id':ID,'true_positives':INT,'false_positives':INT,'measured_precision':PROB,'report_hash':HASH,'fixture_only':BOOL,'review_ref':S}))
add('CandidateRecord',obj({'candidate_id':ID,'tenant_id':ID,'artifact_id':ID,'proposed_predicate_id':ID,'proposed_value':{},'reason':enum('UNREGISTERED_TYPE','INVALID_VALUE','UNRESOLVED_BINDING','UNKNOWN_TAXONOMY'),'production_eligible':{'const':False}}))

add('QuotedTextResult',obj({'text':S}))
# Reusable inline value objects are also exported for code-generation and UML.
add('TimeWindow',WINDOW)
add('ExternalIdentifier',EXTERNAL)
add('ConfidenceAssessment',SCORE)
add('ObjectReferenceRule',REFERENCE_RULE)
add('CoverageCheck',CHECKED)
add('FactRequirement',REQ)


# v4.1: closed end-to-end handoffs. Definitions remain generated, not hand-edited.
def extend(name, fields, required=True):
    SCHEMAS[name]['properties'].update(deepcopy(fields))
    if required: SCHEMAS[name]['required'] += list(fields)

TARGET_REF=obj({'resource_uri':URI,'subject_id':nullable(ID)})
PKG_REF=obj({'package_id':ID,'revision':POS,'content_hash':HASH})
TERMINAL_REASONS=enum('TIMEOUT','POLICY_DENIED','BUDGET_DENIED','CANCELLED','PROVIDER_ERROR','PARTIAL_RESPONSE','NO_RESULTS')
add('IntakeRequest',obj({'intake_id':ID,'tenant_id':ID,'requester_id':ID,'profile_id':ID,'purpose':enum('KNOWLEDGE','REVIEWED_HANDOFF'),
    'targets':arr(TARGET_REF,1),'received_at':UTC,'request_hash':HASH,'idempotency_key':S}))
add('AcquisitionAttempt',obj({'attempt_id':ID,'tenant_id':ID,'intake_id':ID,'source_id':ID,'source_version':VER,'adapter_version':VER,
    'target':TARGET_REF,'scope_id':nullable(ID),'request_hash':HASH,'operation_key':S,'started_at':UTC,'finished_at':UTC,
    'status':enum('SUCCEEDED','EMPTY_RESULT','PARTIAL','TIMEOUT','FAILED','POLICY_DENIED','BUDGET_DENIED','CANCELLED'),
    'artifact_ids':arr(ID,0,True),'terminal_reason':nullable(TERMINAL_REASONS),'pagination':enum('NOT_APPLICABLE','EXHAUSTED','INCOMPLETE','UNKNOWN'),
    'truncated':BOOL,'max_requests':POS,'requests_made':INT,'timeout_seconds':POS,'body_limit_bytes':POS,
    'cost_status':enum('KNOWN','UNKNOWN','NOT_CHARGED'),'cost_minor':nullable(INT),'currency':nullable(CURRENCY)}))
add('ActorGrant',obj({'actor_id':ID,'tenant_id':ID,'permissions':arr(enum('INTAKE','REVIEW_PACKAGE','USE_GATE','EXPORT','RESTRICT'),1,True),
    'fixture_only':BOOL,'active':BOOL}))
add('ReviewDecision',obj({'review_id':ID,'tenant_id':ID,'reviewer_id':ID,'package':PKG_REF,
    'action':enum('APPROVE','REJECT','REQUEST_CHANGE'),'reason':S,'decided_at':UTC,'policy_version':VER}))
add('UseRestriction',obj({'restriction_id':ID,'tenant_id':ID,'subject_id':ID,'recipient_key':nullable(S),'kind':enum('DNC','HOLD'),
    'actor_id':ID,'effective_at':UTC,'released_at':nullable(UTC),'released_by':nullable(ID),'reason':S}))
add('UseGateDecision',obj({'gate_id':ID,'tenant_id':ID,'package':PKG_REF,'review_id':ID,'actor_id':ID,
    'purpose':enum('PREVIEW_EXPORT','CONTACT_EXPORT'),'destination_id':ID,'recipient_key':nullable(S),
    'evaluated_at':UTC,'valid_until':UTC,'version_vector':HASH,'decision':enum('ALLOW','BLOCK'),'reasons':arr(S,0,True)}))
add('DestinationDefinition',obj({'destination_id':ID,'tenant_id':ID,'mapping_version':VER,
    'kind':enum('LOCAL_PREVIEW','CONTACT_HANDOFF'),'fixture_only':BOOL,'enabled':BOOL,'automatic_sending':{'const':False}}))
add('ExportReceipt',obj({'export_id':ID,'tenant_id':ID,'package':PKG_REF,'gate_id':ID,'destination_id':ID,'mapping_version':VER,
    'actor_id':ID,'recipient_key':nullable(S),'payload_hash':HASH,'payload_ref':nullable(S),'idempotency_key':S,
    'requested_at':UTC,'completed_at':nullable(UTC),'status':enum('PREPARED','CONFIRMED','UNKNOWN','FAILED'),
    'external_reference':nullable(S),'automatic_sending':{'const':False}}))
add('TargetResult',obj({'subject_id':ID,'status':enum('COMPLETE','FAILED','ABSTAINED'),
    'completed_at':UTC,'reason':nullable(S)}))
add('ResearchSupportPolicy',obj({'support_policy_id':ID,'version':VER,
    'meaning':enum('REPORTED_NEGATIVE_EXPERIENCE','WORKFLOW_MENTION'),
    'allowed_stances':arr(S,1,True),'allowed_sentiments':arr(S,1,True),
    'counting_unit':{'const':'DISTINCT_ORIGIN'},'denominator_rule':{'const':'ELIGIBLE_RETRIEVED_RECORDS'},
    'unclassified_policy':{'const':'RETAIN_AS_UNMEASURED_NOT_NEGATIVE'}}))
add('SampleRecordDecision',obj({'artifact_id':ID,'status':enum('SUPPORT','CONTRADICT','NO_THEME','UNCLASSIFIED','EXCLUDED'),
    'classification_fact_ids':arr(ID,0,True),'reason':nullable(S)}))
extend('ResearchSample',{'support_policy_id':ID,'theme_id':ID,'record_decisions':arr(ref('SampleRecordDecision'),1),'created_at':UTC})
extend('EvidenceSet',{'attempt_id':nullable(ID),'sample_ids':arr(ID,0,True)})
SCHEMAS['EvidenceSet']['properties']['directness']=enum('RAW','DERIVED','DIAGNOSTIC')
extend('ExecutionRecord',{'input_sample_ids':arr(ID,0,True),'sample_set_hash':HASH,'terminal_reason':nullable(S)})
extend('FunctionDefinition',{'detector_contract':nullable(obj({'capture_modes':arr(S,1,True),'predicate_ids':arr(ID,1,True),'operator':S}))})
extend('CoverageRecord',{'attempt_ids':arr(ID,1,True),'detector_execution_id':ID})
extend('BatchRun',{'knowledge_cutoff':UTC,'sealed_at':UTC,'sample_ids':arr(ID,0,True),'resolution_ids':arr(ID,0,True),
    'target_results':arr(ref('TargetResult'),1),'produced_fact_ids':arr(ID,0,True),
    'imported_execution_ids':arr(ID,0,True),'intake_id':ID})
SCHEMAS['BatchRun']['properties']['status']=enum('OPEN','COMPLETE','PARTIAL','FAILED')
extend('CapabilityProfile',{'product_boundary':enum('KNOWLEDGE','PREVIEW','REVIEWED_HANDOFF'),'export_enabled':BOOL})
extend('ClaimResolution',{'run_id':ID,'resolved_at':UTC})
extend('SignalEvaluation',{'evaluated_at':UTC})
extend('OutreachPackage',{'review_id':nullable(ID)})
SCHEMAS['ModelCall']['properties']['response_artifact_id']=nullable(ID)
# Full claim inputs, not just IDs of duplicated observations, satisfy a minimum.
REQ['properties']['counting_unit']={'const':'DISTINCT_ORIGIN'}
REQ['required'].append('counting_unit')
SCHEMAS['SignalDefinition']['properties']['required_facts']=arr(REQ,1)
SCHEMAS['FactRequirement'].update(deepcopy(REQ))
# G: acquisition failure can support an UNKNOWN, never business truth/absence.
SCHEMAS['CandidateRecord']['properties']['artifact_id']=nullable(ID)
extend('CandidateRecord',{'attempt_id':nullable(ID)})
add('PackageReference',PKG_REF)
add('IntakeTarget',TARGET_REF)

extend('ResearchPriorValue',{'support_policy_id':ID,'classified_eligible_count':INT,'unclassified_count':INT,
    'denominator_definition':{'const':'ELIGIBLE_RETRIEVED_RECORDS_INCLUDING_UNCLASSIFIED'}})

extend('AcquisitionAttempt',{'execution_mode':enum('REPLAY_IMPORT','LIVE_CAPTURE')})

# v4.2: correction authorization and generated-versus-sealed artifact closure.
extend('ChangeRecord',{'actor_id':ID,'target_type':enum('facts','bindings','sources','policies','artifacts','fingerprints','functions'),
    'recorded_at':UTC})
SCHEMAS['ActorGrant']['properties']['permissions']['items']=enum('INTAKE','REVIEW_PACKAGE','USE_GATE','EXPORT','RESTRICT','CHANGE_FACT','CHANGE_BINDING','CHANGE_ARTIFACT','CHANGE_REGISTRY')
extend('BatchRun',{'produced_artifact_ids':arr(ID,0,True)})
extend('ExecutionRecord',{'output_artifact_ids':arr(ID,0,True)})
