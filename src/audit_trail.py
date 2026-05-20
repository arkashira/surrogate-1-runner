from datetime import datetime
from typing import Any, Dict, List, Optional

class AuditEvent:
    """Represents a single event in the audit trail."""

    def __init__(
        self,
        timestamp: datetime,
        event_type: str,
        user_id: str,
        decision_id: str,
        details: Dict[str, Any],
        model_version: Optional[str] = None,
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None,
        compliance_flags: Optional[List[str]] = None,
    ):
        self.timestamp = timestamp
        self.event_type = event_type
        self.user_id = user_id
        self.decision_id = decision_id
        self.details = details
        self.model_version = model_version
        self.input_data = input_data
        self.output_data = output_data
        self.compliance_flags = compliance_flags if compliance_flags is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """Converts the AuditEvent to a dictionary for storage or logging."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "user_id": self.user_id,
            "decision_id": self.decision_id,
            "details": self.details,
            "model_version": self.model_version,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "compliance_flags": self.compliance_flags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEvent":
        """Creates an AuditEvent from a dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            event_type=data["event_type"],
            user_id=data["user_id"],
            decision_id=data["decision_id"],
            details=data["details"],
            model_version=data.get("model_version"),
            input_data=data.get("input_data"),
            output_data=data.get("output_data"),
            compliance_flags=data.get("compliance_flags"),
        )

class AuditTrail:
    """Manages the audit trail for LLM-based decisions."""

    def __init__(self):
        self.events: List[AuditEvent] = []

    def record_event(self, event: AuditEvent):
        """Records a new audit event."""
        self.events.append(event)

    def get_events_by_decision_id(self, decision_id: str) -> List[AuditEvent]:
        """Retrieves all events associated with a specific decision ID."""
        return [event for event in self.events if event.decision_id == decision_id]

    def get_all_events(self) -> List[AuditEvent]:
        """Retrieves all recorded events."""
        return self.events

    def search_events(self, query: str, field: str = "details") -> List[AuditEvent]:
        """Searches events based on a query string in a specified field."""
        # This is a basic search; a real implementation might use a more robust search engine.
        matching_events = []
        for event in self.events:
            if hasattr(event, field) and getattr(event, field) is not None:
                if isinstance(getattr(event, field), str):
                    if query.lower() in getattr(event, field).lower():
                        matching_events.append(event)
                elif isinstance(getattr(event, field), dict):
                    for key, value in getattr(event, field).items():
                        if isinstance(value, str) and query.lower() in value.lower():
                            matching_events.append(event)
                            break  # Found a match in this event's details
        return matching_events

    def export_to_dict(self) -> List[Dict[str, Any]]:
        """Exports the entire audit trail as a list of dictionaries."""
        return [event.to_dict() for event in self.events]

    @classmethod
    def import_from_dict(cls, data: List[Dict[str, Any]]) -> "AuditTrail":
        """Imports an audit trail from a list of dictionaries."""
        audit_trail = cls()
        for event_data in data:
            audit_trail.record_event(AuditEvent.from_dict(event_data))
        return audit_trail