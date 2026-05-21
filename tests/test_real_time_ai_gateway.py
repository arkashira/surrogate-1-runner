import asyncio
import unittest
from unittest.mock import patch
from src.ai_tools.real_time_ai_gateway import RealTimeAIGateway

class TestRealTimeAIGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = RealTimeAIGateway()

    @patch('src.ai_tools.real_time_ai_gateway.asyncio.sleep')
    def test_handle_request(self, mock_sleep):
        mock_sleep.return_value = None
        request = "Test Request"
        result = asyncio.run(self.gateway.handle_request(request))
        self.assertEqual(result, {"result": f"Processed {request}"})

    def test_enqueue_request(self):
        request = "Test Request"
        self.gateway.enqueue_request(request)
        self.assertNotEqual(self.gateway.request_queue.qsize(), 0)

if __name__ == '__main__':
    unittest.main()