"""
Audit‑log data model.

The model is intentionally simple – a single dataclass that can be
converted to/from JSON easily.  The `now()` helper returns an ISO‑8601
UTC timestamp, which is what the rest of the system expects.
"""

from __future__ import annotations

import dataclasses
import datetime
import json
from typing import Any, Dict, Optional

@dataclasses.dataclass(frozen=True)
class AuditEntry:
    """A single audit‑log entry."""

    timestamp: str
    service: str
    cluster: str
    action: str
    details: Dict[str, Any]

    @staticmethod
    def now() -> str:
        """Return current UTC timestamp in ISO‑8601 format."""
        return datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc
        ).isoformat()

    @classmethod
    def create(
        cls,
        service: str,
        cluster: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> "AuditEntry":
        """Convenience constructor that stamps the entry with the current time."""
        return cls(
            timestamp=cls.now(),
            service=service,
            cluster=cluster,
            action=action,
            details=details or {},
        )

    def to_json(self) -> str:
        """Return a JSON string suitable for a log line."""
        return json.dumps(dataclasses.asdict(self), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_line: str) -> "AuditEntry":
        """Parse a JSON line back into an AuditEntry."""
        data = json.loads(json_line)
        return cls(**data)