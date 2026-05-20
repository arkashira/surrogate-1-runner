
import unittest
from unittest.mock import patch
from app.ingestion_worker import IngestionWorker
from app.alerts import send_email_alert

class TestAlerts(unittest.TestCase):

    @patch('app.alerts.send_email_alert')
    def test_failure_to_email_flow(self, mock_send_email_alert):
        worker = IngestionWorker('test_pipeline', 'test_bucket')
        worker.ingest_data = None  # Simulate ingestion failure

        with self.assertRaises(Exception):
            worker.run()

        mock_send_email_alert.assert_called_once_with(
            recipient='test@example.com',
            pipeline_name='test_pipeline',
            error_snippet='Exception occurred during ingestion',
            dashboard_link='https://dashboard.example.com'
        )

if __name__ == '__main__':
    unittest.main()