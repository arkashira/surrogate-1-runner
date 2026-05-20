from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

@dataclass(frozen=True, slots=True)
class Signature:
    """Canonical representation of an API request for drift detection."""
    method: str                     # e.g. "GET", "POST"
    path: str                       # e.g. "/api/v1/users"
    headers: Dict[str, str] = field(default_factory=dict)   # canonical header name → value

    @staticmethod
    def from_raw(method: str, path: str, header_str: str) -> "Signature":
        """
        Helper used when reading the Redis baseline where headers are stored as a
        comma‑separated list of ``name=value`` pairs (legacy format from the first
        proposal).  New deployments should store JSON, but we keep this for
        backward compatibility.
        """
        hdrs: Dict[str, str] = {}
        for pair in filter(None, header_str.split(',')):
            if '=' in pair:
                k, v = pair.split('=', 1)
                hdrs[k.strip().lower()] = v.strip()
            else:                                   # legacy “just a name” case
                hdrs[pair.strip().lower()] = ''
        return Signature(method=method.upper(), path=path, headers=hdrs)