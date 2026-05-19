import unittest
from src.formatting.python_formatter import PythonFormatter

class TestPythonFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = PythonFormatter()
        self.simple_code = """
def hello_world():
    print("Hello, World!")
"""
        self.complex_code = """
class Example:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
"""
        self.default_config = {
            'max_line_length': 88,
            'indent_size': 4,
            'ignore': ['E203', 'E266', 'E704'],
            'aggressive': 1
        }

    def test_format_code(self):
        formatted = self.formatter.format_code(self.simple_code)
        self.assertIsInstance(formatted, str)
        self.assertNotEqual(formatted, self.simple_code)  # Should at least normalize whitespace

    def test_format_complex_code(self):
        formatted = self.formatter.format_code(self.complex_code)
        self.assertIsInstance(formatted, str)
        self.assertNotEqual(formatted, self.complex_code)

    def test_get_config(self):
        config = self.formatter.get_config()
        self.assertIsInstance(config, dict)
        self.assertEqual(config['max_line_length'], 88)

    def test_set_config(self):
        new_config = {
            'max_line_length': 100,
            'indent_size': 2,
            'ignore': ['E203'],
            'aggressive': 2
        }
        self.formatter.set_config(new_config)
        self.assertEqual(self.formatter.get_config()['max_line_length'], 100)

    def test_reset_config(self):
        self.formatter.set_config({'max_line_length': 100})
        self.formatter.reset_config()
        self.assertEqual(self.formatter.get_config(), self.default_config)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.formatter.format_code(123)  # Not a string
        with self.assertRaises(ValueError):
            self.formatter.set_config("not a dict")  # Not a dictionary

if __name__ == '__main__':
    unittest.main()