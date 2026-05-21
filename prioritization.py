from datetime import datetime
from typing import List, Tuple
import logging

from .models import Update, PrioritizationSettings, PriorityLevel

logger = logging.getLogger(__name__)

class UpdatePrioritizer:
    def __init__(self, settings: PrioritizationSettings):
        self.settings = settings

    def prioritize_updates(self, updates: List[Update]) -> Tuple[List[Update], List[Update]]:
        """
        Sort updates by priority and timestamp, and separate high-priority updates
        for notification.

        Args:
            updates: List of Update objects to process.

        Returns:
            A tuple containing:
                - A list of updates sorted by priority (HIGH > MEDIUM > LOW) and
                  then by created_at descending.
                - A list of high-priority updates that should trigger notifications.
        """
        # Assign priority to each update
        for upd in updates:
            upd.__post_init__()

        # Sort updates
        sorted_updates = sorted(
            updates,
            key=lambda u: (
                -u.priority.value,  # Higher priority first
                -u.created_at.timestamp(),  # Newer first
            ),
        )

        # Extract high-priority updates for notification
        high_priority_updates = [u for u in sorted_updates if u.priority == PriorityLevel.HIGH]

        return sorted_updates, high_priority_updates

    def notify_high_priority_updates(self, high_priority_updates: List[Update]) -> None:
        """
        Notify user about high-priority updates.

        Args:
            high_priority_updates: List of high-priority updates to notify about.
        """
        if not high_priority_updates or not self.settings.notification_enabled:
            return

        for upd in high_priority_updates:
            logger.info(
                f"[NOTIFY] High-priority update available: {upd.id} "
                f"(score={sum(upd.importance_scores.values()):.2f})"
            )

    def adjust_prioritization_settings(self, new_importance_weights: Dict[str, float]):
        """
        Adjust the prioritization settings with new importance weights.

        Args:
            new_importance_weights: New weights assigned to different importance criteria.
        """
        self.settings.importance_weights = new_importance_weights