import time
from typing import Dict, Any
from agent_updates import AgentUpdates

class StatusTracker:
    def __init__(self):
        self.agent_updates = AgentUpdates()
        self.agent_updates.start()

    def add_agent(self, agent_id: str, initial_data: Dict[str, Any]):
        self.agent_updates.add_agent(agent_id, initial_data)

    def update_agent_status(self, agent_id: str, status_data: Dict[str, Any]):
        self.agent_updates.update_agent(agent_id, status_data)

    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        return self.agent_updates.agents.get(agent_id, {})

    def close(self):
        self.agent_updates.stop()

# Example usage
if __name__ == "__main__":
    tracker = StatusTracker()
    tracker.add_agent("agent1", {"status": "active", "performance": 0.95})
    tracker.add_agent("agent2", {"status": "active", "performance": 0.92})

    # Simulate real-time updates
    for i in range(10):
        time.sleep(1)
        tracker.update_agent_status("agent1", {"performance": 0.95 + i * 0.01})
        tracker.update_agent_status("agent2", {"performance": 0.92 + i * 0.01})

    tracker.close()