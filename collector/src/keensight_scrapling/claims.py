from __future__ import annotations

from collections import defaultdict
from typing import Iterable
from .core import Capture, Match, Observation, SupportLink, ClaimView, ContractError, identity, canonical, instant, expires_at
from .urls import origin


def observation_candidates(captures: Iterable[Capture], matches: Iterable[Match]) -> tuple[list[Observation],list[SupportLink]]:
    caps = {c.capture_id:c for c in captures}
    observations, support = {}, {}
    for match in matches:
        if match.capture_id not in caps:
            raise ContractError('Match references an unknown capture')
        cap = caps[match.capture_id]
        if match.authority not in {'APPROVED','CANDIDATE'} or match.predicate not in {'vendor.present','vendor.mentioned'}:
            raise ContractError('Unsupported match authority or predicate')
        # Scope is the sampled origin in this mode. It is NOT proof of private
        # company use or complete website coverage. Subject binding stays explicit.
        scope = identity('scope',origin(cap.url),cap.mode,'SAMPLED_PUBLIC_ORIGIN')
        target = {'product_id':match.product_id}
        nature = 'DIRECT_OBSERVATION'
        key = identity('claim',cap.tenant_id,cap.subject_id,match.predicate,nature,scope,target,None)
        oid = identity('observation',key,cap.capture_id,cap.source_id,'OBSERVED',match.object_value)
        obs = Observation(oid,key,cap.tenant_id,cap.subject_id,match.predicate,target,scope,nature,'OBSERVED',match.object_value,
                          cap.capture_id,cap.source_id,identity('sourcegroup',cap.tenant_id,cap.subject_id,cap.source_id,origin(cap.url)),
                          cap.observed_at,expires_at(cap.observed_at,cap.source_ttl_seconds))
        if oid in observations and observations[oid] != obs:
            raise ContractError('Observation identity collision')
        observations[oid] = obs
        support[(oid,match.match_id)] = SupportLink(oid,match.match_id)
    return sorted(observations.values(),key=lambda o:o.observation_id),sorted(support.values(),key=lambda s:(s.observation_id,s.match_id))


def resolve_claims(observations: Iterable[Observation], matches: Iterable[Match], support: Iterable[SupportLink],
                   captures: Iterable[Capture], *, as_of: str,
                   allowed_rule_digests: set[str] | None = None,
                   revoked_capture_ids: set[str] | None = None) -> list[ClaimView]:
    """Display one row per claim, without deleting any observation or support.

    Same-site pages, repeated scans and overlapping detectors do NOT count as
    independent corroboration. No noisy-OR, vote counting, maximum confidence,
    or candidate-to-approved promotion is performed.
    """
    now = instant(as_of)
    obsmap = {o.observation_id:o for o in observations}
    matchmap = {m.match_id:m for m in matches}
    caps = {c.capture_id:c for c in captures}
    links = defaultdict(set)
    revoked = revoked_capture_ids or set()
    for link in support:
        if link.observation_id not in obsmap or link.match_id not in matchmap:
            raise ContractError('Dangling support link')
        o, m = obsmap[link.observation_id],matchmap[link.match_id]
        if (o.capture_id,o.predicate,o.target.get('product_id'),o.object_value) != (m.capture_id,m.predicate,m.product_id,m.object_value):
            raise ContractError('Support from a different capture, target, predicate, or value')
        links[o.observation_id].add(m.match_id)
    groups = defaultdict(list)
    for o in obsmap.values():
        cap = caps.get(o.capture_id)
        if cap is None or (cap.tenant_id,cap.subject_id)!=(o.tenant_id,o.subject_id):
            raise ContractError('Observation has a missing or cross-account capture')
        if instant(o.observed_at) > now:
            continue
        groups[o.claim_key].append(o)
    views=[]
    for key, rows in sorted(groups.items()):
        eligible, all_matches, usable_rows, shadow = set(),set(),[],False
        for o in rows:
            mids = links[o.observation_id]
            all_matches.update(mids)
            cap = caps[o.capture_id]
            usable = (o.state=='OBSERVED' and cap.complete and o.capture_id not in revoked and instant(o.expires_at)>now)
            active = {mid for mid in mids if (allowed_rule_digests is None or matchmap[mid].rule_digest in allowed_rule_digests)}
            good = {mid for mid in active if matchmap[mid].authority=='APPROVED'} if usable else set()
            shadow |= bool(usable and active-good)
            if good:
                eligible.update(good)
                usable_rows.append(o)
        values = {canonical(o.object_value):o.object_value for o in usable_rows}
        status = 'CONFLICT' if len(values)>1 else 'SUPPORTED' if values else 'CANDIDATE' if shadow else 'UNKNOWN'
        views.append(ClaimView(key,rows[0].predicate,rows[0].target,status,next(iter(values.values())) if len(values)==1 else None,
                               sorted(o.observation_id for o in rows),sorted(all_matches),sorted(eligible),
                               sorted({matchmap[m].rule_id for m in all_matches}),len({o.capture_id for o in usable_rows}),
                               len({o.source_group for o in usable_rows}),len({matchmap[m].evidence_key for m in eligible}),
                               tenant_id=rows[0].tenant_id, subject_id=rows[0].subject_id, scope_id=rows[0].scope_id,
                               origins=sorted({origin(caps[o.capture_id].url) for o in rows}),
                               observed_at=max((o.observed_at for o in usable_rows),key=instant,default=None),
                               expires_at=max((o.expires_at for o in usable_rows),key=instant,default=None)))
    return views
