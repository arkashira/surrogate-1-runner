import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...main import app
from ...database import Base, get_db
from ...models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
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
    user = User(id=1, name="Test User", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def test_update_profile(test_user):
    response = client.put(
        "/profile",
        json={"name": "Updated User", "email": "updated@example.com"},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated User"
    assert response.json()["email"] == "updated@example.com"