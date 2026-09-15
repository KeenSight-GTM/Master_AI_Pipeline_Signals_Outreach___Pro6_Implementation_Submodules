#!/usr/bin/env python3
"""One diagram model -> editable Mermaid + Graphviz + self-contained SVG book.

Graphviz performs local rendering; no external web renderer or fonts are bundled.
"""
from pathlib import Path
import html,json,re,subprocess
from keensight_contracts import catalog  # registers the typed payload families
from keensight_contracts.shapes import SCHEMAS
ROOT=Path(__file__).resolve().parent
D=ROOT/'diagrams';D.mkdir(exist_ok=True)

# Links: from, to, UML operator, from multiplicity, to multiplicity, meaning.
GROUPS=[
 ('04-domain-identity','Domain identity, facts and corrections',[
 'Subject','Scope','SubjectBinding','PredicateDefinition','Fact','ClaimResolution','CandidateRecord','ChangeRecord'],[
 ('Scope','Subject','-->','*','1','describes'),('SubjectBinding','Subject','-->','*','1','attributes'),
 ('SubjectBinding','Scope','-->','*','1','binds'),('Fact','Subject','-->','*','1','concerns'),
 ('Fact','PredicateDefinition','-->','*','1','conforms_to'),('Fact','Scope','-->','*','1','scoped_by'),
 ('Fact','SubjectBinding','-->','*','0..1','raw_attribution'),('ClaimResolution','Fact','o--','1','1..*','projects'),
 ('ChangeRecord','Fact','..>','*','0..1','can_retract'),('CandidateRecord','Fact','..>','*','0..1','admit_only_after_validation')]),
 ('05-evidence-access','Evidence acquisition, rights and coverage',[
 'SourceDefinition','DataAccessPolicy','ProviderBlueprint','Artifact','EvidenceLocator','EvidenceSet','CoverageRecord'],[
 ('SourceDefinition','DataAccessPolicy','-->','*','1','governed_by'),('ProviderBlueprint','SourceDefinition','..>','1','0..*','requires_implementation_and_approval'),
 ('Artifact','SourceDefinition','-->','*','1','obtained_from'),('EvidenceLocator','Artifact','-->','*','1','locates'),
 ('EvidenceSet','EvidenceLocator','o--','1','0..*','cites'),('EvidenceSet','CoverageRecord','-->','*','0..1','absence_proof'),
 ('CoverageRecord','Artifact','-->','1','1..*','completed_capture_refs'),('Artifact','Artifact','-->','*','0..1','transformed_from')]),
 ('06-business-payloads','Typed payload examples: tooling, hiring and workflow',[
 'TechnologyValue','TechnologyReportValue','JobPostingValue','SalaryValue','AttributedStatementValue','SurfaceObservationValue','HypothesisValue','QuotedTextResult'],[
 ('JobPostingValue','SalaryValue','..>','1','0..*','separate_fact_by_posting_key'),
 ('JobPostingValue','AttributedStatementValue','..>','1','0..*','may_support_extracted_statements'),
 ('QuotedTextResult','AttributedStatementValue','..>','1','0..1','requires_quote_and_binding_checks'),
 ('AttributedStatementValue','HypothesisValue','..>','*','0..*','inputs_not_proof_of_conclusion'),
 ('SurfaceObservationValue','TechnologyValue','..>','*','0..*','detector_evidence'),
 ('TechnologyReportValue','TechnologyValue','..>','*','*','distinct_epistemic_channels')]),
 ('07-research-measurements','Reviews, research samples and dimensional measurements',[
 'MetricDefinition','MeasurementValue','TaxonomyTerm','ResearchSample','ResearchPriorValue','ReviewRecordValue','DiscussionRecordValue','ThemeClassificationValue'],[
 ('MeasurementValue','MetricDefinition','-->','*','1','unit_dimensions_and_bounds'),
 ('ResearchPriorValue','ResearchSample','-->','*','1','denominator_and_selection'),
 ('ThemeClassificationValue','TaxonomyTerm','-->','*','1','classified_theme'),
 ('ResearchPriorValue','TaxonomyTerm','-->','*','1','summarized_theme'),
 ('ReviewRecordValue','ThemeClassificationValue','..>','1','0..*','input_to_classifier'),
 ('DiscussionRecordValue','ThemeClassificationValue','..>','1','0..*','input_to_classifier'),
 ('ResearchPriorValue','ThemeClassificationValue','o--','1','1..*','support_fact_references')]),
 ('08-registry-phone-outcomes','Registry, authorized call and future outcome payloads',[
 'RegistryRecordValue','CallEventValue','EconomicHypothesisValue','Exposure','OutcomeEvent'],[
 ('CallEventValue','EconomicHypothesisValue','..>','*','0..*','inputs_plus_explicit_assumptions'),
 ('OutcomeEvent','Exposure','-->','*','0..1','matched_or_quarantined')]),
 ('09-evaluation-configuration','Batch execution, versioning and bounded model tasks',[
 'BatchRun','CapabilityProfile','FunctionDefinition','ExecutionRecord','ModelCall','RepairAttempt','FingerprintDefinition','CalibrationRecord','CoverageFamilyPlan'],[
 ('BatchRun','CapabilityProfile','-->','*','1','pins'),('ExecutionRecord','BatchRun','-->','*','1','belongs_to'),
 ('ExecutionRecord','FunctionDefinition','-->','*','1','versioned_function'),('ExecutionRecord','ModelCall','-->','1','0..1','bounded_model_step'),
 ('ModelCall','RepairAttempt','o--','1','0..2','bounded_repair_history'),
 ('FingerprintDefinition','CalibrationRecord','-->','1','0..1','does_not_self_calibrate'),
 ('CapabilityProfile','FunctionDefinition','-->','1','0..*','enabled_dependency_closure'),
 ('CoverageFamilyPlan','CapabilityProfile','..>','*','*','breadth_is_not_activation')]),
 ('10-context-signals-outreach','Scoped research joins, signal evaluation and grounded previews',[
 'ContextJoinRule','ContextAssessment','SignalDefinition','SignalEvaluation','TemplateDefinition','GroundedClause','OutreachPackage'],[
 ('ContextAssessment','ContextJoinRule','-->','*','1','explicit_one_hop_join'),
 ('SignalEvaluation','ContextAssessment','-->','1','0..*','internal_context_only'),
 ('SignalEvaluation','SignalDefinition','-->','*','1','conforms_to'),
 ('OutreachPackage','SignalEvaluation','-->','1','0..*','eligible_results'),
 ('OutreachPackage','GroundedClause','*--','1','1..*','contains'),
 ('OutreachPackage','TemplateDefinition','-->','*','1','reviewed_template'),
 ('GroundedClause','TemplateDefinition','-->','*','1','deterministic_rendering'),
 ('OutreachPackage','ContextAssessment','-->','1','0..*','not_copy_evidence')]),
 ('11-common-value-objects','Shared value objects and requirement records',[
 'TimeWindow','ExternalIdentifier','ConfidenceAssessment','ObjectReferenceRule','CoverageCheck','FactRequirement'],[]),
]

