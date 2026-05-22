import os
import sys
import json
import pathlib
from unittest import mock

import pytest
from click.testing import CliRunner

# Import the click command group. Adjust the import path if the CLI entry point differs.
# The project is expected to expose a `cli` object (click.Group) in `surrogate/cli/__init__.py`.
# The `report` command is registered under this group.
from surrogate.cli import cli  # type: ignore


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def temp_cwd(tmp_path, monkeypatch):
    """Run the CLI in an isolated temporary working directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _set_token(monkeypatch, token_value: str | None):
    """Helper to set or unset the tenant token environment variable."""
    env_var = "SURROGATE_TENANT_TOKEN"
    if token_value is None:
        monkeypatch.delenv(env_var, raising=False)
    else:
        monkeypatch.setenv(env_var, token_value)


def test_report_success(runner, temp_cwd, monkeypatch):
    """Happy path – token present, API returns PDF bytes."""
    _set_token(monkeypatch, "dummy-token")

    fake_pdf = b"%PDF-1.4\n%Fake PDF content\n%%EOF"

    # Patch the low‑level API call that the CLI command uses.
    # The actual implementation is assumed to be `surrogate.api.fetch_report`.
    with mock.patch("surrogate.api.fetch_report", return_value=fake_pdf) as mock_fetch:
        result = runner.invoke(cli, ["report", "--format", "pdf"])

    # CLI should succeed.
    assert result.exit_code == 0, f"CLI failed: {result.output}"
    # The API should have been called with the correct arguments.
    mock_fetch.assert_called_once_with(format="pdf", token="dummy-token")

    # Verify that the file was written to the current directory.
    expected_path = pathlib.Path("investor_report.pdf")
    assert expected_path.is_file(), "PDF file was not created"

    # Verify file content matches the mocked payload.
    assert expected_path.read_bytes() == fake_pdf

    # CLI should print the path to stdout.
    assert "investor_report.pdf" in result.output


def test_report_missing_token(runner, temp_cwd, monkeypatch):
    """Error path – tenant token environment variable is missing."""
    _set_token(monkeypatch, None)

    result = runner.invoke(cli, ["report", "--format", "pdf"])

    # Expect a non‑zero exit code.
    assert result.exit_code != 0
    # The error message should be user‑friendly.
    assert "tenant token" in result.output.lower()
    # No file should be created.
    assert not pathlib.Path("investor_report.pdf").exists()


def test_report_api_error(runner, temp_cwd, monkeypatch):
    """Error path – API raises an exception (e.g., network failure)."""
    _set_token(monkeypatch, "dummy-token")

    # Simulate an exception from the API layer.
    api_error = RuntimeError("API request failed")
    with mock.patch("surrogate.api.fetch_report", side_effect=api_error) as mock_fetch:
        result = runner.invoke(cli, ["report", "--format", "pdf"])

    # CLI should exit with a non‑zero code.
    assert result.exit_code != 0
    # The exception message (or a friendly wrapper) should appear in output.
    assert "api request failed" in result.output.lower()
    # Ensure the API was indeed called.
    mock_fetch.assert_called_once_with(format="pdf", token="dummy-token")
    # No file should be written.
    assert not pathlib.Path("investor_report.pdf").exists()