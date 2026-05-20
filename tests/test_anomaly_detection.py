import unittest
from src.anomalies.detection import AnomalyDetection

class TestAnomalyDetection(unittest.TestCase):
    def setUp(self):
        self.detector = AnomalyDetection("test_budget_data.csv")

    def test_train_model(self):
        self.detector.train_model()
        self.assertIsNotNone(self.detector.model)

    def test_detect_anomalies(self):
        self.detector.train_model()
        anomalies = self.detector.detect_anomalies()
        self.assertIsInstance(anomalies, pd.DataFrame)

    def test_send_email_notification(self):
        # Mocking email sending functionality for testing purposes
        pass

if __name__ == '__main__':
    unittest.main()