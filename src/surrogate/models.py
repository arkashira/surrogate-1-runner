from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class Anomaly:
    """
    Representation of a cost anomaly returned by the API.
    All fields are typed; optional fields default to `None`.
    """

    id: str
    timestamp: datetime
    amount: float
    # Add any other fields you expect from the API here.
    # Example:
    # description: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "Anomaly":
        """
        Helper that converts the raw JSON dict into an `Anomaly`.
        Handles the timestamp conversion from ISO‑8601 string to `datetime`.
        """
        return Anomaly(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
            amount=float(data["amount"]),
            # map other fields here
        )