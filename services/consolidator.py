import time
from collections import defaultdict
from typing import Dict, List

class Alert:
    def __init__(self, service: str, error_message: str, timestamp: int):
        self.service = service
        self.error_message = error_message
        self.timestamp = timestamp

class AlertConsolidator:
    def __init__(self, window_size: int = 300):  # 5 minutes
        self.window_size = window_size
        self.alerts: Dict[str, List[Alert]] = defaultdict(list)

    def ingest_alert(self, alert: Alert):
        key = f"{alert.service}:{alert.error_message}"
        self.alerts[key].append(alert)

    def consolidate(self) -> List[Dict]:
        consolidated_alerts = []
        current_time = int(time.time())
        for key, alert_list in self.alerts.items():
            # Filter alerts within the time window
            recent_alerts = [alert for alert in alert_list if current_time - alert.timestamp <= self.window_size]
            if recent_alerts:
                consolidated_alert = {
                    "service": recent_alerts[0].service,
                    "error_message": recent_alerts[0].error_message,
                    "count": len(recent_alerts),
                    "member_alerts": [{"timestamp": alert.timestamp} for alert in recent_alerts]
                }
                consolidated_alerts.append(consolidated_alert)
            # Clean up old alerts
            self.alerts[key] = recent_alerts
        return consolidated_alerts

def main():
    consolidator = AlertConsolidator()
    # Example usage
    alert1 = Alert("service1", "error1", int(time.time()))
    alert2 = Alert("service1", "error1", int(time.time()) - 100)
    consolidator.ingest_alert(alert1)
    consolidator.ingest_alert(alert2)
    print(consolidator.consolidate())

if __name__ == "__main__":
    main()