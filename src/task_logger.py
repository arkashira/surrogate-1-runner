import logging
from datetime import datetime

class TaskLogger:
    def __init__(self, log_file='task_logs.log'):
        self.log_file = log_file
        self.logger = logging.getLogger('task_logger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_task_start(self, task_name):
        self.logger.info(f'Task {task_name} started at {datetime.now()}')

    def log_task_end(self, task_name):
        self.logger.info(f'Task {task_name} ended at {datetime.now()}')

    def log_task_error(self, task_name, error):
        self.logger.error(f'Task {task_name} encountered an error: {error} at {datetime.now()}')

    def log_task_status(self, task_name, status):
        self.logger.info(f'Task {task_name} status: {status} at {datetime.now()}')