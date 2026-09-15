"""Broad ontology authoring. Core shapes remain closed; extension is via registry release."""
from copy import deepcopy
from pathlib import Path
import json
from .shapes import *
ROOT=Path(__file__).resolve().parents[1]


def specimen(s):
    if 'const' in s:return deepcopy(s['const'])
    if 'enum' in s:return deepcopy(s['enum'][0])
    if 'anyOf' in s:return specimen(s['anyOf'][0])
    if 'oneOf' in s:return specimen(s['oneOf'][0])
    t=s.get('type')
    if isinstance(t,list):t=next(x for x in t if x!='null')
    if t=='object':return {k:specimen(s['properties'][k]) for k in s.get('required',[])}
    if t=='array':
        out=[specimen(s['items']) for _ in range(s.get('minItems',0))]
        if s.get('uniqueItems'):
            for i,x in enumerate(out):
                if isinstance(x,str):out[i]=x+str(i)
        return out
    if t=='boolean':return False
    if t in ('number','integer'):return s.get('minimum',max(1,s.get('exclusiveMinimum',0)+1))
    if t=='null':return None
    if s.get('format')=='date-time':return '2026-09-01T00:00:00Z'
    if s.get('format')=='uri':return 'https://example.test/resource'
    if s.get('format')=='email':return 'fixture@example.test'
    pat=s.get('pattern','')
    if 'sha256' in pat:return 'sha256:'+'0'*64
    if '[A-Z]{3}' in pat:return 'USD'
    if '[A-Z]{2}' in pat:return 'US'
    if '\\d+' in pat and '\\.' in pat:return '1.0.0'
    return 'sample'


def at_schema(s,path):
    for part in path.lstrip('/').split('/'):
        s=s.get('properties',{}).get(part,S)
    return deepcopy(s)

P=[]
def predicate(name,family,shape,*,target=None,kinds=('ORG','LOCATION'),natures=('DIRECT_OBSERVATION',),sections=(),
              absence=False,period=False,event=False,copy='DIRECT_SCOPED',value_class='TypedValue',refs=(),description=None,origin='V4_ADDED',processors=None):
    p={'predicate_id':name,'version':'4.0.0','family':family,'description':description or name.replace('.',' '),
       'subject_kinds':list(kinds),'target_schema':target or obj({}),'value_schema':deepcopy(shape),'allowed_natures':list(natures),
       'allowed_processors':processors or (['DERIVATION'] if set(natures)<={'INFERENCE','DERIVED_MEASUREMENT'} else ['DETERMINISTIC','LLM','HUMAN_REVIEW']),
       'absence_allowed':absence,'temporal_mode':'PERIOD' if period else ('EVENT' if event else 'POINT'),'copy_policy':copy,
       'reference_rules':list(refs),'section_ids':list(sections),'value_class':value_class,'origin':origin,
       'example_target':specimen(target or obj({})),'example_value':specimen(shape)}
    P.append(p);return p

# Preserve every prior identifier, but use the v4 envelope and explicit identities.
legacy=json.loads((ROOT/'reference/v3-predicates.json').read_text())
for old in legacy:
    name=old['predicate']; shape=deepcopy(old['value_schema']); ids=old['identity_paths']
    target=obj({x.lstrip('/').replace('/','_'):at_schema(shape,x) for x in ids})
    natures=['DIRECT_OBSERVATION']; cp='DIRECT_SCOPED'; proc=['DETERMINISTIC','HUMAN_REVIEW']
    if old['allowed_tiers']==['HUMAN']:
        natures=['FIRST_PARTY_STATEMENT'];cp='ATTRIBUTED_ONLY';proc=['HUMAN_REVIEW']
    if 'DERIVED' in old['allowed_tiers'] or 'COHORT' in old['allowed_tiers']:
        natures=['INFERENCE'] if name.startswith('tag.') else ['DERIVED_MEASUREMENT'];cp='INTERNAL_ONLY';proc=['DERIVATION']
    if old['visibility']=='INTERNAL_ONLY':cp='INTERNAL_ONLY'
    if old['visibility']=='COHORT_ONLY':cp='CONTEXT_ONLY'
    if name in ['company.self_claim','crm.note','hiring.role']:
        natures=['FIRST_PARTY_STATEMENT'];cp='ATTRIBUTED_ONLY';proc=['DETERMINISTIC','LLM','HUMAN_REVIEW']
    if name.startswith('review.'):
        natures=['THIRD_PARTY_REPORT'];cp='ATTRIBUTED_ONLY'
    if name in ['seo.authority','seo.keyword.footprint','firmo.revenue_band']:
        natures=['PROVIDER_ESTIMATE','FIRST_PARTY_STATEMENT'];cp='ESTIMATE_ATTRIBUTED'
    revised=False
    # Non-exclusive objects must not be global singletons.
    for field in {'company.self_claim':'claim','crm.note':'note_id','person.contact':'profile_url',
                  'api.public.present':'url','app.mobile.present':'app_id','status.page.present':'url',
                  'cert.new_subdomain':'hostname','vendor.certification_badge':'badge',
                  'competitor.presence':'peer_subject_id'}.get(name,'').split():
        target=obj({field:at_schema(shape,'/'+field)});revised=True
    if name=='review.metrics':
        shape['properties']['monthly_counts']=arr(obj({'window':WINDOW,'count':INT}))
        revised=True
    if name=='headcount.history':
        shape=arr(obj({'effective_at':UTC,'count':INT,'provider':S}),1);revised=True
    if name=='ads.activity':
        shape['properties']['monthly_counts']=arr(obj({'window':WINDOW,'count':INT}));revised=True
    section=[]
    for prefix,sec in [('hiring.',1),('vendor.',2),('dns.',2),('review.',5),('seo.',8),('ads.',8),('app.',8),('company.',11)]:
        if name.startswith(prefix):section.append(sec)
    row=predicate(name,'legacy.'+old['domain'].lower().replace('/','_'),shape,target=target,kinds=old['subject_kinds'],natures=natures,
        sections=section,absence=old['absence_allowed'],copy=cp,origin='V3_REVISED' if revised else 'V3_RETAINED',processors=proc,
        description=old['description'],value_class='LegacyTypedValue')
    # Known chronological examples get distinct interval bounds.
    def fix_windows(x):
        if isinstance(x,dict):
            if 'start' in x and 'end' in x and isinstance(x['end'],str):x['end']='2026-09-02T00:00:00Z'
            for v in x.values():fix_windows(v)
        elif isinstance(x,list):
            for v in x:fix_windows(v)
    fix_windows(row['example_value'])

