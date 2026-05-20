"""
A tiny, self‑contained metrics collector for validation runs.

The module keeps a single global dictionary that is updated by
`collect_validation_metrics`.  The state can be queried, persisted,
or reset.  All functions are intentionally simple so that the test
suite can exercise them in isolation.
"""

from __future__ import annotations

import json
from typing import Dict, Iterable, List, Mapping

# --------------------------------------------------------------------------- #
# Global state
# --------------------------------------------------------------------------- #
_metrics: Dict[str, int] = {
    "total_validations": 0,
    "passes": 0,
    "fails": 0,
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def collect_validation_metrics(
    validation_results: Iterable[Mapping[str, str]]
) -> Dict[str, int]:
    """
    Update the global metrics from an iterable of validation result dicts.

    Parameters
    ----------
    validation_results:
        Each item must expose a ``status`` key whose value is either
        ``"pass"`` or ``"fail"``.  The function is tolerant of missing
        keys – they simply do not affect the counters.

    Returns
    -------
    dict
        A *copy* of the updated metrics dictionary.
    """
    global _metrics

    for result in validation_results:
        _metrics["total_validations"] += 1
        status = result.get("status")
        if status == "pass":
            _metrics["passes"] += 1
        elif status == "fail":
            _metrics["fails"] += 1

    # A lightweight console log – useful for debugging but harmless in CI.
    print(
        f"[metrics] Total: {_metrics['total_validations']}, "
        f"Passes: {_metrics['passes']}, Fails: {_metrics['fails']}"
    )
    return _metrics.copy()


def get_validation_metrics() -> Dict[str, int]:
    """Return a *copy* of the current metrics."""
    return _metrics.copy()


def reset_metrics() -> None:
    """Reset all counters to zero."""
    global _metrics
    _metrics = {"total_validations": 0, "passes": 0, "fails": 0}
    print("[metrics] Reset to initial state")


def save_metrics_to_file(metrics: Mapping[str, int], filename: str = "metrics.json") -> None:
    """
    Persist a metrics snapshot to a JSON file.

    Parameters
    ----------
    metrics:
        Any mapping that can be JSON‑serialised (the default is the
        global `_metrics` dictionary).
    filename:
        Path to the file that will receive the JSON dump.
    """
    try:
        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(metrics, fp, indent=2)
        print(f"[metrics] Saved to {filename}")
    except OSError as exc:
        # In production you might want to log this; for tests we just
        # re‑raise so the failure surfaces.
        raise RuntimeError(f"Could not write metrics to {filename}") from exc