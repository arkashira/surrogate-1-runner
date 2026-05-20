import os
import json
import time
import requests
import threading
from datetime import datetime
from typing import Optional, Dict
from abc import ABC, abstractmethod

class Config:
    """Centralized configuration management"""
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv('SLACK_WEBHOOK_URL')
    SLACK_ENABLED: bool = os.getenv('COMPOSE_GUARD_SLACK_ENABLED', 'true').lower() == 'true'
    POLL_INTERVAL: int = int(os.getenv('HEALTH_MONITOR_INTERVAL', '30'))

    @classmethod
    def validate(cls) -> None:
        """Validate configuration settings"""
        if cls.SLACK_ENABLED and not cls.SLACK_WEBHOOK_URL:
            raise ValueError("SLACK_WEBHOOK_URL must be set when COMPOSE_GUARD_SLACK_ENABLED is true")

class Notifier(ABC):
    """Abstract base class for notification services"""
    @abstractmethod
    def send_notification(self, message: str) -> None:
        pass

class SlackNotifier(Notifier):
    """Slack notification implementation with retry logic"""
    def __init__(self):
        self.webhook_url = Config.SLACK_WEBHOOK_URL
        self.max_retries = 3
        self.initial_delay = 1

    def send_notification(self, message: str) -> None:
        """Send notification with exponential backoff retry"""
        if not Config.SLACK_ENABLED or not self.webhook_url:
            return

        payload = {"text": message}
        retry_delay = self.initial_delay

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.webhook_url,
                    data=json.dumps(payload),
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    print(f"Failed to send Slack notification after {self.max_retries} attempts: {e}")
                time.sleep(retry_delay)
                retry_delay *= 2

class HealthMonitor:
    """Container health monitoring service"""
    def __init__(self, notifier: Notifier):
        self.notifier = notifier
        self.poll_interval = Config.POLL_INTERVAL

    def monitor_containers(self) -> None:
        """Continuous container health monitoring"""
        while True:
            try:
                # Simulate container health check
                container_name = "example-container"
                exit_code = 1  # Simulate unhealthy container
                timestamp = datetime.now().isoformat()

                if exit_code != 0:
                    self._notify_unhealthy(container_name, exit_code, timestamp)

                time.sleep(self.poll_interval)
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(self.poll_interval)

    def _notify_unhealthy(self, container_name: str, exit_code: int, timestamp: str) -> None:
        """Notify about unhealthy container asynchronously"""
        message = f"Container {container_name} became unhealthy with exit code {exit_code} at {timestamp}"
        threading.Thread(
            target=self.notifier.send_notification,
            args=(message,)
        ).start()

def main():
    """Application entry point"""
    try:
        Config.validate()
        notifier = SlackNotifier()
        monitor = HealthMonitor(notifier)
        monitor.monitor_containers()
    except Exception as e:
        print(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main()