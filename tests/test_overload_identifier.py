import unittest
from src.overload_identifier import OverloadIdentifier

class TestOverloadIdentifier(unittest.TestCase):
    def setUp(self):
        self.identifier = OverloadIdentifier()

    def test_normalize_type(self):
        self.assertEqual(self.identifier.normalize_type('String'), 'str')
        self.assertEqual(self.identifier.normalize_type('Int'), 'int')
        self.assertEqual(self.identifier.normalize_type('List<String>'), 'list<str>')
        self.assertEqual(self.identifier.normalize_type('String[]'), 'str[]')
        self.assertEqual(self.identifier.normalize_type('com.example.InlineClass'), 'InlineClass')

    def test_generate_overload_id(self):
        self.assertEqual(
            self.identifier.generate_overload_id('example', ['String', 'Int']),
            'example-str-int'
        )
        self.assertEqual(
            self.identifier.generate_overload_id('example', ['List<String>', 'Int[]']),
            'example-list<str>-int[]'
        )

    def test_parse_function_signature(self):
        self.assertEqual(
            self.identifier.parse_function_signature('example(String, Int)'),
            ('example', ['String', 'Int'])
        )
        self.assertEqual(
            self.identifier.parse_function_signature('example(List<String>, Int[])'),
            ('example', ['List<String>', 'Int[]'])
        )
        self.assertIsNone(self.identifier.parse_function_signature('invalid signature'))

if __name__ == '__main__':
    unittest.main()