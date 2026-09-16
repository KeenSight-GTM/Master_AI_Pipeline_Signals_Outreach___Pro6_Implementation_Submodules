"""Cross-record design validator for the v4 batch profile.

Structural validity is not factual truth or production authorization. All supplied
sources and approvals are synthetic, and production remains disabled.
"""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry, Resource
from .engine import *
from .completion import CompletionChecks

STRICT_FORMATS=FormatChecker()

@STRICT_FORMATS.checks("date-time", raises=(ValueError, TypeError))
def _strict_datetime(value):
    if not isinstance(value,str): return True
    parsed=datetime.fromisoformat(value[:-1]+"+00:00" if value.endswith("Z") else value)
    return parsed.tzinfo is not None

@STRICT_FORMATS.checks("uri", raises=(ValueError, TypeError))
def _strict_uri(value):
    if not isinstance(value,str): return True
    if any(ch.isspace() for ch in value): return False
    return bool(urlsplit(value).scheme)

REGISTRY_TYPES={'predicates':'PredicateDefinition','metrics':'MetricDefinition','taxonomy':'TaxonomyTerm','coverage':'CoverageFamilyPlan',
 'sources':'SourceDefinition','policies':'DataAccessPolicy','functions':'FunctionDefinition','profiles':'CapabilityProfile',
 'context-rules':'ContextJoinRule','templates':'TemplateDefinition','signals':'SignalDefinition','fingerprints':'FingerprintDefinition','providers':'ProviderBlueprint','actors':'ActorGrant','destinations':'DestinationDefinition','support-policies':'ResearchSupportPolicy'}
ROW_TYPES={'subjects':'Subject','scopes':'Scope','bindings':'SubjectBinding','artifacts':'Artifact','locators':'EvidenceLocator','coverage':'CoverageRecord',
 'evidence':'EvidenceSet','facts':'Fact','executions':'ExecutionRecord','runs':'BatchRun','samples':'ResearchSample','contexts':'ContextAssessment',
 'signals':'SignalEvaluation','packages':'OutreachPackage','changes':'ChangeRecord','model-calls':'ModelCall','repairs':'RepairAttempt',
 'resolutions':'ClaimResolution','calibrations':'CalibrationRecord','candidates':'CandidateRecord','exposures':'Exposure','outcomes':'OutcomeEvent','intakes':'IntakeRequest','attempts':'AcquisitionAttempt','reviews':'ReviewDecision','gates':'UseGateDecision','exports':'ExportReceipt','restrictions':'UseRestriction'}
KEYS={'predicates':'predicate_id','metrics':'metric_id','taxonomy':'term_id','coverage':'section','sources':'source_id','policies':'policy_id',
 'functions':'function_id','profiles':'profile_id','context-rules':'join_rule_id','templates':'template_id','signals':'signal_type_id',
 'fingerprints':'fingerprint_id','providers':'blueprint_id','subjects':'subject_id','scopes':'scope_id','bindings':'binding_id','artifacts':'artifact_id',
 'locators':'locator_id','evidence':'evidence_id','facts':'fact_id','executions':'execution_id','runs':'run_id','samples':'sample_id','contexts':'context_id',
 'packages':'package_id','changes':'change_id','model-calls':'call_id','repairs':'attempt_id','resolutions':'resolution_id','calibrations':'calibration_id','candidates':'candidate_id','exposures':'exposure_id','outcomes':'event_id','actors':'actor_id','destinations':'destination_id','support-policies':'support_policy_id','intakes':'intake_id','attempts':'attempt_id','reviews':'review_id','gates':'gate_id','exports':'export_id','restrictions':'restriction_id'}

