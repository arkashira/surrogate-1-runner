from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class MarketSnapshotNormalized(BaseModel):
    """Normalized market snapshot record."""
    symbol: str = Field(..., description="Ticker symbol")
    bid: Optional[Decimal] = Field(None, description="Best bid")
    ask: Optional[Decimal] = Field(None, description="Best ask")
    last: Optional[Decimal] = Field(None, description="Last traded price")
    volume: Optional[Decimal] = Field(None, description="Trade volume")
    timestamp: datetime = Field(..., description="Event-time of snapshot")
    source: str = Field("market_snapshot", description="Source tag")
    extra: Dict[str, Any] = Field(default_factory=dict, description="Raw leftovers")

    @field_validator("bid", "ask", "last", "volume", mode="before")
    @classmethod
    def _to_decimal(cls, v: Any) -> Optional[Decimal]:
        if v is None:
            return None
        try:
            return Decimal(str(v))
        except Exception:
            return None


class ResearchCompleteEvent(BaseModel):
    """Envelope emitted when research connector finishes."""
    event_type: str = Field("research_complete", const=True)
    connector: str
    sequence: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    payload: MarketSnapshotNormalized
    metadata: Dict[str, Any] = Field(default_factory=dict)