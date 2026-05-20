import logging
from datetime import datetime

logging.basicConfig(filename='/opt/axentx/surrogate-1/logs/proxy.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

class LoggingMechanism:
    @staticmethod
    def log_info(message):
        logging.info(message)

    @staticmethod
    def log_error(message):
        logging.error(message)

    @staticmethod
    def log_warning(message):
        logging.warning(message)

# Example usage
if __name__ == "__main__":
    logger = LoggingMechanism()
    logger.log_info("Proxy initialized at {}".format(datetime.now()))
    logger.log_warning("High traffic detected.")