import os
import json
from datetime import datetime
from typing import Dict, Any

class PerformanceMetricsStorage:
    def __init__(self, storage_path: str = "performance_metrics"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def save_metrics(self, workflow_id: str, metrics: Dict[str, Any]) -> None:
        timestamp = datetime.now().isoformat()
        metrics["timestamp"] = timestamp
        metrics["workflow_id"] = workflow_id

        file_path = os.path.join(self.storage_path, f"{workflow_id}_{timestamp}.json")
        with open(file_path, 'w') as f:
            json.dump(metrics, f)

    def load_metrics(self, workflow_id: str) -> Dict[str, Any]:
        metrics = {}
        for file_name in os.listdir(self.storage_path):
            if file_name.startswith(workflow_id):
                file_path = os.path.join(self.storage_path, file_name)
                with open(file_path, 'r') as f:
                    metrics[file_name] = json.load(f)
        return metrics