# Every new contract participates in an existing full class partition.
_EXTRA={
 '04-domain-identity':['IntakeRequest','ActorGrant'],
 '05-evidence-access':['AcquisitionAttempt'],
 '06-business-payloads':['PublishedRecordValue','CaseStudyOutcomeValue'],
 '07-research-measurements':['ResearchSupportPolicy','SampleRecordDecision','LookalikeMatch','ScenarioEstimate'],
 '09-evaluation-configuration':['TargetResult'],
 '10-context-signals-outreach':['ReviewDecision','UseRestriction','UseGateDecision','DestinationDefinition','ExportReceipt'],
 '11-common-value-objects':['PackageReference','IntakeTarget'],
}
for stem,title,classes,links in GROUPS:classes.extend(_EXTRA.get(stem,[]))
for stem,title,classes,links in GROUPS:
    if stem=='05-evidence-access':
        links.extend([('AcquisitionAttempt','Artifact','-->','1','0..*','can_have_no_bytes'),('CoverageRecord','AcquisitionAttempt','-->','1','1..*','completed_acquisition')])
    if stem=='07-research-measurements':
        links.extend([('ResearchSample','SampleRecordDecision','*--','1','1..*','complete_denominator'),('ResearchSample','ResearchSupportPolicy','-->','*','1','counting_rule')])
    if stem=='10-context-signals-outreach':
        links.extend([('ReviewDecision','OutreachPackage','-->','*','1','exact_revision_hash'),('UseGateDecision','ReviewDecision','-->','*','1','current_use_not_just_review'),
                      ('UseGateDecision','UseRestriction','-->','*','0..*','non_expiring_DNC_check'),('ExportReceipt','UseGateDecision','-->','*','1','must_allow_at_dispatch'),
                      ('ExportReceipt','DestinationDefinition','-->','*','1','versioned_mapping')])

