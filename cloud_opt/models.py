"""
Data models for cloud cost optimization.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

# --------------------------------------------------------------------------- #
# Enumerations
# --------------------------------------------------------------------------- #

class ResourceType(str, Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    SERVERLESS = "serverless"


class AnomalyType(str, Enum):
    SPIKE = "spike"
    UNUSUAL_PATTERN = "unusual_pattern"
    TREND_DEVIATION = "trend_deviation"
    IDLE_RESOURCE = "idle_resource"
    OVERPROVISIONED = "overprovisioned"


class RecommendationPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationAction(str, Enum):
    RESIZE = "resize"
    TERMINATE = "terminate"
    SCHEDULE = "schedule"
    RIGHT_SIZE = "right_size"
    USE_SPOT_INSTANCES = "use_spot_instances"
    ENABLE_SAVINGS_PLAN = "enable_savings_plan"
    DELETE_IDLE = "delete_idle"
    ARCHIVE_DATA = "archive_data"
    USE_RESERVED_INSTANCES = "use_reserved_instances"

# --------------------------------------------------------------------------- #
# Data classes
# --------------------------------------------------------------------------- #

@dataclass
class CostMetric:
    resource_id: str
    resource_type: ResourceType
    timestamp: datetime
    cost: float
    usage: float
    region: str
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class CostForecast:
    resource_id: str
    forecast_date: datetime
    predicted_cost: float
    confidence: float  # 0.0 – 1.0
    trend: str  # "increasing" | "decreasing" | "stable"
    factors: List[str] = field(default_factory=list)


@dataclass
class Anomaly:
    id: str
    resource_id: str
    anomaly_type: AnomalyType
    detected_at: datetime
    severity: float  # 0.0 – 1.0
    description: str
    expected_cost: float
    actual_cost: float
    deviation_percentage: float


@dataclass
class Recommendation:
    id: str
    resource_id: str
    resource_type: ResourceType
    priority: RecommendationPriority
    action: RecommendationAction
    title: str
    description: str
    estimated_savings: float
    savings_percentage: float
    created_at: datetime
    updated_at: datetime
    metrics: Dict[str, float] = field(default_factory=dict)
    applicable: bool = True
    implemented: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "resource_id": self.resource_id,
            "resource_type": self.resource_type.value,
            "priority": self.priority.value,
            "action": self.action.value,
            "title": self.title,
            "description": self.description,
            "estimated_savings": self.estimated_savings,
            "savings_percentage": self.savings_percentage,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metrics": self.metrics,
            "applicable": self.applicable,
            "implemented": self.implemented,
        }


@dataclass
class OptimizationReport:
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    total_current_cost: float
    total_potential_savings: float
    recommendations: List[Recommendation] = field(default_factory=list)
    anomalies: List[Anomaly] = field(default_factory=list)
    forecasts: List[CostForecast] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "generated_at": self.generated_at.isoformat(),
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "total_current_cost": self.total_current_cost,
            "total_potential_savings": self.total_potential_savings,
            "recommendations_count": len(self.recommendations),
            "anomalies_count": len(self.anomalies),
            "recommendations": [r.to_dict() for r in self.recommendations],
            "anomalies": [a.__dict__ for a in self.anomalies],
            "forecasts": [f.__dict__ for f in self.forecasts],
        }