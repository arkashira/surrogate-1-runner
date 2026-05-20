from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator

class ConversionRecord(BaseModel):
    price: float
    conversions: int

class PriceRange(BaseModel):
    min: float
    max: float
    step: float

    @validator("step")
    def step_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("step must be positive")
        return v

class SimulationRequest(BaseModel):
    historical_conversions: List[ConversionRecord]
    price_range: PriceRange

    @validator("historical_conversions")
    def must_have_at_least_one_record(cls, v):
        if not v:
            raise ValueError("historical_conversions must contain at least one record")
        return v

class SimulationResultItem(BaseModel):
    price: float
    estimated_revenue: float
    conversion_rate: float