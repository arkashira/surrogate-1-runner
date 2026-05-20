from datetime import datetime
from typing import Dict, List
import json
import os

class UsageTracker:
    def __init__(self, storage_path: str = '/opt/axentx/surrogate-1/data/usage.json'):
        self.storage_path = storage_path
        self.usage_data = self._load_usage_data()

    def _load_usage_data(self) -> Dict:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_usage_data(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.usage_data, f)

    def track_cloud_account(self, user_id: str, cloud_account_id: str):
        if user_id not in self.usage_data:
            self.usage_data[user_id] = {
                'cloud_accounts': [],
                'alerts': [],
                'last_updated': datetime.now().isoformat()
            }

        if len(self.usage_data[user_id]['cloud_accounts']) < 5:
            self.usage_data[user_id]['cloud_accounts'].append(cloud_account_id)
            self.usage_data[user_id]['last_updated'] = datetime.now().isoformat()
            self._save_usage_data()
        else:
            raise Exception("Maximum number of cloud accounts (5) reached. Please upgrade to add more.")

    def get_cloud_accounts(self, user_id: str) -> List[str]:
        return self.usage_data.get(user_id, {}).get('cloud_accounts', [])

    def add_alert(self, user_id: str, alert_message: str):
        if user_id in self.usage_data:
            self.usage_data[user_id]['alerts'].append({
                'message': alert_message,
                'timestamp': datetime.now().isoformat()
            })
            self.usage_data[user_id]['last_updated'] = datetime.now().isoformat()
            self._save_usage_data()

    def get_alerts(self, user_id: str) -> List[Dict]:
        return self.usage_data.get(user_id, {}).get('alerts', [])