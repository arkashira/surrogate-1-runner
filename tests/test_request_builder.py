
import unittest
from unittest.mock import Mock
from src.proxy import request_builder

class TestRequestBuilder(unittest.TestCase):
    def setUp(self):
        self.tool_function = Mock(name="tool_function")
        self.tool_function.return_value = "mock_response"
        self.inputs = [1, 2, 3]

    def test_build_openai_request(self):
        request = request_builder.build_openai_request(self.tool_function, self.inputs)
        self.assertIn("model", request)
        self.assertIn("prompt", request)
        self.assertIn("response_format", request)
        self.assertEqual(request["response_format"]["type"], "json_schema")
        self.tool_function.assert_called_once_with(*self.inputs)

    def test_build_openai_request_no_response_format(self):
        request = request_builder.build_openai_request(self.tool_function, self.inputs, response_format=None)
        self.assertIn("model", request)
        self.assertIn("prompt", request)
        self.assertNotIn("response_format", request)
        self.tool_function.assert_called_once_with(*self.inputs)

    def test_replace_tool_calls_with_response_format(self):
        request = {
            "tool_calls": {
                "name": "test_tool",
                "arguments": self.inputs
            }
        }
        request = request_builder.replace_tool_calls_with_response_format(request)
        self.assertIn("response_format", request)
        self.assertNotIn("tool_calls", request)
        self.assertEqual(request["response_format"]["type"], "json_schema")
        self.assertIn("arguments", request["response_format"]["schema"]["properties"])

if __name__ == "__main__":
    unittest.main()