"""Deterministic design-test examples for the v4.1 completion contracts."""
from copy import deepcopy
from .engine import digest, canonical, claim_key, resolve_claim, code_digest
from .completion import package_hash, export_payload
from .shapes import obj,ID


def add_registry(reg):
    for fn in reg['functions']:fn['detector_contract']=None
    fn=next(f for f in reg['functions'] if f['function_id']=='extract.job_quote_v1')
    fn.update(implementation_status='REFERENCE_IMPLEMENTED',entrypoint='keensight_contracts.completion:extract_job_quote')
    fn=next(f for f in reg['functions'] if f['function_id']=='fixture.theme_v1')
    fn.update(implementation_status='REFERENCE_IMPLEMENTED',entrypoint='keensight_contracts.completion:classify_theme')
    reg['functions'].append({'function_id':'detect.raw_form_v1','version':'1.0.0','processor':'DETERMINISTIC','authority':'ACTIVE','fixture_only':True,
        'input_predicates':[],'output_predicates':['form.surface'],'parameter_schema':obj({'scope_id':ID,'target':obj({'form_key':ID})}),'cross_subject_rule':'SAME_SUBJECT',
        'implementation_status':'REFERENCE_IMPLEMENTED','entrypoint':'keensight_contracts.completion:form_detector',
        'detector_contract':{'capture_modes':['RAW_HTML'],'predicate_ids':['form.surface'],'operator':'HTML_FORM_ELEMENT'}})
    for profile in reg['profiles']:
        profile.update(product_boundary='REVIEWED_HANDOFF',export_enabled=True,version='4.2.0')
        profile['execute_function_ids']=[f['function_id'] for f in reg['functions'] if f['implementation_status']=='REFERENCE_IMPLEMENTED']
    for signal in reg['signals']:
        for req in signal['required_facts']:req['counting_unit']='DISTINCT_ORIGIN'
    reg['actors']=[{'actor_id':'actor.fixture','tenant_id':'tenant.demo','permissions':['INTAKE','REVIEW_PACKAGE','USE_GATE','EXPORT','RESTRICT','CHANGE_FACT','CHANGE_BINDING','CHANGE_ARTIFACT','CHANGE_REGISTRY'],'fixture_only':True,'active':True}]
    reg['destinations']=[{'destination_id':'destination.fixture','tenant_id':'tenant.demo','mapping_version':'1.0.0','kind':'LOCAL_PREVIEW','fixture_only':True,'enabled':True,'automatic_sending':False}]
    reg['support-policies']=[{'support_policy_id':'support.negative_experience','version':'1.0.0','meaning':'REPORTED_NEGATIVE_EXPERIENCE',
        'allowed_stances':['EXPERIENCED'],'allowed_sentiments':['NEGATIVE','MIXED'],'counting_unit':'DISTINCT_ORIGIN',
        'denominator_rule':'ELIGIBLE_RETRIEVED_RECORDS','unclassified_policy':'RETAIN_AS_UNMEASURED_NOT_NEGATIVE'},
        {'support_policy_id':'support.workflow_mention','version':'1.0.0','meaning':'WORKFLOW_MENTION',
        'allowed_stances':['EXPERIENCED'],'allowed_sentiments':['NEGATIVE','MIXED','NEUTRAL','POSITIVE'],'counting_unit':'DISTINCT_ORIGIN',
        'denominator_rule':'ELIGIBLE_RETRIEVED_RECORDS','unclassified_policy':'RETAIN_AS_UNMEASURED_NOT_NEGATIVE'}]
    policy=deepcopy(reg['policies'][0]);policy.update(policy_id='policy.blocked',purposes=['DERIVE','RETAIN','INTERNAL_RESEARCH'])
    reg['policies'].append(policy)
    source=deepcopy(reg['sources'][0]);source.update(source_id='source.blocked',policy_id='policy.blocked')
    reg['sources'].append(source)
    return reg


