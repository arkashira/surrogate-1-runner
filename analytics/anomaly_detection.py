"""
Anomaly detection utilities for finance cost monitoring.

This module provides a simple rolling‑statistics based anomaly detector
that can be used by the alerting system.  The implementation is
dependency‑free (no pandas or numpy) so it can run in the lightweight
surrogate‑1 environment.

Usage
-----
>>> from analytics.anomaly_detection import detect_anomalies
>>> data = [
...     {"timestamp": "2024-05-01T00:00:00Z", "cost": 100},
...     {"timestamp": "2024-05-01T01:00:00Z", "cost": 102},
...     {"timestamp": "2024-05-01T02:00:00Z", "cost": 98},
...     {"timestamp": "2024-05-01T03:00:00Z", "cost": 500},  # anomaly
... ]
>>> anomalies = detect_anomalies(data, window=3, threshold=2.5)
>>> anomalies[0]["timestamp"]
'2024-05-01T03:00:00Z'
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Dict, Any, Optional


@dataclass
class Anomaly:
    """Represents a detected anomaly."""
    timestamp: str
    cost: float
    mean: float
    std: float
    z_score: float


def _rolling_stats(
    costs: List[float], window: int
) -> List[Optional[Dict[str, float]]]:
    """
    Compute rolling mean and standard deviation for a list of costs.

    Parameters
    ----------
    costs : List[float]
        Sequence of cost values.
    window : int
        Size of the rolling window. Must be >= 1.

    Returns
    -------
    List[Optional[Dict[str, float]]]
        For each index i, returns a dict with 'mean' and 'std' if enough
        prior data exists, otherwise None.
    """
    if window < 1:
        raise ValueError("window must be >= 1")

    stats: List[Optional[Dict[str, float]]] = [None] * len(costs)
    for i in range(len(costs)):
        if i < window:
            # Not enough data to compute stats
            continue
        window_slice = costs[i - window : i]
        mean = sum(window_slice) / window
        # Compute population std deviation
        var = sum((x - mean) ** 2 for x in window_slice) / window
        std = var ** 0.5
        stats[i] = {"mean": mean, "std": std}
    return stats


def detect_anomalies(
    data: Iterable[Dict[str, Any]],
    *,
    window: int = 5,
    threshold: float = 3.0,
) -> List[Anomaly]:
    """
    Detect cost anomalies in a time‑series dataset.

    Parameters
    ----------
    data : Iterable[Dict[str, Any]]
        Each element must contain at least 'timestamp' and 'cost' keys.
        The iterable is consumed in order; it is assumed to be sorted by
        timestamp ascending.
    window : int, optional
        Rolling window size for computing mean and std. Default is 5.
    threshold : float, optional
        Z‑score threshold above which a point is considered anomalous.
        Default is 3.0.

    Returns
    -------
    List[Anomaly]
        List of detected anomalies in chronological order.
    """
    # Convert to list to allow multiple passes
    records = list(data)
    if not records:
        return []

    # Extract costs in order
    costs = [float(rec["cost"]) for rec in records]

    # Compute rolling stats
    stats = _rolling_stats(costs, window)

    anomalies: List[Anomaly] = []
    for idx, rec in enumerate(records):
        stat = stats[idx]
        if stat is None:
            # Not enough history to evaluate
            continue
        mean = stat["mean"]
        std = stat["std"]
        if std == 0:
            # Avoid division by zero; treat as no anomaly
            continue
        z = (costs[idx] - mean) / std
        if abs(z) >= threshold:
            anomalies.append(
                Anomaly(
                    timestamp=rec["timestamp"],
                    cost=costs[idx],
                    mean=mean,
                    std=std,
                    z_score=z,
                )
            )
    return anomalies