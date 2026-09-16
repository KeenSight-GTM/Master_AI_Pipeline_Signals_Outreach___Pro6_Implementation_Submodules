"""v4.1 end-to-end reference guards for A–E, G and H.

No network, database, authentication provider or sender is implemented here.
Actor grants are trusted fixture configuration; production must resolve principals
server-side. ChangeRecord authorization (audit F/E07) is explicitly not patched.
"""
from __future__ import annotations
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from typing import Any
from .engine import ContractError, canonical, claim_key, digest, instant, require, resolve_claim


def package_hash(package: dict) -> str:
    """Approval metadata is excluded; every substantive output field is included."""
    return digest({k:v for k,v in package.items() if k not in {'review_id','approved_at','status'}})


def export_payload(package: dict, destination: dict, recipient_key: str | None) -> bytes:
    """Closed JSON handoff, never CSV/HTML, with no internal context claims."""
    return canonical({'package_id':package['package_id'],'revision':package['revision'],
        'content_hash':package_hash(package),'account_subject_id':package['subject_id'],
        'recipient_key':recipient_key,'destination_id':destination['destination_id'],
        'mapping_version':destination['mapping_version'],'text':package['rendered_text'],
        'send_allowed':False,'classification':'DESIGN_TEST_PREVIEW'})


def extract_job_quote(document: dict) -> dict:
    """Deterministic fixture extractor; the live model task is not implemented."""
    text=document.get('workflow')
    require(isinstance(text,str) and bool(text),'NO_WORKFLOW_QUOTE')
    return {'text':text}


def classify_theme(record: dict, theme_id: str) -> dict:
    """Narrow, explicit fixture rubric. Not a general sentiment classifier."""
    text=record.get('text','')
    terms={'theme.reporting':'spreadsheet exports','theme.follow_up':'could not get a callback',
           'theme.spreadsheets':'uses spreadsheets'}
    require(theme_id in terms and terms[theme_id].lower() in text.lower(),'FIXTURE_THEME_ABSTAIN')
    return {'theme_id':theme_id,'stance':'EXPERIENCED',
            'sentiment':'NEUTRAL' if theme_id=='theme.spreadsheets' else 'NEGATIVE'}


def form_detector(html: str) -> bool:
    """Detect real <form> elements in raw HTML, including those in excluded copy areas.

    False means not detected in this captured raw page, never no private intake.
    """
    from html.parser import HTMLParser
    class Parser(HTMLParser):
        found=False
        def handle_starttag(self, tag, attrs):
            if tag.lower()=='form':self.found=True
    parser=Parser();parser.feed(html);parser.close();return parser.found


# Explicit binding table, not imports from untrusted registry entrypoints.
def allowed_entrypoints():
    from .engine import theme_summary,evaluate_requirements
    return {
        'keensight_contracts.engine:theme_summary':theme_summary,
        'keensight_contracts.engine:evaluate_requirements':evaluate_requirements,
        'keensight_contracts.completion:extract_job_quote':extract_job_quote,
        'keensight_contracts.completion:classify_theme':classify_theme,
        'keensight_contracts.completion:form_detector':form_detector,
    }


