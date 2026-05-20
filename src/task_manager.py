from task_logger import TaskLogger

class TaskManager:
    def __init__(self):
        self.task_logger = TaskLogger()

    def execute_task(self, task_name, task_function):
        try:
            self.task_logger.log_task_start(task_name)
            task_function()
            self.task_logger.log_task_end(task_name)
            self.task_logger.log_task_status(task_name, 'completed')
        except Exception as e:
            self.task_logger.log_task_error(task_name, str(e))
            self.task_logger.log_task_status(task_name, 'failed')