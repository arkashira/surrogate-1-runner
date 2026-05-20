import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models import Project
from app.database import get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    # This is a simplified mock; in reality you'd want to use a test database
    db = next(get_db())
    yield db
    db.close()

def test_delete_project(db_session: Session):
    # Create a project first
    response = client.post("/projects", json={
        "name": "Test Project",
        "description": "A test project for deletion"
    })
    assert response.status_code == 200
    project_data = response.json()
    project_id = project_data["id"]
    
    # Verify project was created
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"
    
    # Delete the project
    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Project deleted successfully"}
    
    # Verify project was deleted
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 404

def test_delete_nonexistent_project():
    response = client.delete("/projects/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}