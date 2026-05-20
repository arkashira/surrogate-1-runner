from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CostEntry:
    period_start: datetime
    period_end: datetime
    service: str
    region: str
    usage_type: str
    department: Optional[str]
    cost: float
    usage_quantity: Optional[float] = None