INTERFACES={
 'BatchRunner':(['RegistryLinker registry','FactRepository facts'],['run(intake_id) BatchRun']),
 'RegistryLinker':([],['load_release(release_id) void','validate_closure(profile) void','execution_order(profile) List~FunctionDefinition~']),
 'SourceAdapter':([],['capture(target, scope) AcquisitionAttempt']),
 'AcquisitionService':(['SourceAdapter adapter','RightsGate rights','ContentRepository content'],['collect(intake, scope) AcquisitionAttempt']),
 'RightsGate':([],['assert_use(policy_ids, purpose, as_of) void','retention_deadline(policy_ids) datetime']),
 'ContentRepository':([],['put_immutable(bytes, policy) Artifact','read_verified(artifact_id) bytes','delete(artifact_id) ChangeRecord']),
 'SubjectResolver':([],['bind(artifact, subject, locators) SubjectBinding']),
 'ExtractionService':(['BoundedModelGateway model'],['extract(artifact, definition) List~CandidateRecord~']),
 'BoundedModelGateway':([],['call(task, artifacts) ModelCall','repair_or_abstain(call) QuotedTextResult']),
 'FactAdmission':(['RightsGate rights','RegistryLinker registry'],['validate(candidate, evidence, binding) Fact','quarantine(candidate, reason) CandidateRecord']),
 'FactRepository':([],['append_idempotent(fact) Fact','select_inputs(subject, as_of) List~Fact~','record_change(change) void']),
 'AccountInputSelector':(['FactRepository facts'],['freeze_account_inputs(subject, as_of) BatchRun']),
 'DerivationRunner':([],['evaluate(function, inputs, parameters) ExecutionRecord']),
 'ContextJoiner':([],['join(rule, account_facts, context_facts) ContextAssessment']),
 'SignalEngine':([],['evaluate(definition, facts, contexts) SignalEvaluation']),
 'TemplateRenderer':([],['render(template, eligible_facts) List~GroundedClause~']),
 'PackageValidator':(['RightsGate rights'],['approve_preview(package, as_of) OutreachPackage','revalidate_for_export(package, as_of) void']),
 'RetentionService':(['ContentRepository content','FactRepository facts'],['apply_policy(policy, as_of) List~ChangeRecord~']),
 'UnitOfWork':([],['begin() void','commit_account_result() void','rollback() void']),
}
INTERFACES.update({
 'ReviewService':([],['review(exact_package_revision, principal) ReviewDecision']),
 'UseGate':([],['evaluate(package, destination, principal, current_time) UseGateDecision']),
 'LocalPreviewExporter':([],['export(gate_id, principal_id, at, idempotency_key) LocalExportResult']),
})

INTERFACE_LINKS=[('BatchRunner','ReviewService','..>','','','review_exact_revision'),('BatchRunner','UseGate','..>','','','current_permission'),('UseGate','LocalPreviewExporter','..>','','','allow_local_export_only'),('BatchRunner','RegistryLinker','..>','','','uses'),('BatchRunner','AcquisitionService','..>','','','optional_capture'),
 ('BatchRunner','AccountInputSelector','..>','','','pins_inputs'),('BatchRunner','DerivationRunner','..>','','','sequential_plan'),
 ('BatchRunner','ContextJoiner','..>','','','context_join'),('BatchRunner','SignalEngine','..>','','','evaluate'),
 ('BatchRunner','TemplateRenderer','..>','','','compose'),('BatchRunner','PackageValidator','..>','','','approve_preview'),
 ('BatchRunner','UnitOfWork','..>','','','publish_atomically_per_account'),('AcquisitionService','SourceAdapter','..>','','','port'),
 ('AcquisitionService','ContentRepository','..>','','','persist'),('AcquisitionService','RightsGate','..>','','','before_capture'),
 ('ExtractionService','SubjectResolver','..>','','','attribution'),('ExtractionService','BoundedModelGateway','..>','','','optional'),
 ('ExtractionService','FactAdmission','..>','','','no_direct_promotion'),('FactAdmission','FactRepository','..>','','','append'),
 ('FactAdmission','RightsGate','..>','','','permitted_derivation'),('AccountInputSelector','FactRepository','..>','','','select'),
 ('PackageValidator','RightsGate','..>','','','current_use_check'),('RetentionService','ContentRepository','..>','','','delete_or_expire'),
 ('RetentionService','FactRepository','..>','','','record_changes')]

