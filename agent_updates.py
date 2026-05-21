import time
import threading
from queue import Queue
from typing import Dict, Any

class AgentUpdates:
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.update_queue = Queue()
        self.running = True

    def add_agent(self, agent_id: str, initial_data: Dict[str, Any]):
        self.agents[agent_id] = initial_data
        self.update_queue.put((agent_id, initial_data))

    def update_agent(self, agent_id: str, update_data: Dict[str, Any]):
        if agent_id in self.agents:
            self.agents[agent_id].update(update_data)
            self.update_queue.put((agent_id, self.agents[agent_id]))

    def process_updates(self):
        while self.running:
            try:
                agent_id, update_data = self.update_queue.get(timeout=1)
                # Process the update (e.g., send to a monitoring system)
                print(f"Processing update for agent {agent_id}: {update_data}")
            except:
                pass

    def start(self):
        self.thread = threading.Thread(target=self.process_updates)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()