import psutil
import math

class ResourceManager:
    def __init__(self):
        self.memory_threshold = 0.8  # 80% of available memory

    def get_available_memory(self):
        """Get available memory in bytes"""
        mem = psutil.virtual_memory()
        return mem.available

    def calculate_optimal_batch_size(self, base_batch_size, item_size):
        """
        Calculate optimal batch size based on available memory
        :param base_batch_size: Base batch size to start with
        :param item_size: Approximate size of each item in bytes
        :return: Optimal batch size
        """
        available_memory = self.get_available_memory()
        max_memory_usage = available_memory * self.memory_threshold
        optimal_size = math.floor(max_memory_usage / item_size)

        # Ensure we don't go below the base batch size
        return max(base_batch_size, optimal_size)

    def get_memory_usage_percentage(self):
        """Get current memory usage percentage"""
        mem = psutil.virtual_memory()
        return mem.percent