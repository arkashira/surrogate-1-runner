from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from .models import CostEntry

class CostProvider(ABC):
    @abstractmethod
    def get_cost_entries(
        self,
        start_date: datetime,
        end_date: datetime,
        department_tag: str = "Department"
    ) -> List[CostEntry]:
        """Return a list of CostEntry objects for the given period."""