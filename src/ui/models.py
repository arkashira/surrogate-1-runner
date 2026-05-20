"""
Data models for the signature drift detector UI API.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class DetectorStatus(str, Enum):
    """Status of the signature drift detector."""
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    INITIALIZING = "initializing"


class AlertSeverity(str, Enum):
    """Severity level for alerts."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Alert(BaseModel):
    """Alert model for drift detection events."""
    id: str = Field(..., description="Unique alert identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: AlertSeverity
    message: str
    detector_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    acknowledged: bool = False


class DetectorConfig(BaseModel):
    """Configuration for a signature drift detector."""
    id: str = Field(..., description="Unique detector identifier")
    name: str
    description: Optional[str] = None
    status: DetectorStatus = DetectorStatus.ACTIVE
    
    # Detection thresholds
    drift_threshold: float = Field(default=0.1, ge=0.0, le=1.0)
    min_samples: int = Field(default=100, ge=1)
    window_size: int = Field(default=1000, ge=10)
    
    # Alert settings
    alert_on_drift: bool = True
    alert_threshold: float = Field(default=0.15, ge=0.0, le=1.0)
    
    # Monitoring interval in seconds
    check_interval: int = Field(default=300, ge=10)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DriftMetric(BaseModel):
    """Metric data point for drift detection."""
    timestamp: datetime
    detector_id: str
    metric_name: str
    value: float
    threshold: Optional[float] = None
    is_anomaly: bool = False


class DashboardSummary(BaseModel):
    """Summary data for dashboard display."""
    total_detectors: int
    active_detectors: int
    detectors_with_drift: int
    total_alerts: int
    critical_alerts: int
    recent_metrics: List[DriftMetric] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class DetectorStats(BaseModel):
    """Statistics for a detector."""
    detector_id: str
    total_checks: int = 0
    drift_detected_count: int = 0
    last_drift_detected: Optional[datetime] = None
    average_drift_score: float = 0.0
    current_drift_score: float = 0.0
    uptime_percentage: float = 100.0
    metrics_history: List[DriftMetric] = Field(default_factory=list)


class CreateDetectorRequest(BaseModel):
    """Request model for creating a new detector."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    drift_threshold: float = Field(default=0.1, ge=0.0, le=1.0)
    min_samples: int = Field(default=100, ge=1)
    window_size: int = Field(default=1000, ge=10)
    alert_on_drift: bool = True
    alert_threshold: float = Field(default=0.15, ge=0.0, le=1.0)
    check_interval: int = Field(default=300, ge=10)


class UpdateDetectorRequest(BaseModel):
    """Request model for updating a detector."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[DetectorStatus] = None
    drift_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    min_samples: Optional[int] = Field(None, ge=1)
    window_size: Optional[int] = Field(None, ge=10)
    alert_on_drift: Optional[bool] = None
    alert_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    check_interval: Optional[int] = Field(None, ge=10)


class AlertAcknowledgeRequest(BaseModel):
    """Request model for acknowledging an alert."""
    alert_ids: List[str] = Field(..., min_items=1)