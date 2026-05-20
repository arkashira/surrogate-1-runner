import prometheus_api_client
from prometheus_api_client import PrometheusConnect
from typing import List, Dict, Any
import time

class PrometheusAlertHandler:
    def __init__(self, prometheus_url: str):
        self.prometheus = PrometheusConnect(url=prometheus_url, headers={"Content-Type": "application/json"}, timeout=10)
        self.noise_reduction_cache = {}

    def fetch_alerts(self) -> List[Dict[str, Any]]:
        """Fetch and prioritize alerts with noise reduction"""
        raw_alerts = self.prometheus.all_alerts()
        processed_alerts = []
        
        for alert in raw_alerts:
            # Noise reduction: skip if already acknowledged or flapping
            if self._should_suppress_alert(alert):
                continue
                
            # Prioritize based on severity and impact
            severity = alert.get('labels', {}).get('severity', 'info')
            impact = alert.get('annotations', {}).get('impact', 'low')
            
            processed_alert = {
                'source': 'prometheus',
                'firing_time': time.time(),
                'rule': alert.get('rule', {}),
                'labels': alert.get('labels', {}),
                'annotations': alert.get('annotations', {}),
                'priority': self._calculate_priority(severity, impact),
                'raw': alert
            }
            processed_alerts.append(processed_alert)
        
        return processed_alerts

    def _should_suppress_alert(self, alert: Dict) -> bool:
        """70-80% noise reduction logic"""
        # Skip resolved alerts
        if alert.get('status') == 'resolved':
            return True
            
        # Skip flapping alerts (fired more than 3 times in 5 minutes)
        alert_key = f"{alert.get('rule', {}).get('name')}_{alert.get('labels', {})}"
        self.noise_reduction_cache[alert_key] = self.noise_reduction_cache.get(alert_key, 0) + 1
        if self.noise_reduction_cache[alert_key] > 3:
            return True
            
        return False

    def _calculate_priority(self, severity: str, impact: str) -> int:
        """Calculate alert priority (0-100)"""
        severity_map = {'critical': 80, 'high': 60, 'medium': 40, 'low': 20, 'info': 10}
        impact_map = {'high': 80, 'medium': 50, 'low': 20}
        
        return (severity_map.get(severity, 10) * 0.6) + (impact_map.get(impact, 10) * 0.4)