from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Set

from pydantic import BaseModel, Field, validator


class DriftType(str, Enum):
    METHOD_CHANGE = "method_change"
    URL_PATH_CHANGE = "url_path_change"
    URL_QUERY_CHANGE = "url_query_change"
    HEADER_ADDED = "header_added"
    HEADER_REMOVED = "header_removed"
    HEADER_VALUE_CHANGED = "header_value_changed"
    BODY_HASH_CHANGE = "body_hash_change"
    BODY_STRUCTURE_CHANGE = "body_structure_change"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RequestSignature(BaseModel):
    method: str
    url: str
    headers: Dict[str, str]
    body: Optional[str] = None
    body_hash: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    pipeline_id: str
    endpoint: str = ""

    @validator("body_hash", always=True)
    def compute_body_hash(cls, v, values):
        body = values.get("body")
        if body:
            return hashlib.sha256(body.encode()).hexdigest()
        return ""

    @validator("endpoint", always=True)
    def extract_endpoint(cls, v, values):
        url = values.get("url")
        if url:
            return url.split("?")[0]
        return ""


class SignatureBaseline(BaseModel):
    pipeline_id: str
    endpoint: str
    expected_method: str
    expected_headers: Set[str]
    expected_body_schema: Optional[Dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    enabled: bool = True
    sensitivity: str = "medium"  # low, medium, high


class DriftDetection(BaseModel):
    pipeline_id: str
    endpoint: str
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    drift_type: Optional[DriftType] = None
    severity: Severity = Severity.LOW
    description: str = ""
    previous_value: Optional[str] = None
    current_value: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)

    def notification_message(self) -> str:
        return (
            f"🚨 Signature Drift Detected\n"
            f"Pipeline: {self.pipeline_id}\n"
            f"Endpoint: {self.endpoint}\n"
            f"Type: {self.drift_type or 'unknown'}\n"
            f"Severity: {self.severity}\n"
            f"Description: {self.description}\n"
            f"Previous: {self.previous_value}\n"
            f"Current: {self.current_value}\n"
            f"Detected at: {self.detected_at.isoformat()}"
        )


class NotificationConfig(BaseModel):
    enabled: bool = True
    webhook_url: Optional[str] = None
    email_recipients: list[str] = Field(default_factory=list)
    slack_channel: Optional[str] = None
    notify_on_low: bool = False
    notify_on_medium: bool = True
    notify_on_high: bool = True
    notify_on_critical: bool = True

    def should_notify(self, severity: Severity) -> bool:
        if not self.enabled:
            return False
        return {
            Severity.LOW: self.notify_on_low,
            Severity.MEDIUM: self.notify_on_medium,
            Severity.HIGH: self.notify_on_high,
            Severity.CRITICAL: self.notify_on_critical,
        }[severity]


class PipelineConfig(BaseModel):
    pipeline_id: str
    name: str
    endpoints: list[str] = Field(default_factory=list)
    baseline: Dict[str, SignatureBaseline] = Field(default_factory=dict)
    notification: NotificationConfig = Field(default_factory=NotificationConfig)