import yaml
import hashlib
import os
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, ValidationError

class Route(BaseModel):
    agent: str
    next_agent: List[str]  # Using List instead of comma-separated string for better type safety

class RoutingTable(BaseModel):
    routes: Dict[str, Route]

class RoutingLoader:
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        self.routing_table: Optional[RoutingTable] = None
        self.last_modified: float = 0.0

    def load(self) -> RoutingTable:
        """Load and validate routing configuration from YAML file."""
        try:
            with open(self.yaml_path, 'r') as file:
                yaml_content = yaml.safe_load(file)

            # Validate structure
            if not isinstance(yaml_content, dict):
                raise ValueError("Routing config must be a dictionary")

            self.routing_table = RoutingTable(**yaml_content)
            self.last_modified = Path(self.yaml_path).stat().st_mtime
            return self.routing_table
        except ValidationError as e:
            raise ValueError(f"Invalid routing table: {e}")
        except Exception as e:
            raise ValueError(f"Failed to load routing config: {str(e)}")

    def reload_if_changed(self) -> bool:
        """Reload routing table if the YAML file has been modified."""
        try:
            current_modified = Path(self.yaml_path).stat().st_mtime
            if current_modified != self.last_modified:
                self.load()
                return True
            return False
        except FileNotFoundError:
            raise ValueError(f"Routing config file not found at {self.yaml_path}")

    def get_next_agent(self, agent: str, payload: str) -> str:
        """Deterministically route payload to next agent based on hash of payload."""
        if not self.routing_table:
            raise ValueError("Routing table not loaded")

        if agent not in self.routing_table.routes:
            raise ValueError(f"Agent {agent} not found in routing table")

        route = self.routing_table.routes[agent]
        if not route.next_agent:
            raise ValueError(f"No next agent defined for {agent}")

        # Create deterministic hash of payload
        payload_hash = hashlib.sha256(f"{agent}{payload}".encode()).hexdigest()
        hash_int = int(payload_hash[:8], 16)  # Use first 8 hex chars as integer

        # Select destination using modulo
        index = hash_int % len(route.next_agent)
        return route.next_agent[index]