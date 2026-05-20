"""Domain model for an idle‑resource alert."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict


@dataclass(frozen=True, slots=True)
class IdleResourceAlert:
    """A single recommendation that an EC2 instance is under‑utilised."""

    resource_id: str
    resource_type: str
    current_instance_type: str
    recommended_instance_type: str
    current_utilization: float          # average CPU % over the look‑back window
    estimated_savings: float            # USD per hour
    region: str
    timestamp: datetime
    idle_duration_hours: float
    reason: str

    # ------------------------------------------------------------------
    # Helper – serialise to a plain dict (e.g. for JSON, SNS, S3, etc.)
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, object]:
        payload = asdict(self)
        payload["timestamp"] = self.timestamp.isoformat()
        return payload