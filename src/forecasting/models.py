"""
Data models used by the forecasting engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple


@dataclass(frozen=True)
class CostRecord:
    """
    Represents a single cost entry for a cloud resource.

    Attributes
    ----------
    resource_type : str
        The type of the resource (e.g., 'compute', 'storage').
    location : str
        The geographic location of the resource (e.g., 'us-east-1').
    timestamp : datetime
        The timestamp of the cost record.
    cost : float
        The cost amount in USD.
    """
    resource_type: str
    location: str
    timestamp: datetime
    cost: float


@dataclass
class ForecastResult:
    """
    Result of a forecast for a specific period.

    Attributes
    ----------
    period_start : datetime
        The start of the forecast period.
    period_end : datetime
        The end of the forecast period.
    predicted_cost : float
        The predicted cost for the period.
    """
    period_start: datetime
    period_end: datetime
    predicted_cost: float

    def to_dict(self) -> Dict[str, str | float]:
        """Return a JSON‑serialisable representation."""
        return {
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "predicted_cost": round(self.predicted_cost, 2),
        }


# Helper type for internal grouping
GroupedKey = Tuple[str, str]  # (resource_type, location)