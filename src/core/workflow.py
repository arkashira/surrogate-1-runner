from typing import List

class Interaction:
    def __init__(self, type: str, target_agent_id: int):
        self.type = type
        self.target_agent_id = target_agent_id

class Agent:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.interactions: List[Interaction] = []

class WorkflowInstance:
    def __init__(self):
        self.agents: List[Agent] = []