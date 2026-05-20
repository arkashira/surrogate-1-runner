"""
GitHub Actions integration for surrogate-1.

This module provides a lightweight runner that can be invoked from a
GitHub Actions workflow.  It reads a YAML configuration file, executes
optional pre‑steps, runs the test command, generates a coverage report,
and finally executes optional post‑steps.  The runner is intentionally
minimal so it can be used with any test runner that can be invoked
from the command line.

The configuration file is expected to contain a top‑level ``github_action``
section.  Example:

    github_action:
      enabled: true
      pre_steps:
        - pip install -r requirements.txt
      test_command: pytest -q
      coverage_command: coverage run -m pytest && coverage report
      post_steps:
        - echo "All done"

The runner is safe to import in any environment; it only executes
commands when ``enabled`` is true.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Union

import yaml


class GitHubAction:
    """
    GitHub Actions runner.

    Parameters
    ----------
    config_path : Union[str, Path]
        Path to the YAML configuration file.
    """

    def __init__(self, config_path: Union[str, Path]) -> None:
        self.config_path = Path(config_path)
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        self.config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        self.enabled = bool(
            self.config.get("github_action", {}).get("enabled", False)
        )
        self.pre_steps: List[str] = self.config.get("github_action", {}).get(
            "pre_steps", []
        )
        self.post_steps: List[str] = self.config.get("github_action", {}).get(
            "post_steps", []
        )
        self.test_command: str = self.config.get("github_action", {}).get(
            "test_command", "pytest"
        )
        self.coverage_command: str = self.config.get("github_action", {}).get(
            "coverage_command", "coverage run -m pytest && coverage report"
        )

    def _run_command(self, cmd: str) -> None:
        """Run a shell command, raising on failure."""
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True, check=True, env=os.environ)

    def _run_steps(self, steps: List[str]) -> None:
        for step in steps:
            self._run_command(step)

    def run(self) -> None:
        """
        Execute the configured steps.

        The method will exit with a non‑zero status if any command fails.
        """
        if not self.enabled:
            print("GitHub Action integration is disabled; skipping.")
            return

        # Pre‑steps
        if self.pre_steps:
            print("Executing pre‑steps")
            self._run_steps(self.pre_steps)

        # Test command
        print("Executing test command")
        self._run_command(self.test_command)

        # Coverage command
        print("Executing coverage command")
        self._run_command(self.coverage_command)

        # Post‑steps
        if self.post_steps:
            print("Executing post‑steps")
            self._run_steps(self.post_steps)


if __name__ == "__main__":
    # When run as a script, the first argument is the config path.
    if len(sys.argv) != 2:
        print("Usage: python -m integrations.github_action <config.yaml>", file=sys.stderr)
        sys.exit(1)

    runner = GitHubAction(sys.argv[1])
    runner.run()