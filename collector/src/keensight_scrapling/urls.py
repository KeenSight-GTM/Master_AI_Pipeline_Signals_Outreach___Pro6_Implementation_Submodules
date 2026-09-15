from __future__ import annotations

import ipaddress
import re
import socket
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit, urlunsplit
from .core import ContractError, PolicyDenied


def normalize_url(value: str) -> str:
    value = value.strip()
    if not value or any(ord(x) < 33 for x in value) or "\\" in value:
        raise ContractError("Empty URL, whitespace, control characters, or backslash")
    if value.startswith("//"):
        value = "https:" + value
    elif "://" not in value:
        value = "https://" + value
    p = urlsplit(value)
    if p.scheme.lower() not in {"http", "https"} or not p.hostname or p.username is not None or p.password is not None:
        raise ContractError("Only HTTP(S) URLs without credentials are accepted")
    host = p.hostname.rstrip(".").encode("idna").decode("ascii").lower()
    if "%" in host:
        raise ContractError("Encoded host or IPv6 zone identifier")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not re.fullmatch(r"[a-z0-9.-]+", host) or any(not part or len(part) > 63 or part.startswith('-') or part.endswith('-') for part in host.split('.')):
            raise ContractError("Malformed hostname")
    try:
        port = p.port
    except ValueError as exc:
        raise ContractError("Invalid port") from exc
    if ":" in host:
        host = f"[{host}]"
    netloc = host if port is None or port == (443 if p.scheme.lower() == 'https' else 80) else f"{host}:{port}"
    return urlunsplit((p.scheme.lower(), netloc, p.path or "/", p.query, ""))


def origin(url: str) -> str:
    p = urlsplit(normalize_url(url))
    return f"{p.scheme}://{p.netloc}"


def link_url(base: str, value: str) -> str | None:
    try:
        joined = urljoin(base, value.strip())
        if urlsplit(joined).scheme not in {'http', 'https'}:
            return None
        return normalize_url(joined)
    except (ValueError, UnicodeError):
        return None


def host_match(url: str, pattern: str, *, exact: bool = False) -> bool:
    try:
        host = (urlsplit(url).hostname or "").rstrip(".").encode("idna").decode().lower()
        target = pattern.rstrip(".").encode("idna").decode().lower()
    except (ValueError, UnicodeError):
        return False
    return bool(host and target and (host == target or (not exact and host.endswith("." + target))))


@dataclass(frozen=True)
class NetworkPolicy:
    allowed_origins: tuple[str, ...]
    # Test-only: must be explicitly set through Python, never inferred from a URL.
    allow_loopback_test: bool = False

    def resolve(self, url: str) -> list[str]:
        url = normalize_url(url)
        p = urlsplit(url)
        if origin(url) not in self.allowed_origins:
            raise PolicyDenied("Origin not explicitly allowed")
        if p.port not in {None, 80, 443} and not self.allow_loopback_test:
            raise PolicyDenied("Nonstandard destination port")
        try:
            candidates = sorted({x[4][0] for x in socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == 'https' else 80), type=socket.SOCK_STREAM)})
        except socket.gaierror as exc:
            raise PolicyDenied("DNS resolution failed") from exc
        if not candidates:
            raise PolicyDenied("No destination addresses")
        for address in candidates:
            ip = ipaddress.ip_address(address)
            if (not ip.is_global or ip.is_multicast or ip.is_reserved or ip.is_unspecified) and not (self.allow_loopback_test and ip.is_loopback):
                raise PolicyDenied("Private, reserved or local destination")
        return candidates
