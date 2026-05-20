
import time
import random
from typing import List, Dict
from exceptions import TimeoutError

class StepExecutor:
    def __init__(self, max_retries: int = 3, backoff_multiplier: float = 2.0, error_types: List[Exception] = None):
        self.max_retries = max_retries
        self.backoff_multiplier = backoff_multiplier
        self.error_types = error_types or [Exception]

    def execute_step(self, step_func, timeout: float = 60.0):
        start_time = time.time()
        retries = 0

        while retries < self.max_retries:
            try:
                step_func()
                return
            except self.error_types[retries] as e:
                if retries == self.max_retries - 1:
                    raise e
                time.sleep(timeout * (2 ** retries) * self.backoff_multiplier)
                retries += 1

        raise TimeoutError(f"Step execution timed out after {timeout} seconds.")

# tests/test_step_executor.py

import unittest
from unittest.mock import patch
from src.surrogate_1.services.step_executor import StepExecutor

class TestStepExecutor(unittest.TestCase):
    def test_timeout(self):
        executor = StepExecutor(timeout=1.0)
        with patch.object(time, 'sleep') as mock_sleep:
            with self.assertRaises(TimeoutError):
                executor.execute_step(lambda: None)
                mock_sleep.assert_called_with(1.0)

    def test_retries(self):
        executor = StepExecutor(max_retries=3, backoff_multiplier=2.0)
        with patch.object(time, 'sleep') as mock_sleep:
            with patch.object(Exception, '__name__', 'TestException') as mock_exception:
                with self.assertRaises(TestException):
                    executor.execute_step(lambda: raise TestException())
                mock_sleep.assert_called_with(1.0)
                mock_sleep.assert_called_with(2.0)
                mock_sleep.assert_called_with(4.0)

# src/surrogate_1/services/__init__.py

from .step_executor import StepExecutor

__all__ = ['StepExecutor']