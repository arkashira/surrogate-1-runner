from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json

class AuditLogEntry(BaseModel):
    """Immutable record of LLM prompt/response interactions with execution context.

    Attributes:
        timestamp: ISO 8601 formatted UTC timestamp of record creation
        model_version: Version identifier of the LLM model used
        execution_environment: Dictionary of environment details
        prompt: Original user/system prompt
        response: Generated LLM response
        metadata: Optional additional context (e.g., user ID, session ID)
    """
    timestamp: str = datetime.utcnow().isoformat()
    model_version: str
    execution_environment: Dict[str, Any]
    prompt: str
    response: str
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
        frozen = True  # Enforce immutability
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_json(self) -> str:
        """Serialize to tamper-evident JSON string."""
        return json.dumps(self.dict(), sort_keys=True)

    def __eq__(self, other):
        if not isinstance(other, AuditLogEntry):
            return False
        return self.dict() == other.dict()