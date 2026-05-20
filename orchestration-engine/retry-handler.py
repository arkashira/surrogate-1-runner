import time
import requests
from typing import Callable, Any

class RetryHandler:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 0.5):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def should_retry(self, response: requests.Response) -> bool:
        return response.status_code >= 500 or response.status_code == 408

    def handle_retry(self, func: Callable, *args, **kwargs) -> Any:
        retries = 0
        while retries <= self.max_retries:
            try:
                response = func(*args, **kwargs)
                if not self.should_retry(response):
                    return response
                else:
                    retries += 1
                    sleep_time = self.backoff_factor * (2 ** (retries - 1))
                    time.sleep(sleep_time)
            except requests.exceptions.Timeout:
                retries += 1
                sleep_time = self.backoff_factor * (2 ** (retries - 1))
                time.sleep(sleep_time)
        raise Exception("Max retries exceeded")

# Example usage:
# retry_handler = RetryHandler()
# response = retry_handler.handle_retry(requests.get, 'http://example.com')