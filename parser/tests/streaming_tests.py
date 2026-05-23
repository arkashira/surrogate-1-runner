import unittest
from unittest.mock import patch, MagicMock
from surrogate_1.parser import StreamingParser
from surrogate_1.utils import generate_large_data_stream

class TestStreamingParser(unittest.TestCase):

    def test_large_data_stream(self):
        # Generate a large data stream
        data_stream = generate_large_data_stream(1000000)

        # Create a StreamingParser instance
        parser = StreamingParser()

        # Process the large data stream
        parser.process(data_stream)

        # Check that the parser did not consume unbounded memory
        self.assertLess(parser.get_memory_usage(), 1024 * 1024 * 1024)  # 1 GB

    def test_oom_crashes(self):
        # Generate a large data stream
        data_stream = generate_large_data_stream(1000000)

        # Create a StreamingParser instance
        parser = StreamingParser()

        # Process the large data stream
        try:
            parser.process(data_stream)
        except MemoryError:
            self.fail("OOM crash occurred")

    def test_performance(self):
        # Generate a large data stream
        data_stream = generate_large_data_stream(1000000)

        # Create a StreamingParser instance
        parser = StreamingParser()

        # Process the large data stream
        import time
        start_time = time.time()
        parser.process(data_stream)
        end_time = time.time()

        # Check that the parser maintains the same or better performance
        self.assertLess(end_time - start_time, 10)  # 10 seconds

if __name__ == '__main__':
    unittest.main()