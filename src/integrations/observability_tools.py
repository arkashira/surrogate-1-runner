import requests

class ObservabilityToolIntegration:
    def __init__(self, tool_url):
        self.tool_url = tool_url

    def send_alert(self, alert_data):
        response = requests.post(f"{self.tool_url}/alerts", json=alert_data)
        return response.json()

    def get_metrics(self, metric_query):
        response = requests.get(f"{self.tool_url}/metrics", params={"query": metric_query})
        return response.json()