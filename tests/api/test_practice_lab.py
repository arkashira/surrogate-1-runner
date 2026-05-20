import pytest
from src.api.practice_lab import practice_lab_bp
from src.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.register_blueprint(practice_lab_bp)
    with app.test_client() as client:
        yield client

def test_get_practice_labs(client):
    response = client.get('/practice_labs')
    assert response.status_code == 200
    assert len(response.json) >= 3

def test_get_practice_lab_by_id(client):
    response = client.get('/practice_labs/1')
    assert response.status_code == 200
    assert response.json['id'] == 1

def test_get_practice_lab_not_found(client):
    response = client.get('/practice_labs/999')
    assert response.status_code == 404