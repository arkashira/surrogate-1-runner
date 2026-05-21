from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Metrics:
    """
    Snapshot of a single run.
    """
    timestamp: datetime
    speed: float          # samples/second
    accuracy: float       # 0.0 – 1.0
    sample_count: int
    metric_name: Literal["speed", "accuracy"] = "speed"