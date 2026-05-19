import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.anomaly_detection import AnomalyDetector

class TestAnomalyDetector(unittest.TestCase):
    @patch('src.anomaly_detection.create_engine')
    def test_detect_anomalies(self, mock_create_engine):
        # Setup mock data
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_result = MagicMock()
        mock_conn.execute.return_value = mock_result

        # Create test data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        dates = [start_date + timedelta(days=i) for i in range(30)]
        spends = [100] * 29 + [500]  # One anomaly

        mock_result.fetchall.return_value = list(zip(dates, spends))
        mock_result.keys.return_value = ['date', 'total_spend']

        # Initialize and test
        detector = AnomalyDetector('sqlite:///:memory:')
        anomalies = detector.detect_anomalies()

        self.assertEqual(len(anomalies), 1)
        self.assertTrue(anomalies.iloc[0]['is_anomaly'])

if __name__ == '__main__':
    unittest.main()