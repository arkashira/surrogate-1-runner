import unittest
from src.data_quality_monitor import DataQualityMonitor

class TestDataQualityMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = DataQualityMonitor()

    def test_check_data_quality(self):
        test_data = [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Test2'}]
        self.monitor.check_data_quality(test_data)
        self.assertEqual(len(self.monitor.get_alerts()), 0)

if __name__ == '__main__':
    unittest.main()