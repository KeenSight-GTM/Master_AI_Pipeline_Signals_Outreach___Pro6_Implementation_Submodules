from copy import deepcopy
from pathlib import Path
import importlib
import json
import pytest
from jsonschema import Draft7Validator,FormatChecker
from keensight_contracts.catalog import registries,specimen
from keensight_contracts.shapes import SCHEMAS
from keensight_contracts.engine import *
from keensight_contracts.validation import Bundle
from generate import output_bytes

ROOT=Path(__file__).resolve().parents[1]

@pytest.fixture
def b():return Bundle(ROOT,check_hashes=False)

def test_full_bundle():assert Bundle(ROOT).validate()['status']=='PASS'

def test_generation_matches_disk():
    for path,data in output_bytes().items():assert (ROOT/path).read_bytes()==data,path

@pytest.mark.parametrize('name',list(SCHEMAS))
def test_all_schemas(name):Draft7Validator.check_schema(SCHEMAS[name])

@pytest.mark.parametrize('p',registries()['predicates'],ids=lambda p:p['predicate_id'])
def test_catalog_examples(p):
    Draft7Validator(p['target_schema'],format_checker=FormatChecker()).validate(p['example_target'])
    Draft7Validator(p['value_schema'],format_checker=FormatChecker()).validate(p['example_value'])

@pytest.mark.parametrize('metric',registries()['metrics'],ids=lambda m:m['metric_id'])
def test_metric_definitions(metric):
    Draft7Validator.check_schema(metric['dimensions_schema']);Draft7Validator.check_schema(metric['value_schema'])
    Draft7Validator(metric['dimensions_schema']).validate(specimen(metric['dimensions_schema']))
    Draft7Validator(metric['value_schema']).validate(specimen(metric['value_schema']))

@pytest.mark.parametrize('section',range(1,12))
def test_all_domains_have_declared_coverage(b,section):
    c=b.reg('coverage',section);assert c['predicate_ids']
    for p in c['predicate_ids']:assert b.reg('predicates',p)

# Deliberately bad cases call the actual boundary function, not merely hash checking.
def setfield(fid,key,value):
    return lambda b:b.row('facts',fid).__setitem__(key,value)
