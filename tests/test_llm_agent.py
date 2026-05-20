import unittest
from src.llm_agent import LLMAgent, LLMAgentConfig

class TestLLMAgent(unittest.TestCase):
    def setUp(self):
        self.config = LLMAgentConfig(
            agent_id="test_agent",
            model_name="test_model",
            api_key="test_key",
            parameters={"param1": "value1"}
        )
        self.agent = LLMAgent(self.config)

    def test_connect(self):
        self.agent.connect()

    def test_execute(self):
        response = self.agent.execute("test prompt")
        self.assertEqual(response, "Response from test_agent")

    def test_disconnect(self):
        self.agent.disconnect()

if __name__ == '__main__':
    unittest.main()