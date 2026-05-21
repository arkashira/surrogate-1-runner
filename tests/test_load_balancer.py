import unittest
from unittest.mock import patch, MagicMock
from load_balancer import LoadBalancer

class TestLoadBalancer(unittest.TestCase):
    def test_load_config(self):
        config_file = '/opt/axentx/surrogate-1/config/scale_config.yaml'
        load_balancer = LoadBalancer(config_file)
        worker_nodes = load_balancer.get_worker_nodes()
        self.assertEqual(len(worker_nodes), 5)

    def test_add_worker_node(self):
        config_file = '/opt/axentx/surrogate-1/config/scale_config.yaml'
        load_balancer = LoadBalancer(config_file)
        node = 'worker-node-6'
        load_balancer.add_worker_node(node)
        worker_nodes = load_balancer.get_worker_nodes()
        self.assertEqual(len(worker_nodes), 6)

    def test_remove_worker_node(self):
        config_file = '/opt/axentx/surrogate-1/config/scale_config.yaml'
        load_balancer = LoadBalancer(config_file)
        node_to_remove = 'worker-node-5'
        load_balancer.remove_worker_node(node_to_remove)
        worker_nodes = load_balancer.get_worker_nodes()
        self.assertEqual(len(worker_nodes), 4)

if __name__ == "__main__":
    unittest.main()