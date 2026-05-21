import unittest
from surrogate_1.src.gpt4_api import validate_gpt4_api_key, get_gpt4_api_key

class TestGPT4APIKeyValidation(unittest.TestCase):
    def test_valid_api_key(self):
        api_key = "abcdefghijklmnopqrstuvwxyz012345"
        self.assertEqual(validate_gpt4_api_key(api_key), api_key)

    def test_invalid_api_key(self):
        api_key = "invalid_key"
        with self.assertRaises(ValueError):
            validate_gpt4_api_key(api_key)

    def test_get_gpt4_api_key(self):
        os.environ["GPT4_API_KEY"] = "abcdefghijklmnopqrstuvwxyz012345"
        self.assertEqual(get_gpt4_api_key(), "abcdefghijklmnopqrstuvwxyz012345")

    def test_get_gpt4_api_key_not_set(self):
        del os.environ["GPT4_API_KEY"]
        with self.assertRaises(ValueError):
            get_gpt4_api_key()

if __name__ == "__main__":
    unittest.main()