from abc import ABC, abstractmethod
from datetime import date
from typing import List, Dict

class BaseForecastEngine(ABC):
    @abstractmethod
    def generate(self, days_ahead: int) -> List[Dict]:
        """Return list of forecast dicts: {target_date, predicted_amount, model_version}."""