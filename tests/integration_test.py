import unittest
import os
import time
from surrogate_1 import stream_data, parser

class TestIntegrationStream(unittest.TestCase):
    def test_1gb_stream(self):
        start_time = time.time()
        stream_size = 1 * 1024 * 1024 * 1024  # 1 GB
        stream_data(stream_size)
        end_time = time.time()
        self.assertLess(end_time - start_time, 30 * 60)  # 30 minutes

    def test_parser_coverage(self):
        # Test parser module coverage
        parser_coverage = parser.get_coverage()
        self.assertGreater(parser_coverage, 90)

if __name__ == '__main__':
    unittest.main()