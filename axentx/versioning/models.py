from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


SummaryId = str  # alias for readability; you can replace with a proper ORM PK type later


@dataclass(frozen=True, slots=True)
class SummaryVersion:
    """Immutable representation of a single version of a summary."""
    version: int
    timestamp: str          # ISO‑8601 UTC, e.g. "2026-05-11T12:34:56.789Z"
    content: str
    note: Optional[str] = None

    @staticmethod
    def now(content: str, version: int, note: Optional[str] = None) -> "SummaryVersion":
        """Factory that stamps the current UTC time."""
        ts = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
        return SummaryVersion(version=version, timestamp=ts, content=content, note=note)

    def to_dict(self) -> Dict[str, Any]:
        """Serialisable dict for JSON storage."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SummaryVersion":
        return SummaryVersion(**data)