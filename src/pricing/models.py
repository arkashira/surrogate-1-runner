from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, validator, ValidationError


class PricingData(BaseModel):
    """
    Full‑featured schema used by the production ingest pipeline.
    All fields are required – if any are missing or of the wrong type a
    `pydantic.ValidationError` is raised.
    """
    product_id: str = Field(..., description="Unique identifier of the product")
    market: str = Field(..., description="Market code, e.g. 'US'")
    competitor: str = Field(..., description="Competitor name")
    price: float = Field(..., gt=0, description="Price offered by the competitor")
    currency: Literal["USD", "EUR", "GBP", "JPY", "CAD"] = Field(
        ..., description="ISO‑4217 currency code"
    )
    timestamp: datetime = Field(
        ..., description="When the price was observed (ISO‑8601 string accepted)"
    )

    # ------------------------------------------------------------------
    # Extra validation that is not covered by the simple field definitions
    # ------------------------------------------------------------------
    @validator("timestamp", pre=True)
    def parse_timestamp(cls, v):
        """Accept both datetime objects and ISO‑8601 strings."""
        if isinstance(v, datetime):
            return v
        return datetime.fromisoformat(v.replace("Z", "+00:00"))

    @validator("price")
    def price_must_be_reasonable(cls, v):
        """Guard against obviously bogus prices."""
        if v > 1_000_000:
            raise ValueError("price is unreasonably large")
        return v