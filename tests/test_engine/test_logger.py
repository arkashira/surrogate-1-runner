import unittest
from unittest.mock import Mock
from engine.logger import display_validation_results

class TestLogger(unittest.TestCase):
    def test_display_validation_results(self):
        # Mock the GitHub API
        github = Mock()
        repo = Mock()
        sha = "mock-sha"
        results = "mock-results"
        
        # Call the function
        display_validation_results(github, repo, sha, results)
        
        # Assert that the log message was created
        github.get_repo.assert_called_once_with(repo)
        repo.get_actions_log().create_comment.assert_called_once_with(f"Validation results for commit {sha}: {results}")

if __name__ == "__main__":
    unittest.main()