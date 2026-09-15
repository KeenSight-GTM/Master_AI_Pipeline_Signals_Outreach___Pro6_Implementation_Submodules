"""Safety requirements against the unchanged audited baseline.

Failures are expected until the corresponding application repairs are implemented.
They are NOT marked xfail and must not be mixed into the original passing-test count.
The effective_at policy question is reported separately, not asserted as settled policy.
"""
import pathlib,sys
import pytest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from audit_probes import PROBES
CASES=[key for key in PROBES if key!='R2-A05']
@pytest.mark.parametrize('probe_id',CASES)
def test_required_safety_behaviour(probe_id,tmp_path):
    got=PROBES[probe_id](tmp_path)
    assert not got['violation_present'], f'{probe_id}: {got}'