class CompletionChecks:
    """Mixin used by Bundle, including its individual decision boundaries."""

    def validate_change(self,c):
        self.shape(c,'ChangeRecord')
        mapping={
          'RETRACTION':('facts','CHANGE_FACT'), 'SUBJECT_REBIND':('facts','CHANGE_FACT'),
          'BINDING_CORRECTION':('bindings','CHANGE_BINDING'),
          'AUTHORITY_CHANGE':(None,'CHANGE_REGISTRY'),
          'POLICY_REVOCATION':('policies','CHANGE_REGISTRY'),
          'ARTIFACT_DELETION':('artifacts','CHANGE_ARTIFACT')}
        require(c['kind'] in mapping,'UNSUPPORTED_CHANGE_KIND')
        kind,permission=mapping[c['kind']]
        require(kind is None or c['target_type']==kind,'CHANGE_TARGET_TYPE')
        if c['kind']=='AUTHORITY_CHANGE':require(c['target_type'] in ['sources','fingerprints','functions'],'AUTHORITY_TARGET_TYPE')
        self.require_actor(c['actor_id'],c['tenant_id'],permission)
        typ=c['target_type']
        target=self.row(typ,c['target_id']) if typ in ['facts','bindings','artifacts'] else self.reg(typ,c['target_id'])
        if 'tenant_id' in target:require(target['tenant_id']==c['tenant_id'],'CHANGE_TARGET_TENANT')
        elif typ=='policies':require(target['tenant_ids']==[c['tenant_id']],'SHARED_REGISTRY_REQUIRES_NEW_RELEASE')
        else:
            # Tenant-scoped veto, never mutation of a shared registry release.
            require(c['tenant_id'] in {x['tenant_id'] for x in self.registry['actors']},'UNKNOWN_CHANGE_TENANT')
        require(instant(c['recorded_at'])>=instant(c['effective_at']),'CHANGE_TIME')
        if c['replacement_id'] is not None:
            require(c['kind'] in ['SUBJECT_REBIND','BINDING_CORRECTION'],'REPLACEMENT_NOT_ALLOWED')
            replacement=self.row(typ,c['replacement_id'])
            require(replacement['tenant_id']==c['tenant_id'] and c['target_id']!=c['replacement_id'],'CHANGE_REPLACEMENT_OWNER')
            if typ=='facts':require(target['predicate_id']==replacement['predicate_id'] and target['target']==replacement['target'],'CHANGE_REPLACEMENT_MEANING')
            else:require(target['scope_id']==replacement['scope_id'],'CHANGE_REPLACEMENT_SCOPE')
        elif c['kind'] in ['SUBJECT_REBIND','BINDING_CORRECTION']:
            require(False,'MISSING_CHANGE_REPLACEMENT')
        return True

    def authorized_changes(self,at):
        # Invalid requests never take effect. Full admission rejects them; this
        # read boundary also prevents an unvalidated append becoming a veto.
        for change in self.rows['changes']:
            try:
                self.validate_change(change)
                if instant(change['recorded_at'])<=instant(at):yield change
            except ContractError:
                continue

    def available_artifacts(self,run):
        return set(run['input_artifact_ids'])|set(run.get('produced_artifact_ids',[]))

    def assert_artifact_available(self,aid,run,at,*,consumer_id=None):
        """The shared external-or-produced availability and chronology boundary."""
        artifact=self.row('artifacts',aid)
        require(artifact['tenant_id']==run['tenant_id'],'ARTIFACT_CONSUMER_TENANT')
        if aid in run['input_artifact_ids']:
            require(instant(artifact['captured_at'])<=instant(run['knowledge_cutoff']),'ARTIFACT_AFTER_CUTOFF')
        else:
            require(aid in run['produced_artifact_ids'],'UNPINNED_EXECUTION_ARTIFACT')
            producers=[ex for ex in self.rows['executions'] if ex['run_id']==run['run_id'] and aid in ex['output_artifact_ids']]
            require(len(producers)==1,'AMBIGUOUS_ARTIFACT_PRODUCER')
            producer=producers[0]
            require(producer['execution_id']!=consumer_id,'SELF_CONSUMED_ARTIFACT')
            require(producer['tenant_id']==run['tenant_id'] and producer['status']=='COMPLETE'
                    and instant(producer['finished_at'])<=instant(at),'UNFINISHED_ARTIFACT_PRODUCER')
            require(instant(producer['started_at'])<=instant(artifact['captured_at'])<=instant(producer['finished_at']),'GENERATED_ARTIFACT_TIME')
        require(instant(artifact['captured_at'])<=instant(at),'ARTIFACT_AFTER_CONSUMER')
        return artifact

    def current_claim_eligible(self,fid,at,*,purpose='INTERNAL_RESEARCH',allow_absence=False):
        if not self.usable(fid,at,purpose=purpose,allow_absence=allow_absence):return False
        for parent in self.ancestry(fid):
            target=self.row('facts',parent)
            fs=[f for f in self.rows['facts'] if f['tenant_id']==target['tenant_id'] and claim_key(f)==claim_key(target) and instant(f['recorded_at'])<=instant(at)]
            got=resolve_claim(fs,at,lambda x,t:self.usable(x['fact_id'],t,purpose=purpose,allow_absence=True))
            if got['status']!='KNOWN' or parent not in got['accepted_fact_ids']:return False
        return True

    def require_actor(self,actor_id,tenant_id,permission):
        actor=self.reg('actors',actor_id)
        require(actor['tenant_id']==tenant_id and actor['active'] and permission in actor['permissions'],'ACTOR_NOT_AUTHORIZED')
        return actor

    def available_facts(self,run):
        return set(run['input_fact_ids'])|set(run['produced_fact_ids'])

    def assert_consumed(self,fid,run_id,at=None):
        run=self.row('runs',run_id);f=self.row('facts',fid)
        require(f['tenant_id']==run['tenant_id'],'CONSUMED_FACT_TENANT')
        require(fid in self.available_facts(run),'UNPINNED_CONSUMED_FACT')
        if fid in run['produced_fact_ids']:
            require(f['execution_id'] is not None and f['run_id']==run_id,'UNPRODUCED_RUN_OUTPUT')
            ex=self.row('executions',f['execution_id'])
            require(ex['run_id']==run_id and fid in ex['output_fact_ids'] and ex['status']=='COMPLETE','INVALID_RUN_PRODUCER')
        else:
            require(instant(f['recorded_at'])<=instant(run['knowledge_cutoff']),'INPUT_AFTER_KNOWLEDGE_CUTOFF')
            if f['execution_id']:
                require(f['execution_id'] in run['imported_execution_ids'],'UNPINNED_IMPORTED_EXECUTION')
        if at is not None:require(instant(f['recorded_at'])<=instant(at),'CONSUMER_PRECEDES_FACT')
        # Bindings and every ancestral input matter, not only the first hop.
        for parent in self.ancestry(fid):
            p=self.row('facts',parent)
            require(parent in self.available_facts(run),'UNPINNED_ANCESTRAL_FACT')
            e=self.row('evidence',p['evidence_id'])
            require(set(e['sample_ids'])<=set(run['sample_ids']),'UNPINNED_ANCESTRAL_SAMPLE')
            if p['execution_id'] and p['run_id']!=run_id:
                require(p['execution_id'] in run['imported_execution_ids'],'UNPINNED_ANCESTRAL_EXECUTION')
            if p['binding_id']:
                require(p['binding_id'] in run['binding_ids'],'UNPINNED_CONSUMED_BINDING')
                b=self.row('bindings',p['binding_id'])
                require(instant(b['decided_at'])<=instant(run['sealed_at']),'BINDING_AFTER_SEAL')
        require(self.roots(fid)<=self.available_artifacts(run),'UNPINNED_ANCESTRAL_ARTIFACT')
        return f

    def target_completed(self,run_id,subject_id,at=None):
        run=self.row('runs',run_id)
        require(run['status'] in ['COMPLETE','PARTIAL'],'RUN_NOT_PUBLISHABLE')
        results=[x for x in run['target_results'] if x['subject_id']==subject_id]
        require(len(results)==1 and results[0]['status']=='COMPLETE','TARGET_NOT_COMPLETE')
        if at:require(instant(results[0]['completed_at'])<=instant(at),'USE_PRECEDES_TARGET_COMPLETION')

    def decision_eligible(self,fid,at,*,run_id,purpose='INTERNAL_RESEARCH',allow_absence=False,production=False):
        """Resolve the whole available claim group, not a cherry-picked signal list."""
        f=self.assert_consumed(fid,run_id)
        if not self.usable(fid,at,purpose=purpose,allow_absence=allow_absence,production=production):return False
        run=self.row('runs',run_id)
        # A conflict cannot be laundered through a derived observation.
        for parent in self.ancestry(fid):
            target=self.row('facts',parent)
            fs=[self.row('facts',i) for i in self.available_facts(run) if claim_key(self.row('facts',i))==claim_key(target)]
            got=resolve_claim(fs,at,lambda x,t:self.usable(x['fact_id'],t,purpose=purpose,production=production,allow_absence=True))
            if got['status']!='KNOWN' or parent not in got['accepted_fact_ids']:return False
        return True

    def validate_resolution_closure(self,run):
        groups=defaultdict(list)
        for fid in self.available_facts(run):groups[claim_key(self.row('facts',fid))].append(fid)
        covered={}
        for rid in run['resolution_ids']:
            r=self.row('resolutions',rid)
            require(r['run_id']==run['run_id'] and r['tenant_id']==run['tenant_id'],'RESOLUTION_RUN')
            fs=[self.row('facts',i) for i in r['observation_ids']]
            require(bool(fs),'EMPTY_RESOLUTION');key=claim_key(fs[0])
            require(key not in covered,'DUPLICATE_RESOLUTION_FOR_CLAIM')
            require(set(r['observation_ids'])==set(groups.get(key,[])),'INCOMPLETE_CLAIM_RESOLUTION')
            require(r['as_of']==run['as_of'],'RESOLUTION_LOGICAL_TIME')
            require(all(instant(f['recorded_at'])<=instant(r['resolved_at']) for f in fs),'RESOLUTION_BEFORE_INPUT')
            got=resolve_claim(fs,run['as_of'],lambda f,t:self.usable(f['fact_id'],t,allow_absence=True))
            require(got['status']==r['status'] and got['accepted_fact_ids']==sorted(r['accepted_fact_ids']),'RESOLUTION_POLICY_MISMATCH')
            covered[key]=rid
        require(set(covered)==set(groups),'MISSING_CLAIM_RESOLUTION')

    def validate_attempt(self,a):
        self.shape(a,'AcquisitionAttempt')
        intake=self.row('intakes',a['intake_id']);source=self.reg('sources',a['source_id'])
        require(a['tenant_id']==intake['tenant_id'],'ATTEMPT_TENANT')
        require(a['target'] in intake['targets'],'ATTEMPT_OUTSIDE_INTAKE')
        require(source['version']==a['source_version'],'ATTEMPT_SOURCE_VERSION')
        require(instant(intake['received_at'])<=instant(a['started_at'])<=instant(a['finished_at']),'ATTEMPT_CHRONOLOGY')
        require(a['requests_made']<=a['max_requests'],'ATTEMPT_REQUEST_BUDGET')
        if a['execution_mode']=='LIVE_CAPTURE' and a['requests_made']:
            profile=self.reg('profiles',intake['profile_id'])
            require(a['source_id'] in profile['capture_source_ids'],'CAPTURE_SOURCE_NOT_ENABLED')
        require(a['request_hash']==digest({'target':a['target'],'source_id':a['source_id'],'operation_key':a['operation_key']}),'ATTEMPT_REQUEST_HASH')
        if a['scope_id']:
            scope=self.row('scopes',a['scope_id'])
            require(scope['tenant_id']==a['tenant_id'] and scope['subject_id']==a['target']['subject_id'],'ATTEMPT_SCOPE_SUBJECT')
            require(a['target']['resource_uri'] in scope['resources'],'ATTEMPT_RESOURCE')
        else:require(not a['artifact_ids'],'UNBOUND_ATTEMPT_CANNOT_ADMIT_ARTIFACTS')
        success=a['status'] in ['SUCCEEDED','EMPTY_RESULT']
        if success:
            require(bool(a['artifact_ids']) and a['terminal_reason'] in [None,'NO_RESULTS'],'SUCCESS_WITHOUT_RESPONSE')
            require(not a['truncated'] and a['pagination'] in ['NOT_APPLICABLE','EXHAUSTED'],'INCOMPLETE_SUCCESS')
            require(self.policy_allows(source['policy_id'],'CAPTURE',a['started_at'],tenant=a['tenant_id']),'ATTEMPT_CAPTURE_DENIED')
        else:require(a['terminal_reason'] is not None,'ATTEMPT_FAILURE_REASON')
        if a['status'] in ['POLICY_DENIED','BUDGET_DENIED']:
            require(not a['artifact_ids'] and a['requests_made']==0,'PRECAPTURE_DENIAL_WITH_CAPTURE')
        for aid in a['artifact_ids']:
            artifact=self.row('artifacts',aid)
            require(artifact['tenant_id']==a['tenant_id'] and artifact['scope_id']==a['scope_id'] and artifact['source_id']==a['source_id'],'ATTEMPT_ARTIFACT_BINDING')
            require(instant(a['started_at'])<=instant(artifact['captured_at'])<=instant(a['finished_at']),'ARTIFACT_OUTSIDE_ATTEMPT')
            require(artifact['byte_count']<=a['body_limit_bytes'],'ATTEMPT_BODY_BUDGET')
        if a['cost_status']=='UNKNOWN':require(a['cost_minor'] is None,'UNKNOWN_COST_AS_ZERO')
        elif a['cost_status']=='NOT_CHARGED':require(a['cost_minor']==0,'UNCHARGED_COST')
        else:require(a['cost_minor'] is not None and a['currency'] is not None,'KNOWN_COST_MISSING')

    def validate_coverage_execution(self,c):
        ex=self.row('executions',c['detector_execution_id']);fn=self.reg('functions',ex['function_id'])
        contract=fn['detector_contract'];scope=self.row('scopes',c['scope_id'])
        require(contract is not None,'NOT_A_REGISTERED_DETECTOR')
        if fn['entrypoint']=='keensight_contracts.completion:form_detector':
            require(contract=={'capture_modes':['RAW_HTML'],'predicate_ids':['form.surface'],'operator':'HTML_FORM_ELEMENT'} and fn['output_predicates']==['form.surface'],'DETECTOR_IMPLEMENTATION_CONTRACT')
        require(c['detector_release']==digest(fn),'UNRESOLVED_DETECTOR_RELEASE')
        require(ex['parameters'].get('scope_id')==c['scope_id'] and ex['parameters'].get('target')==c['target'],'DETECTOR_TARGET_MISMATCH')
        require(c['tenant_id']==ex['tenant_id'] and ex['subject_id']==scope['subject_id'],'DETECTOR_SCOPE_SUBJECT')
        require(set(c['predicate_ids'])<=set(contract['predicate_ids']),'DETECTOR_PREDICATES')
        require(scope['capture_mode'] in contract['capture_modes'],'DETECTOR_CAPTURE_MODE')
        require(instant(ex['finished_at'])<=instant(c['checked_at']),'COVERAGE_PRECEDES_DETECTOR')
        collected=set()
        for aid in c['attempt_ids']:
            a=self.row('attempts',aid);self.validate_attempt(a)
            require(a['tenant_id']==c['tenant_id'] and a['scope_id']==c['scope_id'] and a['source_id']==c['source_id'],'COVERAGE_ATTEMPT_SCOPE')
            if c['status']=='COMPLETE':
                require(a['status'] in ['SUCCEEDED','EMPTY_RESULT'] and not a['truncated'] and a['pagination'] in ['NOT_APPLICABLE','EXHAUSTED'],'COVERAGE_ATTEMPT_INCOMPLETE')
                require(instant(a['finished_at'])<=instant(ex['started_at']),'DETECTOR_BEFORE_CAPTURE_FINISH')
            collected |= set(a['artifact_ids'])
        checked={x['artifact_id'] for x in c['checked'] if x['artifact_id']}
        require(checked<=collected and checked<=set(ex['input_artifact_ids']),'UNCHECKED_CAPTURE_IN_COVERAGE')
        if c['status']=='COMPLETE':
            require(ex['status']=='COMPLETE','FAILED_DETECTOR_COVERAGE')
            require(set(ex['input_artifact_ids'])==checked,'DETECTOR_EXTRA_OR_MISSING_CAPTURES')
            for aid in checked:
                a=self.row('artifacts',aid)
                require(instant(a['captured_at'])<=instant(c['checked_at']),'COVERAGE_PREDATES_CAPTURE')
                # This delivered detector really executes; registry bytes alone are not proof.
                if fn['entrypoint']=='keensight_contracts.completion:form_detector' and a['retention_state']=='RETAINED':
                    require(not form_detector((self.root/a['content_ref']).read_text()),'FORM_PRESENT_BUT_ABSENCE_CLAIMED')

    def validate_sample_dependencies(self,s):
        policy=self.reg('support-policies',s['support_policy_id'])
        self.reg('taxonomy',s['theme_id'])
        require(instant(s['created_at'])>=max(instant(self.row('artifacts',i)['captured_at']) for i in s['retrieved_artifact_ids']),'SAMPLE_BEFORE_CAPTURE')
        decisions=s['record_decisions']
        require(len(decisions)==len({d['artifact_id'] for d in decisions}) and {d['artifact_id'] for d in decisions}==set(s['retrieved_artifact_ids']),'INCOMPLETE_SAMPLE_DECISIONS')
        for d in decisions:
            aid=d['artifact_id'];ids=d['classification_fact_ids']
            if d['status']=='EXCLUDED':
                require(aid in s['excluded_artifact_ids'] and bool(d['reason']),'EXCLUSION_WITHOUT_REASON')
            else:require(aid in s['eligible_artifact_ids'],'DECISION_NOT_ELIGIBLE')
            if d['status']=='UNCLASSIFIED':require(not ids and bool(d['reason']),'UNCLASSIFIED_AS_NEGATIVE')
            if d['status'] in ['SUPPORT','CONTRADICT','NO_THEME']:require(bool(ids),'DECISION_WITHOUT_CLASSIFICATION')
            for fid in ids:
                f=self.row('facts',fid)
                require(f['subject_id']==s['subject_id'] and f['state']=='OBSERVED' and f['object']['theme_id']==s['theme_id'],'SAMPLE_CLASSIFICATION_TARGET')
                require(aid in self.roots(fid),'CLASSIFICATION_WRONG_RECORD')
                o=f['object']
                origin=self.row('artifacts',aid)
                for lid in o['support_locator_ids']:
                    loc_art=self.row('artifacts',self.row('locators',lid)['artifact_id'])
                    require((loc_art['origin_namespace'],loc_art['origin_record_id'])==(origin['origin_namespace'],origin['origin_record_id']),'CLASSIFICATION_SUPPORT_LOCATOR_TARGET')
                support=o['stance'] in policy['allowed_stances'] and o['sentiment'] in policy['allowed_sentiments']
                if d['status']=='SUPPORT':require(support,'INVALID_PAIN_SUPPORT')
                if d['status'] in ['CONTRADICT','NO_THEME']:require(not support,'SUPPORT_MISCOUNTED')

    def current_version_vector(self,package_id):
        # Conservative whole-bundle vector; excludes decisions/receipts to avoid self-reference.
        families=['facts','artifacts','evidence','bindings','resolutions','samples','executions','model-calls','changes','restrictions','contexts','signals','runs','reviews']
        return digest({'registry':self.registry,'package':package_hash(self.row('packages',package_id)),
                       'state':{k:self.rows[k] for k in families}})

    def validate_package_dependencies(self,p,*,require_completion=True):
        run=self.row('runs',p['run_id']);profile=self.reg('profiles',run['profile_id'])
        require(p['tenant_id']==run['tenant_id']==self.row('subjects',p['subject_id'])['tenant_id'],'PACKAGE_OWNER')
        require(profile['product_boundary'] in ['PREVIEW','REVIEWED_HANDOFF'],'KNOWLEDGE_PROFILE_CANNOT_PUBLISH_COPY')
        require(p['template_id'] in profile['template_ids'],'TEMPLATE_NOT_ENABLED')
        at=p['approved_at'] or run['as_of']
        if require_completion:self.target_completed(run['run_id'],p['subject_id'],at)
        for sid in p['signal_ids']:
            s=self.row('signals',sid)
            require(s['run_id']==run['run_id'] and s['tenant_id']==p['tenant_id'] and s['subject_id']==p['subject_id'] and s['status']=='RESOLVED','PACKAGE_SIGNAL_ELIGIBILITY')
            require(s['signal_type_id'] in profile['signal_ids'],'SIGNAL_NOT_ENABLED')
            require(instant(s['evaluated_at'])<=instant(at),'PACKAGE_BEFORE_SIGNAL')
            for fid in s['input_fact_ids']:
                self.assert_consumed(fid,run['run_id'],s['evaluated_at'])
                require(self.decision_eligible(fid,at,run_id=run['run_id'],allow_absence=True),'PACKAGE_SIGNAL_INPUT_INELIGIBLE')
        for cid in p['context_ids']:
            c=self.row('contexts',cid)
            require(c['status']=='ELIGIBLE' and c['run_id']==run['run_id'] and c['tenant_id']==p['tenant_id'] and c['account_subject_id']==p['subject_id'],'ABSTAINED_OR_FOREIGN_CONTEXT')
            self.validate_context(c)
            for fid in [c['link_fact_id']]+c['context_fact_ids']:
                require(self.decision_eligible(fid,at,run_id=run['run_id']),'CURRENT_CONTEXT_INELIGIBLE')
        for clause in p['clauses']:
            for fid in clause['fact_ids']:
                self.assert_consumed(fid,run['run_id'],at)
                require(self.decision_eligible(fid,at,run_id=run['run_id'],purpose='OUTREACH',allow_absence=True),'CLAIM_NOT_RESOLVED_FOR_COPY')

    def validate_review(self,r,*,verify_support=True):
        self.require_actor(r['reviewer_id'],r['tenant_id'],'REVIEW_PACKAGE')
        p=self.row('packages',r['package']['package_id'])
        require(r['tenant_id']==p['tenant_id'] and r['package']['revision']==p['revision'] and r['package']['content_hash']==package_hash(p),'REVIEW_REVISION_HASH')
        if r['action']=='APPROVE':
            require(p['review_id']==r['review_id'] and p['approved_at']==r['decided_at'],'PACKAGE_REVIEW_BACKLINK')
            require(r['policy_version']==self.row('runs',p['run_id'])['approval_policy_version'],'REVIEW_POLICY_PIN')
            if verify_support:
                self.validate_package_dependencies(p)
                require(self.render(p)==p['rendered_text'],'REVIEW_UNSUPPORTED_COPY')

    def gate_reasons(self,g,at=None):
        at=at or g['evaluated_at'];p=self.row('packages',g['package']['package_id']);reasons=[]
        try:
            template=self.reg('templates',p['template_id'])
            require(template['authority']=='ACTIVE','TEMPLATE_NOT_CURRENTLY_ACTIVE')
            require(template['renderer'] in {'observed_product_v1','attributed_job_statement_v1','scoped_absence_v1'},'RENDERER_NOT_IMPLEMENTED')
            self.validate_package_dependencies({**p,'approved_at':at})
            require(self.render({**p,'approved_at':at})==p['rendered_text'],'CURRENT_RENDERER_CONTENT_MISMATCH')
            for cl in p['clauses']:
                for fid in cl['fact_ids']:
                    require(self.current_claim_eligible(fid,at,purpose='EXPORT',allow_absence=True),'EXPORT_EVIDENCE_INELIGIBLE')
            for rid in p['signal_ids']:
                for fid in self.row('signals',rid)['input_fact_ids']:
                    require(self.current_claim_eligible(fid,at,allow_absence=True),'SIGNAL_EVIDENCE_INELIGIBLE')
            for cid in p['context_ids']:
                ctx=self.row('contexts',cid)
                for fid in [ctx['link_fact_id']]+ctx['context_fact_ids']:
                    require(self.current_claim_eligible(fid,at),'CONTEXT_CURRENT_CONFLICT')
        except ContractError:reasons.append('INELIGIBLE_CURRENT_SUPPORT')
        for r in self.rows['restrictions']:
            if (r['tenant_id']==p['tenant_id'] and r['subject_id']==p['subject_id'] and
                (r['recipient_key'] is None or r['recipient_key']==g['recipient_key']) and
                instant(r['effective_at'])<=instant(at) and (r['released_at'] is None or instant(at)<instant(r['released_at']))):
                reasons.append(r['kind'])
        return sorted(set(reasons))

    def validate_gate(self,g,at=None):
        self.require_actor(g['actor_id'],g['tenant_id'],'USE_GATE')
        p=self.row('packages',g['package']['package_id']);dest=self.reg('destinations',g['destination_id']);review=self.row('reviews',g['review_id'])
        profile=self.reg('profiles',self.row('runs',p['run_id'])['profile_id'])
        require(profile['export_enabled'] and profile['product_boundary']=='REVIEWED_HANDOFF','EXPORT_DISABLED')
        require(p['tenant_id']==g['tenant_id']==dest['tenant_id']==review['tenant_id'] and dest['enabled'],'GATE_OWNER_OR_DESTINATION')
        require(g['package']==review['package'] and g['package']['content_hash']==package_hash(p),'GATE_CONTENT_HASH')
        require(review['action']=='APPROVE' and p['review_id']==review['review_id'],'UNAPPROVED_GATE')
        self.validate_review(review,verify_support=False)
        require(instant(review['decided_at'])<=instant(g['evaluated_at'])<instant(g['valid_until'])<=instant(g['evaluated_at'])+timedelta(minutes=5),'GATE_CHRONOLOGY')
        require((g['purpose']=='CONTACT_EXPORT')==(dest['kind']=='CONTACT_HANDOFF'),'DESTINATION_PURPOSE')
        require(g['recipient_key'] is not None if g['purpose']=='CONTACT_EXPORT' else g['recipient_key'] is None,'GATE_RECIPIENT_REQUIRED_OR_UNEXPECTED')
        require(g['version_vector']==self.current_version_vector(p['package_id']),'STALE_USE_GATE')
        now=at or g['evaluated_at']
        require(instant(g['evaluated_at'])<=instant(now)<instant(g['valid_until']),'EXPIRED_USE_GATE')
        reasons=self.gate_reasons(g,now)
        require(g['decision']==('BLOCK' if reasons else 'ALLOW') and g['reasons']==reasons,'USE_GATE_DECISION_MISMATCH')

    def validate_export(self,x):
        self.require_actor(x['actor_id'],x['tenant_id'],'EXPORT')
        gate=self.row('gates',x['gate_id']);p=self.row('packages',x['package']['package_id']);dest=self.reg('destinations',x['destination_id'])
        require(x['tenant_id']==p['tenant_id']==gate['tenant_id'],'EXPORT_TENANT')
        require(x['package']==gate['package'] and x['destination_id']==gate['destination_id'] and x['recipient_key']==gate['recipient_key'],'EXPORT_GATE_BINDING')
        require(x['mapping_version']==dest['mapping_version'],'EXPORT_MAPPING_VERSION')
        self.validate_gate(gate,x['requested_at']);require(gate['decision']=='ALLOW','EXPORT_GATE_BLOCKED')
        payload=export_payload(p,dest,x['recipient_key'])
        require(x['payload_hash']==digest(payload),'EXPORT_PAYLOAD_HASH')
        if x['status']=='CONFIRMED':
            require(x['completed_at'] is not None and x['external_reference'] is not None and x['payload_ref'] is not None,'CONFIRMED_EXPORT_WITHOUT_RECEIPT')
            path=(self.root/x['payload_ref']).resolve()
            require(path.is_relative_to(self.root.resolve()) and path.is_file() and path.read_bytes()==payload,'EXPORTED_BYTES_MISMATCH')
        if x['status']=='UNKNOWN':require(x['external_reference'] is None,'UNCERTAIN_EXPORT_AS_CONFIRMED')
        if x['completed_at']:require(instant(x['requested_at'])<=instant(x['completed_at']),'EXPORT_CHRONOLOGY')

    def validate_completion(self):
        """Invoked by the full validator after all schemas, before decision validation."""
        for intake in self.rows['intakes']:
            self.require_actor(intake['requester_id'],intake['tenant_id'],'INTAKE')
            self.reg('profiles',intake['profile_id'])
            require(intake['request_hash']==digest({'profile_id':intake['profile_id'],'purpose':intake['purpose'],'targets':intake['targets']}),'INTAKE_REQUEST_HASH')
            for t in intake['targets']:
                if t['subject_id']:require(self.row('subjects',t['subject_id'])['tenant_id']==intake['tenant_id'],'INTAKE_TARGET_TENANT')
        for a in self.rows['attempts']:self.validate_attempt(a)
        require(len(self.rows['attempts'])==len({(a['tenant_id'],a['operation_key']) for a in self.rows['attempts']}),'DUPLICATE_ACQUISITION_OPERATION')
        for fn in self.registry['functions']:
            if fn['implementation_status']=='REFERENCE_IMPLEMENTED':
                require(fn['entrypoint'] in allowed_entrypoints() and callable(allowed_entrypoints()[fn['entrypoint']]),'ENTRYPOINT_NOT_ALLOWLISTED')
        for run in self.rows['runs']:
            profile=self.reg('profiles',run['profile_id']);intake=self.row('intakes',run['intake_id'])
            require(intake['tenant_id']==run['tenant_id'] and intake['profile_id']==run['profile_id'],'RUN_INTAKE')
            require(instant(run['created_at'])<=instant(run['knowledge_cutoff'])<=instant(run['sealed_at']),'RUN_SEAL_ORDER')
            require(len(run['target_results'])==len({r['subject_id'] for r in run['target_results']}),'DUPLICATE_TARGET_RESULT')
            states={x['status'] for x in run['target_results']}
            if run['status']=='COMPLETE':require(states<={'COMPLETE','ABSTAINED'} and 'FAILED' not in states,'COMPLETE_RUN_WITH_FAILED_TARGET')
            if run['status']=='FAILED':require('COMPLETE' not in states,'FAILED_RUN_HAS_COMPLETE_TARGET')
            if run['status']=='PARTIAL':require('COMPLETE' in states and 'FAILED' in states,'INVALID_PARTIAL_RUN')
            for r in run['target_results']:
                require(self.row('subjects',r['subject_id'])['tenant_id']==run['tenant_id'],'TARGET_RESULT_TENANT')
                require(instant(run['sealed_at'])<=instant(r['completed_at']),'TARGET_BEFORE_SEAL')
                require((r['status']=='COMPLETE')==(r['reason'] is None),'TARGET_RESULT_REASON')
                if r['status']=='COMPLETE':
                    require(all(e['status']=='COMPLETE' and instant(e['finished_at'])<=instant(r['completed_at']) for e in self.rows['executions'] if e['run_id']==run['run_id'] and e['subject_id']==r['subject_id']),'TARGET_WITH_UNFINISHED_EXECUTION')
            produced={fid for e in self.rows['executions'] if e['run_id']==run['run_id'] for fid in e['output_fact_ids']}
            require(produced==set(run['produced_fact_ids']) and not produced&set(run['input_fact_ids']),'RUN_OUTPUT_CLOSURE')
            for fid in self.available_facts(run):
                f=self.assert_consumed(fid,run['run_id'])
                require(f['predicate_id'] in profile['fact_predicate_ids'],'FACT_NOT_ENABLED')
            generated={aid for ex in self.rows['executions'] if ex['run_id']==run['run_id'] for aid in ex['output_artifact_ids']}
            require(generated==set(run['produced_artifact_ids']) and not generated&set(run['input_artifact_ids']),'RUN_ARTIFACT_OUTPUT_CLOSURE')
            declared=[aid for ex in self.rows['executions'] if ex['run_id']==run['run_id'] for aid in ex['output_artifact_ids']]
            require(len(declared)==len(set(declared)),'MULTIPLE_ARTIFACT_PRODUCERS')
            for aid in run['input_artifact_ids']:
                require(instant(self.row('artifacts',aid)['captured_at'])<=instant(run['knowledge_cutoff']),'ARTIFACT_AFTER_CUTOFF')
            for sid in run['sample_ids']:
                sample=self.row('samples',sid)
                require(sample['tenant_id']==run['tenant_id'] and instant(sample['created_at'])<=instant(run['sealed_at']),'SAMPLE_SEAL')
                require(set(sample['retrieved_artifact_ids'])<=set(run['input_artifact_ids']),'SAMPLE_UNPINNED_RECORDS')
        for ex in self.rows['executions']:
            run=self.row('runs',ex['run_id']);fn=self.reg('functions',ex['function_id']);profile=self.reg('profiles',run['profile_id'])
            require(ex['function_id'] in profile['execute_function_ids'],'EXECUTED_FUNCTION_NOT_ENABLED')
            require(instant(run['sealed_at'])<=instant(ex['started_at']),'EXECUTION_BEFORE_SEAL')
            if ex['status']!='COMPLETE':require(not ex['output_fact_ids'] and ex['terminal_reason'] is not None,'FAILED_PRODUCER_OUTPUT')
            else:require(ex['terminal_reason'] is None,'SUCCESS_WITH_FAILURE_REASON')
            require(not set(ex['input_artifact_ids'])&set(ex['output_artifact_ids']),'SELF_CONSUMED_ARTIFACT')
            for aid in ex['input_artifact_ids']:
                self.assert_artifact_available(aid,run,ex['started_at'],consumer_id=ex['execution_id'])
            allowed_generated=set()
            if ex['model_call_id']:
                model=self.row('model-calls',ex['model_call_id'])
                allowed_generated={x for x in [model['request_artifact_id'],model['response_artifact_id']] if x}
                allowed_generated|={r['output_response_artifact_id'] for r in self.rows['repairs'] if r['call_id']==model['call_id']}
            require(set(ex['output_artifact_ids'])<=allowed_generated,'UNSUPPORTED_ARTIFACT_PRODUCER_KIND')
            for aid in ex['output_artifact_ids']:
                artifact=self.row('artifacts',aid)
                require(artifact['tenant_id']==ex['tenant_id'] and ex['status']=='COMPLETE','GENERATED_ARTIFACT_OWNER_OR_PRODUCER')
                require(instant(ex['started_at'])<=instant(artifact['captured_at'])<=instant(ex['finished_at']),'GENERATED_ARTIFACT_TIME')
            for fid in ex['input_fact_ids']:self.assert_consumed(fid,run['run_id'],ex['started_at'])
            samples=[self.row('samples',i) for i in ex['input_sample_ids']]
            require(set(ex['input_sample_ids'])<=set(run['sample_ids']),'UNPINNED_EXECUTION_SAMPLE')
            require(ex['sample_set_hash']==digest(samples),'SAMPLE_INPUT_HASH')
            sample_artifacts={a for s in samples for a in s['retrieved_artifact_ids']}
            require(sample_artifacts<=set(ex['input_artifact_ids']),'MISSING_DENOMINATOR_EXECUTION_INPUT')
            for sid in ex['input_sample_ids']:
                sample=self.row('samples',sid)
                cls={f for d in sample['record_decisions'] for f in d['classification_fact_ids']}
                require(cls<=set(ex['input_fact_ids']),'UNPINNED_SAMPLE_CLASSIFICATION')
            if ex['model_call_id']:
                call=self.row('model-calls',ex['model_call_id'])
                require(call['tenant_id']==ex['tenant_id'] and set(call['input_artifact_ids'])==set(ex['input_artifact_ids']),'MODEL_EXECUTION_INPUT_MISMATCH')
                if ex['status']=='COMPLETE':require(call['status']=='PARSED' and call['response_artifact_id'] is not None,'FAILED_MODEL_PRODUCER')
                for aid in [call['request_artifact_id'],call['response_artifact_id']]:
                    if aid:
                        require(aid in set(run['input_artifact_ids'])|set(ex['output_artifact_ids']),'UNPINNED_MODEL_IO')
                        require(instant(self.row('artifacts',aid)['captured_at'])<=instant(ex['finished_at']),'MODEL_IO_AFTER_EXECUTION')
            for fid in ex['output_fact_ids']:
                f=self.row('facts',fid);e=self.row('evidence',f['evidence_id'])
                require(f['run_id']==ex['run_id'] and f['tenant_id']==ex['tenant_id'],'OUTPUT_RUN_OWNER')
                require(ex['status']=='COMPLETE' and instant(ex['finished_at'])<=instant(f['recorded_at']),'OUTPUT_BEFORE_SUCCESS')
                require(set(e['sample_ids'])==set(ex['input_sample_ids']),'OUTPUT_SAMPLE_LINEAGE')
                direct={self.row('locators',lid)['artifact_id'] for lid in e['locator_ids']}
                require(direct<=set(ex['input_artifact_ids']),'OUTPUT_RAW_INPUT_MISMATCH')
        for c in self.rows['coverage']:self.validate_coverage_execution(c)
        for sample in self.rows['samples']:self.validate_sample_dependencies(sample)
        for run in self.rows['runs']:self.validate_resolution_closure(run)
        for s in self.rows['signals']:
            run=self.row('runs',s['run_id']);profile=self.reg('profiles',run['profile_id'])
            require(s['signal_type_id'] in profile['signal_ids'],'SIGNAL_NOT_ENABLED')
            self.target_completed(run['run_id'],s['subject_id'],s['evaluated_at'])
            for fid in s['input_fact_ids']:self.assert_consumed(fid,run['run_id'],s['evaluated_at'])
            for rid in run['resolution_ids']:
                r=self.row('resolutions',rid)
                if set(r['observation_ids'])&set(s['input_fact_ids']):require(instant(r['resolved_at'])<=instant(s['evaluated_at']),'SIGNAL_BEFORE_RESOLUTION')
            for cid in s['context_ids']:
                c=self.row('contexts',cid)
                require(c['status']=='ELIGIBLE' and c['run_id']==s['run_id'] and c['tenant_id']==s['tenant_id'],'ABSTAINED_OR_FOREIGN_CONTEXT')

    def validate_handoffs(self):
        # Reserved delivery cannot be smuggled in through a no-send preview profile.
        for exposure in self.rows['exposures']:
            p=self.row('packages',exposure['package_id'])
            profile=self.reg('profiles',self.row('runs',p['run_id'])['profile_id'])
            require(profile['delivery_enabled'] and p['send_allowed'],'DELIVERY_DISABLED')
        for event in self.rows['outcomes']:
            e=self.row('evidence',event['evidence_id'])
            require(e['tenant_id']==event['tenant_id'],'OUTCOME_EVIDENCE_TENANT')
        for p in self.rows['packages']:
            if p['status'] in ['DESIGN_TEST_APPROVED','APPROVED']:
                require(p['review_id'] is not None,'APPROVAL_WITHOUT_REVIEW')
                self.validate_review(self.row('reviews',p['review_id']))
        for r in self.rows['reviews']:self.validate_review(r)
        for r in self.rows['restrictions']:
            self.require_actor(r['actor_id'],r['tenant_id'],'RESTRICT')
            require(self.row('subjects',r['subject_id'])['tenant_id']==r['tenant_id'],'RESTRICTION_TENANT')
            require((r['released_at'] is None)==(r['released_by'] is None),'RESTRICTION_RELEASE_AUTH')
            if r['released_by']:
                self.require_actor(r['released_by'],r['tenant_id'],'RESTRICT')
                require(instant(r['effective_at'])<=instant(r['released_at']),'RESTRICTION_RELEASE_TIME')
        for gate in self.rows['gates']:self.validate_gate(gate)
        for x in self.rows['exports']:self.validate_export(x)
        require(len(self.rows['exports'])==len({(x['tenant_id'],x['destination_id'],x['idempotency_key']) for x in self.rows['exports']}),'DUPLICATE_EXPORT_OPERATION')
