from __future__ import annotations

import argparse
import json
import sys
import os
import tempfile
from pathlib import Path
from importlib.resources import files
from dataclasses import asdict
from .core import ContractError,DependencyUnavailable,strict_json,utcnow
from .rules import RulePack
from .storage import Store
from .pipeline import Scanner,ScanConfig
from .transport import ScraplingTransport,FixtureTransport,FetchResult
from .urls import NetworkPolicy,normalize_url,origin
from .importer import import_donor,read_donor
from .commands import COMMANDS


def write_json(path: str | Path,data):
    dest=Path(path);dest.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=dest.parent)
    try:
        with os.fdopen(fd,'w') as f:
            json.dump(data,f,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,dest)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def demo(output: str | Path):
    root=Path(output)
    pack=RulePack.compile(strict_json(files('keensight_scrapling').joinpath('data/demo-rules.json').read_text()))
    fixture=strict_json(files('keensight_scrapling').joinpath('data/demo-site.json').read_text())
    transport=FixtureTransport({u:FetchResult(u,r['status'],r['body'].encode(),r['headers']) for u,r in fixture.items()})
    store=Store(root)
    try:
        scanner=Scanner(store,pack,transport,clock=lambda:'2026-09-14T12:00:00Z',production=False)
        bundle=scanner.scan('https://demo.example.test/',ScanConfig('demo','account:demo','demo-capture-1',max_attempts=8))
        write_json(root/'scan-bundle.json',bundle)
        write_json(root/'claims.json',bundle['claims'])
        return {'bundle':str(root/'scan-bundle.json'),'matches':len(bundle['matches']),'observations':len(bundle['observations']),
                'claims':len(bundle['claims']),'actual_network_requests':0,'fixture_only':True}
    finally:store.close()


