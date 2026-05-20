import pytest
from services.normalizer import normalize_alert
from api.schemas.grafana import GrafanaWebhookPayload

def test_normalize_grafana_payload():
    payload = {
        "alerts": [
            {
                "title": "Test Alert",
                "message": "This is a test alert",
                "state": "firing",
                "evalMatches": [],
                "ruleId": 1,
                "ruleName": "Test Rule",
                "ruleUrl": "https://example.com/rule",
                "tags": {},
            }
        ],
        "commonAnnotations": {},
        "commonLabels": {},
        "externalURL": "https://example.com",
        "groupKey": "",
        "groupLabels": {},
        "numAlerts": 1,
        "receiver": "",
        "status": "firing",
        "truncatedAlerts": 0,
        "version": "1.0",
    }
    grafana_payload = GrafanaWebhookPayload.parse_obj(payload)
    normalized_alerts = normalize_alert(payload, "grafana")
    assert len(normalized_alerts) == 1
    assert normalized_alerts[0]["title"] == "Test Alert"
    assert normalized_alerts[0]["message"] == "This is a test alert"
    assert normalized_alerts[0]["severity"] == "firing"
    assert normalized_alerts[0]["rule_name"] == "Test Rule"
    assert normalized_alerts[0]["rule_url"] == "https://example.com/rule"
    assert normalized_alerts[0]["source"] == "grafana"