from collections import defaultdict
from typing import List, Dict, Tuple

class AlertSuppression:
    def __init__(self, threshold_rules: Dict[str, int]):
        self.threshold_rules = threshold_rules
        self.alert_clusters = defaultdict(list)

    def cluster_alerts(self, alerts: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Clusters alerts by service name/namespace.
        """
        for alert in alerts:
            key = f"{alert['service_name']}/{alert['namespace']}"
            self.alert_clusters[key].append(alert)
        return self.alert_clusters

    def suppress_alerts(self) -> Dict[str, Tuple[List[Dict], int]]:
        """
        Suppresses alerts based on threshold rules and returns top alerts per cluster with suppression count.
        """
        suppressed_alerts = {}
        for key, alerts in self.alert_clusters.items():
            service_name, namespace = key.split('/')
            threshold = self.threshold_rules.get(service_name, 0)
            if len(alerts) > threshold:
                top_alerts = sorted(alerts, key=lambda x: x['timestamp'], reverse=True)[:5]
                suppressed_count = len(alerts) - len(top_alerts)
                suppressed_alerts[key] = (top_alerts, suppressed_count)
            else:
                suppressed_alerts[key] = (alerts, 0)
        return suppressed_alerts

# Example usage
if __name__ == "__main__":
    threshold_rules = {
        'service1': 3,
        'service2': 5,
    }
    alerts = [
        {'service_name': 'service1', 'namespace': 'ns1', 'timestamp': 1623456789},
        {'service_name': 'service1', 'namespace': 'ns1', 'timestamp': 1623456790},
        {'service_name': 'service2', 'namespace': 'ns2', 'timestamp': 1623456791},
        # ... more alerts ...
    ]
    suppression = AlertSuppression(threshold_rules)
    clusters = suppression.cluster_alerts(alerts)
    suppressed = suppression.suppress_alerts()
    print(suppressed)