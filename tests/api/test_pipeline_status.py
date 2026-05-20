import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from ...api.pipeline_status import router
from ...models import Pipeline, PipelineStatus

@pytest.fixture
def client():
    from ...main import app
    app.include_router(router)
    return TestClient(app)

def test_get_pipeline_status(client, db_session):
    # Create test data
    pipeline1 = Pipeline(name="Pipeline 1")
    pipeline2 = Pipeline(name="Pipeline 2")
    db_session.add(pipeline1)
    db_session.add(pipeline2)
    db_session.commit()

    status1 = PipelineStatus(pipeline_id=pipeline1.id, status="Running", timestamp=datetime.now())
    status2 = PipelineStatus(pipeline_id=pipeline2.id, status="Failed", timestamp=datetime.now())
    db_session.add(status1)
    db_session.add(status2)
    db_session.commit()

    # Test the endpoint
    response = client.get("/pipelines/status")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Pipeline 1"
    assert data[0]["status"] == "Running"
    assert data[1]["name"] == "Pipeline 2"
    assert data[1]["status"] == "Failed"