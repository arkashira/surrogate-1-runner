import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Union

class SecureLogStorage:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log_access(self, user_details: Dict[str, str], model_access: Dict[str, str]) -> None:
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "user_details": user_details,
            "model_access": model_access
        }
        log_file = os.path.join(self.log_dir, f"access_log_{timestamp.replace(':', '-')}.json")
        with open(log_file, 'w') as f:
            json.dump(log_entry, f, indent=4)

    def export_logs(self, export_format: str, output_file: str) -> None:
        log_files = [f for f in os.listdir(self.log_dir) if f.endswith('.json')]
        logs = []
        for log_file in log_files:
            with open(os.path.join(self.log_dir, log_file), 'r') as f:
                logs.append(json.load(f))

        if export_format.lower() == 'csv':
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["timestamp", "user_details", "model_access"])
                writer.writeheader()
                for log in logs:
                    writer.writerow(log)
        elif export_format.lower() == 'json':
            with open(output_file, 'w') as f:
                json.dump(logs, f, indent=4)
        else:
            raise ValueError("Unsupported export format. Use 'csv' or 'json'.")

# Example usage
if __name__ == "__main__":
    storage = SecureLogStorage()
    user_details = {"username": "admin", "role": "IT Administrator"}
    model_access = {"model_name": "AI Model", "access_type": "read"}
    storage.log_access(user_details, model_access)
    storage.export_logs("csv", "access_logs.csv")
    storage.export_logs("json", "access_logs.json")