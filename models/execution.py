from enum import Enum
from typing import Dict

class ExecutionState(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    TIMEOUT = 'timeout'
    CLARIFICATION_REQUEST = 'clarification_request'

class Execution:
    def __init__(self, id: str, state: ExecutionState = ExecutionState.PENDING):
        self.id = id
        self.state = state
        self.context_snapshot = {}

    def log_full_context(self):
        # Log the full context snapshot for debugging purposes
        print(f"Execution {self.id} failed. Context snapshot: {self.context_snapshot}")

    def set_context(self, context: Dict):
        self.context_snapshot = context