from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class OpenAIModelInfo:
    id: str
    name: str
    owned_by: str
    permission: List[Dict]
    root: str
    parent: Optional[str]
    created: int

    def is_compatible(self) -> bool:
        """Check if the model is compatible with the system.

        This method should be implemented with specific business logic.
        Example: Verify model ownership and permissions.
        """
        # Placeholder logic (replace with actual checks)
        return self.owned_by == "openai" and self.permission  # Simplified check