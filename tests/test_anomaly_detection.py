import unittest
from unittest.mock import patch, MagicMock
from dashboard.anomaly_display import AnomalyDetection

class TestAnomalyDetection(unittest.TestCase):
    @patch('dashboard.anomaly_display.pd.read_csv')
    def setUp(self, mock_read_csv):
        self.data = pd.DataFrame({
            'cost': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        })
        mock_read_csv.return_value = self.data
        self.anomaly_detector = AnomalyDetection('/path/to/cloud_costs.csv')

    def test_load_data(self):
        data = self.anomaly_detector.load_data()
        self.assertEqual(len(data), 10)

    def test_preprocess_data(self):
        preprocessed_data = self.anomaly_detector.preprocess_data(self.data)
        self.assertEqual(preprocessed_data.shape, (10, 1))

    @patch('dashboard.anomaly_display.IsolationForest.fit')
    def test_train_model(self, mock_fit):
        preprocessed_data = self.anomaly_detector.preprocess_data(self.data)
        self.anomaly_detector.train_model(preprocessed_data)
        mock_fit.assert_called_once_with(preprocessed_data)

    @patch('dashboard.anomaly_display.smtplib.SMTP')
    def test_send_alert(self, mock_smtp):
        anomalies = pd.DataFrame({'cost': [1500]})
        self.anomaly_detector.send_alert(anomalies)
        mock_smtp.assert_called_once()

if __name__ == '__main__':
    unittest.main()