FLOW1_NODES={'A':'Broad catalog: 11 areas plus 52 ledger placements','T':'Intake: known or provisional target and purpose',
 'B':'Enabled callable closure and source policy','C':'Bounded acquisition attempt: import or live capture',
 'D':'Retained artifacts and acquisition completion','Z':'Zero-byte failure: attempt-backed UNKNOWN',
 'E':'Extraction and scoped detector execution','F':'Successful producer, required coverage, lineage and binding admission',
 'Q':'Quarantined or rejected candidates','G':'Reusable fact store','H':'Pinned target inputs and claim resolutions',
 'I':'Successful enabled derivations','J':'Complete research sample: support, unclassified and exclusions',
 'K':'Usable explicit context join','L':'Signal requirements over resolved claims','M':'Evidence-bound template',
 'N':'Completed preview package','R':'Authorized review of exact revision and hash','U':'Fresh purpose and destination gate',
 'O':'Idempotent LOCAL PREVIEW export and receipt','P':'Live delivery disabled'}
FLOW1_EDGES=[('A','B','definitions not automatic activation'),('T','B',''),('B','C','authorized capability'),
 ('C','D','capture or import succeeds'),('C','Z','no bytes; no business absence'),('D','E',''),('E','F',''),
 ('F','Q','invalid / failed / ambiguous'),('F','G','admitted'),('G','H','exact facts and bindings'),
 ('H','I','reject conflicting inputs'),('G','J','exact sample dependency closure'),('H','K','account link'),
 ('J','K','matching product or industry'),('I','L',''),('K','L','internal context only'),('L','M','usable condition'),
 ('H','M','eligible account evidence'),('M','N','whole message validates'),('N','R',''),('R','U','historical approval not current permission'),
 ('U','O','ALLOW; no sending'),('U','P','not enabled in this profile')]
FLOW2_NODES={'A':'Account: eligible product footprint and binding','B':'Canonical software product subject',
 'C':'Permitted review or discussion records','D':'Exact quoted classifications with stance and sentiment',
 'E':'ResearchSample: all retrieved eligible, excluded and unclassified records',
 'P':'Versioned support policy: pain versus workflow mention','F':'Prior: scoped numerator and full denominator',
 'G':'Pinned matching context join: USABLE required','H':'Internal investigation or neutral question selection',
 'I':'Separate account evidence for outward claims','X':'No transfer of reported product pain into company fact',
 'V':'Deletion, expiry or rights change to any denominator input blocks current use'}
FLOW2_EDGES=[('A','B','explicit relationship'),('C','D',''),('D','E','one decision per retrieved record'),
 ('P','F','stance and sentiment semantics'),('E','F','deduplicated record denominator'),('B','G',''),('F','G',''),
 ('G','H','no ABSTAINED context'),('H','I','investigate; do not assert pain'),('G','X','hard boundary'),('E','V','all dependencies retained')]

def esc(x):return html.escape(str(x),quote=True)
def type_of(s):
    if '$ref' in s:return s['$ref'].split('/')[-1].split('.')[0]
    if 'anyOf' in s:return 'Optional~'+type_of(s['anyOf'][0])+'~'
    if 'const' in s:return 'bool' if isinstance(s['const'],bool) else ('int' if isinstance(s['const'],int) else ('number' if isinstance(s['const'],float) else 'string'))
    if 'enum' in s:return 'enum'
    t=s.get('type','PredicateValue')
    if isinstance(t,list):return 'union'
    if t=='array':return 'List~'+type_of(s['items'])+'~'
    if t=='object':return 'Object'
    return {'integer':'int','number':'number','boolean':'bool','string':'string'}.get(t,t)

