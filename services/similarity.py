import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from typing import List, Dict, Any
import time
from sentence_transformers import SentenceTransformer

class AlertSimilarity:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the AlertSimilarity class.

        Args:
        - model_name (str): The name of the sentence transformer model to use for text embedding.
        """
        self.alerts = []
        self.similarity_threshold = 0.8  # Threshold for grouping alerts
        self.model = SentenceTransformer(model_name)

    def ingest_alert(self, alert: Dict[str, Any]):
        """
        Ingest a new alert and group alerts.

        Args:
        - alert (Dict[str, Any]): The alert to ingest.
        """
        self.alerts.append(alert)
        self.group_alerts()

    def group_alerts(self):
        """
        Group alerts by service and 5-minute time window, and consolidate them.
        """
        if len(self.alerts) < 2:
            return
        
        grouped_alerts = {}
        for alert in self.alerts:
            service = alert['service']
            message = alert['message']
            timestamp = alert['timestamp']
            time_window = self.get_time_window(timestamp)

            key = (service, time_window)
            if key not in grouped_alerts:
                grouped_alerts[key] = []

            grouped_alerts[key].append(alert)

        self.alerts = self.consolidate_alerts(grouped_alerts)

    def consolidate_alerts(self, grouped_alerts: Dict[tuple, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Consolidate grouped alerts into a list of consolidated alerts.

        Args:
        - grouped_alerts (Dict[tuple, List[Dict[str, Any]]]): The grouped alerts.

        Returns:
        - List[Dict[str, Any]]: The consolidated alerts.
        """
        consolidated = []
        for alerts in grouped_alerts.values():
            if len(alerts) > 1:
                count = len(alerts)
                message = alerts[0]['message']
                consolidated_alert = {
                    'service': alerts[0]['service'],
                    'message': message,
                    'count': count,
                    'alerts': alerts
                }
                consolidated.append(consolidated_alert)
            else:
                consolidated.append(alerts[0])
        return consolidated

    def get_time_window(self, timestamp: float) -> str:
        """
        Get the 5-minute time window for a given timestamp.

        Args:
        - timestamp (float): The timestamp.

        Returns:
        - str: The 5-minute time window.
        """
        time_window = int(timestamp // 300) * 300
        return str(time_window)

    def calculate_similarity(self, alert1: str, alert2: str) -> float:
        """
        Calculate the similarity between two alerts.

        Args:
        - alert1 (str): The first alert.
        - alert2 (str): The second alert.

        Returns:
        - float: The similarity between the two alerts.
        """
        vector1 = self.embed_text(alert1)
        vector2 = self.embed_text(alert2)
        similarity = cosine_similarity([vector1], [vector2])[0][0]
        return similarity

    def embed_text(self, text: str) -> np.ndarray:
        """
        Embed text into a vector using a sentence transformer model.

        Args:
        - text (str): The text to embed.

        Returns:
        - np.ndarray: The embedded text vector.
        """
        return self.model.encode(text)

# Example usage
if __name__ == "__main__":
    similarity = AlertSimilarity()
    # Simulate alert ingestion
    similarity.ingest_alert({'service': 'serviceA', 'message': 'Error occurred', 'timestamp': time.time()})
    time.sleep(1)
    similarity.ingest_alert({'service': 'serviceA', 'message': 'Error occurred', 'timestamp': time.time()})
    print(similarity.alerts)