"""Synthetic demonstrations, not source licenses, measurements, or prospect records."""
from copy import deepcopy
from pathlib import Path
from .catalog import registries
from .shapes import *
from .engine import canonical,digest

AT='2026-09-14T16:00:00Z';ASOF='2026-09-14T20:00:00Z';EXP='2026-09-28T16:00:00Z'
TENANT='tenant.demo'
POLICY='policy.fixture'

def supplemental(reg):
    ids=[p['predicate_id'] for p in reg['predicates']]
    policies=[{'policy_id':POLICY,'tenant_ids':[TENANT],'version':'1.0.0','review_status':'APPROVED','fixture_only':True,'approval_ref':'SYNTHETIC_TEST_ONLY',
      'terms_ref':'https://example.test/fixture-policy','reviewed_at':'2026-09-01T00:00:00Z','valid_until':'2027-01-01T00:00:00Z',
      'purposes':PURPOSES,'max_raw_retention_seconds':60*86400,'max_derived_retention_seconds':90*86400,'attribution_text':None,
      'allow_personal_data':False,'allow_sensitive_data':False,'deletion_cascades':True}]
    source_specs=[('web','Synthetic website','HTTP_CAPTURE',['DIRECT_OBSERVATION','FIRST_PARTY_STATEMENT']),
      ('review','Synthetic reviews','API',['THIRD_PARTY_REPORT','FIRST_PARTY_STATEMENT']),
      ('forum','Synthetic community','API',['THIRD_PARTY_REPORT']),('estimate','Synthetic estimates','API',['PROVIDER_ESTIMATE']),
      ('data','Synthetic commodity API','API',['THIRD_PARTY_REPORT','DIRECT_OBSERVATION']),
      ('registry','Synthetic registry','API',['REGISTRY_RECORD']),('private','Synthetic authorized export','AUTHORIZED_EXPORT',['DIRECT_OBSERVATION','FIRST_PARTY_STATEMENT']),
      ('derived','KeenSight reference','DERIVATION',['INFERENCE','DERIVED_MEASUREMENT']),('model','Synthetic model','API',['FIRST_PARTY_STATEMENT'])]
    sources=[{'source_id':'source.'+key,'version':'1.0.0','provider':provider,'acquisition_method':method,'authority':'ACTIVE','fixture_only':True,
      'policy_id':POLICY,'emits':[p['predicate_id'] for p in reg['predicates'] if set(nat)&set(p['allowed_natures'])],
      'allowed_natures':nat,'freshness_seconds':14*86400,'adapter_status':'FIXTURE_ONLY','upstream_namespace':'fixture.'+key} for key,provider,method,nat in source_specs]
    functions=[
      {'function_id':'extract.job_quote_v1','version':'1.0.0','processor':'LLM','authority':'ACTIVE','fixture_only':True,
       'input_predicates':[],'output_predicates':['job.workflow_statement'],'parameter_schema':obj({}),'cross_subject_rule':'SAME_SUBJECT','implementation_status':'DESIGN_ONLY','entrypoint':None},
      {'function_id':'fixture.theme_v1','version':'1.0.0','processor':'DERIVATION','authority':'ACTIVE','fixture_only':True,
       'input_predicates':['review.record','discussion.record'],'output_predicates':['review.theme_classification','discussion.theme_classification'],
       'parameter_schema':obj({'theme_id':ID}),'cross_subject_rule':'SAME_RESEARCH_TARGET','implementation_status':'DESIGN_ONLY','entrypoint':None},
      {'function_id':'sample.theme_summary_v1','version':'1.0.0','processor':'DERIVATION','authority':'ACTIVE','fixture_only':True,
       'input_predicates':['review.theme_classification','discussion.theme_classification'],'output_predicates':['product.pain_prior','industry.pain_prior','review.theme_summary'],
       'parameter_schema':obj({'sample_id':ID,'theme_id':ID}),'cross_subject_rule':'SAME_RESEARCH_TARGET','implementation_status':'REFERENCE_IMPLEMENTED','entrypoint':'keensight_contracts.engine:theme_summary'},
      {'function_id':'signal.required_facts_v1','version':'1.0.0','processor':'DETERMINISTIC','authority':'ACTIVE','fixture_only':True,
       'input_predicates':['technology.footprint','job.workflow_statement','form.surface'],'output_predicates':[],
       'parameter_schema':obj({}),'cross_subject_rule':'SAME_SUBJECT','implementation_status':'REFERENCE_IMPLEMENTED','entrypoint':'keensight_contracts.engine:evaluate_requirements'}]
    templates=[
      {'template_id':'template.observed_product','version':'1.0.0','authority':'ACTIVE','mode':'OBSERVATION_QUESTION','required_predicate':'technology.footprint',
       'allowed_natures':['DIRECT_OBSERVATION'],'renderer':'observed_product_v1','question':'How are booked appointments passed into your CRM today?',
       'maturity_required':False,'offered_rung':None,'review_ref':'fixture.review.product'},
      {'template_id':'template.job_question','version':'1.0.0','authority':'ACTIVE','mode':'OBSERVATION_QUESTION','required_predicate':'job.workflow_statement',
       'allowed_natures':['FIRST_PARTY_STATEMENT'],'renderer':'attributed_job_statement_v1','question':'How does your team handle that handoff today?',
       'maturity_required':False,'offered_rung':None,'review_ref':'fixture.review.job'},
      {'template_id':'template.scoped_absence','version':'1.0.0','authority':'ACTIVE','mode':'OBSERVATION_QUESTION','required_predicate':'form.surface',
       'allowed_natures':['DIRECT_OBSERVATION'],'renderer':'scoped_absence_v1','question':'How do new inquiries reach your team?',
       'maturity_required':False,'offered_rung':None,'review_ref':'fixture.review.absence'}]
    signals=[{'signal_type_id':sid,'version':'1.0.0','required_facts':[{'predicate_id':p,'allowed_natures':[nat],'state':state,'minimum':1}],
       'function_id':'signal.required_facts_v1','context_allowed':True,'description':desc,'status':'REFERENCE_IMPLEMENTED'}
      for sid,p,nat,state,desc in [('TECHNOLOGY_FOOTPRINT','technology.footprint','DIRECT_OBSERVATION','OBSERVED','Public product footprint only; not verified deployment.'),
                                 ('JOB_WORKFLOW_STATEMENT','job.workflow_statement','FIRST_PARTY_STATEMENT','OBSERVED','Attributed job language; not proven inefficiency.'),
                                 ('SCOPED_FORM_NONDETECTION','form.surface','DIRECT_OBSERVATION','NOT_FOUND','No configured form found in the completed page sample only.')]]
    rules=[{'join_rule_id':'join.product_footprint','version':'1.0.0','link_predicate':'technology.footprint','link_object_path':'/product_id',
       'context_predicate':'product.pain_prior','target_kinds':['SOFTWARE_PRODUCT'],'link_kind':'FOOTPRINT','purpose':'INTERNAL_RESEARCH','maximum_hops':1,'company_claim_allowed':False},
      {'join_rule_id':'join.industry_membership','version':'1.0.0','link_predicate':'account.industry_membership','link_object_path':'/industry_id',
       'context_predicate':'industry.pain_prior','target_kinds':['INDUSTRY'],'link_kind':'MEMBERSHIP','purpose':'INTERNAL_RESEARCH','maximum_hops':1,'company_claim_allowed':False}]
    profile={'profile_id':'profile.broad_research','version':'4.0.0','production_enabled':False,'capture_source_ids':[],
       'fact_predicate_ids':ids,'execute_function_ids':['sample.theme_summary_v1','signal.required_facts_v1'],'signal_ids':[s['signal_type_id'] for s in signals],
       'template_ids':[t['template_id'] for t in templates],'research_context_enabled':True,'delivery_enabled':False}
    fingerprints=[{'fingerprint_id':'fp.calendly.script','version':'1.0.0','authority':'CANDIDATE','fixture_only':True,'product_subject_id':'product.calendly','emits':'technology.footprint',
       'capture_mode':'RAW_HTML','operator':'SCRIPT_HOST','match_value':'calendly.com',
       'positive_fixtures':['fixtures/fingerprint-positive.html','fixtures/fingerprint-protocol-relative.html'],
       'negative_fixtures':['fixtures/fingerprint-lookalike.html','fixtures/fingerprint-comment.html','fixtures/fingerprint-blog.html','fixtures/fingerprint-footer.html'],
       'calibration_ref':None,'implementation_status':'REFERENCE_IMPLEMENTED'}]
    # Fixture matcher is candidate: demonstration facts are accepted for internal
    # storage. Approval checks also need a deliberate design-only promotion override.
    fingerprints[0]['authority']='ACTIVE' # All production remains disabled; no calibration claim.
    providers=[]
    provider_specs=[('website','Website and ATS',[1,2,3,10,11],['hiring','technology','website_analysis'],['HTTP_CAPTURE'],'https://example.test/terms','Per-site capture policy; deterministic capture plus optional bounded extraction.'),
      ('g2','G2',[4],['reviews','research'],['API'],'https://www.g2.com/static/terms','No authorization asserted. Product-level context only.'),
      ('capterra','Capterra',[4],['reviews','research'],['API'],'https://www.capterra.com/legal/terms-of-use','No authorization asserted. Product-level context only.'),
      ('google','Google Places',[5,8],['reviews','commodity_data'],['API'],'https://developers.google.com/maps/documentation/places/web-service/policies','Retention and attribution restrictions must be reviewed for the specific endpoint/use.'),
      ('reddit','Reddit and approved communities',[6],['community','research'],['API'],'https://redditinc.com/policies/data-api-terms','Commercial agreement and approved purpose required; no user reidentification or sensitive inference.'),
      ('similarweb','Similarweb',[7],['measurement'],['API'],'https://developers.similarweb.com/reference/visits','Provider estimates, dimensions, period and method retained.'),
      ('dataforseo','DataForSEO',[2,5,7,8],['commodity_data','measurement','technology'],['API'],'https://docs.dataforseo.com/v3/business_data-overview/','Each endpoint mapped separately; provider access does not erase origin/rights restrictions.'),
      ('nppes','CMS / NPPES',[9],['public_registry'],['API'],'https://npiregistry.cms.hhs.gov/','NPI enumeration is not licensure or credentialing.'),
      ('iapd','SEC / IAPD',[9],['public_registry'],['API'],'https://www.investor.gov/introduction-investing/investing-basics/glossary/investment-adviser-public-disclosure-iapd','Firm and representative identities separated; preserve filing and effective dates.'),
      ('local_registry','Licensing and permits',[9],['public_registry'],['API','HTTP_CAPTURE'],'https://example.test/authority-terms','Authority/jurisdiction-specific mappings required.'),
      ('call_system','Authorized call systems',[10],['phone'],['AUTHORIZED_EXPORT'],'https://example.test/call-data-agreement','No raw recording or personal call content without appropriate authority; aggregate operations preferred.'),
      ('llm','Approved model processor',[11],['website_analysis'],['API'],'https://example.test/processor-agreement','Raw model I/O, task/prompt version, processing rights and bounded repair required.')]
    for pid,provider,sec,fams,methods,url,notes in provider_specs:
        providers.append({'blueprint_id':'provider.'+pid,'provider':provider,'section_ids':sec,'families':fams,'methods':methods,'terms_url':url,'approval_required':True,'adapter_implemented':False,'notes':notes})
    reg.update(sources=sources,policies=policies,functions=functions,profiles=[profile],templates=templates,signals=signals,
       fingerprints=fingerprints,providers=providers,**{'context-rules':rules})
    return reg


