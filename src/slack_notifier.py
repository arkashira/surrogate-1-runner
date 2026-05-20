import requests
import logging
import time
from typing import Optional
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class SlackNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.max_retries = 2
        self.retry_delay = 5  # seconds

    def send_high_severity_alert(
        self,
        account_id: str,
        control_id: str,
        report_url: str
    ) -> bool:
        payload = {
            "text": (
                f":rotating_light: HIGH-SEVERITY VIOLATION DETECTED\n"
                f"Account ID: {account_id}\n"
                f"Control ID: {control_id}\n"
                f"Report: {report_url}"
            )
        }
        
        retry_count = 0
        while retry_count <= self.max_retries:
            try:
                response = requests.post(
                    self.webhook_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                response.raise_for_status()
                return True
            except RequestException as e:
                retry_count += 1
                if retry_count > self.max_retries:
                    logger.error(
                        f"Slack alert failed after {self.max_retries+1} attempts: {str(e)}",
                        extra={
                            'account_id': account_id,
                            'control_id': control_id,
                            'error': str(e)
                        }
                    )
                    return False
                logger.warning(
                    f"Slack alert attempt {retry_count} failed: {str(e)}",
                    extra={'retry_in_seconds': self.retry_delay}
                )
                time.sleep(self.retry_delay)
        return False