PRODUCT=obj({'product_id':ID})
PRODUCT_REF={'container':'target','path':'/product_id','subject_kinds':['SOFTWARE_PRODUCT']}
STATEMENT=obj({'statement_id':ID,'text':S,'topic_id':ID,'modality':enum('CURRENT_STATE','REQUIREMENT','ASPIRATION','NEGATED','UNCERTAIN')})
STATEMENT_TARGET=obj({'statement_id':ID})
HYPOTHESIS=obj({'hypothesis_id':ID,'conclusion':S,'alternatives':arr(S,1),'limitations':arr(S,1),'verification_question':S})
HYP_TARGET=obj({'hypothesis_id':ID})

# 1 -- hiring. Salary is independent so unavailable pay does not invalidate a posting.
predicate('careers.page','hiring',obj({'url':URI,'discovery_method':enum('LINK','SITEMAP','ATS_API')}),target=obj({'url':URI}),sections=[1],absence=True)
predicate('careers.ats','hiring',obj({'product_id':ID,'tenant_key':nullable(S),'url':URI}),target=PRODUCT,refs=[PRODUCT_REF],sections=[1],value_class='TechnologyValue')
job=obj({'posting_id':S,'namespace':ID,'url':URI,'title':S,'department':nullable(S),'published_at':nullable(UTC),'employment_type':nullable(enum('FULL_TIME','PART_TIME','CONTRACT','TEMPORARY','INTERNSHIP','OTHER'))})
predicate('job.posting','hiring',job,target=obj({'namespace':ID,'posting_id':S}),sections=[1],natures=['FIRST_PARTY_STATEMENT'],copy='ATTRIBUTED_ONLY',value_class='JobPostingValue')
predicate('job.status','hiring',obj({'status':enum('OPEN','CLOSED','REMOVED','PAUSED'),'effective_at':UTC}),target=obj({'namespace':ID,'posting_id':S}),sections=[1],natures=['FIRST_PARTY_STATEMENT'],copy='ATTRIBUTED_ONLY')
salary=obj({'minimum_minor':nullable(INT),'maximum_minor':nullable(INT),'currency':CURRENCY,'minor_unit_exponent':{'type':'integer','minimum':0,'maximum':4},'period':enum('HOUR','DAY','WEEK','MONTH','YEAR','PROJECT'),'basis':enum('BASE','TOTAL_COMPENSATION','UNSPECIFIED')})
predicate('job.salary','hiring',salary,target=obj({'namespace':ID,'posting_id':S,'component':S}),sections=[1],natures=['FIRST_PARTY_STATEMENT'],copy='ATTRIBUTED_ONLY',value_class='SalaryValue')
P[-1]['example_value']['minimum_minor']=6000000;P[-1]['example_value']['maximum_minor']=8000000
for name,shape in {
 'work_arrangement':obj({'mode':enum('REMOTE','HYBRID','ONSITE','UNSPECIFIED')}),
 'location':obj({'country':S,'region':nullable(S),'city':nullable(S)}),
 'skill_requirement':obj({'skill':S,'required':BOOL,'text':S}),
 'department':obj({'department':S}),
}.items():predicate('job.'+name,'hiring',shape,target=obj({'namespace':ID,'posting_id':S,'item_key':S}),sections=[1],natures=['FIRST_PARTY_STATEMENT'],copy='ATTRIBUTED_ONLY')
for typ in ['workflow','document','tool','handoff','manual_process','spreadsheet','crm','follow_up']:
    predicate('job.'+typ+'_statement','hiring',STATEMENT,target=STATEMENT_TARGET,sections=[1,11],natures=['FIRST_PARTY_STATEMENT'],copy='ATTRIBUTED_ONLY',value_class='AttributedStatementValue')
predicate('hiring.change_event','hiring',obj({'posting_id':S,'change':enum('ADDED','REMOVED','UPDATED'),'before_fact_id':nullable(ID),'after_fact_id':nullable(ID),'comparable':BOOL}),target=obj({'event_id':ID}),sections=[1],natures=['DERIVED_MEASUREMENT'],event=True,copy='INTERNAL_ONLY')

