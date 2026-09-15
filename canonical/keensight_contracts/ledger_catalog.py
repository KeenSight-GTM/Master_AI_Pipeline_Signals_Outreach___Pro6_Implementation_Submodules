"""Additional typed evidence families from the 52-row user ledger.

Sources, extractors, compounds, vector matching and new copy renderers are NOT
activated by declaring predicates. Costs, access claims and causal interpretations
in the brainstorming ledger are not copied into normative facts.
"""
from copy import deepcopy
from .shapes import *

RECORD=obj({'namespace':ID,'record_id':S})
PUBLISHED=obj({'namespace':ID,'record_id':S,'url':URI,'publisher':S,'published_at':nullable(UTC),
    'record_type':S,'title':S,'text':S})
CASE_OUTCOME=obj({'case_id':S,'outcome_id':S,'publisher':S,'source_url':URI,'reported_quote':S,
    'metric_name':S,'reported_value':NUM,'unit':S,'baseline_value':nullable(NUM),
    'comparison_kind':enum('ABSOLUTE','ABSOLUTE_CHANGE','RELATIVE_CHANGE','UNSPECIFIED'),
    'measurement_window':nullable(WINDOW),'sample_size':nullable(POS),'method_description':nullable(S),
    'attribution':{'const':'PUBLISHER_REPORTED_NOT_CAUSALLY_VERIFIED'},'transfer_to_target_allowed':{'const':False}})
add('PublishedRecordValue',PUBLISHED)
add('CaseStudyOutcomeValue',CASE_OUTCOME)
add('LookalikeMatch',obj({'match_id':ID,'run_id':ID,'tenant_id':ID,'target_subject_id':ID,'comparison_subject_id':ID,
    'input_fact_ids':arr(ID,1,True),'corpus_release':HASH,'representation_version':VER,'index_version':VER,
    'similarity_score':NUM,'missing_features':arr(S),'differences':arr(S,1),'outcome_transfer_allowed':{'const':False},
    'use':{'const':'INTERNAL_RANKING'},'implementation_status':{'const':'DESIGN_ONLY'}}))
add('ScenarioEstimate',obj({'scenario_id':ID,'tenant_id':ID,'subject_id':ID,'observed_input_fact_ids':arr(ID,0,True),
    'assumptions':arr(obj({'name':ID,'value':NUM,'unit':S,'basis':S}),1),'formula_version':VER,
    'currency':CURRENCY,'lower_minor':INT,'upper_minor':INT,'time_period':S,'limitations':arr(S,1),
    'verified_loss':{'const':False},'implementation_status':{'const':'DESIGN_ONLY'}}))


