import time
import json
from utils import load_config

def deploy_workflow(workflow_id, target_node, config_file):
    config = load_config(config_file)
    latency_threshold = config["latency_threshold"]
    print(f"Deploying workflow {workflow_id} to node {target_node}.")
    start_time = time.time()
    # Add deployment logic here
    end_time = time.time()
    latency = end_time - start_time
    print(f"Deployment latency: {latency * 1000:.2f} ms")
    if latency > latency_threshold:
        print("Latency exceeds threshold. Investigate further.")
    return latency

def measure_latency(workflow_id, target_node, config_file):
    return deploy_workflow(workflow_id, target_node, config_file)

if __name__ == "__main__":
    workflow_id = "workflow123"
    target_node = "primary"
    config_file = "config.json"
    measured_latency = measure_latency(workflow_id, target_node, config_file)