class Bundle(CompletionChecks):
    def __init__(self,root: Path, *,check_hashes: bool=True):
        self.root=Path(root)
        self.schemas={p.stem.replace('.schema',''):read_json(p) for p in (self.root/'schemas').glob('*.json')}
        self.registry={n:read_json(self.root/'registry'/f'{n}.json') for n in REGISTRY_TYPES}
        self.rows=read_json(self.root/'examples/bundle.json')
        require(set(self.rows)==set(ROW_TYPES),'INSTANCE_FAMILY_SET')
        require({p.name for p in (self.root/'registry').glob('*.json')}=={x+'.json' for x in REGISTRY_TYPES},'REGISTRY_FILE_SET')
        self.index={};self.rindex={};self.counts=Counter()
        for name,items in self.registry.items():self.rindex[name]=self.indexed(items,KEYS[name],name)
        for name,items in self.rows.items():
            key='coverage_id' if name=='coverage' else ('signal_id' if name=='signals' else KEYS[name])
            self.index[name]=self.indexed(items,key,name)
        self.resolver=Registry().with_resources((s['$id'],Resource.from_contents(s)) for s in self.schemas.values())
        if check_hashes:
            release=read_json(self.root/'release.json')
            expected={str(p.relative_to(self.root)) for folder in ['registry','schemas','examples','fixtures'] for p in (self.root/folder).rglob('*') if p.is_file()}
            require(set(release['files'])==expected,'RELEASE_FILE_SET')
            for name,h in release['files'].items():require(digest((self.root/name).read_bytes())==h,'RELEASE_HASH:'+name)
    @staticmethod
    def indexed(items,key,name):
        require(len(items)==len({i[key] for i in items}),'DUPLICATE_ID:'+name)
        return {i[key]:i for i in items}
    def row(self,kind,key):
        require(key in self.index[kind],'DANGLING_'+kind+':'+str(key));return self.index[kind][key]
    def reg(self,kind,key):
        require(key in self.rindex[kind],'DANGLING_'+kind+':'+str(key));return self.rindex[kind][key]
    def shape(self,value,schema):
        s=self.schemas[schema] if isinstance(schema,str) else schema
        errors=list(Draft7Validator(s,format_checker=STRICT_FORMATS,registry=self.resolver).iter_errors(value))
        require(not errors,'SCHEMA:'+str(schema if isinstance(schema,str) else 'dispatched-value')+':'+('; '.join(e.message for e in errors[:3])))
        self.counts['schema_instances']+=1
    def artifact_lineage(self,aid,seen=None):
        seen=set() if seen is None else set(seen)
        require(aid not in seen,'ARTIFACT_PROVENANCE_CYCLE');seen.add(aid)
        artifact=self.row('artifacts',aid);ids={aid}
        if artifact['parent_artifact_id']:ids |= self.artifact_lineage(artifact['parent_artifact_id'],seen)
        return ids
    def roots(self,fid,seen=None):
        seen=set() if seen is None else set(seen)
        require(fid not in seen,'PROVENANCE_CYCLE');seen.add(fid)
        f=self.row('facts',fid);e=self.row('evidence',f['evidence_id'])
        roots=set()
        if f['binding_id']:
            binding=self.row('bindings',f['binding_id'])
            require(binding['tenant_id']==f['tenant_id'] and binding['subject_id']==f['subject_id'],'BINDING_LINEAGE_OWNER')
            for aid in binding['artifact_ids']:roots |= self.artifact_lineage(aid)
            for lid in binding['evidence_locator_ids']:
                roots |= self.artifact_lineage(self.row('locators',lid)['artifact_id'])
        for l in e['locator_ids']:roots |= self.artifact_lineage(self.row('locators',l)['artifact_id'])
        for parent in e['input_fact_ids']:roots |= self.roots(parent,seen)
        # Numerator, denominator, exclusions and retained producer inputs all count.
        for sid in e.get('sample_ids',[]):
            for aid in self.row('samples',sid)['retrieved_artifact_ids']:roots |= self.artifact_lineage(aid)
        if f['execution_id']:
            ex=self.row('executions',f['execution_id'])
            for aid in ex['input_artifact_ids']:roots |= self.artifact_lineage(aid)
            if ex['model_call_id']:
                call=self.row('model-calls',ex['model_call_id'])
                for aid in [call['request_artifact_id'],call['response_artifact_id']]:
                    if aid:roots |= self.artifact_lineage(aid)
                for repair in self.rows['repairs']:
                    if repair['call_id']==call['call_id']:roots |= self.artifact_lineage(repair['output_response_artifact_id'])
        return roots
    def corroborating_artifacts(self,fid,seen=None):
        """Evidence leaves, not model I/O, processing requests, or denominators.

        Full provenance still uses roots(). Statistical eligibility still depends
        on the complete sample. Neither is an independence estimate.
        """
        seen=set() if seen is None else set(seen)
        require(fid not in seen,'PROVENANCE_CYCLE');seen.add(fid)
        f=self.row('facts',fid);e=self.row('evidence',f['evidence_id'])
        transcripts={a for c in self.rows['model-calls'] for a in (c['request_artifact_id'],c['response_artifact_id']) if a}
        transcripts|={r['output_response_artifact_id'] for r in self.rows['repairs']}
        out=set()
        for lid in e['locator_ids']:
            aid=self.row('locators',lid)['artifact_id'];visited=set()
            while aid:
                require(aid not in visited,'ARTIFACT_PROVENANCE_CYCLE');visited.add(aid)
                artifact=self.row('artifacts',aid)
                if artifact['parent_artifact_id']: aid=artifact['parent_artifact_id']
                else:
                    if aid not in transcripts:out.add(aid)
                    break
        for parent in e['input_fact_ids']:out|=self.corroborating_artifacts(parent,seen)
        return out

    def ancestry(self,fid,seen=None):
        seen=set() if seen is None else set(seen)
        require(fid not in seen,'PROVENANCE_CYCLE');seen.add(fid)
        f=self.row('facts',fid);e=self.row('evidence',f['evidence_id']);out={fid}
        for parent in e['input_fact_ids']:out |= self.ancestry(parent,seen)
        return out
    def policy_allows(self,pid,purpose,at,production=False,tenant=None):
        p=self.reg('policies',pid)
        if tenant is not None and tenant not in p['tenant_ids']:return False
        if any(c['kind']=='POLICY_REVOCATION' and c['target_id']==pid and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==tenant):return False
        return p['review_status']=='APPROVED' and purpose in p['purposes'] and instant(p['reviewed_at'])<=instant(at)<instant(p['valid_until']) and (not production or not p['fixture_only'])
    def usable(self,fid,at,*,purpose='INTERNAL_RESEARCH',production=False,allow_absence=False):
        """Primitive evidence eligibility. Supersession belongs to resolve_claim over an explicit input group."""
        f=self.row('facts',fid)
        if f['state']=='UNKNOWN' or (f['state']=='NOT_FOUND' and not allow_absence):return False
        for change in self.authorized_changes(at):
            if change['tenant_id']!=f['tenant_id']:continue
            if instant(change['effective_at'])<=instant(at) and change['target_id'] in (fid,f['source_id'],f['binding_id']):return False
        for aid in self.roots(fid):
            a=self.row('artifacts',aid);s=self.reg('sources',a['source_id'])
            if a['status']!='OK' or s['authority']!='ACTIVE':return False
            if a['retention_state']!='RETAINED' or instant(a['retained_until'])<=instant(at):return False
            if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
            if a['classification']=='SENSITIVE':return False
            if any(c['target_id']==aid and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
        for parent in self.ancestry(fid):
            x=self.row('facts',parent);s=self.reg('sources',x['source_id'])
            if x['state']=='UNKNOWN' or instant(x['observed_at'])>instant(at) or instant(x['expires_at'])<=instant(at):return False
            if s['authority']!='ACTIVE' or (production and s['fixture_only']):return False
            if any(c['target_id'] in (parent,x['source_id'],x['binding_id']) and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
            if not self.policy_allows(s['policy_id'],purpose,at,production,tenant=f['tenant_id']):return False
            if x['predicate_id']=='technology.footprint' and x['state']=='OBSERVED':
                fp=self.reg('fingerprints',x['object']['fingerprint_id'])
                if fp['authority']!='ACTIVE' or (production and fp['fixture_only']):return False
                if any(c['target_id']==fp['fingerprint_id'] and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
            if x['binding_id']:
                b=self.row('bindings',x['binding_id'])
                if b['status']!='ACCEPTED' or b['role'] in ['AGENCY','MENTION_ONLY','UNRESOLVED']:return False
            if x['execution_id']:
                ex=self.row('executions',x['execution_id']);fn=self.reg('functions',ex['function_id'])
                if ex['status']!='COMPLETE':return False
                if instant(ex['finished_at'])>instant(x['recorded_at']):return False
                if fn['authority']!='ACTIVE' or (production and fn['fixture_only']):return False
                if any(c['target_id']==fn['function_id'] and instant(c['effective_at'])<=instant(at) for c in self.authorized_changes(at) if c['tenant_id']==f['tenant_id']):return False
                if ex['model_call_id']:
                    call=self.row('model-calls',ex['model_call_id'])
                    if call['status']!='PARSED' or call['response_artifact_id'] is None:return False
                    repairs=sorted([r for r in self.rows['repairs'] if r['call_id']==call['call_id']],key=lambda r:r['ordinal'])
                    if len(repairs)>call['max_repair_attempts'] or (repairs and repairs[-1]['status']!='VALID'):return False
                    for aid in [call['request_artifact_id'],call['response_artifact_id']]:
                        artifact=self.row('artifacts',aid)
                        if artifact['retention_state']!='RETAINED' or instant(artifact['retained_until'])<=instant(at):return False
        return True
    def evidence_text(self,evidence):
        return '\n'.join(self.locator_text(self.row('locators',lid)) for lid in evidence['locator_ids'])
    def locator_text(self,l):
        a=self.row('artifacts',l['artifact_id'])
        if a['retention_state']!='RETAINED':return ''
        raw=(self.root/a['content_ref']).read_bytes()
        try:body=raw.decode('utf-8')
        except UnicodeDecodeError:
            require(l['kind']=='WHOLE_ARTIFACT' and l['quote'] is None and l['start'] is None and l['end'] is None and l['pointer'] is None,'BINARY_LOCATOR_REQUIRES_EXTRACTED_TEXT')
            return ''
        if l['kind']=='TEXT_SPAN':
            require(l['start'] is not None and l['end'] is not None and 0<=l['start']<l['end']<=len(body),'INVALID_TEXT_SPAN')
            text=body[l['start']:l['end']]
            require(l['pointer'] is None,'TEXT_POINTER_CONFLICT')
        elif l['kind']=='JSON_POINTER':
            require(l['pointer'] is not None and l['start'] is None and l['end'] is None,'JSON_LOCATOR_SHAPE')
            value=pointer(read_json(self.root/a['content_ref']),l['pointer']);text=value if isinstance(value,str) else canonical(value).decode()
        else:
            require(l['start'] is None and l['end'] is None and l['pointer'] is None,'WHOLE_LOCATOR_SHAPE');text=body
        if l['quote'] is not None:require(l['quote']==text,'EVIDENCE_QUOTE_MISMATCH')
        return text
    def render(self,pkg):
        self.validate_package_dependencies(pkg)
        t=self.reg('templates',pkg['template_id'])
        require(len(pkg['clauses'])==1,'REFERENCE_RENDERER_ONE_CLAUSE')
        c=pkg['clauses'][0];require(c['template_id']==t['template_id'] and len(c['fact_ids'])==1,'TEMPLATE_CLAUSE_BINDING')
        f=self.row('facts',c['fact_ids'][0]);p=self.reg('predicates',f['predicate_id'])
        require(f['subject_id']==pkg['subject_id'] and f['tenant_id']==pkg['tenant_id'],'CROSS_ACCOUNT_COPY')
        require(f['predicate_id']==t['required_predicate'] and f['nature'] in t['allowed_natures'],'COPY_PREDICATE_OR_NATURE')
        at=pkg['approved_at'] or self.row('runs',pkg['run_id'])['as_of']
        require(self.usable(f['fact_id'],at,purpose='OUTREACH',production=pkg['status']=='APPROVED',allow_absence=t['renderer']=='scoped_absence_v1'),'COPY_INELIGIBLE_EVIDENCE')
        require(p['copy_policy'] not in ['INTERNAL_ONLY','CONTEXT_ONLY'],'INTERNAL_COPY_LEAK')
        natures={self.row('facts',i)['nature'] for i in self.ancestry(f['fact_id'])}
        require('INFERENCE' not in natures,'INFERRED_ANCESTRY_COPY_LEAK')
        if t['renderer']=='observed_product_v1':
            require(f['state']=='OBSERVED' and f['nature']=='DIRECT_OBSERVATION','NOT_DIRECT_TECHNOLOGY')
            product=self.row('subjects',f['object']['product_id'])
            clause=f"I noticed a {product['display_name']} embed on your site."
            require(c['evidence_roles']==['DIRECT'],'COPY_QUALIFIER')
        elif t['renderer']=='attributed_job_statement_v1':
            require(f['state']=='OBSERVED' and f['nature']=='FIRST_PARTY_STATEMENT','NOT_ATTRIBUTED_STATEMENT')
            require(f['object']['modality'] in ['CURRENT_STATE','REQUIREMENT'],'UNSUPPORTED_STATEMENT_MODALITY')
            clause=f'Your job posting states: “{f["object"]["text"]}”'
            require(c['evidence_roles']==['ATTRIBUTED'],'COPY_QUALIFIER')
        else:
            require(f['state']=='NOT_FOUND','ABSENCE_REQUIRED')
            scope=self.row('scopes',f['scope_id'])
            clause=f"In the captured page sample ({scope['population_description']}), the configured detector did not find the specified form surface."
            require(c['evidence_roles']==['SCOPED_ABSENCE'],'COPY_QUALIFIER')
        require(c['text']==clause,'UNSUPPORTED_FIXED_CLAUSE')
        return clause+' '+t['question']

    def validate(self):
        for name,s in self.schemas.items():Draft7Validator.check_schema(s)
        for name,items in self.registry.items():
            for item in items:self.shape(item,REGISTRY_TYPES[name])
        for name,items in self.rows.items():
            for item in items:self.shape(item,ROW_TYPES[name])
        # Validate the global relation before any eligibility traversal.
        stable_order(self.index['facts'],[(f['supersedes_fact_id'],f['fact_id'])
            for f in self.rows['facts'] if f['supersedes_fact_id']])
        self.validate_completion()
        for p in self.registry['predicates']:
            for key in ['target_schema','value_schema']:Draft7Validator.check_schema(p[key])
            self.shape(p['example_target'],p['target_schema']);self.shape(p['example_value'],p['value_schema'])
            require(not (p['absence_allowed'] and p['allowed_natures']==['INFERENCE']),'INFERRED_ABSENCE_FORBIDDEN')
        for m in self.registry['metrics']:
            Draft7Validator.check_schema(m['dimensions_schema']);Draft7Validator.check_schema(m['value_schema'])
        for c in self.registry['coverage']:
            for p in c['predicate_ids']:self.reg('predicates',p)
            for m in c['metric_ids']:self.reg('metrics',m)
        require(set(self.rindex['coverage'])==set(range(1,12)),'MISSING_DOMAIN_COVERAGE')
        for t in self.registry['taxonomy']:
            if t['parent_id']:self.reg('taxonomy',t['parent_id'])
        stable_order(self.rindex['taxonomy'],[(x['parent_id'],x['term_id']) for x in self.registry['taxonomy'] if x['parent_id']])
        for fp in self.registry['fingerprints']:
            product=self.row('subjects',fp['product_subject_id']);require(product['kind']=='SOFTWARE_PRODUCT','FINGERPRINT_PRODUCT_KIND')
            self.reg('predicates',fp['emits'])
            if fp['implementation_status']=='REFERENCE_IMPLEMENTED':
                for paths,expected in [(fp['positive_fixtures'],True),(fp['negative_fixtures'],False)]:
                    for path in paths:
                        p=(self.root/path).resolve();require(p.is_relative_to(self.root.resolve()) and p.is_file(),'FINGERPRINT_FIXTURE_PATH')
                        require(matches_fingerprint(fp,p.read_text())==expected,'FINGERPRINT_FIXTURE_RESULT')
        for s in self.registry['sources']:
            self.reg('policies',s['policy_id'])
            for p in s['emits']:self.reg('predicates',p)
        for fn in self.registry['functions']:
            for p in fn['input_predicates']+fn['output_predicates']:self.reg('predicates',p)
            require(fn['implementation_status']!='REFERENCE_IMPLEMENTED' or fn['entrypoint'] is not None,'MISSING_FUNCTION_ENTRYPOINT')
        for s in self.registry['signals']:
            self.reg('functions',s['function_id'])
            for r in s['required_facts']:
                p=self.reg('predicates',r['predicate_id'])
                require(set(r['allowed_natures'])<=set(p['allowed_natures']),'SIGNAL_NATURE_DECLARATION')
                require(r['state']!='NOT_FOUND' or p['absence_allowed'],'SIGNAL_UNSUPPORTED_ABSENCE')
        for t in self.registry['templates']:
            self.reg('predicates',t['required_predicate'])
            require((t['mode']=='MATURITY_OFFER')==t['maturity_required'],'MATURITY_MODE_MISMATCH')
            require(t['mode']!='OBSERVATION_QUESTION' or t['offered_rung'] is None,'UNSUPPORTED_UNIVERSAL_MATURITY')
        for rule in self.registry['context-rules']:
            self.reg('predicates',rule['link_predicate']);p=self.reg('predicates',rule['context_predicate'])
            require(p['copy_policy']=='CONTEXT_ONLY','RESEARCH_CONTEXT_POLICY')
        for profile in self.registry['profiles']:
            for k,reg in [('capture_source_ids','sources'),('fact_predicate_ids','predicates'),('execute_function_ids','functions'),('signal_ids','signals'),('template_ids','templates')]:
                for i in profile[k]:self.reg(reg,i)
            funcs=[self.reg('functions',i) for i in profile['execute_function_ids']]
            for fn in funcs:
                require(fn['implementation_status']=='REFERENCE_IMPLEMENTED','ENABLED_FUNCTION_UNIMPLEMENTED')
                require(set(fn['input_predicates']+fn['output_predicates'])<=set(profile['fact_predicate_ids']),'PROFILE_DEPENDENCY_CLOSURE')
            edges=[(a['function_id'],b['function_id']) for a in funcs for b in funcs if set(a['output_predicates'])&set(b['input_predicates'])]
            stable_order([f['function_id'] for f in funcs],edges)
            for sid in profile['signal_ids']:
                require(self.reg('signals',sid)['function_id'] in profile['execute_function_ids'],'SIGNAL_FUNCTION_NOT_ENABLED')
            require(not profile['production_enabled'],'PRODUCTION_NOT_IMPLEMENTED')
            for sid in profile['capture_source_ids']:require(self.reg('sources',sid)['adapter_status']!='DESIGN_ONLY','ENABLED_ADAPTER_UNIMPLEMENTED')
        for s in self.rows['scopes']:
            sub=self.row('subjects',s['subject_id']);require(sub['tenant_id']==s['tenant_id'],'SCOPE_TENANT')
        for a in self.rows['artifacts']:
            s=self.reg('sources',a['source_id']);scope=self.row('scopes',a['scope_id']);pol=self.reg('policies',s['policy_id'])
            require(a['tenant_id']==scope['tenant_id'],'ARTIFACT_TENANT');require(a['resource_uri'] in scope['resources'],'ARTIFACT_RESOURCE_SCOPE')
            if a['retention_state']=='RETAINED':
                require(a['content_ref'] is not None,'MISSING_RETAINED_CONTENT')
                path=(self.root/a['content_ref']).resolve();require(path.is_relative_to(self.root.resolve()),'CONTENT_PATH_ESCAPE')
                require(path.is_file(),'CONTENT_MISSING');data=path.read_bytes()
                require(len(data)==a['byte_count'] and digest(data)==a['content_hash'],'CONTENT_HASH_OR_SIZE')
                require(self.policy_allows(s['policy_id'],'CAPTURE',a['captured_at'],tenant=a['tenant_id']) and self.policy_allows(s['policy_id'],'RETAIN',a['captured_at'],tenant=a['tenant_id']),'SOURCE_CAPTURE_OR_RETENTION_DENIED')
                require(instant(a['retained_until'])<=min(instant(a['captured_at'])+timedelta(seconds=pol['max_raw_retention_seconds']),instant(pol['valid_until'])),'RETENTION_EXCEEDS_POLICY')
            else:require(a['content_ref'] is None,'DELETED_OR_REFERENCE_CONTENT_STILL_PRESENT')
            require(a['classification']!='SENSITIVE' or pol['allow_sensitive_data'],'SENSITIVE_DATA_DENIED')
            require(a['classification']!='PERSONAL' or pol['allow_personal_data'],'PERSONAL_DATA_DENIED')
            if a['parent_artifact_id']:
                parent=self.row('artifacts',a['parent_artifact_id']);require(parent['tenant_id']==a['tenant_id'],'DERIVED_ARTIFACT_TENANT')
                require((a['origin_namespace'],a['origin_record_id'],a['independence_group'])==(parent['origin_namespace'],parent['origin_record_id'],parent['independence_group']),'TRANSFORMED_ARTIFACT_ORIGIN_CHANGED')
        stable_order(self.index['artifacts'],[(a['parent_artifact_id'],a['artifact_id']) for a in self.rows['artifacts'] if a['parent_artifact_id']])
        for l in self.rows['locators']:self.row('artifacts',l['artifact_id']);self.locator_text(l)
        for b in self.rows['bindings']:
            sub=self.row('subjects',b['subject_id']);scope=self.row('scopes',b['scope_id'])
            require(sub['tenant_id']==b['tenant_id']==scope['tenant_id'] and scope['subject_id']==sub['subject_id'],'BINDING_SUBJECT_OR_TENANT')
            for aid in b['artifact_ids']:require(self.row('artifacts',aid)['scope_id']==scope['scope_id'],'BINDING_ARTIFACT_SCOPE')
            require(all(self.row('locators',l)['artifact_id'] in b['artifact_ids'] for l in b['evidence_locator_ids']),'BINDING_LOCATOR_OUTSIDE_ARTIFACT')
        for c in self.rows['coverage']:
            scope=self.row('scopes',c['scope_id']);source=self.reg('sources',c['source_id'])
            require(c['tenant_id']==scope['tenant_id'],'COVERAGE_TENANT')
            require(set(c['planned_resources'])==set(scope['resources']),'COVERAGE_SCOPE_EXPANSION')
            require(len(c['checked'])==len({x['resource'] for x in c['checked']}),'DUPLICATE_COVERAGE_RESOURCE')
            for pid in c['predicate_ids']:
                p=self.reg('predicates',pid);require(pid in source['emits'],'COVERAGE_SOURCE_PREDICATE');self.shape(c['target'],p['target_schema'])
            if c['status']=='COMPLETE':
                require({x['resource'] for x in c['checked']}==set(c['planned_resources']),'INCOMPLETE_COVERAGE')
                for x in c['checked']:
                    require(x['result']=='OK' and x['artifact_id'] is not None,'INCOMPLETE_COVERAGE')
                    a=self.row('artifacts',x['artifact_id'])
                    require(a['scope_id']==c['scope_id'] and a['source_id']==c['source_id'] and a['resource_uri']==x['resource'],'COVERAGE_ARTIFACT_MISMATCH')
                    require(a['status']=='OK' and not a['truncated'],'TRUNCATED_COVERAGE')
        for e in self.rows['evidence']:
            require(e['locator_ids'] or e['input_fact_ids'] or e['attempt_id'],'EMPTY_EVIDENCE')
            if e['attempt_id']:
                a=self.row('attempts',e['attempt_id']);self.validate_attempt(a)
                require(a['tenant_id']==e['tenant_id'] and a['status'] not in ['SUCCEEDED','EMPTY_RESULT'],'DIAGNOSTIC_ATTEMPT_INVALID')
                require(e['directness']=='DIAGNOSTIC' and not e['locator_ids'] and not e['input_fact_ids'] and not e['sample_ids'] and e['execution_id'] is None and e['coverage_id'] is None,'DIAGNOSTIC_EVIDENCE_IS_NOT_PROOF')
            else:require(e['directness']!='DIAGNOSTIC','DIAGNOSTIC_WITHOUT_ATTEMPT')
            for lid in e['locator_ids']:
                a=self.row('artifacts',self.row('locators',lid)['artifact_id']);require(a['tenant_id']==e['tenant_id'],'EVIDENCE_TENANT')
            for fid in e['input_fact_ids']:require(self.row('facts',fid)['tenant_id']==e['tenant_id'],'EVIDENCE_PARENT_TENANT')
            if e['execution_id']:self.row('executions',e['execution_id'])
            if e['coverage_id']:self.row('coverage',e['coverage_id'])
            require((e['directness']=='DERIVED')==bool(e['input_fact_ids']),'EVIDENCE_DIRECTNESS')
        edges=[(parent,f['fact_id']) for f in self.rows['facts'] for parent in self.row('evidence',f['evidence_id'])['input_fact_ids']]
        stable_order(self.index['facts'],edges)
        for run in self.rows['runs']:
            require(run['registry_release']==digest(self.registry),'RUN_REGISTRY_PIN_MISMATCH')
            require(run['code_release']==code_digest(self.root),'RUN_CODE_PIN_MISMATCH')
            prof=self.reg('profiles',run['profile_id']);require(run['mode']!='PRODUCTION' or prof['production_enabled'],'PRODUCTION_DISABLED')
            for kind,key in [('artifacts','input_artifact_ids'),('facts','input_fact_ids'),('bindings','binding_ids')]:
                for i in run[key]:require(self.row(kind,i)['tenant_id']==run['tenant_id'],'RUN_INPUT_TENANT')
        for ex in self.rows['executions']:
            fn=self.reg('functions',ex['function_id']);run=self.row('runs',ex['run_id']);self.shape(ex['parameters'],fn['parameter_schema'])
            require(ex['function_version']==fn['version'],'FUNCTION_VERSION_MISMATCH')
            require(ex['tenant_id']==run['tenant_id']==self.row('subjects',ex['subject_id'])['tenant_id'],'EXECUTION_TENANT')
            require(instant(ex['started_at'])<=instant(ex['finished_at']),'EXECUTION_TIME')
            require(ex['input_set_hash']==digest({'facts':sorted(ex['input_fact_ids']),'artifacts':sorted(ex['input_artifact_ids'])}),'EXECUTION_INPUT_HASH')
            for fid in ex['input_fact_ids']:
                f=self.row('facts',fid);require(f['predicate_id'] in fn['input_predicates'],'UNDECLARED_FUNCTION_INPUT')
                require(f['tenant_id']==ex['tenant_id'],'EXECUTION_INPUT_TENANT')
                require(instant(f['recorded_at'])<=instant(ex['started_at']),'UNRECORDED_EXECUTION_INPUT')
                require(f['subject_id']==ex['subject_id'],'UNDECLARED_CROSS_SUBJECT_DERIVATION')
                require(fid in run['input_fact_ids'] or (f['run_id']==run['run_id'] and f['execution_id'] is not None),'INPUT_OUTSIDE_RUN')
                if f['execution_id']:
                    pex=self.row('executions',f['execution_id']);require(instant(pex['finished_at'])<=instant(ex['started_at']),'FORWARD_EXECUTION_DEPENDENCY')
            for aid in ex['input_artifact_ids']:self.assert_artifact_available(aid,run,ex['started_at'],consumer_id=ex['execution_id'])
            for fid in ex['output_fact_ids']:
                f=self.row('facts',fid);require(f['execution_id']==ex['execution_id'] and f['subject_id']==ex['subject_id'],'EXECUTION_OUTPUT_LINK')
                require(f['predicate_id'] in fn['output_predicates'],'UNDECLARED_FUNCTION_OUTPUT')
            if fn['processor']=='LLM':require(ex['model_call_id'] is not None,'UNJOURNALED_MODEL_CALL');self.row('model-calls',ex['model_call_id'])
        for f in self.rows['facts']:self.validate_fact(f)
        for sample in self.rows['samples']:self.validate_sample(sample)
        for f in self.rows['facts']:
            if f['state']=='OBSERVED' and f['predicate_id'] in ['product.pain_prior','industry.pain_prior','review.theme_summary']:self.validate_prior(f)
        for c in self.rows['contexts']:self.validate_context(c)
        for mc in self.rows['model-calls']:
            req=self.row('artifacts',mc['request_artifact_id'])
            resp=self.row('artifacts',mc['response_artifact_id']) if mc['response_artifact_id'] else None
            require(req['tenant_id']==mc['tenant_id'] and (resp is None or resp['tenant_id']==mc['tenant_id']),'MODEL_CALL_TENANT')
            require(resp is not None or mc['status']!='PARSED','PARSED_WITHOUT_RESPONSE')
            require(mc['prompt_hash']==req['content_hash'],'MODEL_REQUEST_PIN_MISMATCH')
            for aid in mc['input_artifact_ids']:
                a=self.row('artifacts',aid);s=self.reg('sources',a['source_id'])
                require(a['tenant_id']==mc['tenant_id'],'MODEL_INPUT_TENANT')
                require(s['policy_id'] in mc['policy_ids'] and self.policy_allows(s['policy_id'],'LLM_PROCESS',req['captured_at'],tenant=mc['tenant_id']),'MODEL_PROCESSING_DENIED')
            attempts=sorted([a for a in self.rows['repairs'] if a['call_id']==mc['call_id']],key=lambda a:a['ordinal'])
            require([a['ordinal'] for a in attempts]==list(range(1,len(attempts)+1)) and len(attempts)<=mc['max_repair_attempts'],'REPAIR_BOUND_OR_SEQUENCE')
            previous=mc['response_artifact_id']
            for a in attempts:
                require(previous is not None and a['input_response_artifact_id']==previous,'REPAIR_CHAIN');out=self.row('artifacts',a['output_response_artifact_id']);previous=a['output_response_artifact_id']
                require(out['tenant_id']==mc['tenant_id'],'REPAIR_OUTPUT_TENANT')
            require(mc['output_schema_id'] in self.schemas,'MODEL_OUTPUT_SCHEMA_MISSING')
            if mc['status']=='PARSED':
                final=self.row('artifacts',previous)
                require(final['retention_state']=='RETAINED' and final['content_ref'] is not None,'MODEL_RESPONSE_UNAVAILABLE')
                self.shape(read_json(self.root/final['content_ref']),mc['output_schema_id'])
                require(not attempts or attempts[-1]['status']=='VALID','PARSED_MODEL_WITH_INVALID_REPAIR')
                if mc['output_schema_id']=='QuotedTextResult':
                    text=read_json(self.root/final['content_ref'])['text']
                    for ex in self.rows['executions']:
                        if ex['model_call_id']==mc['call_id'] and ex['status']=='COMPLETE':
                            for fid in ex['output_fact_ids']:require(self.row('facts',fid)['object'].get('text')==text,'MODEL_OUTPUT_NOT_USED')
                require(mc['terminal_reason'] is None,'PARSED_MODEL_WITH_FAILURE_REASON')
            else:require(mc['terminal_reason'] is not None,'MODEL_FAILURE_WITHOUT_REASON')
        for s in self.rows['signals']:
            definition=self.reg('signals',s['signal_type_id']);run=self.row('runs',s['run_id'])
            require(s['tenant_id']==run['tenant_id'],'SIGNAL_TENANT')
            if s['status']=='RESOLVED':require(s['reason'] is None and bool(s['input_fact_ids']),'RESOLVED_SIGNAL_INVALID')
            if s['status']=='UNRESOLVED':require(s['reason'] in ['THIN_DATA','CONFLICT','POLICY'],'UNRESOLVED_REASON')
            if s['status']=='SUPPRESSED':require(s['reason']=='DNC','SUPPRESSION_REASON')
            if s['status']=='CANDIDATE':require(s['reason']=='CANDIDATE_SOURCE','CANDIDATE_REASON')
            for fid in s['input_fact_ids']:
                f=self.row('facts',fid);require(f['subject_id']==s['subject_id'] and f['tenant_id']==s['tenant_id'],'CROSS_ACCOUNT_SIGNAL')
            for cid in s['context_ids']:
                c=self.row('contexts',cid);require(definition['context_allowed'] and c['account_subject_id']==s['subject_id'],'UNDECLARED_SIGNAL_CONTEXT')
            if s['status']=='RESOLVED':
                verdict=evaluate_requirements(definition,[self.row('facts',fid) for fid in s['input_fact_ids']],
                    s['subject_id'],run['as_of'],
                    lambda fid,at,**kw:self.decision_eligible(fid,at,run_id=run['run_id'],**kw),
                    substantive_origins=lambda fid:distinct_origins(self.row('artifacts',a) for a in self.corroborating_artifacts(fid)))
                require(verdict=='RESOLVED','SIGNAL_REQUIREMENT_UNSATISFIED')
        for p in self.rows['packages']:
            self.row('subjects',p['subject_id']);run=self.row('runs',p['run_id']);t=self.reg('templates',p['template_id'])
            require(p['tenant_id']==run['tenant_id'],'PACKAGE_TENANT')
            for sid in p['signal_ids']:
                s=self.row('signals',sid);require(s['subject_id']==p['subject_id'] and s['status']=='RESOLVED','PACKAGE_SIGNAL_ELIGIBILITY')
            for cid in p['context_ids']:require(self.row('contexts',cid)['account_subject_id']==p['subject_id'],'PACKAGE_CONTEXT_TARGET')
            if p['status'] in ['APPROVED','DESIGN_TEST_APPROVED']:
                require(p['approved_at'] is not None and t['authority']=='ACTIVE','MISSING_APPROVAL')
                require(p['status']!='APPROVED' or run['mode']=='PRODUCTION','FIXTURE_IS_NOT_PRODUCTION')
                require(all(instant(self.row('facts',fid)['recorded_at'])<=instant(p['approved_at']) for clause in p['clauses'] for rootfid in clause['fact_ids'] for fid in self.ancestry(rootfid)),'APPROVAL_PRECEDES_EVIDENCE')
                require(p['rendered_text']==self.render(p),'UNSUPPORTED_RENDERED_COPY')
                # Mature offers are contracted, but deliberately fail closed until a renderer exists.
                require(t['mode']=='OBSERVATION_QUESTION','MATURITY_OFFER_NOT_IMPLEMENTED')
                require(p['maturity_fact_id'] is None,'UNNECESSARY_MATURITY_DEPENDENCY')
        for change in self.rows['changes']:self.validate_change(change)
        for resolution in self.rows['resolutions']:
            self.reg('predicates',resolution['predicate_id'])
            fs=[self.row('facts',fid) for fid in resolution['observation_ids']]
            require(len({claim_key(f) for f in fs})==1,'RESOLUTION_MIXED_KEYS')
            require(all(f['tenant_id']==resolution['tenant_id'] and f['subject_id']==resolution['subject_id'] and f['predicate_id']==resolution['predicate_id'] and f['scope_id']==resolution['scope_id'] and f['target']==resolution['target'] for f in fs),'RESOLUTION_IDENTITY')
            expected=resolve_claim(fs,resolution['as_of'],lambda f,at:self.usable(f['fact_id'],at,allow_absence=True))
            require(expected['status']==resolution['status'] and expected['accepted_fact_ids']==sorted(resolution['accepted_fact_ids']),'RESOLUTION_POLICY_MISMATCH')
        for exposure in self.rows['exposures']:
            pkg=self.row('packages',exposure['package_id']);require(pkg['tenant_id']==exposure['tenant_id'],'EXPOSURE_TENANT')
            if exposure['status'] in ['PROVIDER_ACCEPTED','BOUNCED']:require(exposure['accepted_at'] is not None and exposure['provider_message_id'] is not None,'EXPOSURE_ACCEPTANCE_MISSING')
            if exposure['status']=='UNKNOWN_DELIVERY':require(exposure['accepted_at'] is None,'UNCERTAIN_DELIVERY_NOT_ACCEPTED')
        require(len(self.rows['exposures'])==len({(x['tenant_id'],x['business_send_key']) for x in self.rows['exposures']}),'DUPLICATED_EXPOSURE')
        for cal in self.rows['calibrations']:
            denom=cal['true_positives']+cal['false_positives']
            require(denom>0 and abs(cal['measured_precision']-cal['true_positives']/denom)<1e-9,'INVALID_CALIBRATION_RATE')
        for candidate in self.rows['candidates']:
            require(candidate['artifact_id'] is not None or candidate['attempt_id'] is not None,'CANDIDATE_WITHOUT_ORIGIN')
            if candidate['artifact_id']:
                a=self.row('artifacts',candidate['artifact_id']);require(a['tenant_id']==candidate['tenant_id'],'CANDIDATE_TENANT')
            if candidate['attempt_id']:
                a=self.row('attempts',candidate['attempt_id']);require(a['tenant_id']==candidate['tenant_id'],'CANDIDATE_TENANT')
        for o in self.rows['outcomes']:
            require((o['attribution_status']=='MATCHED')==(o['exposure_id'] is not None),'OUTCOME_ATTRIBUTION')
            if o['exposure_id']:require(self.row('exposures',o['exposure_id'])['tenant_id']==o['tenant_id'],'OUTCOME_TENANT')
        require(len(self.rows['outcomes'])==len({(o['tenant_id'],o['provider'],o['provider_event_id']) for o in self.rows['outcomes']}),'DUPLICATE_PROVIDER_EVENT')
        self.validate_handoffs()
        return {'status':'PASS','schemas':len(self.schemas),'predicates':len(self.registry['predicates']),'metrics':len(self.registry['metrics']),
                'records':sum(map(len,self.rows.values())),'counts':dict(self.counts)}

    def validate_fact(self,f):
        p=self.reg('predicates',f['predicate_id']);s=self.reg('sources',f['source_id']);scope=self.row('scopes',f['scope_id']);sub=self.row('subjects',f['subject_id']);run=self.row('runs',f['run_id']);e=self.row('evidence',f['evidence_id'])
        # A no-byte failure records our own attempt metadata, not derivative vendor content.
        rights_sources=set() if e['attempt_id'] and f['state']=='UNKNOWN' else {f['source_id']}|{self.row('artifacts',aid)['source_id'] for aid in self.roots(f['fact_id'])}
        for source_id in rights_sources:
            pol=self.reg('policies',self.reg('sources',source_id)['policy_id'])
            require(self.policy_allows(pol['policy_id'],'DERIVE',f['recorded_at'],tenant=f['tenant_id']),'DERIVATION_RIGHTS_DENIED')
            require(instant(f['expires_at'])<=instant(f['recorded_at'])+timedelta(seconds=pol['max_derived_retention_seconds']),'DERIVED_RETENTION_EXCEEDED')
        require(f['tenant_id']==scope['tenant_id']==sub['tenant_id']==run['tenant_id']==e['tenant_id'],'FACT_TENANT')
        require(scope['subject_id']==f['subject_id'] and sub['kind'] in p['subject_kinds'],'FACT_SUBJECT_SCOPE')
        require(f['predicate_id'] in s['emits'],'SOURCE_CANNOT_EMIT');require(f['nature'] in p['allowed_natures'] and f['nature'] in s['allowed_natures'],'UNSUPPORTED_EPISTEMIC_KIND')
        self.shape(f['target'],p['target_schema'])
        require(instant(f['observed_at'])<=instant(f['recorded_at']) and instant(f['observed_at'])<=instant(run['as_of']),'FACT_TIME')
        require(f['execution_id']==e['execution_id'],'FACT_EXECUTION_EVIDENCE_MISMATCH')
        if e['attempt_id']:
            a=self.row('attempts',e['attempt_id']);self.validate_attempt(a)
            require(f['state']=='UNKNOWN' and f['object'] is None and e['directness']=='DIAGNOSTIC','ATTEMPT_CANNOT_PROVE_BUSINESS_FACT')
            require(a['target']['subject_id']==f['subject_id'] and a['source_id']==f['source_id'] and a['scope_id']==f['scope_id'],'UNKNOWN_ATTEMPT_TARGET')
            require(f['observed_at']==a['finished_at'] and instant(a['finished_at'])<=instant(f['recorded_at']),'UNKNOWN_BEFORE_FAILURE')
            require(f['reason']=={'POLICY_DENIED':'POLICY_BLOCKED','TIMEOUT':'FETCH_FAILED','FAILED':'FETCH_FAILED','BUDGET_DENIED':'NOT_CHECKED','CANCELLED':'NOT_CHECKED','PARTIAL':'INSUFFICIENT_EVIDENCE'}.get(a['status']),'UNKNOWN_FAILURE_REASON')
        if f['execution_id']:
            ex=self.row('executions',f['execution_id']);fn=self.reg('functions',ex['function_id'])
            require(ex['status']=='COMPLETE' and instant(ex['finished_at'])<=instant(f['recorded_at']),'FAILED_OR_UNFINISHED_PRODUCER')
            if ex['model_call_id']:require(self.row('model-calls',ex['model_call_id'])['status']=='PARSED','FAILED_MODEL_PRODUCER')
            require(f['fact_id'] in ex['output_fact_ids'],'FACT_OUTPUT_BACKLINK');require(set(e['input_fact_ids'])==set(ex['input_fact_ids']),'PROVENANCE_INPUT_SET_MISMATCH')
            processor=fn['processor']
        else:processor='HUMAN_REVIEW' if s['acquisition_method']=='HUMAN_UPLOAD' else 'DETERMINISTIC'
        require(processor in p['allowed_processors'],'UNSUPPORTED_PROCESSOR')
        if f['nature'] in ['INFERENCE','DERIVED_MEASUREMENT']:require(f['execution_id'] is not None,'MISSING_DERIVATION')
        if f['confidence'] and f['confidence']['meaning']=='CALIBRATED_PRECISION':
            require(f['confidence']['calibration_id'] is not None,'UNCITED_CALIBRATION')
            cal=self.row('calibrations',f['confidence']['calibration_id'])
            require(f['confidence']['value']==cal['measured_precision'],'CALIBRATION_VALUE_MISMATCH')
        if f['supersedes_fact_id']:
            prior=self.row('facts',f['supersedes_fact_id'])
            require(claim_key(prior)==claim_key(f) and prior['source_id']==f['source_id'],'WRONG_SUPERSESSION_KEY')
            require(instant(prior['recorded_at'])<instant(f['recorded_at']),'INVALID_SUPERSESSION_ORDER')
            require(f['state']!='UNKNOWN' or prior['state']=='UNKNOWN','UNKNOWN_CANNOT_SUPERSEDE_KNOWN')
        if f['state']=='OBSERVED':self.shape(f['object'],p['value_schema'])
        require((p['temporal_mode']=='PERIOD')==(f['window'] is not None),'MISSING_OR_UNEXPECTED_PERIOD')
        if f['window']:require(instant(f['window']['start'])<instant(f['window']['end'])<=instant(run['as_of']),'INVALID_MEASUREMENT_WINDOW')
        if f['state']!='UNKNOWN' and e['directness']=='RAW':
            require(bool(e['locator_ids']) and f['binding_id'] is not None,'MISSING_RAW_PROVENANCE_OR_BINDING')
            b=self.row('bindings',f['binding_id'])
            require(b['scope_id']==f['scope_id'] and b['subject_id']==f['subject_id'],'WRONG_FACT_BINDING')
            for lid in e['locator_ids']:
                a=self.row('artifacts',self.row('locators',lid)['artifact_id'])
                require(a['scope_id']==f['scope_id'] and a['source_id']==f['source_id'],'RAW_SOURCE_OR_SCOPE_MISMATCH')
                require(a['status']=='OK','FAILED_CAPTURE_AS_OBSERVATION')
                require(a['artifact_id'] in run['input_artifact_ids'],'UNPINNED_RAW_ARTIFACT')
            require(instant(f['observed_at'])==max(instant(self.row('artifacts',self.row('locators',l)['artifact_id'])['captured_at']) for l in e['locator_ids']),'RAW_OBSERVATION_TIME_REFRESH')
        if e['directness']=='DERIVED':
            for fid in e['input_fact_ids']:
                parent=self.row('facts',fid);require(parent['subject_id']==f['subject_id'],'CROSS_SUBJECT_FACT_LAUNDERING')
            if e['input_fact_ids']:require(instant(f['expires_at'])<=min(instant(self.row('facts',i)['expires_at']) for i in e['input_fact_ids']),'DERIVED_FRESHNESS_LAUNDERING')
        require(instant(f['expires_at'])<=instant(f['observed_at'])+timedelta(seconds=s['freshness_seconds']),'SOURCE_TTL_EXCEEDED')
        if f['state']=='NOT_FOUND':
            require(p['absence_allowed'] and e['coverage_id'] is not None,'ABSENCE_NOT_SUPPORTED_OR_UNPROVEN')
            c=self.row('coverage',e['coverage_id'])
            self.validate_coverage_execution(c)
            require(instant(c['checked_at'])<=instant(f['recorded_at']),'ABSENCE_BEFORE_CHECK')
            require(f['execution_id']==c['detector_execution_id'],'ABSENCE_PRODUCER_MISMATCH')
            require(c['status']=='COMPLETE' and c['scope_id']==f['scope_id'] and c['source_id']==f['source_id'] and f['predicate_id'] in c['predicate_ids'] and c['target']==f['target'],'ABSENCE_COVERAGE_MISMATCH')
        if f['state']=='OBSERVED':
            for rr in p['reference_rules']:
                value=pointer(f[rr['container']],rr['path'])
                if value is None:continue
                ids=value if isinstance(value,list) else [value]
                typ=rr.get('target_type','SUBJECT');kind={'SUBJECT':'subjects','FACT':'facts','ARTIFACT':'artifacts','LOCATOR':'locators'}[typ]
                for sid in ids:
                    target=self.row(kind,sid)
                    tenant=target.get('tenant_id') if typ!='LOCATOR' else self.row('artifacts',target['artifact_id'])['tenant_id']
                    require(tenant==f['tenant_id'],'OBJECT_REFERENCE_TENANT')
                    if typ=='SUBJECT':require(target['kind'] in rr['subject_kinds'],'OBJECT_SUBJECT_REFERENCE')
                    if typ=='FACT':require(sid in e['input_fact_ids'],'OBJECT_FACT_REFERENCE_NOT_IN_LINEAGE')
                    if typ=='LOCATOR':require(target['artifact_id'] in self.roots(f['fact_id']),'LOCATOR_OUTSIDE_LINEAGE')
            o=f['object']
            if isinstance(o,dict):
                for field in set(o)&set(f['target']):require(o[field]==f['target'][field],'TARGET_VALUE_MISMATCH:'+field)
                for lo,hi in [('minimum_minor','maximum_minor'),('minimum','maximum')]:
                    if lo in o and hi in o and o[lo] is not None and o[hi] is not None:require(o[lo]<=o[hi],'REVERSED_RANGE')
                if 'statement_id' in o:
                    self.reg('taxonomy',o['topic_id'])
                    require(e['directness']=='RAW' and o['text'] in self.evidence_text(e),'UNSUPPORTED_QUOTED_STATEMENT')
                if 'theme_id' in o:self.reg('taxonomy',o['theme_id'])
                if f['predicate_id']=='job.salary':require(o['minimum_minor'] is not None or o['maximum_minor'] is not None,'EMPTY_SALARY')
                if f['predicate_id']=='review.record' and o['rating'] is not None:require(o['rating_scale_max'] is not None and 0<=o['rating']<=o['rating_scale_max'],'RATING_OUT_OF_RANGE')
                if f['predicate_id']=='technology.footprint':
                    fp=self.reg('fingerprints',o['fingerprint_id']);require(fp['product_subject_id']==o['product_id'] and fp['emits']==f['predicate_id'] and fp['capture_mode']==scope['capture_mode'],'FINGERPRINT_OUTPUT_MISMATCH')
                    require(isinstance(o['matched_value'],str) and bool(o['matched_value']),'UNSUPPORTED_MATCHED_VALUE')
                    actual=False
                    for lid in self.row('evidence',f['evidence_id'])['locator_ids']:
                        artifact=self.row('artifacts',self.row('locators',lid)['artifact_id'])
                        if artifact['scope_id']!=f['scope_id']:continue
                        if artifact['status']!='OK' or artifact['truncated'] or artifact['retention_state']!='RETAINED':continue
                        path=(self.root/artifact['content_ref']).resolve()
                        require(path.is_relative_to(self.root.resolve()) and path.is_file(),'FINGERPRINT_ARTIFACT_UNAVAILABLE')
                        raw=path.read_bytes();require(digest(raw)==artifact['content_hash'],'FINGERPRINT_BYTES_MISMATCH')
                        actual=actual or o['matched_value'].lower().rstrip('.') in fingerprint_hosts(fp,raw.decode('utf-8'))
                    require(actual,'FINGERPRINT_NOT_SUPPORTED_BY_CAPTURE')
                if f['predicate_id'].endswith('.measurement'):self.validate_measurement(f)
                if f['predicate_id'] in ['event.authorized_attendance','phone.call_event','phone.routing_verified','phone.recording_verified','integration.connection.verified','ops.automation.verified','ops.sales.verified']:
                    require(scope['kind']=='AUTHORIZED_SYSTEM','PRIVATE_OPERATIONS_REQUIRE_AUTHORIZED_SCOPE')
        self.counts['semantic_facts']+=1

    def validate_measurement(self,f):
        o=f['object'];m=self.reg('metrics',o['metric_id']);self.shape(o['value'],m['value_schema']);self.shape(o['dimensions'],m['dimensions_schema'])
        require(o['metric_id'].split('.')[0]==f['predicate_id'].split('.')[0],'METRIC_WRONG_FAMILY')
        require(o['unit']==m['unit'] and f['nature'] in m['allowed_natures'],'METRIC_UNIT_OR_NATURE')
        require(self.row('subjects',f['subject_id'])['kind'] in m['subject_kinds'],'METRIC_SUBJECT_KIND')
        require(f['target']['provider']==self.reg('sources',f['source_id'])['provider'],'METRIC_PROVIDER_IDENTITY')
        if m['requires_denominator']:
            require(o['numerator'] is not None and o['denominator'] is not None and o['denominator']>0,'MISSING_OR_ZERO_DENOMINATOR')
            require(0<=o['numerator']<=o['denominator'],'INVALID_RATE_COUNTS')
            require(abs(o['value']-o['numerator']/o['denominator'])<1e-9,'RATE_VALUE_MISMATCH')
        if o['sample_size'] is not None and o['denominator'] is not None:require(o['sample_size']>=o['denominator'],'DENOMINATOR_EXCEEDS_SAMPLE')
        if o['uncertainty']:require(o['uncertainty']['lower']<=o['value']<=o['uncertainty']['upper'],'INVALID_UNCERTAINTY_INTERVAL')
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
        try:ZoneInfo(o['reporting_timezone'])
        except ZoneInfoNotFoundError:raise ContractError('UNKNOWN_REPORTING_TIMEZONE')
        if o['unit']=='rating':require(o['value']<=o['dimensions']['scale_maximum'],'RATING_SCALE')

    def validate_sample(self,s):
        sub=self.row('subjects',s['subject_id']);scope=self.row('scopes',s['scope_id'])
        require(sub['tenant_id']==s['tenant_id']==scope['tenant_id'] and scope['subject_id']==sub['subject_id'],'SAMPLE_SUBJECT')
        require(instant(s['window']['start'])<instant(s['window']['end']),'SAMPLE_WINDOW')
        retrieved=set(s['retrieved_artifact_ids']);eligible=set(s['eligible_artifact_ids']);excluded=set(s['excluded_artifact_ids'])
        require(not eligible&excluded and eligible|excluded==retrieved,'SAMPLE_PARTITION')
        origins=[]
        for aid in retrieved:
            a=self.row('artifacts',aid);require(a['tenant_id']==s['tenant_id'] and a['scope_id']==s['scope_id'],'SAMPLE_ARTIFACT_SCOPE')
            require(self.reg('sources',a['source_id'])['policy_id'] in s['policy_ids'],'SAMPLE_POLICY_MISSING')
            if aid in eligible:
                require(a['status']=='OK' and not a['truncated'],'INELIGIBLE_SAMPLE_CAPTURE')
                require(a['published_at'] is not None and instant(s['window']['start'])<=instant(a['published_at'])<instant(s['window']['end']),'SAMPLE_PUBLICATION_WINDOW')
                origins.append((a['origin_namespace'],a['origin_record_id']))
        require(len(origins)==len(set(origins)),'DUPLICATED_SAMPLE_ORIGIN')
        if s['complete_population']:require(s['selection_method']=='CENSUS' and s['population_size']==len(origins),'UNPROVEN_POPULATION_CENSUS')

    def validate_prior(self,f):
        o=f['object'];s=self.row('samples',o['sample_id']);e=self.row('evidence',f['evidence_id'])
        require(s['subject_id']==f['subject_id'] and f['window']==s['window'],'PRIOR_SAMPLE_SCOPE')
        ids=o['supporting_fact_ids']+o['contradicting_fact_ids'];require(len(ids)==len(set(ids)),'DUPLICATED_PRIOR_SUPPORT')
        require(set(ids)==set(e['input_fact_ids']),'PRIOR_LINEAGE_MISMATCH')
        self.validate_sample_dependencies(s)
        require(e['sample_ids']==[s['sample_id']],'PRIOR_SAMPLE_NOT_IN_LINEAGE')
        expected_support={i for d in s['record_decisions'] if d['status']=='SUPPORT' for i in d['classification_fact_ids']}
        expected_contradict={i for d in s['record_decisions'] if d['status'] in ['CONTRADICT','NO_THEME'] for i in d['classification_fact_ids']}
        require(set(o['supporting_fact_ids'])==expected_support and set(o['contradicting_fact_ids'])==expected_contradict,'PRIOR_SUPPORT_POLICY_MISMATCH')
        supporting=[self.row('facts',i) for i in o['supporting_fact_ids']]
        for sf in supporting:
            require(sf['subject_id']==f['subject_id'] and sf['object'].get('theme_id')==o['theme_id'],'PRIOR_THEME_OR_SUBJECT_MISMATCH')
        got=theme_summary(s,supporting,self.index['artifacts'],self.roots)
        for k,v in got.items():require(o[k]==v,'PRIOR_COUNT_MISMATCH:'+k)

    def validate_context(self,c):
        rule=self.reg('context-rules',c['join_rule_id']);account=self.row('subjects',c['account_subject_id']);target=self.row('subjects',c['context_subject_id']);run=self.row('runs',c['run_id'])
        require(account['kind'] in ['ORG','LOCATION'] and target['kind'] in rule['target_kinds'],'CONTEXT_SUBJECT_KIND')
        require(account['tenant_id']==target['tenant_id']==c['tenant_id']==run['tenant_id'],'CROSS_TENANT_CONTEXT')
        link=self.row('facts',c['link_fact_id'])
        require(link['subject_id']==account['subject_id'] and link['predicate_id']==rule['link_predicate'],'CONTEXT_LINK_PREDICATE')
        require(pointer(link['object'],rule['link_object_path'])==target['subject_id'],'CONTEXT_WRONG_PRODUCT_OR_INDUSTRY')
        require(c['relationship_strength']==rule['link_kind'],'CONTEXT_STRENGTH_LAUNDERING')
        require(self.reg('profiles',run['profile_id'])['research_context_enabled'],'CONTEXT_DISABLED')
        for fid in c['context_fact_ids']:
            f=self.row('facts',fid);require(f['subject_id']==target['subject_id'] and f['predicate_id']==rule['context_predicate'],'CONTEXT_PRIOR_SCOPE')
        for fid in [c['link_fact_id']]+c['context_fact_ids']:self.assert_consumed(fid,run['run_id'])
        if c['status']=='ELIGIBLE':
            require(all(self.decision_eligible(fid,run['as_of'],run_id=run['run_id']) for fid in [c['link_fact_id']]+c['context_fact_ids']),'INELIGIBLE_RESEARCH_CONTEXT')
