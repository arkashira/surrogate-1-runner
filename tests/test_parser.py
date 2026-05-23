import unittest
from parser import parse_data
from error_handling import handle_error

class TestParser(unittest.TestCase):
    def test_parse_data(self):
        # test parsing logic here
        pass

    def test_handle_error(self):
        # test error handling logic here
        e = Exception("Test error")
        result = handle_error(e, "Test context")
        self.assertIn("Test error", result)

if __name__ == "__main__":
    unittest.main()