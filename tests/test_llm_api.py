import unittest
from llm_api import LLMAPI, load_config

class TestLLMAPI(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        self.llm_api = LLMAPI(self.config)

    def test_perform_inference(self):
        input_data = "Test input"
        expected_result = "Generic LLM Runtime Initialized: Test input"
        result = self.llm_api.perform_inference(input_data)
        self.assertEqual(result, expected_result)

    def test_initialize_rag_runtime(self):
        self.config['runtime_type'] = 'rag'
        self.llm_api = LLMAPI(self.config)
        result = self.llm_api.perform_inference("Test input")
        expected_result = "RAG Runtime Initialized: Test input"
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()