def write_class(stem,title,names,links,custom=None):
    lines=['classDiagram','direction LR']
    dot=['digraph G {','graph [rankdir=LR, nodesep=0.5, ranksep=1.2, splines=polyline, fontname="Helvetica", labelloc=t, label='+json.dumps(title)+'];',
         'node [shape=plain, fontname="Helvetica"];','edge [fontname="Helvetica", fontsize=10, arrowsize=0.7];']
    for name in names:
        if custom:attrs,methods=custom[name]
        else:
            attrs=[f'{type_of(s)} {k}' for k,s in SCHEMAS[name].get('properties',{}).items()];methods=[]
        lines.append('class '+name+' {')
        if custom is INTERFACES:lines.append('  <<Interface>>')
        lines.extend('  +'+x for x in attrs+methods);lines.append('}')
        cells='<TR><TD><B>'+esc(name)+'</B></TD></TR>'
        if custom is INTERFACES:cells+='<TR><TD><I>proposed interface</I></TD></TR>'
        cells+=''.join('<TR><TD ALIGN="LEFT">+ '+esc(x.replace('~',' '))+'</TD></TR>' for x in attrs)
        if methods:cells+=''.join('<TR><TD ALIGN="LEFT">+ '+esc(x.replace('~',' '))+'</TD></TR>' for x in methods)
        dot.append(name+' [label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5">'+cells+'</TABLE>>];')
    for a,b,op,ma,mb,label in links:
        cardinal=(f' "{ma}" ' if ma else ' ')+op+(f' "{mb}" ' if mb else ' ')
        lines.append(a+cardinal+b+' : '+label)
        attrs=['label='+json.dumps(label.replace('_',' '))]
        if '..' in op:attrs.append('style=dashed')
        if op in ['o--','*--']:attrs+=['dir=both','arrowtail='+('odiamond' if op=='o--' else 'diamond'),'arrowhead=none']
        if ma:attrs.append('taillabel='+json.dumps(ma))
        if mb:attrs.append('headlabel='+json.dumps(mb))
        dot.append(a+' -> '+b+' ['+', '.join(attrs)+'];')
    dot.append('}')
    (D/(stem+'.mmd')).write_text('\n'.join(lines)+'\n')
    (D/(stem+'.dot')).write_text('\n'.join(dot)+'\n')
    subprocess.run(['dot','-Tsvg',str(D/(stem+'.dot')),'-o',str(D/(stem+'.svg'))],check=True,capture_output=True)
    return stem,title,'class',names

def write_flow(stem,title,nodes,edges):
    m=['flowchart TB'];dot=['digraph G {','rankdir=TB; graph [fontname="Helvetica", labelloc=t, label='+json.dumps(title)+'];',
        'node [shape=box, style=rounded, fontname="Helvetica", margin="0.2,0.15"]; edge [fontname="Helvetica", fontsize=10];']
    for key,label in nodes.items():
        m.append(f'  {key}["{label}"]');dot.append(key+' [label='+json.dumps(label)+'];')
    for a,b,label in edges:
        m.append(f'  {a} -->'+(f'|"{label}"|' if label else '')+' '+b)
        dot.append(a+' -> '+b+((' [label='+json.dumps(label)+']') if label else '')+';')
    dot.append('}')
    (D/(stem+'.mmd')).write_text('\n'.join(m)+'\n');(D/(stem+'.dot')).write_text('\n'.join(dot)+'\n')
    subprocess.run(['dot','-Tsvg',str(D/(stem+'.dot')),'-o',str(D/(stem+'.svg'))],check=True,capture_output=True)
    return stem,title,'flow',[]

SEQUENCE='''sequenceDiagram
    participant B as BatchRunner
    participant A as Acquisition
    participant F as FactAdmission
    participant DB as FactRepository
    participant S as Reasoning
    participant R as ReviewService
    participant G as CurrentUseGate
    participant X as PreviewExporter
    B->>A: Validated intake, enabled profile, bounded attempt
    alt No bytes captured
        A-->>B: Failed attempt plus diagnostic UNKNOWN; no NOT_FOUND
    else Capture or approved replay import
        A->>F: Artifacts, extraction results and executed detector coverage
        F->>DB: Admit only successful, attributable, lineage-closed facts
    end
    B->>DB: Pin inputs, sample records, bindings and target completion
    DB-->>B: Exact input set and resolved claim views
    B->>S: Evaluate enabled functions, usable context and signals
    alt Conflicting, failed or insufficient evidence
        S-->>B: Abstained or unresolved target; no approved positive output
    else Eligible supported result
        S->>DB: Publish completed preview with exact dependencies
        R->>DB: Record authorized review of package revision and hash
        G->>DB: Recheck current evidence, policies and restrictions
        alt Gate permits exact destination and purpose
            G->>X: ALLOW with current state hash and expiry
            X->>DB: Record local preview receipt with payload hash
        else Current use blocked
            G->>DB: Record BLOCK; historical review remains
        end
    end
    Note over G,X: A repeated local export key reuses identical bytes; changed payload fails
    Note over B,X: No remote export, automatic sending or production authentication is implemented
'''

