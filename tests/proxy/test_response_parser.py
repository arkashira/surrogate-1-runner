import unittest
from src.proxy.response_parser import ResponseParser

class TestResponseParser(unittest.TestCase):
    def test_parse_response_with_structured_output(self):
        response = {
            'response_format': 'structured_output',
            'content': '{"function_name": "test_function", "arguments": {"arg1": "value1"}}'
        }
        expected_response = {
            'response_format': 'structured_output',
            'tool_calls': [{
                'function': {
                    'name': 'test_function',
                    'arguments': {'arg1': 'value1'}
                }
            }]
        }
        parsed_response = ResponseParser.parse_response(response)
        self.assertEqual(parsed_response, expected_response)

    def test_parse_response_without_structured_output(self):
        response = {
            'response_format': 'text',
            'content': 'This is a text response.'
        }
        expected_response = {
            'response_format': 'text',
            'content': 'This is a text response.'
        }
        parsed_response = ResponseParser.parse_response(response)
        self.assertEqual(parsed_response, expected_response)

    def test_parse_response_with_invalid_json(self):
        response = {
            'response_format': 'structured_output',
            'content': 'Invalid JSON'
        }
        expected_response = {
            'response_format': 'structured_output',
            'content': 'Invalid JSON'
        }
        parsed_response = ResponseParser.parse_response(response)
        self.assertEqual(parsed_response, expected_response)

if __name__ == '__main__':
    unittest.main()