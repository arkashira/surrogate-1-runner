import unittest
from unittest.mock import patch
from src.worker_metrics import WorkerMetrics

class TestWorkerMetrics(unittest.TestCase):
    @patch('src.worker_metrics.start_http_server')
    def test_start_metrics_server(self, mock_start_http_server):
        metrics = WorkerMetrics()
        metrics.start_metrics_server()
        mock_start_http_server.assert_called_once_with(8000)

    def test_update_worker_status(self):
        metrics = WorkerMetrics()
        metrics.update_worker_status('worker1', 1)
        self.assertEqual(metrics.worker_status.labels(worker_id='worker1')._value.get(), 1)

    def test_update_dataset_size(self):
        metrics = WorkerMetrics()
        metrics.update_dataset_size('worker1', 1000)
        self.assertEqual(metrics.dataset_size.labels(worker_id='worker1')._value.get(), 1000)

if __name__ == '__main__':
    unittest.main()