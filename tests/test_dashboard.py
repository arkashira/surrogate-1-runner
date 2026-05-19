import pytest
from src.dashboard import dashboard_bp
from src.dashboard_config import get_connected_repositories

def test_dashboard_route():
    test_client = dashboard_bp.test_client()
    response = test_client.get('/dashboard')
    assert response.status_code == 200
    assert b'Connected Repositories' in response.data

def test_repository_data():
    repos = get_connected_repositories()
    assert len(repos) >= 2
    assert all('name' in repo and 'url' in repo for repo in repos)