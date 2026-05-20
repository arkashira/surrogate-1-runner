from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    Boolean,
    Enum as SAEnum,
    Text,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class NotificationChannel(str, Enum):
    """Supported notification channels."""
    EMAIL = "email"
    WEBHOOK = "webhook"


class AlertRule(Base):
    """SQLAlchemy ORM for a cost‑threshold alert rule."""

    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(64), nullable=True, index=True)
    account_id = Column(String(64), nullable=True, index=True)

    threshold_amount = Column(Numeric(12, 2), nullable=False)

    notification_channel = Column(SAEnum(NotificationChannel), nullable=False)
    notification_target = Column(Text, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # ------------------------------------------------------------------ #
    # Business helpers
    # ------------------------------------------------------------------ #
    def is_breached(self, current_cost: Decimal) -> bool:
        """Return True if the rule is active and the cost exceeds the threshold."""
        return self.is_active and current_cost >= self.threshold_amount

    # ------------------------------------------------------------------ #
    # Serialization helpers (used by API layer)
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        """Return a JSON‑serialisable dict."""
        return {
            "id": self.id,
            "service_name": self.service_name,
            "account_id": self.account_id,
            "threshold_amount": str(self.threshold_amount),
            "notification_channel": self.notification_channel.value,
            "notification_target": self.notification_target,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }