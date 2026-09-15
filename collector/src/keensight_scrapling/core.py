from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any


class ContractError(ValueError):
    """Malformed or incompatible record; never silently repaired."""


class PolicyDenied(ContractError):
    pass


class DependencyUnavailable(RuntimeError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def identity(prefix: str, *values: Any) -> str:
    return prefix + "_" + hashlib.sha256(canonical(values).encode()).hexdigest()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def instant(value: str) -> datetime:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", value):
        raise ContractError("Expected a UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ContractError("Invalid UTC timestamp") from exc
    return parsed


def expires_at(observed_at: str, ttl_seconds: int) -> str:
    if isinstance(ttl_seconds, bool) or not isinstance(ttl_seconds, int) or ttl_seconds <= 0:
        raise ContractError("TTL must be a positive integer")
    return (instant(observed_at) + timedelta(seconds=ttl_seconds)).isoformat().replace("+00:00", "Z")


def strict_json(text: str) -> Any:
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ContractError(f"Duplicate JSON key: {k}")
            out[k] = v
        return out
    def bad(value):
        raise ContractError(f"Non-finite JSON number: {value}")
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=bad)
    except (ValueError, TypeError) as exc:
        raise ContractError(str(exc)) from exc


@dataclass(frozen=True)
class Capture:
    capture_id: str
    tenant_id: str
    subject_id: str
    run_id: str
    url: str
    observed_at: str
    mode: str
    status_code: int
    body_sha256: str
    body_path: str
    headers: dict[str, str]
    complete: bool
    source_id: str = "source:public-website"
    limitations: tuple[str, ...] = ()
    source_ttl_seconds: int = 2592000


@dataclass(frozen=True)
class Surface:
    surface_id: str
    capture_id: str
    command_id: str
    kind: str
    locator: str
    value: str
    context: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class CommandResult:
    command_id: str
    status: str
    input_ids: list[str] = field(default_factory=list)
    output_ids: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class PageEvidence:
    capture: Capture
    surfaces: list[Surface]
    commands: list[CommandResult]


@dataclass(frozen=True)
class Match:
    match_id: str
    rule_id: str
    rule_digest: str
    release_digest: str
    authority: str
    capture_id: str
    surface_id: str
    branch: str
    predicate: str
    product_id: str
    object_value: Any
    evidence_key: str
    rule_evidence_key: str
    authored_confidence: float | None


@dataclass(frozen=True)
class Observation:
    observation_id: str
    claim_key: str
    tenant_id: str
    subject_id: str
    predicate: str
    target: dict[str, str]
    scope_id: str
    nature: str
    state: str
    object_value: Any
    capture_id: str
    source_id: str
    source_group: str
    observed_at: str
    expires_at: str


@dataclass(frozen=True)
class SupportLink:
    observation_id: str
    match_id: str


@dataclass
class ClaimView:
    claim_key: str
    predicate: str
    target: dict[str, str]
    status: str
    object_value: Any
    observation_ids: list[str]
    supporting_match_ids: list[str]
    eligible_match_ids: list[str]
    rule_ids: list[str]
    capture_count: int
    source_group_count: int
    evidence_count: int
    confidence: None = None
    confidence_policy: str = "NOT_COMBINED"


def record(value: Any) -> dict:
    return asdict(value)
