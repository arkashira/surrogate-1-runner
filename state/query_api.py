from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ResourceMetadata:
    workspace_id: Optional[str] = None
    # other metadata fields...
    created_at: datetime = None

@dataclass
class Resource:
    id: str
    metadata: ResourceMetadata
    # other fields...

class StateQueryAPI:
    def __init__(self):
        self.resources = []  # In-memory storage for demo purposes
    
    def get_resources_by_workspace(self, workspace_id: str) -> List[Resource]:
        """
        Filter resources by workspace_id in state queries.
        
        Args:
            workspace_id: The workspace identifier to filter by
            
        Returns:
            List of resources belonging to the specified workspace
        """
        return [r for r in self.resources if r.metadata.workspace_id == workspace_id]
    
    def get_all_resources(self) -> List[Resource]:
        """Get all resources without filtering."""
        return self.resources
    
    def create_resource(self, resource: Resource) -> None:
        """Create a new resource with workspace context."""
        # This ensures workspace_id is stored in resource metadata
        self.resources.append(resource)
        
    def get_resource_by_id(self, resource_id: str) -> Optional[Resource]:
        """Get a specific resource by ID."""
        for r in self.resources:
            if r.id == resource_id:
                return r
        return None

# Example usage for audit logging
def log_import_audit(workspace_id: str, resource_id: str, action: str):
    """
    Display workspace context in import audit logs.
    
    Args:
        workspace_id: The workspace identifier
        resource_id: The resource being acted upon
        action: The action performed (e.g., 'import', 'update')
    """
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Workspace '{workspace_id}' - Resource '{resource_id}' - Action: {action}")