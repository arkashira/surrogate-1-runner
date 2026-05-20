import os
import subprocess
import pytest
from pathlib import Path

class TestCIContinuity:
    """Ensure CI configuration matches local development"""
    
    def test_requirements_file_exists(self):
        """Verify dependencies are documented"""
        assert Path("requirements.txt").exists() or Path("pyproject.toml").exists()
    
    def test_flake8_config_exists(self):
        """CI linting should match project config"""
        has_config = (
            Path(".flake8").exists() or 
            Path("pyproject.toml").exists() or
            Path("setup.cfg").exists()
        )
        assert has_config, "Add flake8 configuration to avoid CI drift"
    
    def test_pytest_can_discover_tests(self):
        """Verify test discovery works"""
        result = subprocess.run(
            ["pytest", "--collect-only", "-q"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
    
    def test_black_formatting_check_passes(self):
        """Pre-commit check should pass locally first"""
        result = subprocess.run(
            ["black", "--check", "."],
            capture_output=True
        )
        assert result.returncode == 0, "Run 'black .' to fix formatting"

class TestProjectStructure:
    """Validate project layout for CI compatibility"""
    
    def test_has_github_workflows_directory(self):
        assert Path(".github/workflows").exists()
    
    def test_workflow_file_valid_yaml(self):
        import yaml
        workflow_path = Path(".github/workflows/ci.yml")
        if workflow_path.exists():
            with open(workflow_path) as f:
                data = yaml.safe_load(f)
                assert "on" in data
                assert "jobs" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])