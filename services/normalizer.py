from api.schemas.grafana import GrafanaWebhookPayload, normalize_grafana_payload

def normalize_alert(payload: dict, source: str) -> List[dict]:
    if source == "grafana":
        grafana_payload = GrafanaWebhookPayload.parse_obj(payload)
        return normalize_grafana_payload(grafana_payload)
    else:
        # existing normalization logic for other sources
        pass

def normalize_and_store_alert(payload: dict, source: str) -> None:
    normalized_alerts = normalize_alert(payload, source)
    # existing logic to store normalized alerts
    pass