#!/usr/bin/env python3
"""Verify retained component sources or the distributed source snapshot.

This is a local integrity check, not a signature or proof of source authorization.
Editable source changes appropriately fail comparison with the shipped baseline.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {'.git', '__pycache__', '.pytest_cache', '.venv', '.ruff_cache', '.mypy_cache'}


def included(path: Path, root: Path = ROOT) -> bool:
    rel = path.relative_to(root)
    return (not any(part in EXCLUDED_PARTS or part.endswith('.egg-info') for part in rel.parts)
            and path.is_file() and path.suffix not in {'.pyc', '.pyo'})


def check_manifest(root: Path, manifest: dict, strict: bool = False) -> list[str]:
    errors: list[str] = []
    expected: set[str] = set()
    for row in manifest['files']:
        rel = Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            errors.append(f'UNSAFE_MANIFEST_PATH: {rel}'); continue
        key = rel.as_posix()
        if key in expected:
            errors.append(f'DUPLICATE_MANIFEST_PATH: {key}'); continue
        expected.add(key)
        path = root / rel
        if not path.is_file(): errors.append(f'MISSING: {key}')
        elif path.is_symlink(): errors.append(f'SYMLINK_NOT_ALLOWED: {key}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            errors.append(f'MISMATCH: {key}')
    if strict:
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if included(p, root)}
        ignored = set(manifest.get('manifest_excluded_files', []))
        errors += [f'UNEXPECTED: {x}' for x in sorted(actual - expected - ignored)]
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--components', action='store_true', help='Check original component sources only')
    p.add_argument('--strict', action='store_true', help='Also reject unlisted source files (snapshot mode)')
    a = p.parse_args()
    file = ROOT / ('provenance/COMPONENT_SOURCE_MANIFEST.json' if a.components else 'SOURCE_MANIFEST.json')
    if not file.exists(): p.error(f'Manifest missing: {file}')
    manifest = json.loads(file.read_text())
    errors = check_manifest(ROOT, manifest, strict=a.strict and not a.components)
    if errors:
        print('\n'.join(errors)); return 1
    print(f'PASS: {len(manifest["files"])} files match ' + ('supplied component sources' if a.components else 'distributed source snapshot'))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
