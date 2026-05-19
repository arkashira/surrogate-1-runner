from typing import List
import requests

class SurrogateClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_key}'})

    def get_cost_anomalies(self) -> List['Anomaly']:
        """
        Retrieve cost anomalies from the API.
        
        Returns:
            List[Anomaly]: A list of anomaly objects representing cost anomalies.
        """
        response = self.session.get(f"{self.base_url}/v1/costs/anomalies")
        response.raise_for_status()
        data = response.json()
        
        # Assuming the API returns a list of anomaly objects
        # This would need to be adjusted based on the actual API response structure
        anomalies = []
        for item in data.get('anomalies', []):
            anomalies.append(Anomaly(**item))
        
        return anomalies

class Anomaly:
    def __init__(self, id: str, timestamp: str, amount: float, threshold: float, message: str):
        self.id = id
        self.timestamp = timestamp
        self.amount = amount
        self.threshold = threshold
        self.message = message

    def __repr__(self):
        return f"Anomaly(id='{self.id}', timestamp='{self.timestamp}', amount={self.amount}, threshold={self.threshold}, message='{self.message}')"