import pytest
from unittest.mock import patch
from src.integrations.observability_tools import ObservabilityToolIntegration

@pytest.fixture
def observability_tool():
    return ObservabilityToolIntegration("http://test-tool-url")

@patch('requests.post')
def test_send_alert(mock_post, observability_tool):
    mock_post.return_value.json.return_value = {"status": "success"}
    response = observability_tool.send_alert({"alert": "test_alert"})
    assert response == {"status": "success"}

@patch('requests.get')
def test_get_metrics(mock_get, observability_tool):
    mock_get.return_value.json.return_value = {"metrics": "test_metrics"}
    response = observability_tool.get_metrics("test_query")
    assert response == {"metrics": "test_metrics"}