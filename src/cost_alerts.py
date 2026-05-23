import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class CostAlert:
    def __init__(self, config_path: str = "config/cost_alerts.json"):
        self.config_path = config_path
        self.alerts_config = self._load_config()

    def _load_config(self) -> Dict:
        if not os.path.exists(self.config_path):
            return {"thresholds": {}, "alerts": []}
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def _save_config(self) -> None:
        with open(self.config_path, 'w') as f:
            json.dump(self.alerts_config, f, indent=4)

    def set_threshold(self, service: str, threshold: float) -> None:
        self.alerts_config["thresholds"][service] = threshold
        self._save_config()

    def check_costs(self, current_costs: Dict) -> List[Dict]:
        alerts = []
        for service, cost in current_costs.items():
            if service in self.alerts_config["thresholds"]:
                threshold = self.alerts_config["thresholds"][service]
                if cost > threshold:
                    alerts.append({
                        "service": service,
                        "cost": cost,
                        "threshold": threshold,
                        "timestamp": datetime.now().isoformat()
                    })
        self.alerts_config["alerts"].extend(alerts)
        self._save_config()
        return alerts

    def get_alerts(self, hours: Optional[int] = None) -> List[Dict]:
        if hours is None:
            return self.alerts_config["alerts"]
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [alert for alert in self.alerts_config["alerts"]
                if datetime.fromisoformat(alert["timestamp"]) >= cutoff_time]