from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ManufacturerBase(BaseModel):
    name: str = Field(..., example="Acme Textiles")
    pricing: Optional[str] = Field(
        None, example="USD 5–10 per kilogram", description="Free‑form pricing info"
    )
    production_capacity: Optional[int] = Field(
        None,
        ge=0,
        example=50000,
        description="Units produced per month",
    )
    certifications: Optional[List[str]] = Field(
        None,
        example=["ISO 9001", "OEKO‑Tex"],
        description="List of certification names",
    )

    @validator("certifications", each_item=True)
    def strip_cert(cls, v: str) -> str:
        return v.strip()


class ManufacturerCreate(ManufacturerBase):
    """All fields are optional except ``name`` – same as the UI requirements."""
    pass


class ManufacturerRead(ManufacturerBase):
    id: int

    class Config:
        orm_mode = True