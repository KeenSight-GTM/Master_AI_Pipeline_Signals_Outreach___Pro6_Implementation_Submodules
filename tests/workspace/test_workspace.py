from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import pytest

ROOT = Path(__file__).resolve().parents[2]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

w = load('workspace_tools_test', ROOT/'tools/workspace.py')
m = load('manifest_tools_test', ROOT/'tools/verify_manifest.py')


def test_authoritative_code_locations_exist():
    for rel in ['collector/src/keensight_scrapling', 'canonical/keensight_contracts', 'protocol', 'product-design']:
        assert (ROOT/rel).is_dir()


def test_no_duplicate_baseline_tree():
    assert not (ROOT/'audits/poc/baseline').exists()
    assert not (ROOT/'audits/iteration2/baseline').exists()


def test_provenance_manifest_has_safe_component_paths():
    # A developer may legitimately edit the source. Byte equality is a separate
    # explicit release-integrity check, not a permanent barrier in normal CI.
    manifest = json.loads((ROOT/'provenance/COMPONENT_SOURCE_MANIFEST.json').read_text())
    paths = [row['path'] for row in manifest['files']]
    assert len(paths) == len(set(paths)) == manifest['file_count']
    assert all(Path(x).parts[0] in {'collector','canonical','protocol','product-design'} for x in paths)
    assert all(not Path(x).is_absolute() and '..' not in Path(x).parts for x in paths)
    assert all(len(row['sha256']) == 64 for row in manifest['files'])


def test_help_parses_status():
    assert w.parser().parse_args(['status']).action == 'status'


def test_audit_choices_are_closed():
    with pytest.raises(SystemExit):
        w.parser().parse_args(['audit', 'unknown'])


def test_command_output_cannot_modify_source():
    with pytest.raises(ValueError):
        w.external_output(str(ROOT/'outputs'), 'demo')


def test_default_checks_are_local():
    all_args = ' '.join(' '.join(s.args) for s in w.check_steps())
    assert 'pip' not in all_args and 'live-check' not in all_args


def test_component_tests_are_separate_processes(tmp_path):
    steps = w.test_steps(tmp_path)
    assert [x.cwd for x in steps[:3]] == [ROOT/'collector', ROOT/'canonical', ROOT/'protocol']
    assert all(x.expected_exit == 0 for x in steps)


def test_shared_source_override():
    assert w.environment()['KEENSIGHT_BASELINE'] == str(ROOT)


def test_manifest_detects_tamper(tmp_path):
    f = tmp_path/'a.py'; f.write_bytes(b'original')
    manifest = {'files':[{'path':'a.py','sha256':hashlib.sha256(b'original').hexdigest()}]}
    assert m.check_manifest(tmp_path, manifest) == []
    f.write_bytes(b'changed')
    assert m.check_manifest(tmp_path, manifest) == ['MISMATCH: a.py']


def test_manifest_rejects_path_escape(tmp_path):
    assert m.check_manifest(tmp_path, {'files':[{'path':'../secret','sha256':'0'*64}]})


def test_manifest_strict_extra_file(tmp_path):
    (tmp_path/'surprise.py').write_text('pass')
    assert m.check_manifest(tmp_path, {'files':[]}, strict=True) == ['UNEXPECTED: surprise.py']


def test_failed_subprocess_is_not_hidden(tmp_path):
    code = w.run_steps([w.Step('failure', ('-c','raise SystemExit(7)'), ROOT)], tmp_path, 10)
    assert code == 1
    result = json.loads((tmp_path/'run.json').read_text())
    assert result['steps'][0]['returncode'] == 7
    assert result['all_expected_exit_codes'] is False


def test_successful_subprocess_recorded(tmp_path):
    assert w.run_steps([w.Step('ok', ('-c','print("ready")'), ROOT)], tmp_path, 10) == 0
    assert (tmp_path/'01-ok.stdout.txt').read_text().strip() == 'ready'