STATE='''stateDiagram-v2
    [*] --> Intake
    Intake --> Attempt: approved profile and purpose
    Attempt --> DiagnosticUnknown: failure without captured bytes
    Attempt --> CapturedArtifact: permitted capture or import
    CapturedArtifact --> Candidate: extract
    Candidate --> Quarantined: invalid, failed producer or ambiguous binding
    Candidate --> AdmittedFact: all admission checks pass
    AdmittedFact --> EligibleInput: pinned lineage and claim resolution pass
    AdmittedFact --> HistoricalOnly: expired, retracted or rights revoked
    EligibleInput --> Unresolved: missing prerequisites or conflict
    EligibleInput --> ResolvedSignal: enabled condition holds
    ResolvedSignal --> PreviewPackage: supported deterministic template
    PreviewPackage --> ReviewedRevision: authorized exact-hash review
    ReviewedRevision --> UseGate: fresh checks for exact purpose and destination
    UseGate --> Blocked: restrictions, stale evidence or changed inputs
    UseGate --> LocalExport: ALLOW and idempotent file write
    LocalExport --> [*]: no sending
    DiagnosticUnknown --> [*]: retained diagnostic
    Quarantined --> Candidate: explicit corrected extraction
'''

def render_sequence(stem,source):
    """Render the supported sequence syntax directly to local SVG (no Mermaid CLI)."""
    import textwrap
    participants=[];events=[]
    for line in source.splitlines():
        line=line.strip()
        m=re.match(r'participant (\w+) as (.+)',line)
        if m:participants.append((m[1],m[2]));continue
        m=re.match(r'(\w+)(-->>|->>)(\w+): (.+)',line)
        if m:events.append(('message',*m.groups()));continue
        if line.startswith(('opt ','alt ','else ','Note over')):
            events.append(('note',line.split(': ',1)[-1] if line.startswith('Note over') else line))
    width=max(1200,len(participants)*190);left=100;right=width-100
    xpos={p[0]:left+i*(right-left)/max(1,len(participants)-1) for i,p in enumerate(participants)}
    y=110;layout=[]
    for event in events:
        text=event[-1];parts=textwrap.wrap(text,95 if event[0]=='note' else max(22,int(abs(xpos[event[1]]-xpos[event[3]])/7)))
        h=48+len(parts)*15
        layout.append((y,event,parts));y+=h
    height=y+60
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#17212b"/></marker></defs>',
         '<rect width="100%" height="100%" fill="white"/>','<g font-family="Arial,sans-serif" font-size="12" fill="#17212b">']
    for key,label in participants:
        x=xpos[key];out += [f'<rect x="{x-80}" y="25" width="160" height="50" fill="#f3f5f7" stroke="#17212b"/>',f'<text x="{x}" y="54" text-anchor="middle">{esc(label)}</text>',f'<line x1="{x}" y1="75" x2="{x}" y2="{height-30}" stroke="#9ca3aa" stroke-dasharray="4 4"/>']
    for y,event,parts in layout:
        if event[0]=='note':
            out.append(f'<rect x="12" y="{y-20}" width="{width-24}" height="{25+len(parts)*15}" fill="#eef3f8" stroke="#c5cdd5"/>')
            for k,t in enumerate(parts):out.append(f'<text x="30" y="{y+k*15}">{esc(t)}</text>')
        else:
            _,a,arrow,b,text=event;x1=xpos[a];x2=xpos[b];base=y+len(parts)*15
            for k,t in enumerate(parts):out.append(f'<text x="{(x1+x2)/2}" y="{y+k*15}" text-anchor="middle">{esc(t)}</text>')
            dash=' stroke-dasharray="5 4"' if arrow=='-->>' else ''
            out.append(f'<line x1="{x1}" y1="{base}" x2="{x2}" y2="{base}" stroke="#17212b"{dash} marker-end="url(#arrow)"/>')
    out.append('</g></svg>');(D/(stem+'.svg')).write_text('\n'.join(out).replace('\\n','\n'))

