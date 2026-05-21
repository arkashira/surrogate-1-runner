import os
import yaml
from typing import List

class LoadBalancer:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.worker_nodes = self.load_config()

    def load_config(self) -> List[str]:
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)
            return config['worker_nodes']

    def get_worker_nodes(self) -> List[str]:
        return self.worker_nodes

    def add_worker_node(self, node: str):
        self.worker_nodes.append(node)
        self.save_config()

    def remove_worker_node(self, node: str):
        self.worker_nodes.remove(node)
        self.save_config()

    def save_config(self):
        config = {'worker_nodes': self.worker_nodes}
        with open(self.config_file, 'w') as file:
            yaml.dump(config, file)

def main():
    config_file = '/opt/axentx/surrogate-1/config/scale_config.yaml'
    load_balancer = LoadBalancer(config_file)
    worker_nodes = load_balancer.get_worker_nodes()
    print(f"Current worker nodes: {worker_nodes}")

    # Add worker nodes
    for i in range(5, 10):
        node = f"worker-node-{i}"
        load_balancer.add_worker_node(node)

    # Remove worker node
    node_to_remove = "worker-node-5"
    if node_to_remove in load_balancer.get_worker_nodes():
        load_balancer.remove_worker_node(node_to_remove)

if __name__ == "__main__":
    main()