import unittest
from unittest.mock import Mock
from src.middleware.validation import validate_payload, validation_middleware

class TestValidationMiddleware(unittest.TestCase):
    def test_valid_payload(self):
        environ = Mock()
        environ['CONTENT_TYPE'] = 'application/json'
        environ['wsgi.input'] = Mock()
        environ['wsgi.input'].read.return_value = b'{"file_path": "test.txt", "content": "Hello World", "cursor_position": 10, "selection": "Hello"}'
        start_response = Mock()
        response = validation_middleware(environ, start_response)
        self.assertEqual(response, [b''])
        start_response.assert_called_once_with('200 OK', [])

    def test_invalid_payload(self):
        environ = Mock()
        environ['CONTENT_TYPE'] = 'application/json'
        environ['wsgi.input'] = Mock()
        environ['wsgi.input'].read.return_value = b'{"file_path": "test.txt", "content": "Hello World", "cursor_position": 10}'
        start_response = Mock()
        response = validation_middleware(environ, start_response)
        self.assertEqual(response, [b''])
        start_response.assert_called_once_with('400 Bad Request', [])

    def test_non_json_payload(self):
        environ = Mock()
        environ['CONTENT_TYPE'] = 'text/plain'
        environ['wsgi.input'] = Mock()
        environ['wsgi.input'].read.return_value = b'Hello World'
        start_response = Mock()
        response = validation_middleware(environ, start_response)
        self.assertEqual(response, [b''])
        start_response.assert_called_once_with('415 Unsupported Media Type', [])

if __name__ == '__main__':
    unittest.main()