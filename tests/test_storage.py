import os
import json
import unittest
from datetime import datetime
from src.storage import PerformanceMetricsStorage

class TestPerformanceMetricsStorage(unittest.TestCase):
    def setUp(self):
        self.storage = PerformanceMetricsStorage("test_performance_metrics")
        self.test_workflow_id = "test_workflow_123"
        self.test_metrics = {
            "execution_time": 10.5,
            "memory_usage": 2048,
            "status": "completed"
        }

    def tearDown(self):
        for file_name in os.listdir(self.storage.storage_path):
            os.remove(os.path.join(self.storage.storage_path, file_name))
        os.rmdir(self.storage.storage_path)

    def test_save_metrics(self):
        self.storage.save_metrics(self.test_workflow_id, self.test_metrics)
        files = os.listdir(self.storage.storage_path)
        self.assertEqual(len(files), 1)
        with open(os.path.join(self.storage.storage_path, files[0]), 'r') as f:
            saved_metrics = json.load(f)
        self.assertEqual(saved_metrics["workflow_id"], self.test_workflow_id)
        self.assertEqual(saved_metrics["execution_time"], self.test_metrics["execution_time"])
        self.assertEqual(saved_metrics["memory_usage"], self.test_metrics["memory_usage"])
        self.assertEqual(saved_metrics["status"], self.test_metrics["status"])

    def test_load_metrics(self):
        self.storage.save_metrics(self.test_workflow_id, self.test_metrics)
        loaded_metrics = self.storage.load_metrics(self.test_workflow_id)
        self.assertEqual(len(loaded_metrics), 1)
        for file_name, metrics in loaded_metrics.items():
            self.assertEqual(metrics["workflow_id"], self.test_workflow_id)
            self.assertEqual(metrics["execution_time"], self.test_metrics["execution_time"])
            self.assertEqual(metrics["memory_usage"], self.test_metrics["memory_usage"])
            self.assertEqual(metrics["status"], self.test_metrics["status"])

if __name__ == '__main__':
    unittest.main()