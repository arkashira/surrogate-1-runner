import unittest
from surrogate.parser import StreamingParser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = StreamingParser()

    def test_parse(self):
        # Test data
        data = b'test data'

        # Parse the data
        result = self.parser.parse(data)

        # Assert the result is as expected
        self.assertEqual(result, 'parsed_test_data')

    def test_parse_with_error(self):
        # Test data that will cause an error
        data = b''

        # Assert that the parse method raises an exception
        with self.assertRaises(ValueError):
            self.parser.parse(data)

if __name__ == '__main__':
    unittest.main()