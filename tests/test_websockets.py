import pytest
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import re_path
from .websockets import AgentStatusConsumer, WorkflowMetricsConsumer

application = URLRouter([
    re_path(r"ws/agent-status/$", AgentStatusConsumer.as_asgi()),
    re_path(r"ws/workflow-metrics/$", WorkflowMetricsConsumer.as_asgi()),
])

@pytest.mark.asyncio
async def test_agent_status_consumer():
    communicator = WebsocketCommunicator(application, "/ws/agent-status/")
    connected, _ = await communicator.connect()
    assert connected

    response = await communicator.receive_from()
    agent_health_data = json.loads(response)
    assert 'agents' in agent_health_data

    await communicator.disconnect()

@pytest.mark.asyncio
async def test_workflow_metrics_consumer():
    communicator = WebsocketCommunicator(application, "/ws/workflow-metrics/")
    connected, _ = await communicator.connect()
    assert connected

    response = await communicator.receive_from()
    workflow_metrics_data = json.loads(response)
    assert 'workflows' in workflow_metrics_data

    await communicator.disconnect()