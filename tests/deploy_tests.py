import pytest
from unittest import mock
from deploy import trigger_workflow, verify_deployment

@mock.patch("deploy.Github")
def test_trigger_workflow(mock_github):
    mock_workflow = mock.Mock()
    mock_workflow.create_dispatch.return_value = True
    mock_github.return_value.get_repo.return_value.get_workflow.return_value = mock_workflow
    assert "triggered" in trigger_workflow()

@mock.patch("requests.get")
def test_verify_deployment(mock_get):
    mock_get.return_value.status_code = 200
    assert "verified" in verify_deployment()
    
    mock_get.return_value.status_code = 500
    assert "failed" in verify_deployment()