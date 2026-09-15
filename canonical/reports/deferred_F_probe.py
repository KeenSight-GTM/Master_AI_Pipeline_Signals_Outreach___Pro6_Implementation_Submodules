"""Diagnostic: reproduces deliberately deferred F; acceptance below is a known defect."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from keensight_contracts.validation import Bundle
from keensight_contracts.engine import resolve_claim
for tenant,replacement in [('tenant.other',None),('tenant.demo','missing.replacement')]:
    b=Bundle(ROOT,check_hashes=False)
    for kind in ['gates','exports']:b.rows[kind].clear();b.index[kind].clear()
    record={'change_id':'change.deferred','tenant_id':tenant,'kind':'RETRACTION','target_id':'f.vendor1',
        'effective_at':'2026-09-14T19:00:00Z','reason':'F diagnostic','replacement_id':replacement}
    b.rows['changes'].append(record);b.index['changes'][record['change_id']]=record
    for r in b.rows['resolutions']:
        result=resolve_claim([b.row('facts',f) for f in r['observation_ids']],r['as_of'],lambda f,t:b.usable(f['fact_id'],t,allow_absence=True))
        r.update(status=result['status'],accepted_fact_ids=result['accepted_fact_ids'])
    print(tenant,replacement,b.validate()['status'],'usable:',b.usable('f.vendor1','2026-09-14T20:00:00Z'))
