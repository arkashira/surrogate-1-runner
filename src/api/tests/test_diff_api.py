import pytest
import json
from diff_api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_differences(client):
    """Test basic API endpoint"""
    response = client.get('/api/diffs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'differences' in data
    assert 'total' in data
    assert 'timestamp' in data

def test_filter_by_severity(client):
    """Test filtering by severity"""
    response = client.get('/api/diffs?severity=Critical')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(d['severity'] == 'Critical' for d in data['differences'])

def test_filter_by_database(client):
    """Test filtering by database"""
    response = client.get('/api/diffs?database=production')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(d['database'] == 'production' for d in data['differences'])

def test_filter_by_script(client):
    """Test filtering by script name"""
    response = client.get('/api/diffs?script_name=user_migration.sql')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(d['script_name'] == 'user_migration.sql' for d in data['differences'])

def test_csv_export(client):
    """Test CSV export functionality"""
    response = client.get('/api/diffs?format=csv')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert 'differences.csv' in response.headers['Content-Disposition']

def test_refresh_endpoint(client):
    """Test data refresh endpoint"""
    response = client.post('/api/diffs/refresh')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'refreshed'
    assert 'count' in data