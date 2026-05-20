import unittest
from alerts import AnomalyDetector, CostRecord

class TestAnomalyDetector(unittest.TestCase):
    def test_detect_anomalies(self):
        detector = AnomalyDetector()
        historical_records = [
            CostRecord("example_resource", 10, datetime.now() - timedelta(days=31)),
            CostRecord("example_resource", 20, datetime.now() - timedelta(days=30)),
            CostRecord("example_resource", 30, datetime.now() - timedelta(days=29)),
            CostRecord("example_resource", 40, datetime.now() - timedelta(days=28)),
            CostRecord("example_resource", 50, datetime.now() - timedelta(days=27)),
            CostRecord("example_resource", 1000, datetime.now()),  # example anomaly
        ]
        new_record = CostRecord("example_resource", 150, datetime.now())
        alert = detector.detect_anomalies(new_record, historical_records)
        self.assertEqual(alert, AnomalyAlert("example_resource", 40, "high", datetime.now(), "Cost anomaly detected for example_resource"))

if __name__ == '__main__':
    unittest.main()