# 2,3 -- many signatures share a small set of canonical observation predicates.
tech=obj({'product_id':ID,'version':nullable(S),'surface':enum('SCRIPT','IFRAME','FORM','NETWORK','COOKIE','HEADER','CSP','DNS','CERTIFICATE','SUBDOMAIN','JSON_LD','ATTRIBUTE'),
          'matched_value':S,'fingerprint_id':ID,'deployment_claim':{'const':'PUBLIC_FOOTPRINT_ONLY'}})
predicate('technology.footprint','technology',tech,target=PRODUCT,refs=[PRODUCT_REF],sections=[2,3,10],absence=True,value_class='TechnologyValue')
report=obj({'product_id':ID,'provider':S,'provider_detected_at':nullable(UTC),'reported_version':nullable(S)})
predicate('technology.provider_report','technology',report,target=PRODUCT,refs=[PRODUCT_REF],sections=[2,3,8],natures=['THIRD_PARTY_REPORT'],copy='ATTRIBUTED_ONLY',value_class='TechnologyReportValue')
for suffix,fields,key in [
 ('script',{'src':URI},'src'),('form_action',{'action':URI},'action'),('cookie',{'cookie_name':S},'cookie_name'),
 ('header',{'header_name':S,'header_value':S},'header_name'),('csp',{'directive':S,'host':S},'directive'),
 ('subdomain',{'hostname':S,'resolved_target':nullable(S)},'hostname'),('network_request',{'url':URI,'method':enum('GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS'),'resource_type':S},'url'),
 ('static_global',{'symbol':S},'symbol')]:
    predicate('technology.'+suffix,'technology',obj(fields),target=obj({key:fields[key]}),sections=[2],value_class='SurfaceObservationValue')
predicate('technology.account_identifier','technology',obj({'product_id':ID,'identifier_kind':S,'identifier_hash':HASH}),target=obj({'product_id':ID,'identifier_kind':S,'identifier_hash':HASH}),refs=[PRODUCT_REF],sections=[2],copy='INTERNAL_ONLY')
predicate('technology.cooccurrence','technology',obj({'product_ids':arr(ID,2,True),'scope_limitations':S}),target=obj({'set_id':HASH}),sections=[2,3],natures=['DERIVED_MEASUREMENT'],copy='INTERNAL_ONLY')
predicate('technology.change','technology',obj({'product_id':ID,'change':enum('APPEARED','NO_LONGER_DETECTED','VERSION_CHANGED'),'previous_fact_id':ID,'current_fact_id':ID,'comparable_capture':BOOL}),target=obj({'product_id':ID,'event_id':ID}),refs=[PRODUCT_REF],sections=[2,3],natures=['DERIVED_MEASUREMENT'],copy='INTERNAL_ONLY',event=True)
for suffix,shape in {
 'capability':obj({'capability_id':ID,'text':S,'modality':enum('VENDOR_CLAIM','DOCUMENTED_FEATURE')}),
 'vertical':obj({'industry_id':ID,'text':S}),
 'category':obj({'category_id':ID,'text':S}),
 'integration_support':obj({'other_product_id':ID,'text':S,'integration_kind':enum('NATIVE','CONNECTOR','API','UNKNOWN')})}.items():
    predicate('product.'+suffix,'product',shape,target=obj({'item_id':ID}),kinds=['SOFTWARE_PRODUCT'],natures=['FIRST_PARTY_STATEMENT','THIRD_PARTY_REPORT'],sections=[3,4,6],copy='CONTEXT_ONLY')
portal=obj({'url':URI,'portal_type':enum('PATIENT','CLIENT','CASE_MANAGEMENT','IDX','DISPATCH','QUOTE','BOOKING','PAYMENT','ECOMMERCE','INSURANCE','OTHER'),'product_id':nullable(ID)})
predicate('portal.observed','vertical_software',portal,target=obj({'url':URI}),sections=[3,10],absence=True)
predicate('integration.public_marker','vertical_software',obj({'from_product_id':ID,'to_product_id':ID,'marker':S,'verified_connection':{'const':False}}),target=obj({'from_product_id':ID,'to_product_id':ID}),sections=[3],copy='DIRECT_SCOPED')

