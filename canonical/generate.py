#!/usr/bin/env python3
"""Generate deterministic contracts; --check does not overwrite files."""
from pathlib import Path
import argparse,json
from keensight_contracts.catalog import registries
from keensight_contracts.bootstrap import supplemental,example_bundle
from keensight_contracts.bootstrap_completion import add_registry,add_examples
from keensight_contracts.shapes import SCHEMAS
from keensight_contracts.engine import digest,code_digest
ROOT=Path(__file__).resolve().parent

def output_bytes():
    reg=add_registry(supplemental(registries()));rows,blobs=example_bundle(reg)
    rows,blobs=add_examples(reg,rows,blobs,ROOT)
    code_hash=code_digest(ROOT)
    for run in rows['runs']:run['code_release']=code_hash
    files={**{f'schemas/{n}.schema.json':s for n,s in SCHEMAS.items()},**{f'registry/{n}.json':v for n,v in reg.items()},'examples/bundle.json':rows}
    encoded={n:(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode() for n,v in files.items()};encoded.update(blobs)
    release={'version':'4.2.0','code_hash':code_hash,'registry_hash':digest(reg),'files':{n:digest(v) for n,v in sorted(encoded.items())}}
    encoded['release.json']=(json.dumps(release,indent=2,sort_keys=True)+'\n').encode()
    return encoded

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();files=output_bytes()
    if args.check:
        actual={str(p.relative_to(ROOT)) for folder in ['schemas','registry','examples','fixtures'] for p in (ROOT/folder).rglob('*') if p.is_file()}|({'release.json'} if (ROOT/'release.json').exists() else set())
        errors=[n for n,b in files.items() if not (ROOT/n).is_file() or (ROOT/n).read_bytes()!=b]
        errors+=sorted(actual-set(files))
        if errors:raise SystemExit('GENERATION_MISMATCH: '+', '.join(errors))
    else:
        for n,b in files.items():
            p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    print(f'{len(files)} deterministic files '+('match' if args.check else 'generated'))
if __name__=='__main__':main()
