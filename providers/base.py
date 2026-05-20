from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from ..models import CostMetric

class CostProvider(ABC):
    @abstractmethod
    def get_cost_data(self, start: datetime, end: datetime) -> List[CostMetric]:
        """Return raw cost metrics for the period."""