FACT_MUTATIONS=[
 ('bad-value',setfield('f.job','object',{'unexpected':True}),'f.job'),
 ('wrong-account',setfield('f.job','subject_id','org.other'),'f.job'),
 ('wrong-tenant',setfield('f.job','tenant_id','tenant.other'),'f.job'),
 ('missing-evidence',setfield('f.tech','evidence_id','does-not-exist'),'f.tech'),
 ('wrong-binding',setfield('f.tech','binding_id','bind.art.job'),'f.tech'),
 ('source-not-allowed',setfield('f.traffic','source_id','source.web'),'f.traffic'),
 ('estimate-as-observed',setfield('f.traffic','nature','DIRECT_OBSERVATION'),'f.traffic'),
 ('empty-salary',lambda b:b.row('facts','f.salary')['object'].update(minimum_minor=None,maximum_minor=None),'f.salary'),
 ('reverse-salary',lambda b:b.row('facts','f.salary')['object'].update(minimum_minor=9000000,maximum_minor=100),'f.salary'),
 ('quote-invented',lambda b:b.row('facts','f.job_statement')['object'].update(text='Their CRM is broken.'),'f.job_statement'),
 ('unknown-taxonomy',lambda b:b.row('facts','f.job_statement')['object'].update(topic_id='invented.topic'),'f.job_statement'),
 ('negative-rating',lambda b:b.row('facts','f.product1')['object'].update(rating=-1),'f.product1'),
 ('rating-too-high',lambda b:b.row('facts','f.product1')['object'].update(rating=7),'f.product1'),
 ('metric-wrong-unit',lambda b:b.row('facts','f.traffic')['object'].update(unit='dollars'),'f.traffic'),
 ('metric-unknown-dimension',lambda b:b.row('facts','f.traffic')['object']['dimensions'].update(made_up=True),'f.traffic'),
 ('metric-negative-count',lambda b:b.row('facts','f.traffic')['object'].update(value=-5),'f.traffic'),
 ('wrong-period',setfield('f.traffic','window',None),'f.traffic'),
 ('reverse-period',setfield('f.traffic','window',{'start':'2026-09-01T00:00:00Z','end':'2026-08-01T00:00:00Z'}),'f.traffic'),
 ('future-period',setfield('f.traffic','window',{'start':'2026-09-01T00:00:00Z','end':'2026-10-01T00:00:00Z'}),'f.traffic'),
 ('wrong-provider',lambda b:b.row('facts','f.traffic')['target'].update(provider='Other provider'),'f.traffic'),
 ('invalid-timezone',lambda b:[b.row('facts','f.traffic')[k].update(reporting_timezone='Not/A_Timezone') for k in ['object','target']],'f.traffic'),
 ('freshness-launder',setfield('f.prior.product','expires_at','2026-12-01T00:00:00Z'),'f.prior.product'),
 ('refresh-observed-at',setfield('f.tech','observed_at','2026-09-14T16:00:20Z'),'f.tech'),
 ('missing-coverage',lambda b:b.row('evidence','ev.f.no_form').update(coverage_id=None),'f.no_form'),
 ('incomplete-coverage',lambda b:b.row('coverage','coverage.form').update(status='INCOMPLETE'),'f.no_form'),
 ('coverage-wrong-target',lambda b:b.row('coverage','coverage.form').update(target={'form_key':'other'}),'f.no_form'),
 ('wrong-product-reference',lambda b:[b.row('facts','f.tech')[k].update(product_id='org.other') for k in ['object','target']],'f.tech'),
 ('missing-calibration',setfield('f.tech','confidence',{'value':0.99,'meaning':'CALIBRATED_PRECISION','calibration_id':'missing'}),'f.tech'),
 ('private-on-public-scope',lambda b:b.row('scopes','scope.private').update(kind='PAGE'),'f.call'),
 ('research-relabeled-company',setfield('f.prior.product','subject_id','org.acme'),'f.prior.product'),
 ('wrong-output-backlink',setfield('f.prior.product','execution_id','ex.summary.local'),'f.prior.product'),
]
@pytest.mark.parametrize('label,mut,fid',FACT_MUTATIONS,ids=[m[0] for m in FACT_MUTATIONS])
def test_fact_rejection(b,label,mut,fid):
    mut(b)
    with pytest.raises((ContractError,ValueError)):b.validate_fact(b.row('facts',fid))

CONTEXT_MUTATIONS=[
 ('wrong-product',lambda b:b.row('contexts','context.product').update(context_subject_id='product.crm')),
 ('cross-account-link',lambda b:b.row('contexts','context.product').update(link_fact_id='f.product1')),
 ('other-company-target',lambda b:b.row('contexts','context.product').update(account_subject_id='org.other')),
 ('cross-tenant-context',lambda b:b.row('contexts','context.product').update(tenant_id='tenant.other')),
 ('company-pain-as-context',lambda b:b.row('contexts','context.product').update(context_fact_ids=['f.prior.local'])),
 ('strength-upgrade',lambda b:b.row('contexts','context.product').update(relationship_strength='MEMBERSHIP')),
 ('candidate-ancestor',lambda b:b.reg('sources','source.review').update(authority='CANDIDATE')),
 ('candidate-matcher',lambda b:b.reg('fingerprints','fp.calendly.script').update(authority='CANDIDATE')),
 ('revoked-policy',lambda b:b.reg('policies','policy.fixture').update(review_status='REVOKED')),
 ('expired-root',lambda b:b.row('artifacts','art.product1').update(retained_until='2026-09-14T19:00:00Z')),
 ('agency-footprint',lambda b:b.row('bindings','bind.art.home').update(role='AGENCY')),
 ('research-disabled',lambda b:b.reg('profiles','profile.broad_research').update(research_context_enabled=False)),
]
@pytest.mark.parametrize('label,mut',CONTEXT_MUTATIONS,ids=[m[0] for m in CONTEXT_MUTATIONS])
def test_context_rejection(b,label,mut):
    mut(b)
    with pytest.raises(ContractError):b.validate_context(b.row('contexts','context.product'))

