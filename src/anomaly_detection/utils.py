import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import requests

log = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Configuration helpers
# --------------------------------------------------------------------------- #
def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables or a JSON file.
    Expected keys:
        - METRICS_DB_PATH: path to a JSON file containing metric samples
        - ALERT_WEBHOOK_URL: URL to POST anomaly alerts
    """
    config: Dict[str, Any] = {
        "metrics_db_path": os.getenv("METRICS_DB_PATH", "data/metrics.json"),
        "alert_webhook_url": os.getenv("ALERT_WEBHOOK_URL", ""),
    }
    return config


# --------------------------------------------------------------------------- #
# Metrics persistence helpers
# --------------------------------------------------------------------------- #
def get_metrics() -> List[Dict[str, Any]]:
    """
    Retrieve the latest cluster metrics from the persistence layer.
    For the purposes of this example, metrics are stored in a JSON file.
    Each metric entry is expected to have:
        - timestamp: ISO 8601 string
        - name: metric name
        - value: numeric value
    """
    config = load_config()
    path = Path(config["metrics_db_path"])
    if not path.is_file():
        log.warning("Metrics file not found: %s", path)
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            log.warning("Metrics file format invalid: expected list, got %s", type(data))
            return []
    except Exception as exc:
        log.exception("Failed to load metrics: %s", exc)
        return []


# --------------------------------------------------------------------------- #
# Alerting helpers
# --------------------------------------------------------------------------- #
def send_alert(anomaly: Dict[str, Any]) -> None:
    """
    Send an anomaly alert to the configured observability tool.
    The alert is sent as a JSON payload via HTTP POST.
    """
    config = load_config()
    url = config["alert_webhook_url"]
    if not url:
        log.warning("ALERT_WEBHOOK_URL not set; skipping alert for anomaly: %s", anomaly)
        return

    try:
        response = requests.post(url, json=anomaly, timeout=5)
        response.raise_for_status()
        log.info("Alert sent successfully: %s", anomaly)
    except Exception as exc:
        log.exception("Failed to send alert: %s", exc)