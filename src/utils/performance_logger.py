import logging

class PerformanceLogger:
    def __init__(self):
        self.logger = logging.getLogger('performance_logger')
        self.logger.setLevel(logging.INFO)

        # Create file handler
        handler = logging.FileHandler('performance.log')
        handler.setLevel(logging.INFO)

        # Create formatter and add to handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(handler)

    def log_routing_time(self, time_taken):
        self.logger.info(f'Routing time: {time_taken} seconds')

    def log_routing_accuracy(self, is_accurate):
        self.logger.info(f'Routing accuracy: {is_accurate}')