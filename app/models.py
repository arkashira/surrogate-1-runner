from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ArtifactSource(str, Enum):
    GITHUB = "github"
    JENKINS = "jenkins"
    CUSTOM = "custom"

class ArtifactStatus(str, Enum):
    PENDING = "pending"
    COLLECTING = "collecting"
    COLLECTED = "collected"
    FAILED = "failed"
    EXPIRED = "expired"

class Artifact(BaseModel):
    id: str = Field(..., description="Unique artifact ID")
    name: str
    source: ArtifactSource
    source_url: str
    pipeline_id: str
    pipeline_name: str
    build_number: int
    version: str
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None
    checksum_algorithm: Optional[str] = None
    download_url: Optional[str] = None
    collected_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: ArtifactStatus = ArtifactStatus.PENDING
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)

    class Config:
        use_enum_values = True

class ArtifactQuery(BaseModel):
    source: Optional[ArtifactSource] = None
    pipeline_name: Optional[str] = None
    build_number: Optional[int] = None
    version: Optional[str] = None
    status: Optional[ArtifactStatus] = None
    tags: Optional[List[str]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    limit: int = 100
    offset: int = 0