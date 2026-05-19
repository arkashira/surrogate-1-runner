"""
Message model for surrogate‑1.

The model includes a ``confidence_score`` field (0‑100) representing
the system's confidence that a message is high‑impact. The field is
included in ``to_dict`` serialization throughout the codebase.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


def _clamp_confidence(value: int) -> int:
    """Clamp confidence scores to the inclusive range 0-100."""
    return max(0, min(100, value))


@dataclass
class Message:
    """
    Core representation of a chat/message record.

    Attributes
    ----------
    id: str
        Unique identifier for the message.
    text: str
        Raw message content.
    author: str
        Username or identifier of the message sender.
    timestamp: datetime
        When the message was created.
    is_high_impact: bool
        Flag set by downstream logic when the message meets high‑impact
        criteria (keywords, owner users, etc.).
    confidence_score: int
        Confidence (0-100) that the message is high‑impact. Defaults to ``0``
        and is clamped to the valid range.
    """

    id: str
    text: str
    author: str
    timestamp: datetime
    is_high_impact: bool = False
    confidence_score: int = field(default=0)

    def __post_init__(self) -> None:
        """Validate and clamp confidence_score after initialization."""
        object.__setattr__(self, 'confidence_score', _clamp_confidence(self.confidence_score))

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the message to a plain dict suitable for JSON encoding
        or downstream processing.

        Returns
        -------
        dict
            Mapping of field names to serializable values.
        """
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "timestamp": self.timestamp.isoformat(),
            "is_high_impact": self.is_high_impact,
            "confidence_score": self.confidence_score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """
        Construct a Message instance from a dictionary (e.g., loaded from JSON).
        Missing fields default to safe values.

        Parameters
        ----------
        data: dict
            Source mapping containing at least the required fields.

        Returns
        -------
        Message
        """
        return cls(
            id=data["id"],
            text=data["text"],
            author=data["author"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            is_high_impact=data.get("is_high_impact", False),
            confidence_score=data.get("confidence_score", 0),
        )