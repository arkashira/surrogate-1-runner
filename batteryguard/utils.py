"""Utility helpers for the BatteryGuard package."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

Metric = Tuple[datetime, float]

def load_metrics(file_path: Path) -> List[Metric]:
    """
    Load battery health metrics from a JSON file.

    The JSON file must be a list of objects with keys:
        - timestamp: ISO‑8601 string
        - health:   float in [0, 100]

    Returns a list of (datetime, health) tuples sorted chronologically.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    metrics: List[Metric] = []
    for entry in data:
        try:
            ts = datetime.fromisoformat(entry["timestamp"])
            h = float(entry["health"])
            if not 0.0 <= h <= 100.0:
                raise ValueError
            metrics.append((ts, h))
        except Exception as exc:
            raise ValueError(
                f"Invalid metric entry {entry!r}: {exc}"
            ) from exc

    metrics.sort(key=lambda x: x[0])
    return metrics


def filter_last_n_days(
    metrics: List[Metric], days: int = 7
) -> List[Metric]:
    """Return metrics from the last `days` days relative to the latest timestamp."""
    if not metrics:
        return []

    latest_ts = metrics[-1][0]
    cutoff = latest_ts - timedelta(days=days)
    return [(ts, h) for ts, h in metrics if ts >= cutoff]