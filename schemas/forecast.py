from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator

class ForecastRequest(BaseModel):
    """Request payload for a cost forecast."""
    horizon_days: int = Field(
        ...,
        description="Number of days to forecast. Must be one of 30, 60, or 90.",
        example=30,
        ge=30,
        le=90
    )

    @validator("horizon_days")
    def validate_horizon(cls, v: int) -> int:
        if v not in {30, 60, 90}:
            raise ValueError("horizon_days must be 30, 60, or 90")
        return v

class ForecastPoint(BaseModel):
    """A single day's forecasted cost with confidence interval."""
    date: date = Field(..., description="Date of the forecasted cost")
    cost: float = Field(..., description="Point estimate of the cost")
    lower_ci: float = Field(..., description="Lower bound of confidence interval")
    upper_ci: float = Field(..., description="Upper bound of confidence interval")

class ForecastResponse(BaseModel):
    """Response payload containing the full forecast."""
    horizon_days: int = Field(..., description="Requested forecast horizon")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the forecast was generated (UTC)"
    )
    points: List[ForecastPoint] = Field(
        ...,
        description="List of daily forecast points"
    )