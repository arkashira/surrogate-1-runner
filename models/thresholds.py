from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class ThresholdConfig:
    """Model for storing threshold configurations per namespace."""
    
    namespace: str
    threshold_amount: float
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.datetime.utcnow()

    def update_threshold(self, new_threshold: float):
        """Update the threshold amount and timestamp."""
        self.threshold_amount = new_threshold
        self.updated_at = datetime.datetime.utcnow()