"""
Support Manager Module

Tracks user adoption, provides targeted support, and analyzes retention metrics.
Designed for team leads to understand feature usage and user engagement.

Core Concepts:
- Adoption: User enabling/completing a feature
- Retention: User returning after initial adoption
- Support: Contextual assistance based on usage patterns

Author: axentx-dev-bot
"""

import datetime
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class AdoptionEvent:
    """Represents a single feature adoption event."""
    user_id: str
    feature: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)


@dataclass
class RetentionEvent:
    """Tracks user's first adoption and last activity."""
    user_id: str
    first_adoption: datetime.datetime
    last_seen: datetime.datetime


class SupportManager:
    """
    Manages adoption tracking, support provision, and retention analysis.
    Uses in-memory storage; production should integrate with database.
    """

    def __init__(self) -> None:
        # user_id -> list of AdoptionEvent
        self._adoptions: Dict[str, List[AdoptionEvent]] = defaultdict(list)
        # user_id -> RetentionEvent
        self._retention: Dict[str, RetentionEvent] = {}
        # feature -> set of user_ids
        self._feature_users: Dict[str, Set[str]] = defaultdict(set)

    def track_adoption(self, user_id: str, feature: str) -> None:
        """Record user adoption of a feature with automatic timestamp."""
        timestamp = datetime.datetime.utcnow()
        event = AdoptionEvent(user_id=user_id, feature=feature, timestamp=timestamp)
        self._adoptions[user_id].append(event)
        self._feature_users[feature].add(user_id)
        log.debug("Recorded adoption: %s", event)

        # Initialize or update retention tracking
        if user_id not in self._retention:
            self._retention[user_id] = RetentionEvent(
                user_id=user_id,
                first_adoption=timestamp,
                last_seen=timestamp,
            )
        else:
            self._retention[user_id].last_seen = timestamp

    def provide_support(self, user_id: str) -> str:
        """
        Generate contextual support message based on user's adoption history.
        Returns actionable next steps or resources.
        """
        events = self._adoptions.get(user_id, [])
        if not events:
            return f"User {user_id} needs onboarding. Guide them through initial setup."

        latest_feature = max(events, key=lambda e: e.timestamp).feature
        days_since = (datetime.datetime.utcnow() - events[-1].timestamp).days

        # Context-aware support suggestions
        support_map = {
            "dashboard": "Check our dashboard tutorial for advanced tips",
            "reporting": "Explore our reporting templates in the knowledge base",
            "automation": "Try our automation builder for workflow optimization"
        }
        
        if days_since > 7:
            return f"User {user_id} hasn't used {latest_feature} recently. {support_map.get(latest_feature, 'Review recent updates')}"
        return f"User {user_id} recently adopted {latest_feature}. {support_map.get(latest_feature, 'Encourage continued exploration')}"

    def get_adoption_metrics(self) -> Dict[str, int]:
        """Return feature adoption counts (feature -> unique users)."""
        return {feature: len(users) for feature, users in self._feature_users.items()}

    def get_retention_rate(self, period_days: int = 30) -> float:
        """
        Calculate retention rate for users within specified period.
        Returns percentage of users returning after initial adoption.
        """
        if not self._retention:
            return 0.0
            
        now = datetime.datetime.utcnow()
        period = datetime.timedelta(days=period_days)
        retained = sum(
            1 for event in self._retention.values()
            if (event.last_seen - event.first_adoption) <= period
        )
        return retained / len(self._retention)

    def get_user_adoption_history(self, user_id: str) -> List[str]:
        """Return list of features adopted by a specific user."""
        return [event.feature for event in self._adoptions.get(user_id, [])]


def main():
    # Example usage
    manager = SupportManager()
    
    # Track adoptions
    manager.track_adoption("user1", "dashboard")
    manager.track_adoption("user1", "reporting")
    manager.track_adoption("user2", "automation")
    
    # Generate support messages
    print(manager.provide_support("user1"))  # Recent adoption
    print(manager.provide_support("user2"))  # Needs onboarding
    
    # Get metrics
    print("Adoption Metrics:", manager.get_adoption_metrics())
    print("Retention Rate (30 days):", manager.get_retention_rate())
    print("User1 History:", manager.get_user_adoption_history("user1"))


if __name__ == "__main__":
    main()