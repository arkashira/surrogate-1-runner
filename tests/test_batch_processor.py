import unittest
from unittest.mock import patch
from workers.batch_processor import BatchProcessor
from utils.resource_manager import ResourceManager

class TestBatchProcessor(unittest.TestCase):
    @patch.object(ResourceManager, 'calculate_optimal_batch_size')
    def test_get_optimal_batch_size(self, mock_calculate):
        mock_calculate.return_value = 200
        processor = BatchProcessor()
        self.assertEqual(processor.get_optimal_batch_size(), 200)

    def test_process_batch(self):
        processor = BatchProcessor(base_batch_size=10, item_size=1)
        items = ['item1', 'item2', 'item3']
        result = processor.process_batch(items)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, ['ITEM1', 'ITEM2', 'ITEM3'])

    @patch.object(ResourceManager, 'get_memory_usage_percentage')
    def test_monitor_memory_usage_high(self, mock_usage):
        mock_usage.return_value = 85
        processor = BatchProcessor(base_batch_size=100)
        processor.monitor_memory_usage()
        self.assertEqual(processor.base_batch_size, 50)

    @patch.object(ResourceManager, 'get_memory_usage_percentage')
    def test_monitor_memory_usage_low(self, mock_usage):
        mock_usage.return_value = 70
        processor = BatchProcessor(base_batch_size=100)
        processor.monitor_memory_usage()
        self.assertEqual(processor.base_batch_size, 100)

if __name__ == '__main__':
    unittest.main()