def extend_ledger(reg):
    from .catalog import specimen
    reg=deepcopy(reg)
    def addp(pid,value,*,natures=('THIRD_PARTY_REPORT',),kinds=('ORG','LOCATION'),target=RECORD,value_class='TypedValue',description='',refs=()):
        reg['predicates'].append({'predicate_id':pid,'version':'4.2.0','family':'ledger_evidence','description':description,
            'subject_kinds':list(kinds),'target_schema':deepcopy(target),'value_schema':deepcopy(value),'allowed_natures':list(natures),
            'allowed_processors':['DETERMINISTIC','LLM','HUMAN_REVIEW'],'absence_allowed':False,'temporal_mode':'EVENT',
            'copy_policy':'ATTRIBUTED_ONLY' if 'REGISTRY_RECORD' not in natures else 'REGISTRY_ATTRIBUTED','reference_rules':list(refs),
            'section_ids':[],'value_class':value_class,'origin':'V4_ADDED','example_target':specimen(target),'example_value':specimen(value)})
    addp('publication.record',PUBLISHED,natures=('FIRST_PARTY_STATEMENT','THIRD_PARTY_REPORT'),value_class='PublishedRecordValue',
         description='Captured press, social, news or case-study publication; publisher claim, not verified execution of a project.')
    statement=obj({'statement_id':ID,'text':S,'topic_id':ID,'modality':enum('CURRENT_STATE','REQUIREMENT','PLAN','OPINION','UNSPECIFIED'),
        'speaker':S,'publisher':S,'channel':enum('PRESS','SOCIAL','TRANSCRIPT','EMPLOYEE_REVIEW','CASE_STUDY'),
        'timecode_seconds':nullable(NONNEG),'published_at':nullable(UTC)})
    addp('publication.statement',statement,natures=('FIRST_PARTY_STATEMENT','THIRD_PARTY_REPORT'),target=obj({'statement_id':ID}),
        description='Attributable exact statement, including transcript speaker and optional timecode. Not a verified account operating condition.')
    addp('organization.event_report',obj({'event_id':S,'event_type':enum('FUNDING','LAUNCH','HIRE','OPENING','EXPANSION','PARTNERSHIP','PILOT'),
        'reported_event_at':nullable(UTC),'announced_at':UTC,'publisher':S,'text':S}),target=obj({'event_id':S}),
        natures=('FIRST_PARTY_STATEMENT','THIRD_PARTY_REPORT'),description='Reported corporate event with occurrence and announcement times kept separate.')
    addp('repository.activity_observed',obj({'repository_url':URI,'commit_id':S,'branch':S,'path':S,
        'activity':enum('REPOSITORY_CREATED','DEPENDENCY_ADDED','DEPENDENCY_REMOVED','CODE_CHANGED'),'observed_value':S,'committed_at':UTC}),
        natures=('DIRECT_OBSERVATION',),target=obj({'repository_url':URI,'commit_id':S,'path':S}),
        description='Public repository change. A dependency is not evidence of production deployment or organization-wide adoption.')
    addp('event.public_participation',obj({'event_id':S,'event_name':S,'role':enum('SPEAKER','SPONSOR','EXHIBITOR'),
        'event_at':nullable(UTC),'publisher':S,'listing_url':URI}),target=obj({'event_id':S,'role':S}),
        description='Published organizational participation; not attendance, budget or intent.')
    addp('event.authorized_attendance',obj({'event_id':S,'record_id':S,'status':enum('REGISTERED','ATTENDED','INTERESTED'),
        'permission_reference':S,'recorded_by':S}),target=obj({'event_id':S,'record_id':S}),
        kinds=('ORG','PERSON'),natures=('THIRD_PARTY_REPORT','DIRECT_OBSERVATION'),
        description='Permissioned registration/attendance record. Registration and interested are not attendance. Requires authorized scope.')
    reg['predicates'][-1]['copy_policy']='INTERNAL_ONLY'
    addp('trade.shipment_record',obj({'namespace':ID,'record_id':S,'filed_at':UTC,'direction':enum('IMPORT','EXPORT'),
        'commodity_description':S,'quantity':nullable(NONNEG),'quantity_unit':nullable(S),'issuer':S}),
        natures=('REGISTRY_RECORD','THIRD_PARTY_REPORT'),description='Namespaced reported shipment; not purchase intent or a growth conclusion.')
    addp('procurement.record',obj({'namespace':ID,'record_id':S,'issuer':S,'stage':enum('NOTICE','BID','AWARD','CANCELLED'),
        'filed_at':UTC,'description':S,'amount_minor':nullable(INT),'currency':nullable(CURRENCY)}),
        natures=('REGISTRY_RECORD','THIRD_PARTY_REPORT'),description='Procurement stage is explicit. A notice is not a won contract.')
    addp('legal.filing_record',obj({'namespace':ID,'record_id':S,'court':S,'jurisdiction':S,'filed_at':UTC,
        'procedural_status':enum('ALLEGATION','PENDING','DISMISSED','SETTLED','JUDGMENT','UNKNOWN'),'reported_description':S}),
        natures=('REGISTRY_RECORD',),description='Exact legal filing/procedural record. Allegations and settlement do not establish wrongdoing or failed AI implementation.')
    reg['predicates'][-1]['copy_policy']='INTERNAL_ONLY'
    addp('award.listing',obj({'list_id':S,'edition':S,'issuer':S,'rank':nullable(POS),'listed_at':UTC,'category':S}),
        target=obj({'list_id':S,'edition':S}),description='Listing in a named edition; not a current measured growth rate or proof of technical lag.')
    addp('patent.application_record',obj({'namespace':ID,'record_id':S,'jurisdiction':S,'filed_at':UTC,
        'status':enum('APPLICATION','PUBLISHED','GRANTED','ABANDONED','EXPIRED','UNKNOWN'),'title':S}),natures=('REGISTRY_RECORD',),
        description='Patent status and date, not deployed capability or available budget.')
    addp('franchise.disclosure_record',obj({'namespace':ID,'record_id':S,'edition_year':POS,'issuer':S,'reported_unit_count':nullable(INT),
        'system_scope':S,'item_reference':S,'reported_text':S}),natures=('REGISTRY_RECORD','THIRD_PARTY_REPORT','FIRST_PARTY_STATEMENT'),
        description='System/edition-bound disclosure, not a franchisee-specific revenue assertion.')
    addp('registry.financing_filing',obj({'namespace':ID,'record_id':S,'issuer':S,'jurisdiction':S,'filed_at':UTC,
        'filing_kind':enum('UCC_INITIAL','UCC_AMENDMENT','UCC_TERMINATION','OTHER'),'collateral_description':nullable(S)}),
        natures=('REGISTRY_RECORD',),description='Financing-statement filing. No assumption about cash received, solvency, growth or spending willingness.')
    addp('registry.loan_record',obj({'namespace':ID,'record_id':S,'program':S,'issuer':S,'record_date':UTC,
        'status':S,'amount_minor':nullable(INT),'currency':nullable(CURRENCY)}),natures=('REGISTRY_RECORD',),
        description='Historical program/loan record. Not current company size, budget or propensity to buy.')
    addp('case_study.report',obj({'case_id':S,'publisher':S,'source_url':URI,'reported_customer_name':S,
        'product_id':nullable(ID),'published_at':nullable(UTC),'project_description':S,'size_at_project':nullable(S),
        'customer_relationship':{'const':'PUBLISHER_REPORTED'}}),target=obj({'case_id':S}),
        description='Vendor/customer-reported case about the comparison organization, never a claim that KeenSight delivered it.')
    reg['predicates'][-1]['reference_rules']=[{'container':'object','path':'/product_id','subject_kinds':['SOFTWARE_PRODUCT'],'target_type':'SUBJECT'}]
    addp('case_study.outcome_report',CASE_OUTCOME,target=obj({'case_id':S,'outcome_id':S}),value_class='CaseStudyOutcomeValue',
        description='Reported outcome with denominator/method gaps preserved. Exact percentage is specificity, not credibility or causal proof.')
    return reg
