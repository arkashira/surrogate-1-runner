from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# ------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------
class AdoptionEventType(str, Enum):
    USER_SIGNUP = "user_signup"
    FIRST_LOGIN = "first_login"
    FEATURE_USED = "feature_used"
    ONBOARDING_COMPLETE = "onboarding_complete"
    SUPPORT_REQUEST = "support_request"
    FEEDBACK_SUBMITTED = "feedback_submitted"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    RETENTION_CHECK = "retention_check"
    UPGRADE = "upgrade"


class UserStatus(str, Enum):
    NEW = "new"
    ONBOARDING = "onboarding"
    ACTIVE = "active"
    AT_RISK = "at_risk"
    CHURNED = "churned"
    POWER_USER = "power_user"


# ------------------------------------------------------------------
# Event
# ------------------------------------------------------------------
@dataclass(frozen=True)
class AdoptionEvent:
    event_id: str
    user_id: str
    event_type: AdoptionEventType
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    shard_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "shard_id": self.shard_id,
        }


# ------------------------------------------------------------------
# Profile
# ------------------------------------------------------------------
@dataclass
class UserAdoptionProfile:
    user_id: str
    status: UserStatus = UserStatus.NEW
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
    onboarding_progress: float = 0.0  # 0–100%
    feature_usage_count: Dict[str, int] = field(default_factory=dict)
    support_tickets_count: int = 0
    feedback_count: int = 0
    retention_score: float = 0.0
    events: List[AdoptionEvent] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "onboarding_progress": self.onboarding_progress,
            "feature_usage_count": self.feature_usage_count,
            "support_tickets_count": self.support_tickets_count,
            "feedback_count": self.feedback_count,
            "retention_score": self.retention_score,
        }