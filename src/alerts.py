import os
import json
from typing import Dict, Any
from storage import PerformanceMetricsStorage

class PerformanceAlerts:
    def __init__(self, threshold_metrics: Dict[str, Any]):
        self.threshold_metrics = threshold_metrics
        self.storage = PerformanceMetricsStorage()

    def check_thresholds(self, workflow_id: str) -> None:
        metrics = self.storage.load_metrics(workflow_id)
        for file_name, metric in metrics.items():
            for key, threshold in self.threshold_metrics.items():
                if key in metric and metric[key] > threshold:
                    self.trigger_alert(workflow_id, key, metric[key], threshold)

    def trigger_alert(self, workflow_id: str, metric_name: str, actual_value: Any, threshold: Any) -> None:
        alert_message = f"Alert: Workflow {workflow_id} - {metric_name} exceeded threshold. Actual: {actual_value}, Threshold: {threshold}"
        print(alert_message)
        # Here you can add code to send alerts via email, Slack, etc.