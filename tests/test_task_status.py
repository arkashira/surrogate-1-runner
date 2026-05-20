import pytest
import asyncio
import websockets
import json
from datetime import datetime, timedelta
from task_status import TaskStatusManager, app

@pytest.mark.asyncio
async def test_realtime_updates():
    manager = TaskStatusManager()

    # Test initial state
    async with websockets.connect("ws://localhost:8765") as websocket:
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "INITIAL_STATE"
        assert len(data["tasks"]) == 0

        # Update task and verify broadcast
        task_id = "T-001"
        await manager.update_task(
            task_id,
            "IN_PROGRESS",
            deadline=(datetime.utcnow() + timedelta(days=7)).isoformat(),
            milestone="RESEARCH_PHASE"
        )

        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "TASK_UPDATE"
        assert task_id in data["tasks"]
        assert data["tasks"][task_id]["status"] == "IN_PROGRESS"
        assert "milestone" in data["tasks"][task_id]
        assert len(data["milestones"][task_id]) == 1

def test_rest_api():
    client = app.test_client()
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert "milestones" in data