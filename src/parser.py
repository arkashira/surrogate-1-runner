import logging
from logging.handlers import RotatingFileHandler

class Parser:
    def __init__(self, log_file='parser.log', log_level=logging.INFO):
        self.logger = logging.getLogger('Parser')
        self.logger.setLevel(log_level)

        # Create a rotating file handler
        handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
        handler.setLevel(log_level)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def parse(self, data):
        try:
            # Simulate parsing operation
            if not data:
                raise ValueError("Empty data provided for parsing")
            # Add your parsing logic here
            self.logger.info("Parsing operation completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error during parsing: {str(e)}")
            raise