"""
Alert engine data models.

* `Severity` – an ordered IntEnum so that comparisons (>, >=) work naturally.
* `Alert` – the core representation used throughout the engine.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class Severity(enum.IntEnum):
    """Ordered severity levels (low → high)."""

    INFO = 0
    LOW = 1          # synonym for INFO‑level noise
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def from_str(cls, value: str) -> "Severity":
        """Case‑insensitive conversion from a string to ``Severity``."""
        mapping = {
            "info": cls.INFO,
            "low": cls.LOW,
            "medium": cls.MEDIUM,
            "high": cls.HIGH,
            "critical": cls.CRITICAL,
        }
        try:
            return mapping[value.lower()]
        except KeyError as exc:
            raise ValueError(f"Unknown severity string: {value!r}") from exc


@dataclass
class Alert:
    """
    Core alert representation.

    Attributes
    ----------
    id : str
        Unique identifier (UUID, monitoring‑system ID, …).
    service : str
        Name of the service that emitted the alert.
    severity : Severity
        Urgency level.
    message : str
        Human‑readable description.
    retries : int, default 0
        Number of automatic retry attempts already performed.
    timeout : bool, default False
        True if the alert originated from a timeout condition.
    metadata : dict, default {}
        Arbitrary key/value pairs – e.g. ``log_url``, ``dashboard_url``.
    """

    id: str
    service: str
    severity: Severity
    message: str
    retries: int = 0
    timeout: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    # --------------------------------------------------------------------- #
    # Helper constructors
    # --------------------------------------------------------------------- #
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Alert":
        """
        Build an ``Alert`` from a plain dict (e.g. JSON payload).

        Expected keys: ``id``, ``service``, ``severity``, ``message``.
        Optional keys: ``retries``, ``timeout``, ``metadata``.
        """
        return cls(
            id=data["id"],
            service=data["service"],
            severity=Severity.from_str(data["severity"]),
            message=data["message"],
            retries=int(data.get("retries", 0)),
            timeout=bool(data.get("timeout", False)),
            metadata=data.get("metadata", {}),
        )