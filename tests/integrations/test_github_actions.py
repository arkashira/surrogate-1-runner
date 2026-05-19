import os
import pytest
from src.integrations.github_actions import GitHubActionsIntegration

@pytest.fixture
def github_actions_integration():
    config = {
        'python_versions': ['3.8', '3.9', '3.10'],
        'workflow_file': '.github/workflows/test_coverage.yml'
    }
    return GitHubActionsIntegration(config)

def test_setup_workflow(github_actions_integration):
    github_actions_integration.setup_workflow()
    assert os.path.exists(github_actions_integration.workflow_file)

def test_run_tests(github_actions_integration, monkeypatch):
    def mock_run(*args, **kwargs):
        class Result:
            returncode = 0
            stdout = "Tests passed"
            stderr = ""
        return Result()

    monkeypatch.setattr('subprocess.run', mock_run)
    output = github_actions_integration.run_tests()
    assert output == "Tests passed"