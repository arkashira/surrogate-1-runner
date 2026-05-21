import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from src.utils.scheduler import TaskScheduler
import time

def test_task_registration():
    scheduler = TaskScheduler()
    mock_func = MagicMock()
    
    # Test interval task
    scheduler.register_task('test1', mock_func, 'interval', interval=5)
    assert 'test1' in scheduler.tasks
    assert scheduler.tasks['test1']['type'] == 'interval'
    
    # Test event task
    scheduler.register_task('test2', mock_func, 'event', event_trigger='test_event')
    assert 'test2' in scheduler.tasks
    assert scheduler.tasks['test2']['type'] == 'event'
    
    scheduler.shutdown()

def test_interval_task_execution():
    scheduler = TaskScheduler()
    mock_func = MagicMock()
    
    scheduler.register_task('test', mock_func, 'interval', interval=1)
    time.sleep(1.1)  # Wait for task to trigger
    
    mock_func.assert_called_once()
    scheduler.shutdown()

def test_event_trigger():
    scheduler = TaskScheduler()
    mock_func = MagicMock()
    
    scheduler.register_task('test', mock_func, 'event', event_trigger='test_event')
    scheduler.trigger_event('test_event')
    
    mock_func.assert_called_once()
    scheduler.shutdown()

def test_error_handling(caplog):
    scheduler = TaskScheduler()
    
    def failing_task():
        raise ValueError("Test error")
    
    scheduler.register_task('test', failing_task, 'interval', interval=1)
    time.sleep(1.1)
    
    assert "Task test failed" in caplog.text
    scheduler.shutdown()