import unittest
from firmware.load_balancer import LoadBalancer

class TestLoadBalancer(unittest.TestCase):
    def test_balance_load(self):
        num_gpus = 4
        load_balancer = LoadBalancer(num_gpus)

        # Simulate task sizes
        task_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]

        # Balance the load
        gpu_tasks = load_balancer.balance_load(task_sizes)

        # Check if the tasks are assigned to the GPUs
        self.assertEqual(len(gpu_tasks), num_gpus)
        self.assertEqual(sum([len(tasks) for tasks in gpu_tasks]), len(task_sizes))

    def test_update_utilization(self):
        num_gpus = 4
        load_balancer = LoadBalancer(num_gpus)

        # Simulate task sizes
        task_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]

        # Balance the load
        gpu_tasks = load_balancer.balance_load(task_sizes)

        # Update the utilization of each GPU
        load_balancer.update_utilization(gpu_tasks)

        # Check if the utilization of each GPU is updated
        self.assertEqual(len(load_balancer.gpu_utilization), num_gpus)
        self.assertGreater(sum(load_balancer.gpu_utilization), 0)

if __name__ == "__main__":
    unittest.main()