from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator

from ..models.alert_rule import NotificationChannel


class AlertRuleBase(BaseModel):
    service_name: Optional[str] = Field(
        None, max_length=64, description="Specific service (e.g. ec2) or null for all services"
    )
    account_id: Optional[str] = Field(
        None, max_length=64, description="AWS account ID or null for all accounts"
    )
    threshold_amount: Decimal = Field(
        ...,
        gt=Decimal("0"),
        description="USD amount that triggers the alert",
    )
    notification_channel: NotificationChannel
    notification_target: str = Field(..., min_length=1)

    @validator("notification_target")
    def _validate_target(cls, v, values):
        channel = values.get("notification_channel")
        if channel == NotificationChannel.EMAIL and "@" not in v:
            raise ValueError("Invalid e‑mail address")
        if channel == NotificationChannel.WEBHOOK and not v.startswith(("http://", "https://")):
            raise ValueError("Webhook URL must start with http:// or https://")
        return v


class AlertRuleCreate(AlertRuleBase):
    """Payload for creating a rule."""


class AlertRuleOut(AlertRuleBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True