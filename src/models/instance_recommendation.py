"""EC2 Instance Recommendation Models."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class RecommendationPriority(str, Enum):
    """Priority level for recommendations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationStatus(str, Enum):
    """Status of the recommendation."""
    PENDING = "pending"
    DISMISSED = "dismissed"
    APPLIED = "applied"


@dataclass
class UsageDataPoint:
    """Single data point of historical resource usage."""
    timestamp: datetime
    cpu_utilization_percent: float
    memory_utilization_percent: float
    network_in_bytes: int = 0
    network_out_bytes: int = 0
    disk_io_read_bytes: int = 0
    disk_io_write_bytes: int = 0


@dataclass
class InstanceMetrics:
    """Aggregated metrics for an EC2 instance."""
    instance_id: str
    instance_type: str
    instance_name: str
    region: str
    usage_data: list[UsageDataPoint] = field(default_factory=list)
    
    @property
    def avg_cpu_utilization(self) -> float:
        if not self.usage_data:
            return 0.0
        return sum(d.cpu_utilization_percent for d in self.usage_data) / len(self.usage_data)
    
    @property
    def avg_memory_utilization(self) -> float:
        if not self.usage_data:
            return 0.0
        return sum(d.memory_utilization_percent for d in self.usage_data) / len(self.usage_data)
    
    @property
    def max_cpu_utilization(self) -> float:
        if not self.usage_data:
            return 0.0
        return max(d.cpu_utilization_percent for d in self.usage_data)
    
    @property
    def max_memory_utilization(self) -> float:
        if not self.usage_data:
            return 0.0
        return max(d.memory_utilization_percent for d in self.usage_data)


@dataclass
class InstanceRecommendation:
    """Right-sizing recommendation for an EC2 instance."""
    instance_id: str
    instance_type: str
    instance_name: str
    region: str
    
    # Analysis
    avg_cpu_utilization: float
    avg_memory_utilization: float
    max_cpu_utilization: float
    max_memory_utilization: float
    analysis_period_days: int
    
    # Recommendation
    recommended_instance_type: str
    recommendation_reason: str
    priority: RecommendationPriority
    
    # Savings
    current_monthly_cost_estimate: float
    recommended_monthly_cost_estimate: float
    monthly_savings_estimate: float
    annual_savings_estimate: float
    savings_percentage: float
    
    # Metadata
    status: RecommendationStatus = RecommendationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    applied_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "instance_id": self.instance_id,
            "instance_type": self.instance_type,
            "instance_name": self.instance_name,
            "region": self.region,
            "analysis": {
                "avg_cpu_utilization": round(self.avg_cpu_utilization, 2),
                "avg_memory_utilization": round(self.avg_memory_utilization, 2),
                "max_cpu_utilization": round(self.max_cpu_utilization, 2),
                "max_memory_utilization": round(self.max_memory_utilization, 2),
                "period_days": self.analysis_period_days,
            },
            "recommendation": {
                "recommended_instance_type": self.recommended_instance_type,
                "reason": self.recommendation_reason,
                "priority": self.priority.value,
            },
            "savings": {
                "current_monthly_cost": round(self.current_monthly_cost_estimate, 2),
                "recommended_monthly_cost": round(self.recommended_monthly_cost_estimate, 2),
                "monthly_savings": round(self.monthly_savings_estimate, 2),
                "annual_savings": round(self.annual_savings_estimate, 2),
                "savings_percentage": round(self.savings_percentage, 2),
            },
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
        }