import logging
import time

logger = logging.getLogger(__name__)

class ErrorHandler:
    def __init__(self):
        self.recovery_time_threshold = 0.1  # 100ms

    def handle_error(self, error, chunk_data, chunk_index):
        start_time = time.time()
        
        logger.error(f"Error processing chunk {chunk_index}: {error}")
        logger.debug(f"Chunk data causing error: {chunk_data}")

        # Simulate recovery logic here
        self._simulate_recovery()

        end_time = time.time()
        recovery_time = end_time - start_time

        if recovery_time > self.recovery_time_threshold:
            logger.warning(f"Recovery took {recovery_time:.2f}s which exceeds the threshold of {self.recovery_time_threshold}s")

    def _simulate_recovery(self):
        # Placeholder for actual recovery logic
        pass