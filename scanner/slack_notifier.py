"""
Slack notifier module with retry logic for high-severity violations.
"""
import os
import time
import logging
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_BACKOFF_SECONDS = 1


@dataclass
class SlackConfig:
    """Configuration for Slack webhook."""
    webhook_url: Optional[str] = None
    enabled: bool = False
    notify_severity_threshold: str = "high"  # minimum severity to notify


class SlackNotifier:
    """Handles Slack notifications with retry logic."""
    
    SEVERITY_LEVELS = ["low", "medium", "high", "critical"]
    SEVERITY_EMOJI = {
        "critical": ":rotating_light:",
        "high": ":warning:",
        "medium": ":large_yellow_circle:",
        "low": ":small_blue_diamond:",
    }
    
    def __init__(self, config: Optional[SlackConfig] = None):
        self.config = config or SlackConfig()
        self.session = requests.Session()
    
    def _format_violation_message(self, violation: Dict[str, Any]) -> Dict[str, Any]:
        """Format a violation as a Slack message with rich formatting."""
        severity = violation.get("severity", "unknown").lower()
        severity_emoji = self.SEVERITY_EMOJI.get(severity, ":white_circle:")
        
        # Build fields dynamically based on available data
        fields = [
            {"type": "mrkdwn", "text": f"*Severity:*\n{severity.upper()}"},
            {"type": "mrkdwn", "text": f"*Type:*\n{violation.get('type', 'unknown')}"},
        ]
        
        if violation.get("file_path"):
            fields.append({
                "type": "mrkdwn", 
                "text": f"*File:*\n