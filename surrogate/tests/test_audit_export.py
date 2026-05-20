import pytest
from fastapi.testclient import TestClient

from ..main import app
from ..db import engine, get_db
from ..models import AuditLog, Base
from datetime import datetime

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Create tables, insert sample data, then drop tables."""
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    db.add_all(
        [
            AuditLog(
                article_id=1,
                timestamp=datetime(2023, 1, 1, 12, 0),
                author="alice",
                action="create",
            ),
            AuditLog(
                article_id=1,
                timestamp=datetime(2023, 1, 2, 13, 0),
                author="bob",
                action="update",
            ),
        ]
    )
    db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


def test_export_audit_logs():
    response = client.get("/audit/export")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv"
    content = response.content.decode()
    lines = content.strip().splitlines()
    assert lines[0] == "id,article_id,timestamp,author,action"
    assert len(lines) == 3  # header + 2 rows