import os
import subprocess
from typing import Dict, Any

class GitHubActionsIntegration:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.workflow_file = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', '.github', 'workflows', 'test_coverage.yml'
        )

    def setup_workflow(self):
        """Set up the GitHub Actions workflow file."""
        self._ensure_workflow_file_exists()

    def run_tests(self):
        """Run tests with coverage reporting."""
        result = subprocess.run(
            ['python', '-m', 'pytest', '--cov=./src', '--cov-report=xml:coverage.xml'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Tests failed: {result.stderr}")
        return result.stdout

    def _ensure_workflow_file_exists(self):
        """Ensure the workflow file exists."""
        if not os.path.exists(self.workflow_file):
            raise FileNotFoundError(f"Workflow file not found at {self.workflow_file}")