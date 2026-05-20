from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GrafanaAlert(BaseModel):
    title: str
    message: str
    state: str
    evalMatches: List[dict]
    imageUrl: Optional[str]
    ruleId: int
    ruleName: str
    ruleUrl: str
    state: str
    tags: dict
    executionError: Optional[str]
    evalMatches: List[dict]

class GrafanaWebhookPayload(BaseModel):
    alerts: List[GrafanaAlert]
    commonAnnotations: dict
    commonLabels: dict
    externalURL: str
    groupKey: str
    groupLabels: dict
    numAlerts: int
    receiver: str
    status: str
    truncatedAlerts: int
    version: str

def normalize_grafana_alert(alert: GrafanaAlert) -> dict:
    normalized_alert = {
        "title": alert.title,
        "message": alert.message,
        "severity": alert.state,
        "rule_name": alert.ruleName,
        "rule_url": alert.ruleUrl,
        "timestamp": datetime.now().isoformat(),
        "source": "grafana"
    }
    return normalized_alert

def normalize_grafana_payload(payload: GrafanaWebhookPayload) -> List[dict]:
    normalized_alerts = [normalize_grafana_alert(alert) for alert in payload.alerts]
    return normalized_alerts