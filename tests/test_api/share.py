import pytest
from fastapi.testclient import TestClient
from src.api import share

client = TestClient(share.app)

def test_create_lab_configuration():
    response = client.post('/lab-configurations', json={'name': 'Test Lab Configuration', 'configuration': 'Test configuration'})
    assert response.status_code == 200
    assert response.json()['id'] == 1

def test_get_lab_configurations():
    response = client.get('/lab-configurations')
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'Test Lab Configuration'}]

def test_get_lab_configuration():
    response = client.get('/lab-configurations/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Test Lab Configuration', 'configuration': 'Test configuration'}

def test_update_lab_configuration():
    response = client.put('/lab-configurations/1', json={'name': 'Updated Lab Configuration', 'configuration': 'Updated configuration'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Updated Lab Configuration', 'configuration': 'Updated configuration'}

def test_delete_lab_configuration():
    response = client.delete('/lab-configurations/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1}