# 4,5,6 -- attributed records and sample-bounded summaries, not prospect pain assertions.
review=obj({'review_key':S,'platform':S,'published_at':UTC,'rating':nullable(NONNEG),'rating_scale_max':nullable(NONNEG),'text':S,'language':S,'edited':BOOL})
review_target=obj({'platform':S,'review_key':S})
predicate('review.record','reviews',review,target=review_target,kinds=['ORG','LOCATION','SOFTWARE_PRODUCT','APPLICATION','LISTING'],natures=['THIRD_PARTY_REPORT'],sections=[4,5,8],copy='ATTRIBUTED_ONLY',value_class='ReviewRecordValue',event=True)
predicate('review.statement','reviews',STATEMENT,target=STATEMENT_TARGET,kinds=['ORG','LOCATION','SOFTWARE_PRODUCT','APPLICATION'],natures=['THIRD_PARTY_REPORT'],sections=[4,5],copy='ATTRIBUTED_ONLY',value_class='AttributedStatementValue',event=True)
predicate('review.owner_response','reviews',obj({'review_key':S,'response_key':S,'text':S,'published_at':UTC}),target=obj({'platform':S,'response_key':S}),natures=['FIRST_PARTY_STATEMENT'],sections=[5,8],copy='ATTRIBUTED_ONLY',event=True)
classification=obj({'theme_id':ID,'record_key':S,'sentiment':enum('POSITIVE','NEGATIVE','NEUTRAL','MIXED'),'stance':enum('EXPERIENCED','ASKED','NEGATED','QUOTED','UNCERTAIN'),'support_locator_ids':arr(ID,1,True)})
predicate('review.theme_classification','reviews',classification,target=obj({'record_key':S,'theme_id':ID}),kinds=['ORG','LOCATION','SOFTWARE_PRODUCT','APPLICATION'],natures=['INFERENCE'],sections=[4,5,8],copy='INTERNAL_ONLY',value_class='ThemeClassificationValue')
post=obj({'post_key':S,'community':S,'thread_key':S,'published_at':UTC,'text':S,'language':S,'role':enum('POST','COMMENT')})
predicate('discussion.record','community',post,target=obj({'community':S,'post_key':S}),kinds=['SOFTWARE_PRODUCT','INDUSTRY'],natures=['THIRD_PARTY_REPORT'],sections=[6],copy='CONTEXT_ONLY',event=True,value_class='DiscussionRecordValue')
predicate('discussion.statement','community',STATEMENT,target=STATEMENT_TARGET,kinds=['SOFTWARE_PRODUCT','INDUSTRY'],natures=['THIRD_PARTY_REPORT'],sections=[6],copy='CONTEXT_ONLY',value_class='AttributedStatementValue',event=True)
predicate('discussion.theme_classification','community',classification,target=obj({'record_key':S,'theme_id':ID}),kinds=['SOFTWARE_PRODUCT','INDUSTRY'],natures=['INFERENCE'],sections=[6],copy='CONTEXT_ONLY',value_class='ThemeClassificationValue')
for name,kinds,sections,cp in [('product.pain_prior',['SOFTWARE_PRODUCT'],[4,6],'CONTEXT_ONLY'),('industry.pain_prior',['INDUSTRY'],[6],'CONTEXT_ONLY'),('review.theme_summary',['ORG','LOCATION'],[5],'INTERNAL_ONLY')]:
    predicate(name,'research',SCHEMAS['ResearchPriorValue'],target=obj({'sample_id':ID,'theme_id':ID}),kinds=kinds,natures=['DERIVED_MEASUREMENT'],sections=sections,period=True,copy=cp,value_class='ResearchPriorValue')
predicate('account.industry_membership','identity',obj({'industry_id':ID,'basis':enum('EXPLICIT_SELF_DESCRIPTION','REGISTRY_CLASSIFICATION')}),target=obj({'industry_id':ID}),refs=[{'container':'target','path':'/industry_id','subject_kinds':['INDUSTRY']}],sections=[9,11],natures=['FIRST_PARTY_STATEMENT','REGISTRY_RECORD'],copy='ATTRIBUTED_ONLY')

# 8 -- primitive records supplement metric definitions, not a provider-shaped JSON bag.
for name,fields,target in [
 ('search.result',{'query':S,'engine':S,'rank':POS,'url':URI,'title':S,'result_type':enum('ORGANIC','PAID','LOCAL','SHOPPING','APP')},{'query':S,'engine':S,'rank':POS,'country':S,'device':S}),
 ('business.profile_attribute',{'profile_id':S,'attribute_id':ID,'reported_value':S},{'profile_id':S,'attribute_id':ID}),
 ('backlink.record',{'source_url':URI,'target_url':URI,'anchor':S,'rel':arr(S),'first_seen':nullable(UTC),'last_seen':nullable(UTC)},{'source_url':URI,'target_url':URI}),
 ('web.mention',{'url':URI,'text':S,'published_at':nullable(UTC),'matched_entity':S},{'mention_key':S}),
 ('web.mention_sentiment',{'mention_key':S,'sentiment':enum('POSITIVE','NEGATIVE','NEUTRAL','MIXED'),'basis':S},{'mention_key':S}),
 ('app.listing',{'store':S,'app_id':S,'url':URI,'title':S,'category':S,'published_at':nullable(UTC)},{'store':S,'app_id':S}),
 ('shopping.listing',{'marketplace':S,'listing_id':S,'title':S,'url':URI,'price_minor':nullable(INT),'currency':nullable(CURRENCY),'availability':enum('IN_STOCK','OUT_OF_STOCK','UNKNOWN')},{'marketplace':S,'listing_id':S}),
 ('advertisement.record',{'platform':S,'ad_id':S,'creative_text':S,'landing_url':nullable(URI),'status':enum('ACTIVE','INACTIVE','UNKNOWN'),'start_at':nullable(UTC),'end_at':nullable(UTC)},{'platform':S,'ad_id':S})]:
    nat=['INFERENCE'] if 'sentiment' in name else ['THIRD_PARTY_REPORT']
    predicate(name,'commodity_data',obj(fields),target=obj(target),kinds=['ORG','LOCATION','WEBSITE','APPLICATION','LISTING'],natures=nat,sections=[8],copy='INTERNAL_ONLY' if nat==['INFERENCE'] else 'ATTRIBUTED_ONLY')

