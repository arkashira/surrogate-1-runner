import time
from typing import Callable, Any

class RetryStrategy:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        retries = 0
        while retries <= self.max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if retries == self.max_retries:
                    raise e
                wait_time = self.backoff_factor * (2 ** retries)
                time.sleep(wait_time)
                retries += 1

def orchestrate_llm_calls(call_func: Callable, *args, **kwargs) -> Any:
    retry_strategy = RetryStrategy()
    return retry_strategy.execute_with_retry(call_func, *args, **kwargs)

# Example usage:
# result = orchestrate_llm_calls(make_llm_call, arg1, arg2, kwarg1=value1)