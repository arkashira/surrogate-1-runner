"""
Integration tests for the analytics API.
"""

from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from ..main import app  # Assuming the FastAPI app is defined in src/main.py
from ..dependencies import get_db, jwt_encode
from ..models import NavLog
from sqlalchemy.orm import Session

client = TestClient(app)


def _create_fake_logs(db: Session):
    """Populate the nav_logs table with fake data."""
    now = datetime.utcnow()
    logs = [
        NavLog(page_url="/home", timestamp=now - timedelta(hours=1)),
        NavLog(page_url="/home", timestamp=now - timedelta(hours=2)),
        NavLog(page_url="/about", timestamp=now - timedelta(days=1)),
    ]
    db.add_all(logs)
    db.commit()


def test_stats_endpoint(monkeypatch):
    # Mock JWT verification
    def fake_decode(token: str):
        return {"sub": "admin"}

    monkeypatch.setattr("..dependencies.jwt_decode", fake_decode)

    # Get a DB session
    with next(get_db()) as db:
        _create_fake_logs(db)

    # Create a fake JWT
    token = jwt_encode({"sub": "admin"})

    resp = client.get(
        "/analytics/stats",
        headers={"Authorization": f"Bearer {token}"},
        params={"start": (datetime.utcnow() - timedelta(days=2)).isoformat()},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "page_counts" in data
    assert "heatmap" in data
    assert any(entry["page_url"] == "/home" for entry in data["page_counts"])


def test_export_csv(monkeypatch):
    # Mock JWT verification
    def fake_decode(token: str):
        return {"sub": "admin"}

    monkeypatch.setattr("..dependencies.jwt_decode", fake_decode)

    with next(get_db()) as db:
        _create_fake_logs(db)

    token = jwt_encode({"sub": "admin"})

    resp = client.get(
        "/analytics/export",
        headers={"Authorization": f"Bearer {token}"},
        params={"start": (datetime.utcnow() - timedelta(days=2)).isoformat()},
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "text/csv"
    content = resp.text
    assert "page_url,views" in content
    assert "/home" in content