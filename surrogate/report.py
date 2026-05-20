"""
surrogate.report
----------------

Core utilities for turning a list of *issue* dictionaries into a
human‑readable report.

The implementation is deliberately lightweight yet defensive:
* Missing keys are filled with sensible defaults.
* Unknown keys are preserved so callers can attach arbitrary metadata.
* All functions are pure and return new data structures – no hidden
  mutation occurs.

Public API
~~~~~~~~~~
* ``generate_report(issues: list[dict]) -> dict``
* ``summarize_issues(issues: list[dict]) -> dict``
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


# ----------------------------------------------------------------------
# Normalisation helpers
# ----------------------------------------------------------------------
def _normalize_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a shallow copy of *issue* where the three expected keys are
    guaranteed to exist.

    Expected keys (all optional):
        - ``type``      – category of the issue (default: ``"unknown"``)
        - ``severity``  – ``"low"``, ``"medium"``, ``"high"`` (default: ``"low"``)
        - ``message``   – free‑form description (default: ``""``)

    Any additional keys are copied unchanged.
    """
    # Start with the defaults, then overlay the supplied values.
    normalized: Dict[str, Any] = {
        "type": "unknown",
        "severity": "low",
        "message": "",
    }
    normalized.update(issue)          # preserves extra fields
    # Ensure the three canonical keys are present (they may have been
    # overwritten by ``issue`` already, which is fine).
    normalized.setdefault("type", "unknown")
    normalized.setdefault("severity", "low")
    normalized.setdefault("message", "")
    return normalized


# ----------------------------------------------------------------------
# Summarisation
# ----------------------------------------------------------------------
def summarize_issues(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Produce a high‑level aggregation of *issues*.

    Returned mapping:
        {
            "total":        int,                     # number of issues
            "by_type":      dict[str, int],          # type → count
            "by_severity":  dict[str, int],          # severity → count
            "has_errors":   bool,                    # any ``high`` severity?
        }
    """
    total = len(issues)
    type_counter: Counter = Counter()
    severity_counter: Counter = Counter()
    has_errors = False

    for raw in issues:
        issue = _normalize_issue(raw)
        type_counter[issue["type"]] += 1
        severity_counter[issue["severity"]] += 1
        if issue["severity"] == "high":
            has_errors = True

    return {
        "total": total,
        "by_type": dict(type_counter),
        "by_severity": dict(severity_counter),
        "has_errors": has_errors,
    }


# ----------------------------------------------------------------------
# Full report
# ----------------------------------------------------------------------
def generate_report(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Return the complete report structure expected by the test suite.

    The report contains:
        * ``summary`` – the output of :func:`summarize_issues`.
        * ``details`` – a list of *normalized* issue dictionaries,
          preserving the order in which they were supplied.
    """
    normalized = [_normalize_issue(i) for i in issues]
    summary = summarize_issues(normalized)
    return {"summary": summary, "details": normalized}