import pytest
from src.services.job_queue import JobQueue

@pytest.fixture
def job_queue():
    return JobQueue()

def test_enqueue_hardening_job(job_queue, mocker):
    mocker.patch.object(job_queue.db, 'cursor')
    mocker.patch.object(job_queue.db, 'commit')
    job_id = job_queue.enqueue_hardening_job(['vm1', 'vm2'], '1.0')
    assert isinstance(job_id, str)

def test_get_job_status(job_queue, mocker):
    mocker.patch.object(job_queue.db, 'cursor')
    mocker.patch.object(job_queue.db.cursor.return_value, 'execute')
    mocker.patch.object(job_queue.db.cursor.return_value, 'fetchone', return_value=('queued', None))
    status = job_queue.get_job_status('12345')
    assert status == {'job_id': '12345', 'status': 'queued', 'error_details': None}