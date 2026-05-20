import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..main import app
from ..api import transaction_router
from ..models import TransactionLog
from ..transaction_schema import TransactionLogBase

app.include_router(transaction_router)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    # Mock database session setup here
    pass

def test_capture_transaction_log(client, db_session):
    transaction_data = [
        {"db_type": "mysql", "transaction_id": "tx123", "commit_status": True, "isolation_level": "READ_COMMITTED", "log": "INSERT INTO users (name) VALUES ('John')"},
        {"db_type": "mariadb", "transaction_id": "tx123", "commit_status": True, "isolation_level": "READ_COMMITTED", "log": "INSERT INTO users (name) VALUES ('John')"}
    ]
    response = client.post("/transactions/capture/", json=transaction_data)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_compare_transaction_logs(client, db_session):
    # Setup some test data in the database
    mysql_log = TransactionLog(database_type="mysql", transaction_id="tx123", commit_status=True, isolation_level="READ_COMMITTED")
    mariadb_log = TransactionLog(database_type="mariadb", transaction_id="tx123", commit_status=True, isolation_level="READ_COMMITTED")
    db_session.add_all([mysql_log, mariadb_log])
    db_session.commit()

    response = client.get("/transactions/compare_transaction_logs/")
    assert response.status_code == 200
    comparison_results = response.json()["comparison_results"]
    assert len(comparison_results) > 0
    assert comparison_results[0]["transaction_id"] == "tx123"