import unittest
from unittest.mock import MagicMock
from src.llm_agent_integration import LLMAgentIntegration, OpenAIAgent, HuggingFaceAgent

class TestLLMAgentIntegration(unittest.TestCase):
    def setUp(self):
        self.integration = LLMAgentIntegration()
        self.openai_agent = OpenAIAgent(api_key="test_key")
        self.huggingface_agent = HuggingFaceAgent(model_name="test_model")

    def test_add_agent(self):
        self.integration.add_agent("openai", self.openai_agent)
        self.assertIn("openai", self.integration.agents)

    def test_get_response(self):
        self.openai_agent.generate_response = MagicMock(return_value="test_response")
        self.integration.add_agent("openai", self.openai_agent)
        response = self.integration.get_response("openai", "test_prompt")
        self.assertEqual(response, "test_response")

    def test_switch_agent(self):
        self.integration.add_agent("openai", self.openai_agent)
        self.integration.add_agent("huggingface", self.huggingface_agent)
        self.integration.switch_agent("openai", "huggingface")
        # Add assertions based on the expected behavior of switch_agent

if __name__ == '__main__':
    unittest.main()