def render_state(stem,source):
    nodes={};edges=[];last=0
    for line in source.splitlines():
        m=re.match(r'\s*(\[\*\]|\w+) --> (\[\*\]|\w+)(?:: (.+))?',line)
        if not m:continue
        a,b,label=m.groups()
        if a=='[*]':a='Start'
        if b=='[*]':b='End'
        nodes[a]=a;nodes[b]=b;edges.append((a,b,label or ''))
    original=(D/(stem+'.mmd')).read_text()
    write_flow(stem,'Evidence-to-reviewed-local-export lifecycle',nodes,edges)
    (D/(stem+'.mmd')).write_text(original)

def main():
    entries=[write_flow('01-broad-dataflow','Broad facts, verified handoffs and reviewed local export',FLOW1_NODES,FLOW1_EDGES),
             write_flow('02-research-context','Research context is not account-specific proof',FLOW2_NODES,FLOW2_EDGES)]
    (D/'03-batch-sequence.mmd').write_text(SEQUENCE)
    render_sequence('03-batch-sequence',SEQUENCE)
    entries.append(('03-batch-sequence','Batch evaluation sequence','sequence',[]))
    covered=[]
    for group in GROUPS:
        covered+=group[2];entries.append(write_class(*group))
    assert set(covered)==set(SCHEMAS), (set(SCHEMAS)-set(covered),set(covered)-set(SCHEMAS))
    assert len(covered)==len(set(covered))
    entries.append(write_class('12-proposed-code-interfaces','Proposed application interfaces, not deployed services',list(INTERFACES),INTERFACE_LINKS,INTERFACES))
    (D/'13-lifecycle.mmd').write_text(STATE);entries.append(('13-lifecycle','Evidence-to-reviewed-local-export lifecycle','state',[]))
    render_state('13-lifecycle',STATE)
    overview_names=['Subject','PredicateDefinition','Fact','EvidenceSet','Artifact','ExecutionRecord','BatchRun','ContextAssessment','SignalEvaluation','OutreachPackage','GroundedClause','MetricDefinition']
    overview_fields={name:([f'{type_of(shape)} {key}' for key,shape in SCHEMAS[name]['properties'].items() if key.endswith('_id') or key in ['state','nature','target','window','as_of','status','company_claim_allowed']],[]) for name in overview_names}
    overview_links=[('Fact','Subject','-->','*','1','about'),('Fact','PredicateDefinition','-->','*','1','typed_by'),('Fact','EvidenceSet','-->','*','1','supported_by'),('EvidenceSet','Artifact','-->','*','0..*','through_locators'),('EvidenceSet','Fact','-->','*','0..*','derived_input_refs'),('Fact','ExecutionRecord','-->','*','0..1','produced_by'),('ExecutionRecord','BatchRun','-->','*','1','pinned_run'),('ExecutionRecord','Fact','-->','*','*','reads_and_produces'),('Fact','MetricDefinition','-->','*','0..1','measurement_contract'),('ContextAssessment','Fact','-->','*','2..*','account_link_and_context_fact'),('SignalEvaluation','Fact','-->','*','0..*','eligible_inputs'),('SignalEvaluation','ContextAssessment','-->','*','0..*','internal_context'),('OutreachPackage','SignalEvaluation','-->','*','0..*','based_on'),('OutreachPackage','GroundedClause','*--','1','1..*','contains'),('GroundedClause','Fact','-->','*','1..*','own_account_claim_support')]
    entries.append(write_class('14-system-associations','Cross-partition domain relationships — selected fields only',overview_names,overview_links,overview_fields))
    index={'contract_classes':len(covered),'proposed_interfaces':len(INTERFACES),'diagrams':entries,
           'renderer':'Graphviz SVG plus a local sequence SVG renderer; Mermaid sources are editable, not CLI-rendered.'}
    (D/'index.json').write_text(json.dumps(index,indent=2))
    md=['# Dataflows, UML and complete class reference','',
        'All '+str(len(SCHEMAS))+' exported contract/value-object classes appear exactly once in the full class partitions. '+str(len(INTERFACES))+' proposed code interfaces are separate. ',
        'Primitive and object payloads are selected by the PredicateDefinition registry: 213 predicates do not require 213 classes or database tables. Payload-family boxes show reusable shapes; individual predicate schemas remain normative.',
        'Association labels denote logical references, not separate services. `..>` is a dependency; `o--` aggregation; `*--` composition. Method bodies on proposed interfaces are not implemented runtime code.',
        'SVGs were rendered locally with Graphviz from the same model as the Mermaid class/flow sources. The state view is rendered through Graphviz; the sequence view uses a local SVG renderer over its message declarations. Mermaid CLI parsing was not run.','']
    pages=[]
    for stem,title,kind,names in entries:
        code=(D/(stem+'.mmd')).read_text();md += ['## '+title,'','```mermaid',code.strip(),'```','']
        svgpath=D/(stem+'.svg')
        visual=svgpath.read_text() if svgpath.exists() else '<pre>'+esc(code)+'</pre>'
        if svgpath.exists():visual=visual[visual.index('<svg'):]
        pages.append('<section id="'+stem+'"><h2>'+esc(title)+'</h2><p>'+esc('Complete fields; proposed data contracts.' if kind=='class' else kind.title()+' view.')+'</p><div class="canvas">'+visual+'</div><details><summary>Editable Mermaid source</summary><pre>'+esc(code)+'</pre></details></section>')
    (ROOT/'docs/DIAGRAMS.md').write_text('\n'.join(md))
    nav=''.join('<a href="#'+x[0]+'">'+esc(x[1])+'</a>' for x in entries)
    book='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>KeenSight v4.1 — Dataflows and UML</title>