COPY_MUTATIONS=[
 ('unsupported-fixed-text',lambda b:b.row('packages','package.product')['clauses'][0].update(text='Your CRM and booking do not talk.')),
 ('wrong-account-fact',lambda b:b.row('packages','package.product')['clauses'][0].update(fact_ids=['f.product1'])),
 ('prior-used-as-proof',lambda b:b.row('packages','package.product')['clauses'][0].update(fact_ids=['f.prior.product'])),
 ('candidate-source',lambda b:b.reg('sources','source.web').update(authority='CANDIDATE')),
 ('stale-evidence',lambda b:b.row('facts','f.tech').update(expires_at='2026-09-14T19:00:00Z')),
 ('unknown-hook',lambda b:b.row('facts','f.tech').update(state='UNKNOWN',object=None,reason='INSUFFICIENT_EVIDENCE')),
 ('absence-hook',lambda b:b.row('facts','f.tech').update(state='NOT_FOUND',object=None,reason='NOT_DETECTED_IN_SCOPE')),
 ('missing-qualification',lambda b:b.row('packages','package.product')['clauses'][0].update(evidence_roles=['ATTRIBUTED'])),
 ('purpose-forbidden',lambda b:b.reg('policies','policy.fixture')['purposes'].remove('OUTREACH')),
 ('binding-revoked',lambda b:b.row('bindings','bind.art.home').update(status='REJECTED')),
]
@pytest.mark.parametrize('label,mut',COPY_MUTATIONS,ids=[m[0] for m in COPY_MUTATIONS])
def test_copy_rejection(b,label,mut):
    mut(b)
    with pytest.raises(ContractError):b.render(b.row('packages','package.product'))

@pytest.mark.parametrize('pid',['package.product','package.job','package.absence'])
def test_supported_template_no_maturity_needed(b,pid):
    pkg=b.row('packages',pid);assert pkg['maturity_fact_id'] is None
    assert b.render(pkg)==pkg['rendered_text']

def test_mathematical_prior_sample(b):
    b.validate_prior(b.row('facts','f.prior.product'))
    assert b.row('facts','f.prior.product')['object']['sample_share']==2/3

@pytest.mark.parametrize('field,value',[('support_count',3),('eligible_count',50),('sample_share',0.99),('population_claim',True)])
def test_bad_prior_counts(b,field,value):
    b.row('facts','f.prior.product')['object'][field]=value
    with pytest.raises(ContractError):b.validate_prior(b.row('facts','f.prior.product'))

def test_duplicate_underlying_review(b):
    b.row('artifacts','art.product2')['origin_record_id']='art.product1'
    with pytest.raises(ContractError):b.validate_sample(b.row('samples','sample.product'))

def test_incomplete_population_not_census(b):
    b.row('samples','sample.product').update(complete_population=True,population_size=3)
    with pytest.raises(ContractError):b.validate_sample(b.row('samples','sample.product'))

def test_unknown_does_not_erase_known(b):
    f=deepcopy(b.row('facts','f.tech'));unknown=deepcopy(f);unknown.update(fact_id='u',state='UNKNOWN',object=None,reason='INSUFFICIENT_EVIDENCE')
    got=resolve_claim([f,unknown],'2026-09-14T20:00:00Z',lambda f,at:True)
    assert got=={'status':'KNOWN','accepted_fact_ids':['f.tech']}

def test_conflict_abstains(b):
    f=deepcopy(b.row('facts','f.vendor1'));other=deepcopy(f);other['fact_id']='different';other['object']['class_id']='other'
    assert resolve_claim([f,other],'2026-09-14T20:00:00Z',lambda f,at:True)['status']=='CONFLICT'

def test_multivalue_identity(b):assert claim_key(b.row('facts','f.vendor1'))!=claim_key(b.row('facts','f.vendor2'))

@pytest.mark.parametrize('field,value',[('provider','Other provider'),('reporting_timezone','America/Phoenix'),('method_version','2.0.0')])
def test_measurement_identity_dimensions(b,field,value):
    a=b.row('facts','f.traffic');other=deepcopy(a);other['target'][field]=value
    assert claim_key(a)!=claim_key(other)

