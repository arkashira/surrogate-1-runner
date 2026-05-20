from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_read_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello World"}


def test_run_workflow():
    resp = client.get("/workflow/test_workflow")
    assert resp.status_code == 200
    assert resp.json() == {"workflow_name": "test_workflow", "status": "success"}

    # Verify that a metric line for this request exists
    metrics = client.get("/metrics").text
    assert (
        'surrogate_workflow_latency_seconds_count{workflow_name="test_workflow",status="success"} 1'
        in metrics
    )


def test_metrics_endpoint():
    resp = client.get("/metrics")
    assert resp.status_code == 200
    # Content‑type must be the one Prometheus expects
    assert resp.headers["content-type"].startswith("text/plain")