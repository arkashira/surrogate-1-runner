import pytest
from httpx import AsyncClient
from src.api import app

@pytest.mark.asyncio
async def test_download_valid_url():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/download", headers={"api-key": "valid-key"}, json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        assert response.status_code == 200
        assert response.json()["status"] == "ready"
        assert response.json()["download_url"] == "https://example.com/download"

@pytest.mark.asyncio
async def test_download_invalid_url():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/download", headers={"api-key": "valid-key"}, json={"url": "invalid-url"})
        assert response.status_code == 500
        assert response.json()["error"] == "Internal Server Error"

@pytest.mark.asyncio
async def test_download_missing_api_key():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/download", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        assert response.status_code == 401
        assert response.json()["error"] == "Unauthorized"