def test_period_identity(b):
    a=b.row('facts','f.traffic');other=deepcopy(a);other['window']={'start':'2026-07-01T00:00:00Z','end':'2026-08-01T00:00:00Z'}
    assert claim_key(a)!=claim_key(other)

@pytest.mark.parametrize('nodes,edges',[
    (['a'],[('a','a')]),(['a','b'],[('a','b'),('b','a')]),(['a'],[('b','a')]),(['a','a'],[]),
    (['a','b','c'],[('a','b'),('b','c'),('c','a')])])
def test_bad_dependency_graph(nodes,edges):
    with pytest.raises(ContractError):stable_order(nodes,edges)

def test_dependency_order_stable():assert stable_order(['c','b','a'],[('a','b'),('b','c')])==['a','b','c']

@pytest.mark.parametrize('path,expected',[
 ('fingerprint-positive.html',True),('fingerprint-protocol-relative.html',True),('fingerprint-lookalike.html',False),
 ('fingerprint-comment.html',False),('fingerprint-blog.html',False),('fingerprint-footer.html',False)])
def test_real_reference_matcher(b,path,expected):
    assert matches_fingerprint(b.registry['fingerprints'][0],(ROOT/'fixtures'/path).read_text()) is expected

@pytest.mark.parametrize('body',['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'])
def test_strict_json(tmp_path,body):
    p=tmp_path/'bad.json';p.write_text(body)
    with pytest.raises(ContractError):read_json(p)

def test_bad_timestamp_schema(b):
    x=deepcopy(b.row('facts','f.tech'));x['observed_at']='2026-99-99T00:00:00Z'
    with pytest.raises(ContractError):b.shape(x,'Fact')

@pytest.mark.parametrize('state,obj,reason',[
 ('OBSERVED',None,None),('OBSERVED',{'x':1},'CONFLICT'),('UNKNOWN',{'x':1},'INSUFFICIENT_EVIDENCE'),
 ('NOT_FOUND',{'x':1},'NOT_DETECTED_IN_SCOPE'),('UNKNOWN',None,None),('NOT_FOUND',None,'FETCH_FAILED')])
def test_fact_state_shapes(b,state,obj,reason):
    f=deepcopy(b.row('facts','f.tech'));f.update(state=state,object=obj,reason=reason)
    with pytest.raises(ContractError):b.shape(f,'Fact')

# A few complete-pipeline mutations ensure the individual boundaries are invoked.
@pytest.mark.parametrize('kind', ['truncated_coverage','duplicate_id','wrong_run_pin','llm_policy_denied','unimplemented_enabled','production_attempt','provenance_cycle','forward_dependency'])
def test_full_pipeline_rejects(b,kind):
    if kind=='truncated_coverage':b.row('artifacts','art.home')['truncated']=True
    elif kind=='duplicate_id':
        b.rows['facts'].append(deepcopy(b.rows['facts'][0]))
        with pytest.raises(ContractError):b.indexed(b.rows['facts'],'fact_id','facts')
        return
    elif kind=='wrong_run_pin':b.row('runs','run.demo')['registry_release']='sha256:'+'a'*64
    elif kind=='llm_policy_denied':b.reg('policies','policy.fixture')['purposes'].remove('LLM_PROCESS')
    elif kind=='unimplemented_enabled':b.reg('profiles','profile.broad_research')['execute_function_ids'].append('fixture.theme_v1')
    elif kind=='production_attempt':b.row('runs','run.demo')['mode']='PRODUCTION'
    elif kind=='provenance_cycle':b.row('evidence','ev.f.prior.product')['input_fact_ids']=['f.prior.product']
    elif kind=='forward_dependency':b.row('executions','ex.summary.product')['started_at']='2026-09-14T16:00:00Z'
    if kind not in ['wrong_run_pin']:b.row('runs','run.demo')['registry_release']=digest(b.registry)
    with pytest.raises(ContractError):b.validate()


def test_entrypoints_exist(b):
    for fn in b.registry['functions']:
        if fn['implementation_status']=='REFERENCE_IMPLEMENTED':
            mod,name=fn['entrypoint'].split(':');assert callable(getattr(importlib.import_module(mod),name))


