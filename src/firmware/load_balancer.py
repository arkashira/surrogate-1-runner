import numpy as np
import torch

class LoadBalancer:
    def __init__(self, num_gpus):
        self.num_gpus = num_gpus
        self.gpu_utilization = [0] * num_gpus

    def balance_load(self, task_sizes):
        # Sort tasks by size in descending order
        task_sizes = sorted(task_sizes, reverse=True)

        # Initialize GPU task lists
        gpu_tasks = [[] for _ in range(self.num_gpus)]

        # Assign tasks to GPUs
        for task in task_sizes:
            # Find the GPU with the lowest utilization
            min_utilization_gpu = np.argmin(self.gpu_utilization)

            # Assign the task to the GPU with the lowest utilization
            gpu_tasks[min_utilization_gpu].append(task)

            # Update the utilization of the assigned GPU
            self.gpu_utilization[min_utilization_gpu] += task

        return gpu_tasks

    def update_utilization(self, gpu_tasks):
        # Update the utilization of each GPU
        self.gpu_utilization = [sum(tasks) for tasks in gpu_tasks]

def main():
    num_gpus = 4
    load_balancer = LoadBalancer(num_gpus)

    # Simulate task sizes
    task_sizes = np.random.randint(1, 100, size=16)

    # Balance the load
    gpu_tasks = load_balancer.balance_load(task_sizes)

    # Print the assigned tasks for each GPU
    for i, tasks in enumerate(gpu_tasks):
        print(f"GPU {i}: {tasks}")

    # Update the utilization of each GPU
    load_balancer.update_utilization(gpu_tasks)

    # Print the updated utilization of each GPU
    print("GPU Utilization:", load_balancer.gpu_utilization)

if __name__ == "__main__":
    main()