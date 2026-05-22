import requests
import json
import time
from datetime import datetime

class Dashboard:
    def __init__(self):
        self.costinel_api_url = "https://api.costinel.com/v1"
        self.surrogate_1_api_url = "https://api.surrogate-1.com/v1"
        self.health_score_threshold = 0.8  # 80% of budget

    def fetch_data(self):
        costinel_response = requests.get(f"{self.costinel_api_url}/accounts")
        surrogate_1_response = requests.get(f"{self.surrogate_1_api_url}/accounts")

        costinel_data = json.loads(costinel_response.text)
        surrogate_1_data = json.loads(surrogate_1_response.text)

        return costinel_data, surrogate_1_data

    def calculate_health_score(self, account_data):
        total_spend = sum(account["spend"] for account in account_data)
        budget = sum(account["budget"] for account in account_data)
        health_score = (budget - total_spend) / budget
        return health_score

    def update_dashboard(self):
        costinel_data, surrogate_1_data = self.fetch_data()

        for account in costinel_data:
            account["health_score"] = self.calculate_health_score([account])

        for account in surrogate_1_data:
            account["health_score"] = self.calculate_health_score([account])

        return costinel_data, surrogate_1_data

    def run(self):
        while True:
            costinel_data, surrogate_1_data = self.update_dashboard()
            # Update dashboard UI with new data
            print("Dashboard updated")
            time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()