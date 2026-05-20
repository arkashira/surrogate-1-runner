from typing import Dict, Any
from .pagerduty import PagerDutyIntegration
from .datadog import DatadogIntegration
from .slack import SlackIntegration

class IntegrationManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.integrations = {}

    def initialize_integrations(self):
        if "pagerduty" in self.config:
            self.integrations["pagerduty"] = PagerDutyIntegration(self.config["pagerduty"]["api_key"])

        if "datadog" in self.config:
            self.integrations["datadog"] = DatadogIntegration(
                self.config["datadog"]["api_key"],
                self.config["datadog"]["app_key"]
            )

        if "slack" in self.config:
            self.integrations["slack"] = SlackIntegration(self.config["slack"]["webhook_url"])

    def create_incident(self, service_id: str, title: str, description: str) -> Dict[str, Any]:
        if "pagerduty" in self.integrations:
            return self.integrations["pagerduty"].create_incident(service_id, title, description)
        raise Exception("PagerDuty integration not initialized")

    def create_event(self, title: str, text: str, tags: Dict[str, str] = None) -> Dict[str, Any]:
        if "datadog" in self.integrations:
            return self.integrations["datadog"].create_event(title, text, tags)
        raise Exception("Datadog integration not initialized")

    def send_message(self, text: str, channel: str = None, username: str = None) -> Dict[str, Any]:
        if "slack" in self.integrations:
            return self.integrations["slack"].send_message(text, channel, username)
        raise Exception("Slack integration not initialized")