def example_bundle(reg):
    from .validation import ROW_TYPES
    rows={k:[] for k in ROW_TYPES};blobs={};pmap={p['predicate_id']:p for p in reg['predicates']}
    def subject(i,kind,label):rows['subjects'].append({'subject_id':i,'tenant_id':TENANT,'kind':kind,'display_name':label,'external_ids':[]})
    for i,k,l in [('org.acme','ORG','Acme Test Practice'),('org.other','ORG','Other Test Company'),('location.acme','LOCATION','Acme Test Location'),
      ('product.calendly','SOFTWARE_PRODUCT','Calendly'),('product.crm','SOFTWARE_PRODUCT','ExampleCRM'),('industry.medical','INDUSTRY','Medical practices'),
      ('person.provider','PERSON','Synthetic Business Professional'),('app.acme','APPLICATION','Test App'),('listing.acme','LISTING','Test Listing')]:subject(i,k,l)
    def scope(i,sub,resources,mode='API_BODY',kind='PROVIDER_QUERY',desc='bounded synthetic test sample'):
        rows['scopes'].append({'scope_id':i,'tenant_id':TENANT,'subject_id':sub,'kind':kind,'resources':resources,'capture_mode':mode,'population_description':desc,'stable_scope_key':i})
    home='https://acme.example.test/';jobs='https://acme.example.test/careers/operations';product_urls=[f'https://reviews.example.test/product/{i}' for i in range(1,4)]
    local_urls=[f'https://reviews.example.test/local/{i}' for i in range(1,3)];forum_urls=[f'https://forum.example.test/posts/{i}' for i in range(1,3)]
    scope('scope.home','org.acme',[home],'RAW_HTML','PAGE','homepage raw HTML captured on September 14, 2026')
    scope('scope.job','org.acme',[jobs])
    scope('scope.product','product.calendly',product_urls,kind='RESEARCH_SAMPLE')
    scope('scope.local','location.acme',local_urls,kind='RESEARCH_SAMPLE')
    scope('scope.industry','industry.medical',forum_urls,kind='RESEARCH_SAMPLE')
    for key,sub in [('traffic','org.acme'),('data','org.acme'),('registry','person.provider'),('private','org.acme'),('model','org.acme'),('product_docs','product.calendly')]:
        resources=[f'https://fixture.example.test/{key}'] if key!='model' else ['https://fixture.example.test/model/request','https://fixture.example.test/model/response']
        scope('scope.'+key,sub,resources,kind='AUTHORIZED_SYSTEM' if key=='private' else 'PROVIDER_QUERY')
    smap={s['scope_id']:s for s in rows['scopes']}
    def artifact(i,sc,source,body,url=None,pub=None):
        scope_=smap[sc];url=url or scope_['resources'][0];raw=body.encode() if isinstance(body,str) else canonical(body)
        ext='html' if isinstance(body,str) and body.startswith('<') else 'json';path='fixtures/'+i+'.'+ext;blobs[path]=raw
        a={'artifact_id':i,'tenant_id':TENANT,'source_id':'source.'+source,'scope_id':sc,'resource_uri':url,'media_type':'text/html' if ext=='html' else 'application/json',
           'content_ref':path,'content_hash':digest(raw),'byte_count':len(raw),'captured_at':AT,'published_at':pub,'status':'OK','truncated':False,
           'retained_until':'2026-10-01T00:00:00Z','retention_state':'RETAINED','classification':'PUBLIC_BUSINESS',
           'origin_namespace':'fixture.'+source,'origin_record_id':i,'origin_revision':'1','independence_group':i,'parent_artifact_id':None}
        rows['artifacts'].append(a)
        l={'locator_id':'loc.'+i,'artifact_id':i,'kind':'WHOLE_ARTIFACT','start':None,'end':None,'pointer':None,'quote':None};rows['locators'].append(l)
        sub=scope_['subject_id'];kind=next(s['kind'] for s in rows['subjects'] if s['subject_id']==sub)
        role='RESEARCH_TARGET' if kind in ['SOFTWARE_PRODUCT','INDUSTRY'] else ('REGISTRY_SUBJECT' if source=='registry' else ('REVIEW_TARGET' if source=='review' else 'FIRST_PARTY'))
        rows['bindings'].append({'binding_id':'bind.'+i,'tenant_id':TENANT,'subject_id':sub,'scope_id':sc,'artifact_ids':[i],'role':role,'status':'ACCEPTED','method':'synthetic_fixture_binding',
          'decided_at':AT,'evidence_locator_ids':[l['locator_id']]})
        return i
    html='<html><head><script src="https://assets.calendly.com/assets/external/widget.js"></script></head><body><h1>Acme medical practice</h1><a href="tel:+15550102030">Call us</a></body></html>'
    artifact('art.home','scope.home','web',html)
    quote='Maintain the Excel reconciliation workbook and update CRM records.'
    job_value={'posting_id':'job-1','namespace':'ats.fixture','url':jobs,'title':'Operations Coordinator','department':'Operations','published_at':'2026-09-01T00:00:00Z','employment_type':'FULL_TIME'}
    artifact('art.job','scope.job','web',{'posting':job_value,'workflow':quote,'salary':{'minimum_minor':6500000,'maximum_minor':8500000,'currency':'USD','minor_unit_exponent':2,'period':'YEAR','basis':'BASE'}},pub='2026-09-01T00:00:00Z')
    for idx,url in enumerate(product_urls,1):artifact(f'art.product{idx}','scope.product','review',{'review_key':f'r{idx}','text':'Reporting requires spreadsheet exports.' if idx<3 else 'Booking works well.'},url,pub=f'2026-09-0{idx}T00:00:00Z')
    for idx,url in enumerate(local_urls,1):artifact(f'art.local{idx}','scope.local','review',{'review_key':f'l{idx}','text':'I could not get a callback.' if idx==1 else 'The team called me back.'},url,pub=f'2026-09-0{idx}T00:00:00Z')
    for idx,url in enumerate(forum_urls,1):artifact(f'art.forum{idx}','scope.industry','forum',{'post_key':f'p{idx}','text':'Our practice uses spreadsheets to coordinate referrals.' if idx==1 else 'We use a shared inbox.'},url,pub=f'2026-09-0{idx}T00:00:00Z')
    artifact('art.traffic','scope.traffic','estimate',{'visits':12000,'country':'US','device':'ALL','period':'2026-08','estimated':True})
    artifact('art.data','scope.data','data',{'rank':3,'query':'test clinic','country':'US','engine':'fixture-search','url':home})
    artifact('art.registry','scope.registry','registry',{'identifier':'SYNTHETIC-NPI-RECORD','status':'ACTIVE_RECORD','specialty':'example specialty','not_licensure':True})
    artifact('art.private','scope.private','private',{'call_key':'call-1','direction':'INBOUND','status':'MISSED','duration_seconds':0})
    artifact('art.product_docs','scope.product_docs','web',{'capability':'Appointment scheduling','portal':'Booking','vertical':'medical practices'})
    artifact('art.request','scope.model','model',{'task':'Extract only a quote about workflow','source_artifact':'art.job'},'https://fixture.example.test/model/request')
    artifact('art.response','scope.model','model',{'text':quote},'https://fixture.example.test/model/response')
    def fact(fid,pid,aid,value,target=None,nature=None,state='OBSERVED',window=None,exid=None,parents=None,scope_id=None):
        p=pmap[pid];a=next((a for a in rows['artifacts'] if a['artifact_id']==aid),None);sc=smap[scope_id or a['scope_id']]
        eid='ev.'+fid
        rows['evidence'].append({'evidence_id':eid,'tenant_id':TENANT,'locator_ids':[] if parents else ['loc.'+aid],
             'input_fact_ids':parents or [],'execution_id':exid,'coverage_id':None,'directness':'DERIVED' if parents else 'RAW'})
        f={'schema_version':'4.0.0','fact_id':fid,'tenant_id':TENANT,'subject_id':sc['subject_id'],'predicate_id':pid,'target':deepcopy(target if target is not None else p['example_target']),
           'scope_id':sc['scope_id'],'state':state,'object':deepcopy(value),'nature':nature or p['allowed_natures'][0],
           'source_id':'source.derived' if parents else a['source_id'],'binding_id':None if parents else 'bind.'+aid,'evidence_id':eid,'execution_id':exid,'run_id':'run.demo',
           'observed_at':AT,'recorded_at':'2026-09-14T18:00:00Z','effective_at':None,'window':window,
           'reason':None if state=='OBSERVED' else ('NOT_DETECTED_IN_SCOPE' if state=='NOT_FOUND' else 'INSUFFICIENT_EVIDENCE'),
           'expires_at':EXP,'confidence':None,'supersedes_fact_id':None}
        rows['facts'].append(f);return f
    fact('f.tech','technology.footprint','art.home',{'product_id':'product.calendly','version':None,'surface':'SCRIPT','matched_value':'assets.calendly.com','fingerprint_id':'fp.calendly.script','deployment_claim':'PUBLIC_FOOTPRINT_ONLY'},{'product_id':'product.calendly'})
    fact('f.vendor1','vendor.present','art.home',{'class_id':'booking','entity_id':'product.calendly'},{'entity_id':'product.calendly'})
    fact('f.vendor2','vendor.present','art.home',{'class_id':'crm','entity_id':'product.crm'},{'entity_id':'product.crm'})
    # Both vendor observations are illustrative; the raw fixture explicitly includes the second marker.
    blobs['fixtures/art.home.html']=blobs['fixtures/art.home.html'].replace(b'</head>',b'<script src="https://crm.example.test/widget.js"></script></head>')
    a=next(a for a in rows['artifacts'] if a['artifact_id']=='art.home');a.update(content_hash=digest(blobs['fixtures/art.home.html']),byte_count=len(blobs['fixtures/art.home.html']))
    fact('f.job','job.posting','art.job',job_value,{'namespace':'ats.fixture','posting_id':'job-1'})
    fact('f.salary','job.salary','art.job',{'minimum_minor':6500000,'maximum_minor':8500000,'currency':'USD','minor_unit_exponent':2,'period':'YEAR','basis':'BASE'},
         {'namespace':'ats.fixture','posting_id':'job-1','component':'base'})
    fact('f.job_statement','job.workflow_statement','art.job',{'statement_id':'st.job1','text':quote,'topic_id':'theme.spreadsheets','modality':'REQUIREMENT'},
         {'statement_id':'st.job1'},exid='ex.job_llm')
    fact('f.capability','product.capability','art.product_docs',{'capability_id':'scheduling','text':'Appointment scheduling','modality':'DOCUMENTED_FEATURE'},{'item_id':'scheduling'})
    for prefix,count,sc in [('product',3,'scope.product'),('local',2,'scope.local')]:
        for i in range(1,count+1):
            text=('Reporting requires spreadsheet exports.' if i<3 else 'Booking works well.') if prefix=='product' else ('I could not get a callback.' if i==1 else 'The team called me back.')
            fact(f'f.{prefix}{i}','review.record',f'art.{prefix}{i}',{'review_key':prefix+str(i),'platform':'fixture_reviews','published_at':f'2026-09-0{i}T00:00:00Z','rating':2 if i<3 else 5,'rating_scale_max':5,'text':text,'language':'en','edited':False},
                 {'platform':'fixture_reviews','review_key':prefix+str(i)})
    for i in range(1,3):
        fact(f'f.forum{i}','discussion.record',f'art.forum{i}',{'post_key':'p'+str(i),'community':'fixture_medical','thread_key':'thread'+str(i),'published_at':f'2026-09-0{i}T00:00:00Z',
          'text':'Our practice uses spreadsheets to coordinate referrals.' if i==1 else 'We use a shared inbox.','language':'en','role':'POST'}, {'community':'fixture_medical','post_key':'p'+str(i)})
    def execute(exid,fn,sub,ins,outs,params,arts=None,model=None,started='2026-09-14T17:00:00Z',finished='2026-09-14T17:01:00Z'):
        rows['executions'].append({'execution_id':exid,'tenant_id':TENANT,'run_id':'run.demo','function_id':fn,'function_version':'1.0.0','subject_id':sub,
          'input_fact_ids':ins,'input_artifact_ids':arts or [],'output_fact_ids':outs,'input_set_hash':digest({'facts':sorted(ins),'artifacts':sorted(arts or [])}),
          'parameters':params,'started_at':started,'finished_at':finished,'status':'COMPLETE','model_call_id':model})
    execute('ex.job_llm','extract.job_quote_v1','org.acme',[],['f.job_statement'],{},['art.job'],model='call.fixture')
    for key,parent,theme,scopeid in [('product1','f.product1','reporting','scope.product'),('product2','f.product2','reporting','scope.product'),('local1','f.local1','follow_up','scope.local'),('forum1','f.forum1','spreadsheets','scope.industry')]:
        exid='ex.classify.'+key;pid='discussion.theme_classification' if key.startswith('forum') else 'review.theme_classification';fid='f.classify.'+key
        fact(fid,pid,None,{'theme_id':'theme.'+theme,'record_key':key,'sentiment':'NEGATIVE','stance':'EXPERIENCED','support_locator_ids':['loc.art.'+key]},
             {'record_key':key,'theme_id':'theme.'+theme},parents=[parent],exid=exid,scope_id=scopeid)
        execute(exid,'fixture.theme_v1',smap[scopeid]['subject_id'],[parent],[fid],{'theme_id':'theme.'+theme})
    window={'start':'2026-09-01T00:00:00Z','end':'2026-09-14T00:00:00Z'}
    for key,scopeid,artids,parents,theme,pid in [('product','scope.product',['art.product1','art.product2','art.product3'],['f.classify.product1','f.classify.product2'],'reporting','product.pain_prior'),
      ('local','scope.local',['art.local1','art.local2'],['f.classify.local1'],'follow_up','review.theme_summary'),
      ('industry','scope.industry',['art.forum1','art.forum2'],['f.classify.forum1'],'spreadsheets','industry.pain_prior')]:
        sample='sample.'+key;fid='f.prior.'+key;exid='ex.summary.'+key;sub=smap[scopeid]['subject_id']
        rows['samples'].append({'sample_id':sample,'tenant_id':TENANT,'subject_id':sub,'scope_id':scopeid,'window':window,'sampling_frame':'Synthetic bounded sample; not representative of all users.',
          'selection_method':'CURATED_SAMPLE','retrieved_artifact_ids':artids,'eligible_artifact_ids':artids,'excluded_artifact_ids':[],
          'dedupe_policy_version':'1.0.0','population_size':None,'complete_population':False,'limitations':['Synthetic only; small selected sample, no population inference.'],'policy_ids':[POLICY]})
        value={'sample_id':sample,'theme_id':'theme.'+theme,'supporting_fact_ids':parents,'contradicting_fact_ids':[],
          'support_count':len(parents),'eligible_count':len(artids),'sample_share':len(parents)/len(artids),'population_claim':False}
        fact(fid,pid,None,value,{'sample_id':sample,'theme_id':'theme.'+theme},parents=parents,exid=exid,scope_id=scopeid,window=window)
        execute(exid,'sample.theme_summary_v1',sub,parents,[fid],{'sample_id':sample,'theme_id':'theme.'+theme},started='2026-09-14T17:02:00Z',finished='2026-09-14T17:03:00Z')
    fact('f.industry','account.industry_membership','art.home',{'industry_id':'industry.medical','basis':'EXPLICIT_SELF_DESCRIPTION'},{'industry_id':'industry.medical'})
    dims={'country':'US','device':'ALL','granularity':'MONTHLY'}
    fact('f.traffic','traffic.measurement','art.traffic',{'metric_id':'traffic.visits','value':12000,'unit':'count','dimensions':dims,'method_version':'fixture-estimator-v1','reporting_timezone':'UTC',
          'numerator':None,'denominator':None,'sample_size':None,'uncertainty':None},
          {'metric_id':'traffic.visits','dimensions':dims,'provider':'Synthetic estimates','method_version':'fixture-estimator-v1','reporting_timezone':'UTC'},nature='PROVIDER_ESTIMATE',window={'start':'2026-08-01T00:00:00Z','end':'2026-09-01T00:00:00Z'})
    fact('f.serp','search.result','art.data',{'query':'test clinic','engine':'fixture-search','rank':3,'url':home,'title':'Acme Test Practice','result_type':'ORGANIC'},
         {'query':'test clinic','engine':'fixture-search','rank':3,'country':'US','device':'DESKTOP'})
    fact('f.registry','registry.registration','art.registry',{'namespace':'fixture.npi','record_id':'SYNTHETIC-NPI-RECORD','issuer':'Synthetic Registry','jurisdiction':'US','effective_at':None,'filed_at':None,
          'record_status':'ACTIVE_RECORD','registration_kind':'NPI','identifier':'SYNTHETIC-NPI-RECORD'}, {'namespace':'fixture.npi','record_id':'SYNTHETIC-NPI-RECORD'})
    fact('f.call','phone.call_event','art.private',{'call_key':'call-1','started_at':'2026-09-14T15:00:00Z','direction':'INBOUND','status':'MISSED','duration_seconds':0,'callback_of':None},
        {'system_id':'fixture.pbx','call_key':'call-1'})
    absent=fact('f.no_form','form.surface','art.home',None,{'form_key':'primary_contact'},state='NOT_FOUND')
    rows['coverage'].append({'coverage_id':'coverage.form','tenant_id':TENANT,'scope_id':'scope.home','source_id':'source.web','predicate_ids':['form.surface'],
       'target':absent['target'],'planned_resources':[home],'checked':[{'resource':home,'artifact_id':'art.home','result':'OK'}],
       'status':'COMPLETE','checked_at':AT,'detector_release':digest('fixture-detector'.encode()),'scope_limitations':'Raw homepage only; not rendered content or private intake systems.'})
    next(e for e in rows['evidence'] if e['evidence_id']==absent['evidence_id'])['coverage_id']='coverage.form'
    for key,sub,rule,link,prior,strength in [('product','product.calendly','join.product_footprint','f.tech','f.prior.product','FOOTPRINT'),
       ('industry','industry.medical','join.industry_membership','f.industry','f.prior.industry','MEMBERSHIP')]:
        rows['contexts'].append({'context_id':'context.'+key,'tenant_id':TENANT,'run_id':'run.demo','account_subject_id':'org.acme','context_subject_id':sub,
            'join_rule_id':rule,'link_fact_id':link,'context_fact_ids':[prior],'relationship_strength':strength,'purpose':'INTERNAL_RESEARCH','company_claim_allowed':False,'status':'ELIGIBLE'})
    for sid,pid,fid in [('signal.tech','TECHNOLOGY_FOOTPRINT','f.tech'),('signal.job','JOB_WORKFLOW_STATEMENT','f.job_statement'),('signal.form','SCOPED_FORM_NONDETECTION','f.no_form')]:
        rows['signals'].append({'signal_id':sid,'run_id':'run.demo','tenant_id':TENANT,'subject_id':'org.acme','signal_type_id':pid,'input_fact_ids':[fid],
          'context_ids':['context.product'] if sid=='signal.tech' else [],'status':'RESOLVED','reason':None})
    clauses=[('product','f.tech','I noticed a Calendly embed on your site.','DIRECT','signal.tech'),
      ('job','f.job_statement',f'Your job posting states: “{quote}”','ATTRIBUTED','signal.job'),
      ('absence','f.no_form','In the captured page sample (homepage raw HTML captured on September 14, 2026), the configured detector did not find the specified form surface.','SCOPED_ABSENCE','signal.form')]
    tm={'product':'template.observed_product','job':'template.job_question','absence':'template.scoped_absence'}
    for key,fid,text,role,sid in clauses:
        tid=tm[key];q=next(t['question'] for t in reg['templates'] if t['template_id']==tid)
        rows['packages'].append({'package_id':'package.'+key,'revision':1,'run_id':'run.demo','tenant_id':TENANT,'subject_id':'org.acme','template_id':tid,
           'clauses':[{'clause_id':'clause.'+key,'fact_ids':[fid],'template_id':tid,'text':text,'evidence_roles':[role]}],'signal_ids':[sid],
           'context_ids':['context.product'] if key=='product' else [],'maturity_fact_id':None,'status':'DESIGN_TEST_APPROVED','rendered_text':text+' '+q,'approved_at':ASOF,'send_allowed':False})
    rows['model-calls'].append({'call_id':'call.fixture','tenant_id':TENANT,'task_version':'1.0.0','provider':'Synthetic model','model':'not-a-live-model',
       'prompt_hash':digest(blobs['fixtures/art.request.json']),'output_schema_id':'QuotedTextResult','input_artifact_ids':['art.job'],'request_artifact_id':'art.request','response_artifact_id':'art.response',
       'policy_ids':[POLICY],'max_repair_attempts':2,'status':'PARSED','terminal_reason':None})
    reg_hash=digest(reg)
    rows['runs'].append({'run_id':'run.demo','tenant_id':TENANT,'mode':'DESIGN_TEST','as_of':ASOF,'created_at':'2026-09-14T15:00:00Z',
      'code_release':digest(b'contract-reference-4.0.0'),'registry_release':reg_hash,'profile_id':'profile.broad_research',
      'input_artifact_ids':[a['artifact_id'] for a in rows['artifacts']],
      'input_fact_ids':[f['fact_id'] for f in rows['facts'] if not next(e for e in rows['evidence'] if e['evidence_id']==f['evidence_id'])['input_fact_ids']],
      'binding_ids':[b['binding_id'] for b in rows['bindings']],'status':'COMPLETE','approval_policy_version':'4.0.0'})
    blobs.update({
      'fixtures/fingerprint-positive.html':b'<script src="https://assets.calendly.com/widget.js"></script>',
      'fixtures/fingerprint-protocol-relative.html':b'<script src="//assets.calendly.com/widget.js"></script>',
      'fixtures/fingerprint-lookalike.html':b'<script src="https://calendly.com.evil.test/widget.js"></script>',
      'fixtures/fingerprint-comment.html':b'<!-- <script src="https://assets.calendly.com/widget.js"></script> -->',
      'fixtures/fingerprint-blog.html':b'<a href="https://calendly.com">A blog about Calendly</a>',
      'fixtures/fingerprint-footer.html':b'<footer><script src="https://assets.calendly.com/widget.js"></script>Agency</footer>'})
    execs={e['execution_id']:e for e in rows['executions']}
    for f in rows['facts']:
        f['recorded_at']=execs[f['execution_id']]['finished_at'] if f['execution_id'] else '2026-09-14T16:00:30Z'
        if isinstance(f['object'],dict):f['effective_at']=f['object'].get('published_at') or f['object'].get('started_at') or f['object'].get('effective_at')
    return rows,blobs
