from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CostEvent:
    """Represents a detected cost anomaly event."""
    
    provider: str
    current_cost: float
    baseline_cost: float
    cost_delta: float
    timestamp: datetime
    anomaly_z_score: float
    
    def to_dict(self) -> dict:
        """Convert cost event to dictionary representation."""
        return {
            'provider': self.provider,
            'current_cost': self.current_cost,
            'baseline_cost': self.baseline_cost,
            'cost_delta': self.cost_delta,
            'timestamp': self.timestamp.isoformat(),
            'anomaly_z_score': self.anomaly_z_score
        }
    
    def get_alert_message(self) -> str:
        """Generate alert message for this cost event."""
        direction = "increased" if self.cost_delta > 0 else "decreased"
        return (f"Cost anomaly detected for {self.provider}: "
                f"{direction} by ${abs(self.cost_delta):.2f} "
                f"(current: ${self.current_cost:.2f}, "
                f"baseline: ${self.baseline_cost:.2f})")