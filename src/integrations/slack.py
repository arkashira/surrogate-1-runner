import os
import logging
from typing import Dict, Optional
import requests

logger = logging.getLogger(__name__)

class SlackIntegration:
    """Handles Slack notifications with proper error handling and configuration validation."""

    def __init__(self, config: Dict):
        """Initialize Slack integration with required configuration.

        Args:
            config: Dictionary containing 'slack_token' and 'slack_channel'
        """
        self.config = config
        self.slack_token = config['slack_token']
        self.slack_channel = config['slack_channel']
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate required configuration parameters."""
        if not self.slack_token:
            raise ValueError("Slack token is required")
        if not self.slack_channel:
            raise ValueError("Slack channel is required")

    def send_notification(self, message: str, retry: int = 3) -> bool:
        """Send notification to Slack with retry mechanism.

        Args:
            message: The message to send
            retry: Number of retry attempts (default: 3)

        Returns:
            bool: True if notification was sent successfully
        """
        url = "https://slack.com/api/chat.postMessage"
        headers = {'Authorization': f'Bearer {self.slack_token}'}
        data = {
            'channel': self.slack_channel,
            'text': message
        }

        for attempt in range(retry):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data.get('ok'):
                        return True
                    logger.warning(f"Slack API error: {response_data.get('error')}")
                else:
                    logger.warning(f"Slack API request failed with status {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Slack request attempt {attempt + 1} failed: {str(e)}")

            if attempt < retry - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        logger.error(f"Failed to send Slack notification after {retry} attempts")
        return False

# src/integrations/__init__.py
from .slack import SlackIntegration

# tests/integrations/test_slack.py
import unittest
from unittest.mock import patch, MagicMock
import time
from src.integrations.slack import SlackIntegration

class TestSlackIntegration(unittest.TestCase):
    def setUp(self):
        self.config = {
            'slack_token': 'test_token',
            'slack_channel': 'test_channel'
        }
        self.slack = SlackIntegration(self.config)

    def test_initialization(self):
        with self.assertRaises(ValueError):
            SlackIntegration({'slack_token': ''})
        with self.assertRaises(ValueError):
            SlackIntegration({'slack_channel': ''})

    @patch('requests.post')
    def test_send_notification_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ok': True}
        mock_post.return_value = mock_response

        result = self.slack.send_notification("Test message")
        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_notification_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = self.slack.send_notification("Test message")
        self.assertFalse(result)
        self.assertEqual(mock_post.call_count, 3)  # Default retry count

    @patch('requests.post')
    def test_send_notification_retry(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            {'ok': False},  # First attempt fails
            {'ok': True}    # Second attempt succeeds
        ]
        mock_post.return_value = mock_response

        result = self.slack.send_notification("Test message")
        self.assertTrue(result)
        self.assertEqual(mock_post.call_count, 2)

# tests/integrations/__init__.py
from .test_slack import TestSlackIntegration