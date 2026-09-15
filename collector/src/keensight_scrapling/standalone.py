"""Independent offline module entrypoints; no network or provider side effects.

The Store is trusted local-owner input, not an authentication service. Returned
JSON is an artifact, not a canonical Fact. Hosted transport is deliberately absent.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
from pathlib import Path
import sys
from .core import ContractError,Capture,Surface,PageEvidence,CommandResult,canonical,strict_json,utcnow
from .storage import Store
from .extraction import extract
from .rules import RulePack,match_pages
from .claims import observation_candidates,resolve_claims
from .validation import validate_bundle
from .cli import write_json


def verify_page(store: Store,page: PageEvidence) -> None:
    actual=extract(page.capture,store.body(page.capture))
    if canonical(asdict(actual))!=canonical(asdict(page)):
        raise ContractError('PageEvidence differs from deterministic extraction of trusted original capture')


def page_from_json(data):
    if not isinstance(data,dict) or set(data)!={'capture','surfaces','commands'}:
        raise ContractError('Expected a closed PageEvidence record')
    return PageEvidence(Capture(**data['capture']),[Surface(**x) for x in data['surfaces']],
                        [CommandResult(**x) for x in data['commands']])


def main(argv=None):
    parser=argparse.ArgumentParser(description='Independent offline collector operations; local owner only.')
    sub=parser.add_subparsers(dest='operation',required=True)
    ext=sub.add_parser('extract');ext.add_argument('--capture-id',required=True);ext.add_argument('--tenant',required=True)
    mat=sub.add_parser('match');mat.add_argument('--page',action='append',required=True);mat.add_argument('--rules',required=True)
    chk=sub.add_parser('check');chk.add_argument('--bundle',required=True)
    res=sub.add_parser('resolve');res.add_argument('--bundle',required=True);res.add_argument('--as-of',required=True)
    for p in (ext,mat,chk,res):p.add_argument('--store',required=True);p.add_argument('--output',required=True)
    args=parser.parse_args(argv);store=None
    try:
        store=Store(args.store)
        if args.operation=='extract':
            caps=[c for c in store.captures(args.tenant) if c.capture_id==args.capture_id]
            if len(caps)!=1:raise ContractError('Unknown or cross-tenant capture')
            page=extract(caps[0],store.body(caps[0]));result=asdict(page)
        elif args.operation=='match':
            pages=[page_from_json(strict_json(Path(p).read_text())) for p in args.page]
            for page in pages:verify_page(store,page)
            if len({p.capture.capture_id for p in pages})!=len(pages):raise ContractError('Duplicate capture')
            pack=RulePack.load(args.rules);matches,reports=match_pages(pack,pages)
            result={'schema_version':'1.0','kind':'StandaloneMatchResult','release_digest':pack.digest,
                    'input_capture_ids':[p.capture.capture_id for p in pages],
                    'matches':[asdict(m) for m in matches],'rule_evaluations':reports,
                    'canonical_admission':False,'send_allowed':False}
        else:
            data=strict_json(Path(args.bundle).read_text());validate_bundle(data)
            for raw in data['captures']:store.body(Capture(**raw))
            for cid in data['evaluated_capture_ids']:
                cap=next(Capture(**c) for c in data['captures'] if c['capture_id']==cid)
                page=PageEvidence(cap,[Surface(**s) for s in data['surfaces'] if s['capture_id']==cid],
                     [CommandResult(**c) for c in data['commands'] if c['command_id'].startswith('EXTRACT_') and c['input_ids']==[cid]])
                verify_page(store,page)
            if args.operation=='check':result={'valid':True,'capture_metadata_and_bytes_checked':True}
            else:
                from .core import Observation,Match,SupportLink
                result={'kind':'StandaloneClaimResult','as_of':args.as_of,'claims':[asdict(v) for v in resolve_claims(
                    [Observation(**x) for x in data['observations']],[Match(**x) for x in data['matches']],
                    [SupportLink(**x) for x in data['support_links']],[Capture(**x) for x in data['captures']],as_of=args.as_of)],
                    'historical_evaluation_only':True,'send_allowed':False}
        write_json(args.output,result)
        print(canonical({'operation':args.operation,'output':str(Path(args.output)),'network_attempts':0,'status':'SUCCEEDED'}))
        return 0
    except (ContractError,ValueError,TypeError,OSError,KeyError) as exc:
        print(f'{type(exc).__name__}: {exc}',file=sys.stderr);return 2
    finally:
        if store is not None:store.close()

if __name__=='__main__':raise SystemExit(main())
