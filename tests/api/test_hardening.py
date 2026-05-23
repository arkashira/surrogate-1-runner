import pytest
from flask import json
from src.api.hardening import hardening_bp
from src.services.job_queue import JobQueue

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(hardening_bp)
    client = app.test_client()
    yield client

def test_trigger_hardening_valid_payload(client, mocker):
    mocker.patch.object(JobQueue, 'enqueue_hardening_job', return_value='12345')
    response = client.post('/hardening/windows', json={'vm_ids': ['vm1', 'vm2']})
    assert response.status_code == 202
    assert json.loads(response.data) == {'job_id': '12345'}

def test_trigger_hardening_invalid_payload(client):
    response = client.post('/hardening/windows', json={'invalid_key': 'value'})
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Invalid payload'}

def test_get_hardening_status(client, mocker):
    mocker.patch.object(JobQueue, 'get_job_status', return_value={'job_id': '12345', 'status': 'queued'})
    response = client.get('/hardening/status/12345')
    assert response.status_code == 200
    assert json.loads(response.data) == {'job_id': '12345', 'status': 'queued'}