def test_all_prior_predicates_retained(b):
    old=read_json(ROOT/'reference/v3-predicates.json')
    assert {p['predicate'] for p in old}<={p['predicate_id'] for p in b.registry['predicates']}


def test_code_release_is_real(b):
    assert b.row('runs','run.demo')['code_release']==code_digest(ROOT)

def test_code_release_mismatch_rejected(b):
    b.row('runs','run.demo')['code_release']='sha256:'+'0'*64
    with pytest.raises(ContractError,match='RUN_CODE_PIN_MISMATCH'):b.validate()

def test_prompt_hash_matches_retained_request(b):
    b.row('model-calls','call.fixture')['prompt_hash']='sha256:'+'0'*64
    with pytest.raises(ContractError,match='MODEL_REQUEST_PIN_MISMATCH'):b.validate()

def test_account_approval_cannot_precede_support(b):
    b.row('packages','package.job')['approved_at']='2026-09-14T15:00:00Z'
    with pytest.raises(ContractError):b.validate()

def test_computation_wall_clock_can_follow_as_of(b):
    # Logical cutoff is not wall-clock finish. All dependent decisions must follow
    # the later computation; v4's old test left those newly required clocks stale.
    b.rows['gates'].clear();b.index['gates'].clear();b.rows['exports'].clear();b.index['exports'].clear()
    ex=b.row('executions','ex.summary.product')
    ex['started_at']='2026-09-14T21:00:00Z';ex['finished_at']='2026-09-14T21:01:00Z'
    b.row('facts','f.prior.product')['recorded_at']=ex['finished_at']
    for result in b.row('runs','run.demo')['target_results']:result['completed_at']='2026-09-14T21:02:00Z'
    for r in b.rows['resolutions']:
        if 'f.prior.product' in r['observation_ids']:r['resolved_at']='2026-09-14T21:01:30Z'
    for signal in b.rows['signals']:signal['evaluated_at']='2026-09-14T21:03:00Z'
    for pkg in b.rows['packages']:
        pkg['approved_at']='2026-09-14T21:05:00Z'
        b.row('reviews',pkg['review_id'])['decided_at']=pkg['approved_at']
    assert b.validate()['status']=='PASS'

def test_full_class_partitions_match_all_schemas():
    index=read_json(ROOT/'diagrams/index.json')
    names=[name for stem,title,kind,classes in index['diagrams'] if '04-'<=stem[:3]<='11-' for name in classes]
    assert set(names)==set(SCHEMAS)
    assert len(names)==len(set(names))

def test_all_diagram_sources_exist():
    index=read_json(ROOT/'diagrams/index.json')
    for stem,*_ in index['diagrams']:assert (ROOT/'diagrams'/f'{stem}.mmd').is_file()


def test_enabled_signals_require_enabled_implementation(b):
    profile=b.reg('profiles','profile.broad_research')
    fn=b.reg('signals',profile['signal_ids'][0])['function_id']
    profile['execute_function_ids'].remove(fn)
    b.row('runs','run.demo')['registry_release']=digest(b.registry)
    with pytest.raises(ContractError,match='SIGNAL_FUNCTION_NOT_ENABLED'):b.validate()


@pytest.mark.parametrize('kind',['wrong_tenant','derive_denied','derived_retention'])
def test_source_rights_are_not_only_capture_rights(b,kind):
    p=b.reg('policies','policy.fixture')
    if kind=='wrong_tenant':p['tenant_ids']=['tenant.other']
    elif kind=='derive_denied':p['purposes'].remove('DERIVE')
    else:p['max_derived_retention_seconds']=1
    b.row('runs','run.demo')['registry_release']=digest(b.registry)
    with pytest.raises(ContractError):b.validate()

def test_policy_change_vetoes_current_use(b):
    b.rows['changes'].append({'actor_id':'actor.fixture','target_type':'policies','recorded_at':'2026-09-14T19:00:00Z','change_id':'change.policy','tenant_id':'tenant.demo','kind':'POLICY_REVOCATION','target_id':'policy.fixture','effective_at':'2026-09-14T19:00:00Z','reason':'test','replacement_id':None})
    assert not b.usable('f.tech','2026-09-14T20:00:00Z')
