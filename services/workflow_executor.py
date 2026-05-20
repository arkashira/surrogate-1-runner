import time
from enum import Enum
from typing import List, Type, Optional
from models.execution import ExecutionState, Execution, TimeoutError

class StepStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    TIMEOUT = 'timeout'
    CLARIFICATION_REQUEST = 'clarification_request'

class WorkflowExecutor:
    def __init__(self, execution: Execution, max_retries: int = 3, backoff_multiplier: int = 2, retry_on: List[Type[Exception]] = []):
        self.execution = execution
        self.max_retries = max_retries
        self.backoff_multiplier = backoff_multiplier
        self.retry_on = retry_on

    def execute_step(self, step_func, timeout: int = 60):
        retries = 0
        while retries <= self.max_retries:
            try:
                self.execution.state = StepStatus.RUNNING
                result = self._run_with_timeout(step_func, timeout)
                self.execution.state = StepStatus.COMPLETED
                return result
            except TimeoutError:
                self.execution.state = StepStatus.TIMEOUT
                raise
            except Exception as e:
                if not any(isinstance(e, err_type) for err_type in self.retry_on) or retries == self.max_retries:
                    self.execution.state = StepStatus.FAILED
                    self.execution.log_full_context()
                    raise
                retries += 1
                time.sleep(self.backoff_multiplier ** retries)

    def _run_with_timeout(self, func, timeout):
        start_time = time.time()
        result = func()
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(f"Step exceeded {timeout}s timeout")
        return result

class TimeoutError(Exception):
    pass