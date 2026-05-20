"""Slack notification service for task updates."""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from slack_sdk import WebClient

logger = logging.getLogger(__name__)

# Add necessary imports for Slack SDK

@dataclass
class TaskNotification:
    """Represents a task notification payload."""

    # Keep the existing properties

    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary format."""
        return {
            # Keep the existing properties and their formatting
            **{key: value for key, value in self.__dict__.items() if key != "metadata"},
            "metadata": self.metadata
        }

class SlackNotificationService:
    """Service for sending Slack notifications for task updates."""

    def __init__(
        self,
        webhook_url: Optional[str] = None,
        bot_token: Optional[str] = None,
        default_channel: str = "#tasks"
    ):
        """Initialize the Slack notification service.

        Args:
            webhook_url: Slack webhook URL for simple notifications
            bot_token: Slack bot token for advanced messaging
            default_channel: Default channel to send notifications to
        """
        self.webhook_url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
        self.bot_token = bot_token or os.environ.get("SLACK_BOT_TOKEN")
        self.default_channel = default_channel
        self._client = None
        self._initialized = False

    def _ensure_client(self) -> bool:
        """Ensure Slack client is initialized."""
        if self._initialized:
            return True

        if self.bot_token:
            try:
                self._client = WebClient(token=self.bot_token)
                self._initialized = True
                logger.info("Slack client initialized with bot token")
                return True
            except ImportError:
                logger.warning("slack_sdk not installed, falling back to webhook")

        if self.webhook_url:
            self._initialized = True
            logger.info("Using webhook-based Slack notifications")
            return True

        logger.error("No Slack credentials configured")
        return False

    def _build_task_message(self, notification: TaskNotification) -> Dict[str, Any]:
        # Keep the existing properties and their formatting
        # Add necessary blocks for the Slack message

    def _send_via_webhook(self, payload: Dict[str, Any]) -> bool:
        """Send notification via webhook."""
        # Keep the existing implementation

    def _send_via_client(self, payload: Dict[str, Any], channel: str) -> bool:
        """Send notification via Slack client."""
        # Keep the existing implementation

    def send_task_notification(
        self,
        notification: TaskNotification,
        channel: Optional[str] = None
    ) -> bool:
        """Send a task notification to Slack.

        Args:
            notification: The task notification to send
            channel: Optional channel override (defaults to default_channel)

        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not self._ensure_client():
            logger.error("Slack client not initialized, cannot send notification")
            return False

        payload = self._build_task_message(notification)
        target_channel = channel or self.default_channel

        if self._client:
            return self._send_via_client(payload, target_channel)
        elif self.webhook_url:
            return self._send_via_webhook(payload)

        return False

    def notify_task_created(
        self,
        task_id: str,
        task_title: str,
        task_description: Optional[str] = None,
        source: str = "slack",
        priority: str = "normal",
        channel: Optional[str] = None
    ) -> bool:
        """Send a task creation notification to Slack.

        Args:
            task_id: The task's unique identifier
            task_title: The task's title
            task_description: The task's description (optional)
            source: The source of the task (defaults to "slack")
            priority: The task's priority (defaults to "normal")
            channel: The channel to send the notification to (optional)

        Returns:
            True if the notification was sent successfully, False otherwise
        """
        notification = TaskNotification(
            task_id=task_id,
            task_title=task_title,
            task_description=task_description,
            source=source,
            priority=priority
        )

        return self.send_task_notification(notification, channel)