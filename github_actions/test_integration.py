
import os
import unittest
from github import Github

# Replace with your own access token
ACCESS_TOKEN = "your_access_token_here"
REPO_OWNER = "axentx"
REPO_NAME = "surrogate-1"

class TestGitHubActionsIntegration(unittest.TestCase):

    def setUp(self):
        self.g = Github(ACCESS_TOKEN)
        self.repo = self.g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

    def test_workflow_runs(self):
        workflows = self.repo.get_workflows()
        for workflow in workflows:
            runs = workflow.get_runs()
            for run in runs:
                self.assertEqual(run.status, "completed", f"Workflow run {run.id} is not completed")

if __name__ == '__main__':
    unittest.main()