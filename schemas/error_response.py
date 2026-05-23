from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Represents an error response for invalid requests."""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Timestamp of the error in ISO 8601 format")

    @classmethod
    def create(cls, error: str, details: Optional[str] = None) -> "ErrorResponse":
        """Factory method to create an ErrorResponse with auto-generated timestamp."""
        return cls(
            error=error,
            details=details,
            timestamp=datetime.now(timezone.utc).isoformat()
        )