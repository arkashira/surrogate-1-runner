import pytest
from datetime import datetime, timedelta
from src.models.lock import Lock

def test_lock_creation():
    lock = Lock(
        id="123e4567-e89b-12d3-a456-426614174000",
        doc_id="doc123",
        section_id="section123",
        owner="user123"
    )
    assert lock.id == "123e4567-e89b-12d3-a456-426614174000"
    assert lock.doc_id == "doc123"
    assert lock.section_id == "section123"
    assert lock.owner == "user123"
    assert isinstance(lock.created_at, datetime)
    assert lock.expires_at == lock.created_at + timedelta(hours=2)
    assert lock.ttl == 7200

def test_lock_default_expiration():
    now = datetime.utcnow()
    lock = Lock(
        id="123e4567-e89b-12d3-a456-426614174000",
        doc_id="doc123",
        section_id="section123",
        owner="user123",
        created_at=now
    )
    assert lock.expires_at == now + timedelta(hours=2)