"""
Data models for signature drift detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class RequestSignature:
    """
    Represents the canonical signature of an API request.
    The signature is a deterministic hash of the request payload
    (sorted keys, canonical JSON) and is used to detect drift.
    """
    endpoint: str
    signature: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DriftEvent:
    """
    Represents a detected signature drift event.
    
    Attributes:
        api_name: Identifier for the API service (e.g., "users-api", "payments-service")
        endpoint: The API endpoint path (e.g., "/v1/users")
        baseline_signature: The expected signature hash
        current_signature: The actual signature from the incoming request
        request_payload: The full request payload for investigation
        detected_at: Timestamp when the drift was detected
        details: Additional context (headers, query params, etc.)
    """
    api_name: str
    endpoint: str
    baseline_signature: str
    current_signature: str
    request_payload: Dict[str, Any]
    detected_at: datetime = field(default_factory=datetime.utcnow)
    details: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the drift event after initialization."""
        if not isinstance(self.request_payload, dict):
            raise TypeError("request_payload must be a dict")
        if not self.api_name:
            raise ValueError("api_name cannot be empty")
        if not self.endpoint:
            raise ValueError("endpoint cannot be empty")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a serializable dictionary."""
        return {
            "api_name": self.api_name,
            "endpoint": self.endpoint,
            "baseline_signature": self.baseline_signature,
            "current_signature": self.current_signature,
            "request_payload": self.request_payload,
            "detected_at": self.detected_at.isoformat(),
            "details": self.details,
        }

    @property
    def has_baseline(self) -> bool:
        """Check if this event has a valid baseline."""
        return self.baseline_signature != "__no_baseline__"

    @property
    def is_new_endpoint(self) -> bool:
        """Check if this is a drift event for a previously unknown endpoint."""
        return self.baseline_signature == "__no_baseline__"