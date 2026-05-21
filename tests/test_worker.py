import unittest
from unittest.mock import patch, MagicMock
from src.worker import Worker

class TestWorker(unittest.TestCase):
    @patch('src.worker.WorkerMetrics')
    def test_worker_initialization(self, mock_worker_metrics):
        worker = Worker('worker1', 1000)
        self.assertEqual(worker.worker_id, 'worker1')
        self.assertEqual(worker.dataset_size, 1000)
        mock_worker_metrics.assert_called_once()

    @patch('src.worker.WorkerMetrics')
    def test_worker_start(self, mock_worker_metrics):
        mock_metrics_instance = MagicMock()
        mock_worker_metrics.return_value = mock_metrics_instance
        worker = Worker('worker1', 1000)
        worker.start()
        mock_metrics_instance.start_metrics_server.assert_called_once()
        mock_metrics_instance.update_worker_status.assert_called_once_with('worker1', 1)
        mock_metrics_instance.update_dataset_size.assert_called_once_with('worker1', 1000)

if __name__ == '__main__':
    unittest.main()