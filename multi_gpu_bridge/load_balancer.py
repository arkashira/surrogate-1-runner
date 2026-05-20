class LoadBalancer:
    def __init__(self, gpus):
        self.gpus = gpus
        self.load = {gpu: 0 for gpu in gpus}

    def optimize_load_balancing(self, tasks):
        """Distribute tasks across GPUs based on current load."""
        for task in tasks:
            selected_gpu = min(self.load, key=self.load.get)
            self.assign_task_to_gpu(selected_gpu, task)

    def assign_task_to_gpu(self, gpu, task):
        """Assign a task to a specific GPU and update load."""
        # Simulate task assignment
        print(f"Assigning task {task} to GPU {gpu}")
        self.load[gpu] += 1  # Increment load for the assigned GPU

    def get_load(self):
        """Return the current load of each GPU."""
        return self.load

# Example usage
if __name__ == "__main__":
    gpus = ['GPU1', 'GPU2', 'GPU3']
    tasks = ['Task1', 'Task2', 'Task3', 'Task4']
    load_balancer = LoadBalancer(gpus)
    load_balancer.optimize_load_balancing(tasks)
    print(load_balancer.get_load())