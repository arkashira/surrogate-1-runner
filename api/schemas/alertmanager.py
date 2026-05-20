from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class AlertmanagerAlert(BaseModel):
    """Schema for individual alert in Alertmanager webhook payload"""
    status: str = Field(..., description="Status of the alert (firing/resolved)")
    labels: Dict[str, str] = Field(..., description="Labels associated with the alert")
    annotations: Optional[Dict[str, str]] = Field(None, description="Annotations for the alert")
    startsAt: datetime = Field(..., alias="startsAt", description="Start time of the alert")
    endsAt: Optional[datetime] = Field(None, alias="endsAt", description="End time of the alert")
    generatorURL: Optional[str] = Field(None, alias="generatorURL", description="URL of the alert generator")

    class Config:
        allow_population_by_field_name = True

class AlertmanagerWebhookPayload(BaseModel):
    """Schema for Alertmanager webhook payload"""
    version: str = Field(..., description="Version of the payload")
    groupKey: str = Field(..., alias="groupKey", description="Key identifying the group of alerts")
    status: str = Field(..., description="Status of the alert group")
    receiver: str = Field(..., description="Receiver that handled the alert")
    groupLabels: Dict[str, str] = Field(..., alias="groupLabels", description="Labels shared by all alerts in the group")
    commonLabels: Dict[str, str] = Field(..., alias="commonLabels", description="Labels common to all alerts")
    commonAnnotations: Optional[Dict[str, str]] = Field(None, alias="commonAnnotations", description="Annotations common to all alerts")
    externalURL: str = Field(..., alias="externalURL", description="External URL of the Alertmanager instance")
    alerts: List[AlertmanagerAlert] = Field(..., description="List of alerts in the payload")

    @validator('version')
    def validate_version(cls, v):
        if v not in ['4']:
            raise ValueError('Only version 4 is supported')
        return v

    @validator('status')
    def validate_status(cls, v):
        if v not in ['firing', 'resolved']:
            raise ValueError('Status must be either "firing" or "resolved"')
        return v

    class Config:
        allow_population_by_field_name = True