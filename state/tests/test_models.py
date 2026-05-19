import pytest
from .models import ResourceMetadata

def test_resource_metadata():
    metadata = ResourceMetadata(id="123", name="Test Resource", workspace_id="workspace-1")
    assert metadata.id == "123"
    assert metadata.name == "Test Resource"
    assert metadata.workspace_id == "workspace-1"