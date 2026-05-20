from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, validator, root_validator

class AutomationStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class ChangeType(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class AutomationVersion(BaseModel):
    version_id: str = Field(default_factory=lambda: f"v{uuid4()}")
    automation_id: str
    version_number: int
    config: Dict
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    changelog: str
    status: AutomationStatus

class AutomationChange(BaseModel):
    change_id: str = Field(default_factory=lambda: f"c{uuid4()}")
    automation_id: str
    version_id: str
    change_type: ChangeType
    description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user: str
    diff: Dict = Field(default_factory=dict)

class Automation(BaseModel):
    id: str
    name: str
    description: str
    category: str
    current_version: int
    versions: List[AutomationVersion] = Field(default_factory=list)
    changes: List[AutomationChange] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: AutomationStatus = AutomationStatus.DRAFT
    tags: List[str] = Field(default_factory=list)
    config_schema: Dict = Field(default_factory=dict)

    @validator("config_schema", pre=True, always=True)
    def _default_schema(cls, v):
        return v or {}

    @root_validator
    def _check_versions(cls, values):
        versions = values.get("versions", [])
        if versions:
            values["current_version"] = max(v.version_number for v in versions)
        return values