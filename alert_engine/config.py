from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


class ThresholdConfig(BaseModel):
    speed_threshold_percent: float = Field(10.0, gt=0)
    accuracy_threshold_percent: float = Field(5.0, gt=0)
    min_samples: int = Field(100, gt=0)


class SlackConfig(BaseModel):
    webhook_url: Optional[str] = None


class SmtpConfig(BaseModel):
    host: str = Field("smtp.gmail.com")
    port: int = Field(587, ge=1, le=65535)
    username: str
    password: str
    from_addr: str
    to_addrs: List[str] = Field(default_factory=list)


class AlertEngineConfig(BaseModel):
    thresholds: ThresholdConfig = ThresholdConfig()
    slack: SlackConfig = SlackConfig()
    smtp: Optional[SmtpConfig] = None

    @validator("slack", always=True)
    def validate_slack(cls, v):
        if not v.webhook_url:
            v.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        return v

    @validator("smtp", always=True)
    def validate_smtp(cls, v):
        if v is None:
            # Try to load from env
            if os.getenv("SMTP_HOST"):
                v = SmtpConfig(
                    host=os.getenv("SMTP_HOST"),
                    port=int(os.getenv("SMTP_PORT", 587)),
                    username=os.getenv("SMTP_USER"),
                    password=os.getenv("SMTP_PASS"),
                    from_addr=os.getenv("SMTP_FROM"),
                    to_addrs=os.getenv("SMTP_TO", "").split(","),
                )
        return v


def load_config(path: Optional[Path] = None) -> AlertEngineConfig:
    """
    Load configuration from a YAML file or environment variables.
    """
    if path and path.exists():
        import yaml

        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return AlertEngineConfig(**data)
    return AlertEngineConfig()