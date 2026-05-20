import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base, get_db
from .main import app
from .models import User
from .utils import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = User(email="test@example.com", password_hash=get_password_hash("testpassword"))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def test_request_password_reset(test_user):
    response = client.post("/password-reset/", json={"email": test_user.email})
    assert response.status_code == 200
    assert "reset_token" in response.json()

def test_confirm_password_reset(test_user):
    response = client.post("/password-reset/", json={"email": test_user.email})
    reset_token = response.json()["reset_token"]
    new_password = "newpassword"
    response = client.post("/password-reset/confirm/", json={"token": reset_token, "new_password": new_password})
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

def test_confirm_password_reset_invalid_token():
    invalid_token = "invalid.token.here"
    new_password = "newpassword"
    response = client.post("/password-reset/confirm/", json={"token": invalid_token, "new_password": new_password})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired token"