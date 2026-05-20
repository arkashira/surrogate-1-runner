from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pydantic import BaseModel

# ---- Domain models ----
@dataclass
class CostMetric:
    timestamp: datetime
    resource_id: str
    resource_name: str
    resource_type: str
    cost: float
    currency: str = "USD"
    tags: Optional[Dict[str, str]] = None

    def to_dict(self):
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d

class CostSummary(BaseModel):
    period_start: datetime
    period_end: datetime
    total_cost: float
    currency: str
    by_resource_type: Dict[str, float]
    by_service: Dict[str, float]
    trend: float  # % change vs previous period

# ---- API schemas ----
class RealtimeRequest(BaseModel):
    hours: int = 24

class SummaryRequest(BaseModel):
    days: int = 30

class AuditEntry(BaseModel):
    timestamp: datetime
    action: str
    user: str
    resource: str
    details: Dict[str, str]