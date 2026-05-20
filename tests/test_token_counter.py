import unittest
from src.token_counter import TokenCounter

class TestTokenCounter(unittest.TestCase):
    def setUp(self):
        self.token_counter = TokenCounter("gpt2")

    def test_count_tokens(self):
        text = "Hello, world!"
        input_tokens, output_tokens = self.token_counter.count_tokens(text)
        self.assertGreater(input_tokens, 0)
        self.assertGreater(output_tokens, 0)

    def test_get_cost(self):
        input_tokens = 10
        output_tokens = 20
        cost = self.token_counter.get_cost(input_tokens, output_tokens)
        self.assertGreater(cost, 0)

if __name__ == "__main__":
    unittest.main()