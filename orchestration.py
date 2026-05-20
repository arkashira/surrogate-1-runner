from deployment import DeploymentManager

class OrchestrationController:
    def __init__(self):
        self.deployment_manager = DeploymentManager()

    def orchestrate_deployments(self, workflow_ids):
        results = []
        for workflow_id in workflow_ids:
            result = self.deployment_manager.deploy_workflow(workflow_id)
            results.append(result)
        return results

# Example usage
if __name__ == "__main__":
    controller = OrchestrationController()
    workflow_ids = ["AIWorkflow1", "AIWorkflow2", "AIWorkflow3"]
    results = controller.orchestrate_deployments(workflow_ids)
    for result in results:
        print(result)