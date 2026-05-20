import unittest
from src.openai_api import OpenAIAPI

class TestOpenAIAPI(unittest.TestCase):
    def setUp(self):
        self.api_key = 'your_openai_api_key'
        self.openai_api = OpenAIAPI(self.api_key)

    def test_generate_text(self):
        prompt = "Once upon a time"
        generated_text = self.openai_api.generate_text(prompt)
        self.assertIsInstance(generated_text, str)
        self.assertTrue(len(generated_text) > 0)

    def test_get_embeddings(self):
        text = "Hello world"
        embeddings = self.openai_api.get_embeddings(text)
        self.assertIsInstance(embeddings, list)
        self.assertTrue(len(embeddings) > 0)

    def test_list_models(self):
        models = self.openai_api.list_models()
        self.assertIsInstance(models, list)
        self.assertTrue(len(models) > 0)

if __name__ == '__main__':
    unittest.main()