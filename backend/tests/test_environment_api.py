import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..dependencies import get_current_user

client = TestClient(app)

@pytest.fixture
def mock_current_user():
    def override_get_current_user():
        return "test_user"
    app.dependency_overrides[get_current_user] = override_get_current_user

def test_list_environments(mock_current_user):
    response = client.get("/environments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_environment(mock_current_user):
    environment_id = "test_env_id"
    response = client.get(f"/environments/{environment_id}")
    assert response.status_code == 200
    assert response.json()["id"] == environment_id