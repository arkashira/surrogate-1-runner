import unittest
from unittest.mock import patch, MagicMock
from .claude import ClaudeAPI
import os

class TestClaudeAPI(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.claude = ClaudeAPI(self.api_key)

    @patch('requests.post')
    def test_complete_prompt(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"text": "test response"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.claude.complete_prompt("test prompt")
        self.assertEqual(result, "test response")

    @patch('requests.post')
    def test_analyze_text(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "analysis": "test analysis"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.claude.analyze_text("test text")
        self.assertEqual(result, {"analysis": "test analysis"})

    @patch('requests.post')
    def test_get_usage_stats(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "usage": "test usage"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.claude.get_usage_stats()
        self.assertEqual(result, {"usage": "test usage"})

    def test_log_access(self):
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.claude._log_access("test_endpoint", {"test": "data"}, {"response": "data"})
            mock_file.assert_called_once_with("/var/log/axentx/claude_audit.log", "a")

if __name__ == '__main__':
    unittest.main()