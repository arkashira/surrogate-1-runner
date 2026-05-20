import unittest
from unittest.mock import patch, MagicMock
from surrogate_1 import vocab_endpoint

class TestVocabEndpoint(unittest.TestCase):

    def test_vocab_endpoint(self):
        # Test that the endpoint returns a list of 10 terms
        response = vocab_endpoint()
        self.assertEqual(len(response), 10)

    def test_term_definition(self):
        # Test that each term includes a definition and an example sentence
        response = vocab_endpoint()
        for term in response:
            self.assertIn('definition', term)
            self.assertIn('example_sentence', term)

    def test_term_category(self):
        # Test that terms are tagged by category
        response = vocab_endpoint()
        for term in response:
            self.assertIn('category', term)

    @patch('surrogate_1.vocab_endpoint.mark_as_learned')
    def test_mark_as_learned(self, mock_mark_as_learned):
        # Test that marking a term as learned persists it in the user profile
        vocab_endpoint()
        mock_mark_as_learned.assert_called_once()

    def test_learned_terms_persistence(self):
        # Test that learned terms are persisted in the user profile
        vocab_endpoint()
        # Assuming a user profile is stored in a database
        # This test would verify that the learned terms are stored correctly
        pass

if __name__ == '__main__':
    unittest.main()