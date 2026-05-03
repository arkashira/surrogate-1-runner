import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.audit import Base, AuditLog
from src.services.audit_service import log_status_change, validate_status, ALLOWED_STATUSES

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DB_URL)
TestingSession = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_validate_status_valid():
    for s in ALLOWED_STATUSES:
        validate_status(s)  # should not raise


def test_validate_status_invalid():
    with pytest.raises(ValueError, match="Invalid status"):
        validate_status("invalid_status")


def test_log_status_change_creates_audit():
    db = TestingSession()
    request_id = "req-123"

    entry = log_status_change(db, request_id, old_status="pending", new_status="processing")
    assert entry.request_id == request_id
    assert entry.field == "status"
    assert entry.old_value == "pending"
    assert entry.new_value == "processing"
    assert entry.created_at is not None

    fetched = db.query(AuditLog).filter_by(request_id=request_id).first()
    assert fetched is not None
    assert fetched.id == entry.id


def test_log_status_change_no_old_status():
    db = TestingSession()
    entry = log_status_change(db, "req-456", old_status=None, new_status="pending")
    assert entry.old_value is None
    assert entry.new_value == "pending"


def test_log_status_change_invalid_new_status_raises():
    db = TestingSession()
    with pytest.raises(ValueError):
        log_status_change(db, "req-789", old_status="pending", new_status="nope")