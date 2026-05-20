import requests
from typing import Optional
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError

class DatabricksAPI:
    def __init__(self, provider_workspace_id: str):
        self.provider_workspace_id = provider_workspace_id
        self._client = WorkspaceClient(workspace_id=provider_workspace_id)
    
    def validate_workspace_id(self, workspace_id: str) -> bool:
        """Validate workspace_id against Databricks API permissions"""
        try:
            # Use the Databricks SDK to check workspace existence and permissions
            # This endpoint will fail with 403 if permissions are insufficient
            self._client.workspace.get(workspace_id)
            return True
        except DatabricksError as e:
            if e.http_status == 404:
                raise ValueError(f"Workspace ID {workspace_id} does not exist")
            elif e.http_status == 403:
                raise PermissionError(
                    f"Insufficient permissions for workspace ID {workspace_id}"
                )
            else:
                raise
    
    def import_resource(self, resource_id: str, workspace_id: Optional[str] = None):
        """Import Databricks resource with optional workspace override"""
        # Validate if workspace_id is provided
        if workspace_id:
            self.validate_workspace_id(workspace_id)
            # Create temporary client with override
            override_client = WorkspaceClient(workspace_id=workspace_id)
        else:
            override_client = self._client
        
        # Execute import with validated workspace context
        try:
            # Example import operation using the override client
            response = override_client.jobs.import_job(resource_id)
            return response
        except DatabricksError as e:
            # Re-raise with workspace context
            raise DatabricksError(
                message=f"Import failed in workspace {workspace_id or self.provider_workspace_id}: {e.message}",
                http_status=e.http_status
            )