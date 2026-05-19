"""
Metric utilities for the surrogate‑1 synthetic data generator.

Provides:
* `Metric` – immutable representation of a single data point.
* Low‑level generators (`generate_steady`, `generate_spike`, `generate_custom`).
* Small helper `datetime_range` used by both metrics and events.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Iterable, List, Tuple

# --------------------------------------------------------------------------- #
#  Core data object
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class Metric:
    """A single metric data point, ready for JSON‑serialisation."""
    service: str
    name: str
    timestamp: int          # epoch seconds
    value: float
    tags: Tuple[Tuple[str, str], ...] = ()

    def to_dict(self) -> dict:
        """Return a dict compatible with Datadog’s metric ingest API."""
        return {
            "service": self.service,
            "metric": self.name,
            "points": [[self.timestamp, self.value]],
            "tags": [f"{k}:{v}" for k, v in self.tags],
        }

# --------------------------------------------------------------------------- #
#  Timestamp helpers
# --------------------------------------------------------------------------- #
def _now_ts() -> int:
    """Current epoch seconds (int)."""
    return int(time.time())


def datetime_range(
    start: datetime, end: datetime, step: timedelta
) -> Iterable[datetime]:
    """
    Yield ``datetime`` objects from *start* to *end* inclusive,
    stepping by ``step``.  Works with both naive and timezone‑aware
    ``datetime`` instances.
    """
    cur = start
    while cur <= end:
        yield cur
        cur += step


# --------------------------------------------------------------------------- #
#  Low‑level metric generators
# --------------------------------------------------------------------------- #
def generate_steady(
    service: str,
    name: str,
    start: datetime,
    end: datetime,
    interval: timedelta,
    base: float = 100.0,
    jitter: float = 5.0,
    tags: Tuple[Tuple[str, str], ...] = (),
) -> List[Metric]:
    """
    Produce a “steady‑state” series: values hover around ``base`` with
    optional random jitter.
    """
    metrics: List[Metric] = []
    for ts in datetime_range(start, end, interval):
        value = base + random.uniform(-jitter, jitter)
        metrics.append(
            Metric(service, name, int(ts.timestamp()), value, tags)
        )
    return metrics


def generate_spike(
    service: str,
    name: str,
    start: datetime,
    end: datetime,
    interval: timedelta,
    base: float = 100.0,
    spike_value: float = 500.0,
    spike_chance: float = 0.02,
    jitter: float = 5.0,
    tags: Tuple[Tuple[str, str], ...] = (),
) -> List[Metric]:
    """
    Same as ``generate_steady`` but with occasional high‑value spikes.
    ``spike_chance`` is the per‑point probability of a spike.
    """
    metrics: List[Metric] = []
    for ts in datetime_range(start, end, interval):
        if random.random() < spike_chance:
            value = spike_value
        else:
            value = base + random.uniform(-jitter, jitter)
        metrics.append(
            Metric(service, name, int(ts.timestamp()), value, tags)
        )
    return metrics


def generate_custom(
    service: str,
    name: str,
    generator: Callable[[int], float],
    start: datetime,
    end: datetime,
    interval: timedelta,
    tags: Tuple[Tuple[str, str], ...] = (),
) -> List[Metric]:
    """
    User‑supplied ``generator`` receives the epoch timestamp (int) and
    must return a float.  This makes it trivial to plug in sinusoidal,
    exponential‑decay, or any domain‑specific pattern.
    """
    metrics: List[Metric] = []
    for ts in datetime_range(start, end, interval):
        value = generator(int(ts.timestamp()))
        metrics.append(
            Metric(service, name, int(ts.timestamp()), value, tags)
        )
    return metrics