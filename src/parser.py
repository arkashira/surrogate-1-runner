import json
import re
from typing import Dict, Optional
from .model import DiagnosticOutput

# ----------------------------------------------------------------------
# 1️⃣  Regex patterns (same as Candidate 1, but compiled once)
# ----------------------------------------------------------------------
_REGEX_PATTERNS: Dict[str, re.Pattern] = {
    "resource_usage": re.compile(r"Resource\s*Usage:\s*(.+)", re.IGNORECASE),
    "logs": re.compile(r"Logs:\s*(.+)", re.IGNORECASE),
    "config_diff": re.compile(r"Config\s*Diff:\s*(.+)", re.IGNORECASE),
}


def _parse_with_regex(text: str) -> DiagnosticOutput:
    """Fallback parser – works on the free‑form logs used in the unit tests."""
    data = {}
    for key, pat in _REGEX_PATTERNS.items():
        m = pat.search(text)
        data[key] = m.group(1).strip() if m else None
    return DiagnosticOutput(**data)


def _parse_json(text: str) -> Optional[DiagnosticOutput]:
    """If the whole payload is valid JSON we can decode it directly."""
    try:
        payload = json.loads(text)
        # Accept both camelCase and snake_case keys
        return DiagnosticOutput(
            resource_usage=payload.get("resource_usage") or payload.get("resourceUsage"),
            logs=payload.get("logs"),
            config_diff=payload.get("config_diff") or payload.get("configDiff"),
        )
    except json.JSONDecodeError:
        return None


def parse_diagnostic(text: str) -> DiagnosticOutput:
    """
    Public entry point.
    1️⃣ Try JSON → 2️⃣ Regex fallback → 3️⃣ Return a DiagnosticOutput with whatever we got.
    """
    diag = _parse_json(text)
    if diag:
        return diag
    return _parse_with_regex(text)