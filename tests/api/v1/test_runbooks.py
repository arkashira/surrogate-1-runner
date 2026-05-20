import pytest
from flask import url_for
from models import Runbook
from extensions import db


@pytest.fixture
def app_context(app):
    """Create application context for tests."""
    with app.app_context():
        yield


@pytest.fixture
def client(app):
    """Create test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_runbook(app_context):
    """Create a sample runbook for testing."""
    runbook = Runbook(title='Test Runbook', content='Test Content')
    db.session.add(runbook)
    db.session.commit()
    yield runbook
    # Cleanup
    db.session.rollback()


class TestDeleteRunbook:
    """Tests for the DELETE /runbooks/<id> endpoint."""
    
    def test_delete_runbook_success(self, client, sample_runbook):
        """Test successful deletion of an existing runbook."""
        runbook_id = sample_runbook.id
        
        response = client.delete(f'/api/v1/runbooks/{runbook_id}')
        
        assert response.status_code == 204
        assert response.data == b''  # Empty body for 204
        
        # Verify deletion in database
        deleted_runbook = Runbook.query.get(runbook_id)
        assert deleted_runbook is None
    
    def test_delete_nonexistent_runbook(self, client):
        """Test deletion of a non-existent runbook returns 404."""
        response = client.delete('/api/v1/runbooks/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'message' in data
        assert 'not found' in data['message'].lower()
    
    def test_delete_runbook_idempotent(self, client, sample_runbook):
        """Test that deleting twice returns 404 on second attempt."""
        runbook_id = sample_runbook.id
        
        # First delete - should succeed
        response1 = client.delete(f'/api/v1/runbooks/{runbook_id}')
        assert response1.status_code == 204
        
        # Second delete - should fail (already deleted)
        response2 = client.delete(f'/api/v1/runbooks/{runbook_id}')
        assert response2.status_code == 404


class TestGetRunbook:
    """Tests for GET endpoint (bonus from Candidate 2)."""
    
    def test_get_runbook_success(self, client, sample_runbook):
        """Test retrieving an existing runbook."""
        response = client.get(f'/api/v1/runbooks/{sample_runbook.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Test Runbook'
        assert data['content'] == 'Test Content'
    
    def test_get_nonexistent_runbook(self, client):
        """Test retrieving a non-existent runbook."""
        response = client.get('/api/v1/runbooks/99999')
        
        assert response.status_code == 404


class TestListRunbooks:
    """Tests for listing runbooks."""
    
    def test_list_runbooks_empty(self, client):
        """Test listing when no runbooks exist."""
        response = client.get('/api/v1/runbooks/')
        
        assert response.status_code == 200
        assert response.get_json() == []
    
    def test_list_runbooks_with_data(self, client, sample_runbook):
        """Test listing runbooks."""
        response = client.get('/api/v1/runbooks/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Test Runbook'