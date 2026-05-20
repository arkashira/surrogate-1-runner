from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field, validator
import re

class AlertConfig(BaseModel):
    """Enhanced alert configuration with validation and defaults."""
    enabled: bool = Field(default=False, description="Whether alerts are enabled")
    cost_threshold: float = Field(gt=0, description="Cost threshold in USD")
    email_recipients: List[EmailStr] = Field(default_factory=list, min_items=1, max_items=10)
    slack_webhook_url: Optional[str] = Field(default=None, description="Slack webhook URL")
    notify_on_exceed: bool = Field(default=True, description="Notify when threshold exceeded")
    notify_on_warning: bool = Field(default=False, description="Notify at 80% of threshold")
    notify_on_recovery: bool = Field(default=False, description="Notify when costs drop below threshold")
    notification_frequency: int = Field(default=60, ge=15, le=1440, description="Minutes between notifications (0 for immediate)")

    @validator('slack_webhook_url')
    def validate_slack_webhook(cls, v):
        if v and not re.match(r'^https://hooks\.slack\.com/services/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+$', v):
            raise ValueError("Invalid Slack webhook URL format")
        return v

class UserSettings(BaseModel):
    """User settings with enhanced validation and defaults."""
    user_id: str = Field(..., description="User identifier")
    team_id: Optional[str] = Field(default=None, description="Team identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Alert configuration
    alert_config: AlertConfig = Field(default_factory=AlertConfig)

    # Job preferences
    max_parallel_jobs: int = Field(default=4, ge=1, le=16)
    default_timeout: int = Field(default=3600, ge=60, le=86400)
    enable_notifications: bool = Field(default=True)
    preferred_notification_time: Optional[str] = Field(default=None, description="ISO 8601 time format for preferred notification time")

class CostAlert(BaseModel):
    """Cost alert payload with additional context fields."""
    alert_id: str
    user_id: str
    team_id: Optional[str]
    job_id: str
    threshold: float
    current_cost: float
    percentage: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    job_context: Dict = Field(default_factory=dict)
    severity: str = Field(default="warning", description="warning, critical, or informational")
    status: str = Field(default="active", description="active, resolved, or acknowledged")