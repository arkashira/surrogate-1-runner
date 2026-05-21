import os
import json
import tempfile
import pytest

# Ensure the modules import the test‑specific log path.
from surrogate_1.src import logging as audit_logging
from surrogate_1.src import admin as admin_module


@pytest.fixture(autouse=True)
def isolated_audit_log():
    """Redirect audit logging to a temporary file for each test."""
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        temp_path = tf.name
    original_path = audit_logging.AUDIT_LOG_PATH
    os.environ["AUDIT_LOG_PATH"] = temp_path
    # Reload module variables that depend on the env var.
    audit_logging.AUDIT_LOG_PATH = temp_path
    yield
    # Cleanup
    os.remove(temp_path)
    os.environ["AUDIT_LOG_PATH"] = ""
    audit_logging.AUDIT_LOG_PATH = original_path


def test_log_and_view_audit_trail():
    # Arrange
    user_id = "user123"
    ai_tool = "gpt-4"
    payload = {"prompt": "Hello world", "metadata": {"session": "abc"}}
    audit_logging.log_ai_request(user_id, ai_tool, payload)

    # Act
    trail = admin_module.view_audit_trail("admin@example.com")

    # Assert
    assert len(trail) == 1
    entry = trail[0]
    assert entry["user_id"] == user_id
    assert entry["ai_tool"] == ai_tool
    assert entry["request"] == payload
    # Timestamp should be ISO‑8601 and end with 'Z'
    assert entry["timestamp"].endswith("Z")


def test_non_admin_cannot_view():
    with pytest.raises(admin_module.AuthorizationError):
        admin_module.view_audit_trail("regular_user@example.com")