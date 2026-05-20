import asyncio
import aiohttp
import json

class LLMDecisionError(Exception):
    pass

class LLMDecisionSDK:
    def __init__(self, base_url):
        self.base_url = base_url

    async def decide(self, input_data):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/decide", json=input_data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise LLMDecisionError(f"Error {response.status}: {await response.text()}")
        except aiohttp.ClientError as e:
            raise LLMDecisionError(f"Network error: {e}")

# opt/axentx/surrogate-1/sdk/llm_decision_test.py
import asyncio
import unittest
from unittest.mock import patch, MagicMock
from .llm_decision import LLMDecisionSDK, LLMDecisionError

class TestLLMDecisionSDK(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sdk = LLMDecisionSDK("http://localhost:8000")

    @patch("aiohttp.ClientSession.post")
    async def test_decide_success(self, mock_post):
        mock_post.return_value.__aenter__ = MagicMock(return_value=MagicMock(status=200, json=MagicMock(return_value={"output": "success"})))
        result = await self.sdk.decide({"input": "test"})
        self.assertEqual(result, {"output": "success"})

    @patch("aiohttp.ClientSession.post")
    async def test_decide_error(self, mock_post):
        mock_post.return_value.__aenter__ = MagicMock(return_value=MagicMock(status=500, text=MagicMock(return_value="Internal server error")))
        with self.assertRaises(LLMDecisionError) as context:
            await self.sdk.decide({"input": "test"})
        self.assertTrue("Error 500: Internal server error" in str(context.exception))

    @patch("aiohttp.ClientSession.post")
    async def test_decide_timeout(self, mock_post):
        mock_post.side_effect = asyncio.TimeoutError
        with self.assertRaises(LLMDecisionError) as context:
            await self.sdk.decide({"input": "test"})
        self.assertTrue("Network error: Timeout" in str(context.exception))

if __name__ == '__main__':
    unittest.main()

## Summary
- Created `llm_decision.py` with `decide` function and error handling
- Added unit tests for success, error, and timeout scenarios in `llm_decision_test.py`