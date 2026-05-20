import time
from typing import Any, Dict

class LLM_Agent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.latency_threshold = 200  # in milliseconds

    def execute(self, task: str) -> str:
        start_time = time.time()
        result = self._process_task(task)
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds

        if latency > self.latency_threshold:
            print(f"Warning: Task '{task}' exceeded latency threshold ({latency} ms)")
        
        return result

    def _process_task(self, task: str) -> str:
        # Placeholder for actual task processing logic
        return f"Processed task: {task}"