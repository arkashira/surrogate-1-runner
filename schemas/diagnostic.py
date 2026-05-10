from datetime import datetime
from pydantic import BaseModel, Field, validator

class DiagnosticPayload(BaseModel):
    """
    Pydantic model for an IoT diagnostic report.
    All fields are required; lengths are capped to protect the DB and
    to keep the payload small.
    """
    device_id: str = Field(..., min_length=1, max_length=64,
                           description="Unique identifier of the device")
    error_code: str = Field(..., min_length=1, max_length=32,
                            description="Numeric or textual error code")
    error_message: str = Field(..., min_length=1, max_length=1024,
                               description="Human‑readable error message")
    timestamp: datetime = Field(
        ...,
        description="ISO 8601 timestamp of the error",
        example="2023-05-01T12:00:00Z",
    )
    protocol_version: str = Field(..., min_length=1, max_length=16,
                                  description="Protocol version used by the device")

    @validator("timestamp", pre=True)
    def _parse_timestamp(cls, v):
        """
        Accept either a datetime instance or an ISO‑8601 string.
        """
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("timestamp must be a valid ISO 8601 string")
        return v