<style>body{font:16px/1.5 Arial,sans-serif;max-width:1500px;margin:auto;padding:32px;color:#17212b;background:#fff}h1{font-size:36px}h2{margin-top:1em}nav{columns:2;column-gap:32px;padding:20px;background:#f3f5f7}nav a{display:block;margin:8px 0;color:#123b64}section{padding:28px 0;border-bottom:1px solid #ddd}.canvas{overflow:auto;border:1px solid #ddd;padding:16px;background:#fff}.canvas svg{max-width:none;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.5 monospace;padding:16px;background:#f4f6f8}details{margin:16px 0}.note{padding:18px;background:#f4f6f8}button{padding:6px 12px;margin:5px}</style></head><body>
<h1>KeenSight v4.1</h1><p>Broad fact and research-context architecture · September 14, 2026</p><div class="note"><b>Complete class partitions:</b> '''+str(len(SCHEMAS))+''' contract/value-object classes and '''+str(len(INTERFACES))+''' proposed application interfaces. The runtime services are proposed; the bundle includes contract validation and limited pure reference helpers. Pan the scrollable canvases or use browser zoom. No automatic sending is enabled.</div><nav>'''+nav+'</nav>'+''.join(pages)+'''<p>Generated from contract shapes and an explicit diagram model. SVG flow/class diagrams use Graphviz; editable Mermaid sources accompany every view. No external network resources are required.</p></body></html>'''
    (ROOT/'KeenSight_v4_1_Diagrams.html').write_text(book)
    # A class index with exact fields and constraints is easier to audit than giant canvases.
    lines=['# Full class reference','','Every exported schema and its complete fields. JSON Schema files are normative; tables below are generated.','']
    for name,s in sorted(SCHEMAS.items()):
        lines += ['## '+name,'','| Field | Type | Required | Constraints / semantics |','|---|---|---|---|']
        for field,shape in s.get('properties',{}).items():
            extra={k:v for k,v in shape.items() if k not in ['type','properties','items']}
            detail=json.dumps(extra,ensure_ascii=False).replace('|','\\|') if extra else ('Closed object' if shape.get('type')=='object' and shape.get('additionalProperties') is False else '')
            lines.append(f"| `{field}` | `{type_of(shape)}` | {'yes' if field in s.get('required',[]) else 'no'} | {detail} |")
        lines.append('')
    for name,(attrs,methods) in INTERFACES.items():
        lines+=['## '+name+' — proposed interface','','Attributes: '+(', '.join('`'+a+'`' for a in attrs) or 'none specified')+'.','']
        lines+=['`'+method+'`  ' for method in methods];lines.append('')
    (ROOT/'docs/CLASS_REFERENCE.md').write_text('\n'.join(lines))
    print(json.dumps({'contract_classes':len(covered),'interfaces':len(INTERFACES),'diagrams':len(entries),'rendered_svg':len(list(D.glob('*.svg')))}))
if __name__=='__main__':main()