# 9 -- registry assertions have their own semantics; identifier != licensure.
regbase={'namespace':ID,'record_id':S,'issuer':S,'jurisdiction':S,'effective_at':nullable(UTC),'filed_at':nullable(UTC),'record_status':S}
for suffix,fields in {
 'registration':{'registration_kind':enum('NPI','ADVISER_FIRM','ADVISER_REPRESENTATIVE','BAR_REGISTRATION','BUSINESS_REGISTRATION'),'identifier':S},
 'license':{'license_kind':S,'license_number':S,'valid_from':nullable(UTC),'valid_until':nullable(UTC)},
 'permit':{'permit_type':S,'permit_number':S,'site_address':S,'project_description':S},
 'specialty':{'taxonomy_system':S,'specialty_code':S,'specialty_label':S},
 'filing':{'form':S,'filing_period':WINDOW,'document_url':URI},
 'affiliation':{'organization_subject_id':ID,'role':S,'basis':S},
}.items():
    predicate('registry.'+suffix,'public_registry',obj({**regbase,**fields}),target=obj({'namespace':ID,'record_id':S}),kinds=['ORG','LOCATION','PERSON'],
       natures=['REGISTRY_RECORD'],sections=[9],copy='REGISTRY_ATTRIBUTED',value_class='RegistryRecordValue',event=True)

# 10 -- public surfaces, authorized operations, and economic estimates stay separate.
predicate('phone.cta','phone',obj({'number_public':S,'href':S,'placement':enum('HEADER','BODY','FOOTER','STICKY'),'label':S}),target=obj({'number_public':S,'placement':S}),sections=[10])
predicate('phone.routing_observed','phone',obj({'destination_public':S,'surface':enum('TEL_LINK','TRACKING_SCRIPT','IVR_PUBLIC_DESCRIPTION'),'text':S}),target=obj({'surface_key':S}),sections=[10],copy='DIRECT_SCOPED')
predicate('phone.routing_verified','phone',obj({'system_id':ID,'routing_rule':S,'verified_at':UTC}),target=obj({'system_id':ID,'rule_key':S}),natures=['FIRST_PARTY_STATEMENT','DIRECT_OBSERVATION'],sections=[10],copy='ATTRIBUTED_ONLY')
predicate('phone.recording_verified','phone',obj({'system_id':ID,'enabled':BOOL,'authorization_ref':S}),target=obj({'system_id':ID}),natures=['FIRST_PARTY_STATEMENT','DIRECT_OBSERVATION'],sections=[10],copy='INTERNAL_ONLY')
call=obj({'call_key':S,'started_at':UTC,'direction':enum('INBOUND','OUTBOUND'),'status':enum('ANSWERED','MISSED','ABANDONED','VOICEMAIL','UNKNOWN'),'duration_seconds':nullable(NONNEG),'callback_of':nullable(S)})
predicate('phone.call_event','phone',call,target=obj({'system_id':ID,'call_key':S}),natures=['DIRECT_OBSERVATION'],sections=[10],copy='INTERNAL_ONLY',event=True,value_class='CallEventValue')
predicate('phone.economics_hypothesis','phone',obj({'currency':CURRENCY,'estimated_amount_minor':INT,'assumptions':arr(S,1),'limitations':arr(S,1)}),target=obj({'scenario_id':ID}),natures=['INFERENCE'],sections=[10],period=True,copy='INTERNAL_ONLY',value_class='EconomicHypothesisValue')

# 11 -- broad business/workflow statements are separate from internal inference.
for area in ['business_model','customer_type','lead_channel','sales_motion','document_type','handoff','intent','service_offering',
             'geographic_market','workflow_step','role_responsibility','knowledge_source','intake_method','manual_process',
             'approval_process','data_reentry','reporting_process','follow_up','billing_process','scheduling_process','compliance_process']:
    predicate('website.'+area+'_statement','website_analysis',STATEMENT,target=STATEMENT_TARGET,sections=[11],natures=['FIRST_PARTY_STATEMENT'],copy='ATTRIBUTED_ONLY',value_class='AttributedStatementValue')
for area in ['workflow','business_model','customer_type','lead_channel','knowledge_complexity','document_complexity','handoff_risk','automation_opportunity']:
    predicate(area+'.hypothesis','website_analysis',HYPOTHESIS,target=HYP_TARGET,sections=[11],natures=['INFERENCE'],copy='INTERNAL_ONLY',value_class='HypothesisValue')
predicate('document.surface','website_analysis',obj({'url':URI,'media_type':S,'document_type':S,'access':enum('PUBLIC','AUTHENTICATED','UNKNOWN')}),target=obj({'url':URI}),sections=[11],absence=True)
predicate('form.surface','website_analysis',obj({'url':URI,'field_labels':arr(S),'action':nullable(URI),'method':enum('GET','POST','UNKNOWN')}),target=obj({'form_key':S}),sections=[11],absence=True)

