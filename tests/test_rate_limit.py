import time
import threading

import pytest

# The RateLimiter implementation is expected to live in `rate_limit.py` at the project root.
# It should expose a `RateLimiter` class with the following interface:
#   rl = RateLimiter(limit: int, period_seconds: int)
#   allowed, retry_after = rl.check(api_key: str) -> (bool, int)
#   # `allowed` is True if the request is permitted, False otherwise.
#   # `retry_after` is the number of seconds the caller should wait before retrying
#   #   (0 when `allowed` is True).
# The class should also log rate‑limit events using the standard `logging` module.
from rate_limit import RateLimiter


@pytest.fixture
def fresh_limiter():
    """Provide a fresh RateLimiter for each test."""
    return RateLimiter(limit=100, period_seconds=60)


def test_allow_up_to_limit(fresh_limiter):
    """Requests up to the limit should be allowed."""
    rl = fresh_limiter
    api_key = "test-key"

    for i in range(100):
        allowed, retry = rl.check(api_key)
        assert allowed, f"Request #{i+1} should be allowed"
        assert retry == 0, "Retry‑after must be 0 for allowed requests"


def test_exceed_limit_returns_429_like_response(fresh_limiter):
    """The request that exceeds the limit should be denied with a retry‑after."""
    rl = fresh_limiter
    api_key = "exceed-key"

    # Exhaust the quota
    for _ in range(100):
        allowed, _ = rl.check(api_key)
        assert allowed

    # 101st request should be denied
    allowed, retry = rl.check(api_key)
    assert not allowed, "Request exceeding the limit must be denied"
    assert retry > 0, "Retry‑after should be a positive integer"


def test_retry_after_decreases_after_wait(fresh_limiter):
    """After waiting enough time, the retry‑after should drop to zero."""
    rl = fresh_limiter
    api_key = "wait-key"

    # Fill the bucket
    for _ in range(100):
        rl.check(api_key)

    # Capture the retry‑after value
    _, retry_initial = rl.check(api_key)
    assert retry_initial > 0

    # Wait half the period and check that retry‑after has decreased
    time.sleep(30)
    _, retry_half = rl.check(api_key)
    assert 0 < retry_half < retry_initial

    # Wait until the period expires; the next request must be allowed
    time.sleep(31)
    allowed, retry_final = rl.check(api_key)
    assert allowed
    assert retry_final == 0


def test_concurrent_requests_respect_limit(fresh_limiter):
    """Concurrent bursts must not allow more than the configured limit."""
    rl = fresh_limiter
    api_key = "concurrent-key"
    results = []

    def make_request():
        allowed, _ = rl.check(api_key)
        results.append(allowed)

    threads = [threading.Thread(target=make_request) for _ in range(120)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Exactly 100 requests should be allowed; the rest denied
    assert results.count(True) == 100
    assert results.count(False) == 20


def test_rate_limit_events_are_logged(fresh_limiter, caplog):
    """Each denied request must emit a log entry with timestamp and API key."""
    rl = fresh_limiter
    api_key = "log-key"

    # Exhaust quota
    for _ in range(100):
        rl.check(api_key)

    # Trigger a denied request
    with caplog.at_level("WARNING"):
        rl.check(api_key)

    # Verify a log record exists containing the API key
    matching = [rec for rec in caplog.records if api_key in rec.getMessage()]
    assert matching, "A log entry containing the API key should be emitted on rate‑limit breach"
    # Ensure the log includes a timestamp (standard LogRecord always has created attribute)
    for rec in matching:
        assert hasattr(rec, "created")