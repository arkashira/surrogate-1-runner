import time
import logging
from datetime import datetime
from typing import Callable, Dict, Any
from threading
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self, max_workers: int = 4):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler)
        self._scheduler_thread.start()

    def register_task(
        self,
        task_id: str,
        task_func: Callable,
        schedule_type: str,
        interval: int = None,
        cron_expr: str = None,
        event_trigger: str = None
    ) -> None:
        """Register a new task with the scheduler.
        
        Args:
            task_id: Unique identifier for the task
            task_func: Callable to execute
            schedule_type: 'interval' or 'cron' or 'event'
            interval: Seconds between executions (for interval type)
            cron_expr: Cron expression (for cron type)
            event_trigger: Event name to trigger on (for event type)
        """
        if schedule_type not in ['interval', 'cron', 'event']:
            raise ValueError("Invalid schedule_type. Must be 'interval', 'cron', or 'event'")
            
        self.tasks[task_id] = {
            'func': task_func,
            'type': schedule_type,
            'interval': interval,
            'cron': cron_expr,
            'event': event_trigger,
            'last_run': None,
            'next_run': self._calculate_next_run(schedule_type, interval, cron_expr)
        }

    def trigger_event(self, event_name: str) -> None:
        """Trigger all tasks registered for this event."""
        for task_id, task in self.tasks.items():
            if task['type'] == 'event' and task['event'] == event_name:
                self._execute_task(task_id)

    def _calculate_next_run(self, schedule_type: str, interval: int = None, cron_expr: str = None) -> datetime:
        """Calculate the next run time for a task."""
        now = datetime.now()
        if schedule_type == 'interval':
            return now + timedelta(seconds=interval)
        elif schedule_type == 'cron':
            # Simplified cron implementation - would use croniter in production
            return now + timedelta(minutes=1)
        return None

    def _execute_task(self, task_id: str) -> None:
        """Execute a task and handle errors."""
        task = self.tasks[task_id]
        try:
            logger.info(f"Executing task {task_id}")
            self.executor.submit(task['func'])
            task['last_run'] = datetime.now()
            task['next_run'] = self._calculate_next_run(
                task['type'], task['interval'], task['cron']
            )
        except Exception as e:
            logger.error(f"Task {task_id} failed: {str(e)}", exc_info=True)

    def _run_scheduler(self) -> None:
        """Main scheduler loop checking for tasks to run."""
        while self._running:
            now = datetime.now()
            for task_id, task in self.tasks.items():
                if task['next_run'] and now >= task['next_run']:
                    self._execute_task(task_id)
            time.sleep(1)

    def shutdown(self) -> None:
        """Clean shutdown of the scheduler."""
        self._running = False
        self._scheduler_thread.join()
        self.executor.shutdown()