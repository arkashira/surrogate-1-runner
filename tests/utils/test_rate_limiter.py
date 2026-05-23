import time

import fakeredis
import pytest

from backend.utils.rate_limiter import RateLimiter


@pytest.fixture
def redis_client():
    return fakeredis.FakeRedis()


@pytest.fixture
def limiter(redis_client):
    # Use a short window for tests: 5 seconds
    return RateLimiter(redis_client, max_requests=2, window_seconds=5)


def test_allow_within_limit(limiter):
    user = "user-1"
    assert limiter.allow(user) is True
    assert limiter.allow(user) is True
    # Third request should be blocked
    assert limiter.allow(user) is False


def test_reset_after_window(limiter):
    user = "user-2"
    assert limiter.allow(user) is True
    assert limiter.allow(user) is True
    assert limiter.allow(user) is False
    # Wait for window to expire
    time.sleep(6)
    assert limiter.allow(user) is True
    assert limiter.allow(user) is True
    assert limiter.allow(user) is False


def test_reset_method(limiter):
    user = "user-3"
    assert limiter.allow(user) is True
    assert limiter.allow(user) is True
    limiter.reset(user)
    assert limiter.allow(user) is True
    assert limiter.allow(user) is True
    assert limiter.allow(user) is False