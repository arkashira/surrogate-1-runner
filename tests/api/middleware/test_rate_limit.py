import pytest
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient

from src.api.middleware.rate_limit import RateLimitMiddleware, FREE_TIER_DAILY_LIMIT


def create_app():
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/download/video")
    async def download_video(x_user_tier: str = Header(None)):
        # Simulate a download endpoint; the tier header is not used here
        # because the middleware reads only X-User-Id for identification.
        return {"status": "ok"}

    return app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_free_tier_rate_limit_enforced(client):
    # Use a constant user id to hit the same rate‑limit bucket.
    headers = {"X-User-Id": "test_user", "X-User-Tier": "free"}

    # First (limit) requests should succeed.
    for i in range(FREE_TIER_DAILY_LIMIT):
        resp = client.get("/download/video", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    # The next request must be rejected with 429.
    resp = client.get("/download/video", headers=headers)
    assert resp.status_code == 429
    assert "Daily download limit exceeded" in resp.json()["detail"]


def test_non_download_endpoint_not_rate_limited(client):
    # Endpoint not under /download should bypass the middleware.
    headers = {"X-User-Id": "test_user", "X-User-Tier": "free"}
    for _ in range(FREE_TIER_DAILY_LIMIT + 10):
        resp = client.get("/", headers=headers)
        # 404 is expected because root is not defined, but not 429.
        assert resp.status_code != 429