# Typed metric families; definitions constrain unit, dimensions, range, and epistemic kind.
METRICS=[]
def metric(mid,desc,unit='count',dims=None,sections=(8,),aggregation='COUNT',natures=('DIRECT_OBSERVATION','THIRD_PARTY_REPORT'),den=False,kinds=('ORG','LOCATION','WEBSITE'),maximum=None,minimum=0):
    value={'type':'number','minimum':minimum}
    if unit in ['count','rank']:value['type']='integer'
    if unit=='rank':value['minimum']=1
    if maximum is not None:value['maximum']=maximum
    METRICS.append({'metric_id':mid,'description':desc,'unit':unit,'value_schema':value,
      'dimensions_schema':obj(dims or {}),'requires_denominator':den,'aggregation':aggregation,
      'allowed_natures':list(natures),'subject_kinds':list(kinds),'section_ids':list(sections)})
TRAFFIC_DIMS={'country':S,'device':enum('DESKTOP','MOBILE_WEB','ALL'),'granularity':enum('DAILY','WEEKLY','MONTHLY')}
for mid,desc,unit,agg in [
 ('visits','Estimated visits','count','ESTIMATE'),('unique_visitors','Estimated unique visitors','count','ESTIMATE'),
 ('pageviews','Estimated pageviews','count','ESTIMATE'),('pages_per_visit','Estimated pages per visit','pages_per_visit','ESTIMATE'),
 ('visit_duration','Estimated visit duration','seconds','ESTIMATE'),('bounce_rate','Estimated bounce proportion','proportion','ESTIMATE'),
 ('growth','Estimated growth across comparable periods','proportion_change','ESTIMATE'),('global_rank','Estimated worldwide rank','rank','RANK'),
 ('country_rank','Estimated country rank','rank','RANK'),('category_rank','Estimated category rank','rank','RANK')]:
    metric('traffic.'+mid,desc,unit,TRAFFIC_DIMS,sections=[7],aggregation=agg,natures=['PROVIDER_ESTIMATE'],maximum=1 if unit=='proportion' else None,minimum=-1 if mid=='growth' else 0)
for mid,extra in [('channel_share',{'channel':S}),('geography_share',{'visitor_country':S}),('popular_page_share',{'page_url':URI}),
 ('referral_share',{'referring_domain':S}),('outgoing_share',{'outgoing_domain':S}),('paid_referral_concentration',{'top_n':POS}),
 ('audience_overlap',{'peer_domain':S,'basis':S}),('social_source_share',{'social_network':S}),('device_share',{'device_segment':S})]:
    metric('traffic.'+mid,mid.replace('_',' '),'proportion',{**TRAFFIC_DIMS,**extra},sections=[7],aggregation='ESTIMATE',natures=['PROVIDER_ESTIMATE'],maximum=1)
for mid in ['organic_visits','paid_visits','referral_visits','social_visits','direct_visits','search_visits']:
    metric('traffic.'+mid,mid.replace('_',' '),'count',TRAFFIC_DIMS,sections=[7],aggregation='ESTIMATE',natures=['PROVIDER_ESTIMATE'])
for mid in ['open_postings','new_postings','closed_postings','workflow_mention_count','spreadsheet_mention_count','document_mention_count']:
    metric('hiring.'+mid,mid.replace('_',' '),dims={'department':S,'country':S},sections=[1],natures=['DERIVED_MEASUREMENT'])
for mid in ['count','new_reviews','owner_responses','negative_reviews','theme_support_count']:
    metric('review.'+mid,mid.replace('_',' '),dims={'platform':S,'profile_id':S},sections=[4,5,8],natures=['THIRD_PARTY_REPORT','DERIVED_MEASUREMENT'],kinds=['ORG','LOCATION','SOFTWARE_PRODUCT','APPLICATION'])
metric('review.rating','Reported mean rating','rating',{'platform':S,'profile_id':S,'scale_maximum':NONNEG},sections=[4,5,8],aggregation='MEAN',natures=['THIRD_PARTY_REPORT','DERIVED_MEASUREMENT'],kinds=['ORG','LOCATION','SOFTWARE_PRODUCT','APPLICATION'])
for mid in ['response_ratio','negative_share','theme_share']:
    metric('review.'+mid,mid.replace('_',' '),'proportion',{'platform':S,'profile_id':S},sections=[4,5,8],aggregation='RATE',natures=['DERIVED_MEASUREMENT'],den=True,maximum=1,kinds=['ORG','LOCATION','SOFTWARE_PRODUCT','APPLICATION'])
for mid in ['keyword_count','indexed_pages','backlinks','referring_domains','mentions','broken_links','pages_crawled','local_results_count']:
    metric('seo.'+mid,mid.replace('_',' '),dims={'country':S,'engine':S,'device':S},sections=[8])
for mid in ['organic_rank','paid_rank','local_rank','shopping_rank']:
    metric('seo.'+mid,mid.replace('_',' '),'rank',{'query':S,'country':S,'engine':S,'device':S},sections=[8],aggregation='RANK')
for mid,unit in [('lcp','milliseconds'),('inp','milliseconds'),('cls','score'),('authority','score')]:
    metric('seo.'+mid,mid,'milliseconds' if unit=='milliseconds' else unit,{'country':S,'device':S,'scope_level':enum('PAGE','ORIGIN')},sections=[8],aggregation='DESCRIPTIVE')
