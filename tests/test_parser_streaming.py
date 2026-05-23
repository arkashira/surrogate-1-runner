import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from surrogate.parser import StreamingParser

class TestStreamingParser(unittest.TestCase):
    def setUp(self):
        self.parser = StreamingParser()

    def test_parse_10mb_stream(self):
        # Create a mock 10MB stream
        mock_stream = BytesIO(b'0' * 10 * 1024 * 1024)

        # Mock the parse method to return a known value
        with patch.object(self.parser, 'parse', return_value='parsed_data') as mock_parse:
            result = self.parser.parse_stream(mock_stream)

        # Assert the parse method was called once
        mock_parse.assert_called_once()

        # Assert the result is as expected
        self.assertEqual(result, 'parsed_data')

    def test_parse_1gb_stream(self):
        # Create a mock 1GB stream
        mock_stream = BytesIO(b'0' * 1024 * 1024 * 1024)

        # Mock the parse method to return a known value
        with patch.object(self.parser, 'parse', return_value='parsed_data') as mock_parse:
            result = self.parser.parse_stream(mock_stream)

        # Assert the parse method was called once
        mock_parse.assert_called_once()

        # Assert the result is as expected
        self.assertEqual(result, 'parsed_data')

    def test_parse_stream_with_error(self):
        # Create a mock stream that raises an error
        mock_stream = MagicMock()
        mock_stream.read.side_effect = Exception('Stream error')

        # Assert that the parse_stream method raises an exception
        with self.assertRaises(Exception):
            self.parser.parse_stream(mock_stream)

if __name__ == '__main__':
    unittest.main()