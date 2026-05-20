import datetime
import json

class QuotaManager:
    def __init__(self):
        self.quota = 2  # 2 hours/day
        self.usage = {}

    def get_quota(self, user_id):
        if user_id not in self.usage:
            self.usage[user_id] = 0
        return self.quota - self.usage[user_id]

    def update_usage(self, user_id, hours_used):
        if user_id not in self.usage:
            self.usage[user_id] = 0
        self.usage[user_id] += hours_used
        if self.usage[user_id] > self.quota:
            self.usage[user_id] = self.quota

    def reset_quota(self):
        for user_id in self.usage:
            self.usage[user_id] = 0

    def save_usage(self):
        with open('/opt/axentx/surrogate-1/data/usage.json', 'w') as f:
            json.dump(self.usage, f)

    def load_usage(self):
        try:
            with open('/opt/axentx/surrogate-1/data/usage.json', 'r') as f:
                self.usage = json.load(f)
        except FileNotFoundError:
            pass

    def check_quota(self, user_id):
        if user_id not in self.usage:
            self.usage[user_id] = 0
        if self.usage[user_id] >= self.quota:
            return False
        return True