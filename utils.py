import json

def load_config(config_file):
    with open(config_file, "r") as f:
        return json.load(f)

def check_node_health(node):
    # Simulate health check logic
    return True  # Replace with actual health check logic