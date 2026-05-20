import unittest
from src.proxy_layer import ProxyLayer

class TestProxyLayer(unittest.TestCase):
    def setUp(self):
        self.proxy_layer = ProxyLayer("gpt2")

    def test_process_request(self):
        request = {"text": "Hello, world!"}
        response = self.proxy_layer.process_request(request)
        self.assertIn("response", response)
        self.assertIn("token_usage", response)
        self.assertIn("input_tokens", response["token_usage"])
        self.assertIn("output_tokens", response["token_usage"])
        self.assertIn("cost", response["token_usage"])

if __name__ == "__main__":
    unittest.main()