import smtplib
from email.mime.text import MIMEText
from typing import Dict, List
from config.alerts import alert_config
from datetime import datetime, timedelta

class AlertManager:
    def __init__(self):
        self.alert_throttle: Dict[str, List[datetime]] = {}

    def send_alert(self, policy_name: str, violation_details: str, recipients: List[str]):
        """Send an alert if the policy is not silenced and throttling limits are not exceeded."""
        if alert_config.is_policy_silenced(policy_name):
            return

        if not self._check_throttle(policy_name):
            return

        subject = f"Compliance Violation: {policy_name}"
        body = f"Policy: {policy_name}\nDetails: {violation_details}"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'alerts@axentx.com'
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP('localhost') as server:
            server.sendmail('alerts@axentx.com', recipients, msg.as_string())

        self._log_alert(policy_name, violation_details)

    def _check_throttle(self, policy_name: str) -> bool:
        """Check if the alert can be sent based on throttling limits."""
        now = datetime.now()
        if policy_name not in self.alert_throttle:
            self.alert_throttle[policy_name] = []

        # Remove alerts older than 1 hour
        self.alert_throttle[policy_name] = [
            alert_time for alert_time in self.alert_throttle[policy_name]
            if now - alert_time <= timedelta(hours=1)
        ]

        if len(self.alert_throttle[policy_name]) >= 5:
            return False

        self.alert_throttle[policy_name].append(now)
        return True

    def _log_alert(self, policy_name: str, violation_details: str):
        """Log the alert in the audit trail."""
        with open('/var/log/axentx/audit.log', 'a') as log_file:
            log_file.write(f"{datetime.now()} - Alert sent for policy: {policy_name}, Details: {violation_details}\n")

alert_manager = AlertManager()