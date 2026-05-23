import unittest
from unittest.mock import patch, MagicMock
from src.parser import Parser
import resource

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(max_workers=2, chunk_size=2, memory_limit_mb=10)
        self.test_data = [
            {"id": 1, "name": "Test 1"},
            {"id": 2, "name": "Test 2"},
            {"id": 3, "name": "Test 3"},
            {"id": 4, "name": "Test 4"}
        ]

    def test_parse_data(self):
        results = self.parser.parse_data(self.test_data)
        self.assertEqual(len(results), len(self.test_data))
        self.assertIsNone(results[0])  # First item should be None due to deduplication

    def test_normalize_item(self):
        item = {"id": 1, "name": "  TEST 1  "}
        normalized = self.parser._normalize_item(item)
        self.assertEqual(normalized['name'], "test 1")

    def test_deduplicate_item(self):
        item1 = {"id": 1, "name": "Test"}
        item2 = {"id": 2, "name": "Test"}
        self.parser._seen_hashes = set()
        self.assertIsNotNone(self.parser._deduplicate_item(item1))
        self.assertIsNone(self.parser._deduplicate_item(item2))

    @patch('resource.getrusage')
    def test_memory_monitoring(self, mock_getrusage):
        mock_getrusage.return_value = MagicMock(ru_maxrss=15)  # 15MB
        with self.assertRaises(MemoryError):
            self.parser._check_memory_usage()

    def test_chunked_processing(self):
        with patch.object(self.parser, '_process_item') as mock_process:
            mock_process.return_value = {"processed": True}
            results = self.parser.parse_data(self.test_data)
            self.assertEqual(mock_process.call_count, len(self.test_data))

if __name__ == '__main__':
    unittest.main()