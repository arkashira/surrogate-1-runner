from .workflow_management import WorkflowManagement

class TerminalEnvironment:
    def __init__(self):
        self.workflow_manager = WorkflowManagement()

    def create_and_manage_workflow(self, name, steps, action):
        workflow = self.workflow_manager.create_workflow(name, steps)
        managed_workflow = self.workflow_manager.manage_workflow(id(workflow), action)
        return managed_workflow

    def execute_workflow_with_feedback(self, workflow_id):
        executed_workflow = self.workflow_manager.execute_workflow(workflow_id)
        feedback = self.workflow_manager.get_real_time_feedback(workflow_id)
        return executed_workflow, feedback

# Example usage
if __name__ == "__main__":
    env = TerminalEnvironment()
    workflow = env.create_and_manage_workflow("Test Workflow", ["Step 1", "Step 2"], "start")
    executed_workflow, feedback = env.execute_workflow_with_feedback(id(workflow))
    print(feedback)