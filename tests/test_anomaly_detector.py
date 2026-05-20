import unittest
from models.anomaly_detector import AnomalyDetector

class TestAnomalyDetector(unittest.TestCase):
    def setUp(self):
        self.detector = AnomalyDetector()

    def test_detect_high_severity_anomalies(self):
        sample_data = [
            {"severity": "HIGH", "provider": "AWS", "service": "EC2", "observed_spend": 1000, "threshold_breach": True},
            {"severity": "LOW", "provider": "GCP", "service": "Compute Engine", "observed_spend": 500, "threshold_breach": False}
        ]
        anomalies = self.detector.detect_anomalies(sample_data)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['severity'], 'HIGH')

    def test_notify_slack(self):
        # Mocking the requests.post method
        class MockResponse:
            status_code = 200

        requests.post = lambda *args, **kwargs: MockResponse()

        anomaly = {"severity": "HIGH", "provider": "AWS", "service": "EC2", "observed_spend": 1000, "threshold_breach": True}
        self.detector.notify_slack(anomaly)

if __name__ == '__main__':
    unittest.main()