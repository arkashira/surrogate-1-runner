from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

class PriorityLevel(Enum):
    """Enumeration of priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass
class Update:
    """
    Represents an update that can be summarized.

    Attributes:
        id: Unique identifier for the update.
        title: Title of the update.
        description: Description of the update.
        importance_scores: Dictionary of importance scores based on different criteria.
        created_at: Timestamp when the update was created.
        priority: Computed priority level based on aggregated importance scores.
    """
    id: str
    title: str
    description: str
    importance_scores: Dict[str, float]
    created_at: datetime = field(default_factory=datetime.utcnow)
    priority: PriorityLevel = field(init=False)

    def __post_init__(self):
        # Calculate overall importance score using weighted sum
        importance_score = sum(score * weight for criterion, score in self.importance_scores.items() 
                               for criterion, weight in self.settings.importance_weights.items() 
                               if criterion in self.importance_scores)
        
        # Determine priority based on importance_score thresholds
        if importance_score >= self.settings.high_threshold:
            self.priority = PriorityLevel.HIGH
        elif importance_score >= self.settings.medium_threshold:
            self.priority = PriorityLevel.MEDIUM
        else:
            self.priority = PriorityLevel.LOW

@dataclass
class PrioritizationSettings:
    """
    Settings that influence how updates are prioritized.

    Attributes:
        importance_weights: Weights assigned to different importance criteria.
        high_threshold: Score above which an update is considered HIGH priority.
        medium_threshold: Score above which an update is considered MEDIUM priority.
        notification_enabled: Whether to send notifications for high priority updates.
    """
    importance_weights: Dict[str, float]
    high_threshold: float = 0.8
    medium_threshold: float = 0.5
    notification_enabled: bool = True