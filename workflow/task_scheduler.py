import schedule
import time
import yaml
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('/opt/axentx/surrogate-1/workflow/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def schedule_task(task_name, task_func, interval):
    """
    Schedule a task to run at a specified interval.

    Args:
        task_name (str): The name of the task.
        task_func (function): The function to run for the task.
        interval (int): The interval at which to run the task.
    """
    schedule.every(interval).minutes.do(task_func)

def run_scheduled_tasks():
    """
    Run all scheduled tasks.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)

def monitor_task_execution(task_name):
    """
    Monitor the execution of a task.

    Args:
        task_name (str): The name of the task.
    """
    logger.info(f"Monitoring task execution: {task_name}")

def control_task_execution(task_name):
    """
    Control the execution of a task.

    Args:
        task_name (str): The name of the task.
    """
    logger.info(f"Controlling task execution: {task_name}")

def maintain_task_logs(task_name):
    """
    Maintain logs for a task.

    Args:
        task_name (str): The name of the task.
    """
    logger.info(f"Maintaining task logs: {task_name}")

# Schedule tasks
schedule_task('task1', monitor_task_execution, 1)
schedule_task('task2', control_task_execution, 2)
schedule_task('task3', maintain_task_logs, 3)

# Run scheduled tasks
run_scheduled_tasks()