"""
SQLAlchemy models for the Manufacturer domain.

* A manufacturer has a name, optional free‑form pricing text, and a numeric
  production capacity (units / month).
* Certifications are stored in a dedicated lookup table and linked with a
  many‑to‑many association – this is more normalized than a JSON column and
  lets us query “all manufacturers with ISO 9001” efficiently.
* A small ``to_dict`` helper is provided for fast API serialization when we
  bypass Pydantic (e.g., for background jobs).
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
)

Base = declarative_base()

# ----------------------------------------------------------------------
# Association table (many‑to‑many)
# ----------------------------------------------------------------------
manufacturer_certifications = Table(
    "manufacturer_certifications",
    Base.metadata,
    Column(
        "manufacturer_id",
        Integer,
        ForeignKey("manufacturers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "certification_id",
        Integer,
        ForeignKey("certifications.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# ----------------------------------------------------------------------
# Lookup table for certifications
# ----------------------------------------------------------------------
class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Certification id={self.id} name={self.name!r}>"

# ----------------------------------------------------------------------
# Core Manufacturer table
# ----------------------------------------------------------------------
class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    pricing = Column(Text, nullable=True)                     # free‑form description
    production_capacity = Column(Integer, nullable=True)     # units / month

    # relationship to Certification via the association table
    certifications: List[Certification] = relationship(
        "Certification",
        secondary=manufacturer_certifications,
        backref="manufacturers",
        lazy="joined",          # eager load for API speed
    )

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Return a JSON‑serialisable dict (used by FastAPI when we need raw dicts)."""
        return {
            "id": self.id,
            "name": self.name,
            "pricing": self.pricing,
            "production_capacity": self.production_capacity,
            "certifications": [c.name for c in self.certifications],
        }

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Manufacturer id={self.id} name={self.name!r} "
            f"capacity={self.production_capacity}>"
        )