for mid in ['search_volume','keyword_difficulty','estimated_organic_traffic','estimated_paid_traffic']:
    metric('seo.'+mid,mid.replace('_',' '),'score' if mid=='keyword_difficulty' else 'count',{'country':S,'query':S,'engine':S},sections=[8],aggregation='ESTIMATE',natures=['PROVIDER_ESTIMATE'])
metric('seo.cpc','Estimated cost per click','currency_major',{'country':S,'query':S,'currency':CURRENCY},sections=[8],aggregation='ESTIMATE',natures=['PROVIDER_ESTIMATE'])
metric('seo.ai_citation_share','Citation proportion in the completed probe set','proportion',{'engine':S,'prompt_set_id':ID,'locale':S},sections=[8],aggregation='RATE',natures=['DERIVED_MEASUREMENT'],den=True,maximum=1)
for family,names,sec in [('registry',['providers','advisers','locations','licenses','permits'],9),('phone',['inbound_calls','answered_calls','missed_calls','callbacks','voicemail_calls'],10),('app',['reviews','ratings','downloads_reported'],8),('shopping',['listings','offers','sellers'],8),('ads',['active_ads','creatives'],8),('technology',['products_detected','domains_observed','cooccurrence_support'],2)]:
    for mid in names:
        n=['REGISTRY_RECORD','DERIVED_MEASUREMENT'] if family=='registry' else ['DIRECT_OBSERVATION','THIRD_PARTY_REPORT','DERIVED_MEASUREMENT']
        metric(family+'.'+mid,mid.replace('_',' '),dims={'segment':S},sections=[sec],natures=n,kinds=['ORG','LOCATION','WEBSITE','SOFTWARE_PRODUCT','APPLICATION','LISTING'])
metric('registry.aum','Reported regulatory assets under management','currency_major',{'currency':CURRENCY,'filing_namespace':S,'form_item':S},sections=[9],natures=['REGISTRY_RECORD'],aggregation='DESCRIPTIVE')
for mid in ['missed_call_rate','callback_rate','booking_conversion_rate']:
    metric('phone.'+mid,mid.replace('_',' '),'proportion',{'system_id':S},sections=[10],natures=['DERIVED_MEASUREMENT'],aggregation='RATE',den=True,maximum=1)
metric('phone.callback_delay','Mean callback delay','seconds',{'system_id':S},sections=[10],natures=['DERIVED_MEASUREMENT'],aggregation='MEAN')
metric('research.theme_share','Sample theme share; not a population frequency','proportion',{'sample_id':S,'theme_id':ID},sections=[4,6],natures=['DERIVED_MEASUREMENT'],aggregation='RATE',den=True,maximum=1,kinds=['SOFTWARE_PRODUCT','INDUSTRY'])
M_TARGET=obj({'metric_id':ID,'dimensions':{'type':'object'},'provider':S,'method_version':S,'reporting_timezone':S})
for family in sorted({m['metric_id'].split('.')[0] for m in METRICS}):
    ms=[m for m in METRICS if m['metric_id'].startswith(family+'.')]
    kinds=sorted({k for m in ms for k in m['subject_kinds']});nat=sorted({n for m in ms for n in m['allowed_natures']});secs=sorted({s for m in ms for s in m['section_ids']})
    p=predicate(family+'.measurement','measurement',SCHEMAS['MeasurementValue'],target=M_TARGET,kinds=kinds,natures=nat,
        sections=secs,period=True,copy='INTERNAL_ONLY' if family in ['research','phone'] else ('ESTIMATE_ATTRIBUTED' if family=='traffic' else 'ATTRIBUTED_ONLY'),value_class='MeasurementValue',processors=['DETERMINISTIC','DERIVATION'])
    first=ms[0];d=specimen(first['dimensions_schema'])
    p['example_target']={'metric_id':first['metric_id'],'dimensions':d,'provider':'Synthetic provider','method_version':'1.0.0','reporting_timezone':'UTC'}
    p['example_value']={'metric_id':first['metric_id'],'value':specimen(first['value_schema']),'unit':first['unit'],'dimensions':d,'method_version':'1.0.0','reporting_timezone':'UTC','numerator':None,'denominator':None,'sample_size':None,'uncertainty':None}
    if first['requires_denominator']:p['example_value'].update(value=0,numerator=0,denominator=10,sample_size=10)

THEMES=['scheduling','missed_calls','billing','paperwork','follow_up','reporting','integration','support','missing_features','data_reentry','spreadsheets','manual_handoff','switching','automation_question','document_search','approval_delay','intake','crm','salary','sales','compliance','inventory','dispatch','quoting','case_management','knowledge_complexity']
TAXONOMY=[{'term_id':'theme.'+t,'scheme_id':'keensight.workflow','scheme_version':'1.0.0','label':t.replace('_',' '),'parent_id':None} for t in THEMES]

