import time
from utils.resource_manager import ResourceManager

class BatchProcessor:
    def __init__(self, base_batch_size=100, item_size=1024):
        self.base_batch_size = base_batch_size
        self.item_size = item_size
        self.resource_manager = ResourceManager()

    def process_batch(self, items):
        """Process a batch of items"""
        # Simulate processing time
        time.sleep(0.1)
        return [self._process_item(item) for item in items]

    def _process_item(self, item):
        """Process a single item"""
        # Simulate item processing
        return item.upper()

    def get_optimal_batch_size(self):
        """Get optimal batch size based on current memory conditions"""
        return self.resource_manager.calculate_optimal_batch_size(
            self.base_batch_size,
            self.item_size
        )

    def monitor_memory_usage(self):
        """Monitor memory usage and adjust batch size if needed"""
        memory_usage = self.resource_manager.get_memory_usage_percentage()
        if memory_usage > 80:
            # Reduce batch size if memory usage is too high
            self.base_batch_size = max(10, self.base_batch_size // 2)