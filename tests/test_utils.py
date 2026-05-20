import time
import pytest
from unittest import mock

from utils import retry

# Helper function to simulate a flaky operation
def flaky_factory(success_at: int):
    """
    Returns a function that raises an exception until the call count reaches
    `success_at`, then returns 'success'.
    """
    call_count = {"count": 0}

    def flaky():
        call_count["count"] += 1
        if call_count["count"] < success_at:
            raise RuntimeError(f"fail {call_count['count']}")
        return "success"

    return flaky

def test_retry_success_before_max_attempts(monkeypatch):
    # Patch time.sleep to avoid real delays
    monkeypatch.setattr(time, "sleep", lambda _: None)

    # Function succeeds on 3rd attempt
    flaky = flaky_factory(success_at=3)
    decorated = retry(max_attempts=5, backoff_factor=1)(flaky)

    result = decorated()
    assert result == "success"

def test_retry_exhausts_attempts_and_raises(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda _: None)

    # Function always fails
    flaky = flaky_factory(success_at=10)
    decorated = retry(max_attempts=5, backoff_factor=1)(flaky)

    with pytest.raises(RuntimeError) as excinfo:
        decorated()
    assert "fail 5" in str(excinfo.value)

def test_retry_backoff_pattern(monkeypatch):
    # Capture sleep calls
    sleep_calls = []

    def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(time, "sleep", fake_sleep)

    # Function fails twice then succeeds
    flaky = flaky_factory(success_at=3)
    decorated = retry(max_attempts=5, backoff_factor=1)(flaky)

    result = decorated()
    assert result == "success"

    # Backoff should be 1s then 2s
    assert sleep_calls == [1, 2]

def test_retry_on_failure_callback(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda _: None)

    callback_calls = []

    def on_failure(func, exc, attempts):
        callback_calls.append((func.__name__, str(exc), attempts))

    # Function always fails
    flaky = flaky_factory(success_at=10)
    decorated = retry(
        max_attempts=3,
        backoff_factor=1,
        on_failure=on_failure
    )(flaky)

    with pytest.raises(RuntimeError):
        decorated()

    assert len(callback_calls) == 1
    func_name, exc_msg, attempts = callback_calls[0]
    assert func_name == "flaky"
    assert "fail 3" in exc_msg
    assert attempts == 3