def main(argv=None):
    p=argparse.ArgumentParser(description='Scrapling collector: retain matches, deduplicate claims, never inflate confidence.')
    sub=p.add_subparsers(dest='command',required=True)
    d=sub.add_parser('demo');d.add_argument('--output',default='./demo-output')
    c=sub.add_parser('commands')
    s=sub.add_parser('scan');s.add_argument('url');s.add_argument('--rules',required=True);s.add_argument('--store',required=True)
    for arg in ('tenant','subject','run'):s.add_argument('--'+arg,required=True)
    s.add_argument('--output',required=True);s.add_argument('--max-attempts',type=int,default=8);s.add_argument('--max-pages',type=int,default=5)
    s.add_argument('--probes',action='store_true')
    r=sub.add_parser('replay');r.add_argument('--store',required=True);r.add_argument('--rules',required=True);r.add_argument('--tenant',required=True)
    r.add_argument('--capture-run',required=True);r.add_argument('--evaluation-run',required=True);r.add_argument('--as-of',required=True);r.add_argument('--output',required=True)
    q=sub.add_parser('claims');q.add_argument('--store',required=True);q.add_argument('--tenant',required=True);q.add_argument('--as-of',required=True);q.add_argument('--rules',required=True)
    q=sub.add_parser('candidates');q.add_argument('--store',required=True);q.add_argument('--tenant',required=True);q.add_argument('--min-hosts',type=int,default=3)
    i=sub.add_parser('import-donor');i.add_argument('--input',required=True);i.add_argument('--vendor-map',required=True);i.add_argument('--output',required=True);i.add_argument('--report',required=True)
    a=sub.add_parser('analyze-file');a.add_argument('--html',required=True);a.add_argument('--url',required=True);a.add_argument('--observed-at',required=True)
    for arg in ('tenant','subject','run','rules','store','output'):a.add_argument('--'+arg,required=True)
    v=sub.add_parser('check');v.add_argument('bundle');v.add_argument('--store')
    args=p.parse_args(argv)
    try:
        if args.command=='demo':result=demo(args.output)
        elif args.command=='commands':result=list(COMMANDS)
        elif args.command=='check':
            from .validation import validate_bundle
            data=strict_json(Path(args.bundle).read_text());validate_bundle(data)
            if args.store:
                from .core import Capture
                from .extraction import extract
                from .core import canonical
                store=Store(args.store)
                try:
                    for raw in data['captures']:
                        cap=Capture(**raw);body=store.body(cap)
                        if cap.capture_id in data['evaluated_capture_ids']:
                            from .core import PageEvidence,Surface,CommandResult
                            from .standalone import verify_page
                            page=PageEvidence(cap,[Surface(**s) for s in data['surfaces'] if s['capture_id']==cap.capture_id],
                                [CommandResult(**c) for c in data['commands'] if c['command_id'].startswith('EXTRACT_') and c['input_ids']==[cap.capture_id]])
                            verify_page(store,page)
                finally:store.close()
            result={'valid':True,'original_bytes_checked':bool(args.store)}
        elif args.command=='import-donor':
            pack,report=import_donor(read_donor(args.input),strict_json(Path(args.vendor_map).read_text()))
            write_json(args.output,pack);write_json(args.report,report)
            result={k:v for k,v in report.items() if k!='dispositions'}
        else:
            store=Store(args.store)
            try:
                if args.command=='analyze-file':
                    from .extraction import extract
                    pack=RulePack.load(args.rules);url=normalize_url(args.url);body=Path(args.html).read_bytes()
                    if len(body)>2_000_000:raise ContractError('Imported HTML exceeds 2 MB; supply an explicit bounded capture')
                    store.begin_run(args.tenant,args.run,{'input_mode':'USER_PROVIDED_SNAPSHOT','url':url,'observed_at':args.observed_at,'release_digest':pack.digest})
                    cap=store.put_capture(tenant_id=args.tenant,subject_id=args.subject,run_id=args.run,url=url,observed_at=args.observed_at,body=body,headers={'content-type':'text/html'},source_id='source:user-provided-snapshot')
                    bundle=Scanner(store,pack,FixtureTransport({}),production=not pack.fixture_only).evaluate([extract(cap,body)],args.run,args.observed_at)
                    write_json(args.output,bundle);result={'bundle':args.output,'claims':len(bundle['claims']),'network_requests':0,'timestamp_is_user_supplied':True}
                elif args.command=='candidates':result=store.candidates(args.tenant,args.min_hosts)
                elif args.command=='claims':
                    pack=RulePack.load(args.rules)
                    result=[asdict(c) for c in store.stored_claims(args.tenant,as_of=args.as_of,allowed_rule_digests={r.digest for r in pack.rules if r.status=='APPROVED'})]
                elif args.command=='replay':
                    pack=RulePack.load(args.rules)
                    # Replay never invokes this deliberately unusable transport.
                    runner=Scanner(store,pack,FixtureTransport({}),production=not pack.fixture_only)
                    result=runner.replay(args.tenant,args.capture_run,args.evaluation_run,args.as_of)
                    write_json(args.output,result);result={'bundle':args.output,'claims':len(result['claims'])}
                else:
                    # Missing dependencies are a CLI error, not a successful empty scan.
                    try:
                        from scrapling.fetchers import FetcherSession
                    except ImportError as exc:
                        raise DependencyUnavailable('Scrapling live extra missing; pip install -e ".[live]"') from exc
                    pack=RulePack.load(args.rules)
                    if pack.fixture_only:raise ContractError('Fixture-only release cannot be used for a live scan')
                    url=normalize_url(args.url)
                    transport=ScraplingTransport(NetworkPolicy((origin(url),)))
                    config=ScanConfig(args.tenant,args.subject,args.run,max_attempts=args.max_attempts,max_pages=args.max_pages,probe_paths=args.probes)
                    bundle=Scanner(store,pack,transport).scan(url,config)
                    write_json(args.output,bundle)
                    result={'bundle':args.output,'claims':len(bundle['claims']),'send_allowed':False}
            finally:store.close()
        print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
        return 0
    except (ContractError,DependencyUnavailable,OSError,ValueError) as exc:
        print(f'{type(exc).__name__}: {exc}',file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
