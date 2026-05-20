# -------------------------------------------------
# SQLAlchemy model for the “accounts” table.
# -------------------------------------------------
from __future__ import annotations

from typing import Any, Dict

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    JSON,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

# ----------------------------------------------------------------------
# Base class – keep a single metadata object so migrations can be
# generated reliably across the whole code‑base.
# ----------------------------------------------------------------------
Base = declarative_base()


class Account(Base):
    """
    Represents a customer / user account.

    Key new feature:
        * ``bulk_low_threshold`` – an **integer percentage** (10‑30) that
          tells the system when to raise a “low bulk‑credit” alert.
          Stored as an integer because percentages are discrete and
          easier to compare/validate than floating‑point numbers.
    """

    __tablename__ = "accounts"

    # ------------------------------------------------------------------
    # Core columns – keep the original fields and add the new one.
    # ------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Business‑critical identifiers – unique and non‑null.
    name = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)

    # Operational flags / balances.
    is_active = Column(Boolean, default=True, nullable=False)
    credit_balance = Column(Float, default=0.0, nullable=False)

    # JSON blob for any legacy or future‑proof settings.
    settings = Column(JSON, nullable=False, default=dict)

    # --------------------------------------------------------------
    # New column – bulk low‑threshold (percentage of bulk credit usage
    # that triggers an alert).  Stored as an integer for exact range
    # checking and to avoid floating‑point rounding issues.
    # --------------------------------------------------------------
    bulk_low_threshold = Column(
        Integer,
        nullable=False,
        default=20,          # sensible default = 20 %
        server_default="20",  # ensures DB‑side default for migrations
    )

    # ------------------------------------------------------------------
    # Validation – guarantees the value stays inside the business‑rule
    # window (10 % … 30 %).  Raises early, before the object is flushed.
    # ------------------------------------------------------------------
    @validates("bulk_low_threshold")
    def _validate_bulk_low_threshold(self, key: str, value: Any) -> int:
        if not isinstance(value, int):
            raise ValueError("bulk_low_threshold must be an integer percentage")
        if not 10 <= value <= 30:
            raise ValueError("bulk_low_threshold must be between 10 and 30 (inclusive)")
        return value

    # ------------------------------------------------------------------
    # Helper methods – JSON‑friendly conversion for API layers.
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the model to a plain‑dict.  All fields that are part of the
        public API are included, making it easy for FastAPI / Flask /
        GraphQL resolvers to return a clean payload.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "credit_balance": self.credit_balance,
            "bulk_low_threshold": self.bulk_low_threshold,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        """
        Build (or update) an ``Account`` instance from a dict.  Only the
        whitelisted fields are copied – this prevents accidental injection
        of unexpected keys.
        """
        instance = cls()
        for field in (
            "name",
            "email",
            "is_active",
            "credit_balance",
            "bulk_low_threshold",
            "settings",
        ):
            if field in data:
                setattr(instance, field, data[field])
        return instance