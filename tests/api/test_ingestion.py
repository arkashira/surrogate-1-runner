import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.main import app  # Assuming app is initialized in src/main.py
from src.database import Base, get_db

# Setup In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_ingest_aws_success(client, db_session):
    csv_content = (
        "timestamp,resource_id,cost,currency,service\n"
        "2023-10-01T12:00:00Z,res-1,0.5,USD,ec2\n"
        "2023-10-01T12:00:00Z,res-1,0.5,USD,ec2\n"  # Duplicate
        "2023-10-01T13:00:00Z,res-2,1.2,USD,s3\n"
    )
    
    response = client.post(
        "/ingest/aws",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )
    
    assert response.status_code == 202
    
    # Since it's a background task, we might need a tiny sleep or 
    # check the DB after the task completes. In a test environment, 
    # we can manually trigger the logic or wait.
    import time
    time.sleep(0.1) 

    # Verify records
    result = db_session.execute(text("SELECT count(*) FROM cost_records")).scalar()
    # Should be 2 (the duplicate is ignored)
    assert result == 2

def test_ingest_aws_invalid_file(client):
    response = client.post(
        "/ingest/aws",
        files={"file": ("test.txt", "not a csv", "text/plain")}
    )
    assert response.status_code == 400