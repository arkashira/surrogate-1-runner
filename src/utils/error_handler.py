import logging
from typing import Dict

class WorkflowError(Exception):
    """Base class for workflow-related exceptions."""
    pass

class WorkflowErrorHandler:
    """Handles errors and logging for workflows."""
    
    def __init__(self, logger: logging.Logger = None):
        """Initializes the error handler with a logger."""
        self.logger = logger or logging.getLogger(__name__)

    def handle_error(self, error: Exception, workflow_id: str, workflow_step: str) -> Dict:
        """Handles an error by logging it and returning an error dictionary."""
        error_message = f"Error in workflow {workflow_id} at step {workflow_step}: {str(error)}"
        self.logger.error(error_message)
        return {"error": error_message, "workflow_id": workflow_id, "step": workflow_step}

    def log_workflow_completion(self, workflow_id: str, status: str) -> None:
        """Logs the completion status of a workflow."""
        self.logger.info(f"Workflow {workflow_id} completed with status: {status}")

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    error_handler = WorkflowErrorHandler()
    try:
        # Simulate a workflow error
        raise WorkflowError("Simulated workflow error")
    except Exception as e:
        error_handler.handle_error(e, "example_workflow", "step_1")