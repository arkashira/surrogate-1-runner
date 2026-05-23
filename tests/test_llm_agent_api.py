import unittest
from fastapi.testclient import TestClient
from src.api.llm_agent_api import app

class TestLLMAgentAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_response(self):
        response = self.client.post("/generate_response", json={"agent_name": "openai", "prompt": "test_prompt"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())

    def test_switch_agent(self):
        response = self.client.post("/switch_agent", json={"current_agent_name": "openai", "new_agent_name": "huggingface"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

if __name__ == '__main__':
    unittest.main()