SECTIONS={
1:('Careers / ATS and job-description workflow mining',['careers.page','careers.ats','job.posting','job.status','job.salary','job.work_arrangement','job.workflow_statement','job.spreadsheet_statement','job.crm_statement','job.document_statement','job.handoff_statement','hiring.change_event','hiring.measurement']),
2:('SaaS signatures and technographics',['technology.footprint','technology.provider_report','technology.script','technology.form_action','technology.network_request','technology.csp','technology.cookie','technology.header','technology.subdomain','dns.mx.provider','dns.cname.service','technology.account_identifier','technology.cooccurrence','technology.measurement']),
3:('Vertical SaaS',['technology.footprint','product.vertical','product.category','product.capability','portal.observed','integration.public_marker','integration.connection.verified']),
4:('Product-review pain priors',['review.record','review.statement','review.theme_classification','review.measurement','product.pain_prior']),
5:('Local review and operational pain reports',['review.record','review.owner_response','review.statement','review.theme_classification','review.theme_summary','review.measurement']),
6:('Forums and industry/vendor communities',['discussion.record','discussion.statement','discussion.theme_classification','product.pain_prior','industry.pain_prior','research.measurement']),
7:('Traffic and acquisition estimates',['traffic.measurement']),
8:('Commodity provider data',['search.result','business.profile_attribute','technology.provider_report','backlink.record','web.mention','web.mention_sentiment','app.listing','shopping.listing','advertisement.record','seo.measurement','app.measurement','shopping.measurement','ads.measurement','review.measurement']),
9:('Vertical public registries',['registry.registration','registry.license','registry.permit','registry.specialty','registry.filing','registry.affiliation','registry.measurement']),
10:('Phone and inbound economics',['technology.footprint','phone.cta','phone.routing_observed','phone.routing_verified','phone.recording_verified','phone.call_event','phone.measurement','phone.economics_hypothesis','review.statement']),
11:('Website / workflow extraction and inference',['company.self_claim','website.business_model_statement','website.customer_type_statement','website.lead_channel_statement','website.document_type_statement','website.handoff_statement','website.intent_statement','website.manual_process_statement','website.knowledge_source_statement','document.surface','form.surface','workflow.hypothesis','knowledge_complexity.hypothesis'])}

# Value-family schema examples are documented once; individual predicates retain strict specializations.
VALUE_CLASSES={
 'TechnologyValue':tech,'TechnologyReportValue':report,'AttributedStatementValue':STATEMENT,'JobPostingValue':job,'SalaryValue':salary,
 'ReviewRecordValue':review,'DiscussionRecordValue':post,'ThemeClassificationValue':classification,'HypothesisValue':HYPOTHESIS,
 'CallEventValue':call,'RegistryRecordValue':obj(regbase),'SurfaceObservationValue':obj({'surface_key':S,'observed_value':S}),
 'EconomicHypothesisValue':obj({'currency':CURRENCY,'estimated_amount_minor':INT,'assumptions':arr(S,1),'limitations':arr(S,1)})}
for key,shape in VALUE_CLASSES.items():
    if key not in SCHEMAS:add(key,shape)


def registries():
    # Explicit foreign-key metadata, not free-text dependency extraction.
    declared={
      'product_id':('SUBJECT',['SOFTWARE_PRODUCT']), 'product_ids':('SUBJECT',['SOFTWARE_PRODUCT']),
      'entity_id':('SUBJECT',['SOFTWARE_PRODUCT']), 'from_entity':('SUBJECT',['SOFTWARE_PRODUCT']),
      'to_entity':('SUBJECT',['SOFTWARE_PRODUCT']), 'from_product_id':('SUBJECT',['SOFTWARE_PRODUCT']),
      'to_product_id':('SUBJECT',['SOFTWARE_PRODUCT']), 'other_product_id':('SUBJECT',['SOFTWARE_PRODUCT']),
      'industry_id':('SUBJECT',['INDUSTRY']), 'organization_subject_id':('SUBJECT',['ORG']),
      'target_subject_id':('SUBJECT',SUBJECTS), 'peer_subject_id':('SUBJECT',['ORG','LOCATION']),
      'checked_location_ids':('SUBJECT',['LOCATION']), 'previous_fact_id':('FACT',[]), 'current_fact_id':('FACT',[]),
      'before_fact_id':('FACT',[]), 'after_fact_id':('FACT',[]), 'supporting_fact_ids':('FACT',[]),
      'contradicting_fact_ids':('FACT',[]), 'support_locator_ids':('LOCATOR',[]),
      'response_snapshot_id':('ARTIFACT',[]), 'current_snapshot_id':('ARTIFACT',[]), 'previous_snapshot_id':('ARTIFACT',[])}
    for p in P:
        for container,sh in [('target',p['target_schema']),('object',p['value_schema'])]:
            for key in sh.get('properties',{}):
                if key not in declared:continue
                if any(x['container']==container and x['path']=='/'+key for x in p['reference_rules']):continue
                typ,kinds=declared[key]
                p['reference_rules'].append({'container':container,'path':'/'+key,'subject_kinds':kinds,'target_type':typ})
    ids=[p['predicate_id'] for p in P]
    assert len(ids)==len(set(ids)), 'duplicate predicate'
    assert len([p for p in P if p['origin']!='V4_ADDED'])==87
    from .ledger_catalog import extend_ledger
    return extend_ledger({'predicates':P,'metrics':METRICS,'taxonomy':TAXONOMY,
            'coverage':[{'section':i,'title':v[0],'predicate_ids':v[1],'metric_ids':[m['metric_id'] for m in METRICS if i in m['section_ids']],
              'contract_status':'SCHEMA_DEFINED','live_adapter_status':'NOT_IMPLEMENTED'} for i,v in SECTIONS.items()]})
