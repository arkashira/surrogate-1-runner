import unittest
from unittest.mock import patch
from utils.resource_manager import ResourceManager

class TestResourceManager(unittest.TestCase):
    @patch('psutil.virtual_memory')
    def test_get_available_memory(self, mock_virtual_memory):
        mock_mem = type('Mem', (), {'available': 1024 * 1024 * 1024})  # 1GB
        mock_virtual_memory.return_value = mock_mem
        rm = ResourceManager()
        self.assertEqual(rm.get_available_memory(), 1024 * 1024 * 1024)

    @patch('psutil.virtual_memory')
    def test_calculate_optimal_batch_size(self, mock_virtual_memory):
        mock_mem = type('Mem', (), {'available': 1024 * 1024 * 1024})  # 1GB
        mock_virtual_memory.return_value = mock_mem
        rm = ResourceManager()
        optimal_size = rm.calculate_optimal_batch_size(100, 1024)  # 1KB per item
        self.assertGreater(optimal_size, 100)  # Should be larger than base size

    @patch('psutil.virtual_memory')
    def test_get_memory_usage_percentage(self, mock_virtual_memory):
        mock_mem = type('Mem', (), {'percent': 75})
        mock_virtual_memory.return_value = mock_mem
        rm = ResourceManager()
        self.assertEqual(rm.get_memory_usage_percentage(), 75)

if __name__ == '__main__':
    unittest.main()