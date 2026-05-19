from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class MatchBase(BaseModel):
    """Base fields shared by request and response schemas."""
    investor_name: str = Field(..., description="Display name of the matched investor")
    stage_focus: str = Field(..., description="Stage focus of the investor (e.g., Seed, Series A)")
    ticket_range: str = Field(..., description="Typical ticket size (e.g., $100k-$500k)")
    score: float = Field(..., ge=0, le=100, description="Match score, higher is better")


class MatchOut(MatchBase):
    """Schema returned by the matches-list endpoint."""
    id: int = Field(..., description="Unique identifier of the match")
    provider_id: int = Field(..., description="Identifier of the provider who owns the match")
    investor_id: int = Field(..., description="Unique ID of the investor in the system")

    # Enable ORM mode for SQLAlchemy compatibility
    model_config = ConfigDict(from_attributes=True)


class InteractionCreate(BaseModel):
    """Payload for signalling interest in a match."""
    provider_id: int = Field(..., description="Identifier of the provider signalling interest")
    match_id: int = Field(..., description="Identifier of the match being signalled")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of interaction")


class InteractionOut(InteractionCreate):
    """Response schema after successfully signalling interest."""
    id: int
    model_config = ConfigDict(from_attributes=True)