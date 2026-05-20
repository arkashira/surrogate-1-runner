import time
from concurrent.futures import ThreadPoolExecutor

class DeploymentManager:
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def deploy_workflow(self, workflow_id):
        start_time = time.time()
        future = self.executor.submit(self._deploy_workflow_internal, workflow_id)
        result = future.result()
        end_time = time.time()
        latency = end_time - start_time
        if latency > 0.2:
            print(f"Warning: Deployment latency exceeded 200ms: {latency}s")
        return result

    def _deploy_workflow_internal(self, workflow_id):
        # Simulate deployment process
        print(f"Deploying workflow {workflow_id}")
        time.sleep(0.1)  # Simulate some work
        return f"Workflow {workflow_id} deployed successfully"

# Example usage
if __name__ == "__main__":
    manager = DeploymentManager()
    result = manager.deploy_workflow("AIWorkflow123")
    print(result)