def add_examples(reg,rows,blobs,root):
    for name in ['intakes','attempts','reviews','gates','exports','restrictions']:rows[name]=[]
    for e in rows['evidence']:e.update(attempt_id=None,sample_ids=[])
    for c in rows['candidates']:c['attempt_id']=None
    fs={f['fact_id']:f for f in rows['facts']};evs={e['evidence_id']:e for e in rows['evidence']}
    for f in rows['facts']:f['schema_version']='4.2.0'
    tenant='tenant.demo';intake_id='intake.fixture';profile=reg['profiles'][0]
    scope_by={s['scope_id']:s for s in rows['scopes']}
    targets=[{'resource_uri':a['resource_uri'],'subject_id':scope_by[a['scope_id']]['subject_id']} for a in rows['artifacts']]
    denied_target={'resource_uri':'https://fixture.example.test/blocked-careers','subject_id':'org.other'}
    targets.append(denied_target)
    intake={'intake_id':intake_id,'tenant_id':tenant,'requester_id':'actor.fixture','profile_id':profile['profile_id'],'purpose':'REVIEWED_HANDOFF',
        'targets':targets,'received_at':'2026-09-14T14:59:00Z','request_hash':digest({'profile_id':profile['profile_id'],'purpose':'REVIEWED_HANDOFF','targets':targets}),'idempotency_key':'intake-fixture-v41'}
    rows['intakes'].append(intake)
    for a in rows['artifacts']:
        target={'resource_uri':a['resource_uri'],'subject_id':scope_by[a['scope_id']]['subject_id']};operation='capture.'+a['artifact_id']
        rows['attempts'].append({'attempt_id':'attempt.'+a['artifact_id'],'tenant_id':tenant,'intake_id':intake_id,'source_id':a['source_id'],
            'source_version':'1.0.0','adapter_version':'1.0.0','target':target,'scope_id':a['scope_id'],
            'operation_key':operation,'request_hash':digest({'target':target,'source_id':a['source_id'],'operation_key':operation}),
            'started_at':'2026-09-14T15:59:00Z','finished_at':'2026-09-14T16:00:05Z','status':'SUCCEEDED','artifact_ids':[a['artifact_id']],
            'execution_mode':'REPLAY_IMPORT','terminal_reason':None,'pagination':'NOT_APPLICABLE','truncated':False,'max_requests':1,'requests_made':1,'timeout_seconds':90,
            'body_limit_bytes':100000,'cost_status':'NOT_CHARGED','cost_minor':0,'currency':None})
    rows['scopes'].append({'scope_id':'scope.denied','tenant_id':tenant,'subject_id':'org.other','kind':'PAGE','resources':[denied_target['resource_uri']],
        'capture_mode':'RAW_HTML','population_description':'A policy-blocked request; not checked.','stable_scope_key':'blocked-page'})
    denied=deepcopy(rows['attempts'][0]);denied.update(attempt_id='attempt.denied',target=denied_target,scope_id='scope.denied',source_id='source.blocked',
        operation_key='capture.denied',execution_mode='LIVE_CAPTURE',status='POLICY_DENIED',artifact_ids=[],terminal_reason='POLICY_DENIED',requests_made=0)
    denied['request_hash']=digest({'target':denied_target,'source_id':denied['source_id'],'operation_key':denied['operation_key']});rows['attempts'].append(denied)
    unknown=deepcopy(fs['f.tech']);unknown.update(fact_id='f.unknown',subject_id='org.other',scope_id='scope.denied',source_id='source.blocked',
        state='UNKNOWN',object=None,reason='POLICY_BLOCKED',binding_id=None,evidence_id='ev.unknown',execution_id=None,
        observed_at=denied['finished_at'],recorded_at='2026-09-14T16:00:30Z')
    rows['facts'].append(unknown);fs['f.unknown']=unknown
    rows['evidence'].append({'evidence_id':'ev.unknown','tenant_id':tenant,'locator_ids':[],'input_fact_ids':[],'execution_id':None,'coverage_id':None,
        'directness':'DIAGNOSTIC','attempt_id':'attempt.denied','sample_ids':[]})
    # A real reference detector execution backs the absence fixture.
    rows['executions'].append({'execution_id':'ex.detect.form','tenant_id':tenant,'run_id':'run.ingest','function_id':'detect.raw_form_v1','function_version':'1.0.0',
        'subject_id':'org.acme','input_fact_ids':[],'input_artifact_ids':['art.home'],'output_fact_ids':['f.no_form'],
        'input_set_hash':digest({'facts':[],'artifacts':['art.home']}),'parameters':{'scope_id':'scope.home','target':{'form_key':'primary_contact'}},'started_at':'2026-09-14T16:35:00Z','finished_at':'2026-09-14T16:36:00Z',
        'status':'COMPLETE','model_call_id':None})
    fs['f.no_form'].update(execution_id='ex.detect.form',recorded_at='2026-09-14T16:36:00Z')
    evs['ev.f.no_form']['execution_id']='ex.detect.form'
    fn=next(f for f in reg['functions'] if f['function_id']=='detect.raw_form_v1')
    rows['coverage'][0].update(checked_at='2026-09-14T16:36:00Z',detector_release=digest(fn),attempt_ids=['attempt.art.home'],detector_execution_id='ex.detect.form')
    # The denominator retains unclassified reviews explicitly. Not a negative label.
    for sample in rows['samples']:
        key=sample['sample_id'].split('.')[-1]
        sample.update(support_policy_id='support.workflow_mention' if key=='industry' else 'support.negative_experience',
            theme_id={'product':'theme.reporting','local':'theme.follow_up','industry':'theme.spreadsheets'}[key],
            created_at='2026-09-14T17:01:30Z',record_decisions=[])
        prior=fs['f.prior.'+key]
        classifications=prior['object']['supporting_fact_ids']
        for aid in sample['retrieved_artifact_ids']:
            matching=[fid for fid in classifications if fid.endswith(aid.replace('art.',''))]
            sample['record_decisions'].append({'artifact_id':aid,'status':'SUPPORT' if matching else 'UNCLASSIFIED',
                'classification_fact_ids':matching,'reason':None if matching else 'Not theme-classified; retained in the retrieved-record denominator.'})
        evs[prior['evidence_id']]['sample_ids']=[sample['sample_id']]
        prior['object'].update(support_policy_id=sample['support_policy_id'],classified_eligible_count=len(classifications),
            unclassified_count=len(sample['eligible_artifact_ids'])-len(classifications),
            denominator_definition='ELIGIBLE_RETRIEVED_RECORDS_INCLUDING_UNCLASSIFIED')
    fs['f.classify.forum1']['object']['sentiment']='NEUTRAL'
    for ex in rows['executions']:
        is_summary=ex['function_id']=='sample.theme_summary_v1'
        ex['run_id']='run.demo' if is_summary else 'run.ingest'
        ex['input_sample_ids']=[ex['parameters']['sample_id']] if is_summary else []
        samples=[s for s in rows['samples'] if s['sample_id'] in ex['input_sample_ids']]
        ex['sample_set_hash']=digest(samples);ex['terminal_reason']=None
        if samples:ex['input_artifact_ids']=sorted({a for s in samples for a in s['retrieved_artifact_ids']})
        ex['input_set_hash']=digest({'facts':sorted(ex['input_fact_ids']),'artifacts':sorted(ex['input_artifact_ids'])})
    for f in rows['facts']:f['run_id']='run.demo' if f['fact_id'].startswith('f.prior.') else 'run.ingest'
    ingest=deepcopy(rows['runs'][0]);demo=rows['runs'][0]
    all_subjects=sorted({f['subject_id'] for f in rows['facts']})
    for run,name,seal,cut,complete in [(ingest,'run.ingest','2026-09-14T16:30:00Z','2026-09-14T16:30:00Z','2026-09-14T17:01:10Z'),
                                      (demo,'run.demo','2026-09-14T17:02:00Z','2026-09-14T17:01:45Z','2026-09-14T19:00:00Z')]:
        output={fid for e in rows['executions'] if e['run_id']==name for fid in e['output_fact_ids']}
        input_ids=[f['fact_id'] for f in rows['facts'] if f['fact_id'] not in output and (name=='run.demo' or f['run_id']=='run.ingest')]
        run.update(run_id=name,input_fact_ids=sorted(input_ids),produced_fact_ids=sorted(output),knowledge_cutoff=cut,sealed_at=seal,
            sample_ids=[] if name=='run.ingest' else [s['sample_id'] for s in rows['samples']],resolution_ids=[],intake_id=intake_id,
            imported_execution_ids=[] if name=='run.ingest' else [e['execution_id'] for e in rows['executions'] if e['run_id']=='run.ingest'],
            target_results=[{'subject_id':sub,'status':'ABSTAINED' if sub=='org.other' else 'COMPLETE','completed_at':complete,
                             'reason':'POLICY_DENIED' if sub=='org.other' else None} for sub in all_subjects],
            registry_release=digest(reg),code_release=code_digest(root),approval_policy_version='4.2.0')
    rows['runs'].insert(0,ingest)
    for run in rows['runs']:
        groups={}
        for fid in set(run['input_fact_ids'])|set(run['produced_fact_ids']):groups.setdefault(claim_key(fs[fid]),[]).append(fid)
        for n,(_,ids) in enumerate(sorted(groups.items(),key=lambda pair:str(pair[0]))):
            facts=[fs[i] for i in ids];f=facts[0]
            got=resolve_claim(facts,run['as_of'],lambda f,at:f['state']!='UNKNOWN')
            rid='resolution.'+run['run_id']+'.'+str(n)
            rows['resolutions'].append({'resolution_id':rid,'tenant_id':tenant,'subject_id':f['subject_id'],'predicate_id':f['predicate_id'],
                'scope_id':f['scope_id'],'target':f['target'],'observation_ids':sorted(ids),'accepted_fact_ids':got['accepted_fact_ids'],'status':got['status'],
                'policy_version':'1.0.0','as_of':run['as_of'],'run_id':run['run_id'],
                'resolved_at':'2026-09-14T17:01:20Z' if run['run_id']=='run.ingest' else '2026-09-14T18:00:00Z'})
            run['resolution_ids'].append(rid)
    for signal in rows['signals']:signal['evaluated_at']='2026-09-14T19:30:00Z'
    for p in rows['packages']:
        p['review_id']='review.'+p['package_id']
        rows['reviews'].append({'review_id':p['review_id'],'tenant_id':tenant,'reviewer_id':'actor.fixture',
            'package':{'package_id':p['package_id'],'revision':p['revision'],'content_hash':package_hash(p)},'action':'APPROVE',
            'reason':'Synthetic reviewer approval of the exact evidence-bound fixture message.', 'decided_at':p['approved_at'],'policy_version':'4.2.0'})
    p=next(p for p in rows['packages'] if p['package_id']=='package.product');dest=reg['destinations'][0]
    for run in rows['runs']:run['produced_artifact_ids']=[]
    for ex in rows['executions']:ex['output_artifact_ids']=[]
    families=['facts','artifacts','evidence','bindings','resolutions','samples','executions','model-calls','changes','restrictions','contexts','signals','runs','reviews']
    vector=digest({'registry':reg,'package':package_hash(p),'state':{k:rows[k] for k in families}})
    pref={'package_id':p['package_id'],'revision':p['revision'],'content_hash':package_hash(p)}
    rows['gates'].append({'gate_id':'gate.fixture','tenant_id':tenant,'package':pref,'review_id':p['review_id'],'actor_id':'actor.fixture',
        'purpose':'PREVIEW_EXPORT','destination_id':dest['destination_id'],'recipient_key':None,'evaluated_at':'2026-09-14T20:00:10Z',
        'valid_until':'2026-09-14T20:05:00Z','version_vector':vector,'decision':'ALLOW','reasons':[]})
    payload=export_payload(p,dest,None);ref='fixtures/export-preview.json';blobs[ref]=payload
    rows['exports'].append({'export_id':'export.fixture','tenant_id':tenant,'package':pref,'gate_id':'gate.fixture','destination_id':dest['destination_id'],
        'mapping_version':dest['mapping_version'],'actor_id':'actor.fixture','recipient_key':None,'payload_hash':digest(payload),'payload_ref':ref,
        'idempotency_key':'fixture-preview-v41','requested_at':'2026-09-14T20:00:20Z','completed_at':'2026-09-14T20:00:21Z',
        'status':'CONFIRMED','external_reference':'fixture://preview/no-external-side-effect','automatic_sending':False})
    return rows,blobs
