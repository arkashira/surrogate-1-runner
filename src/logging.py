import logging
from datetime import datetime

class AIModelUsageLogger:
    def __init__(self, db_handler):
        self.logger = logging.getLogger('AIModelUsage')
        self.logger.setLevel(logging.INFO)
        self.db_handler = db_handler

    def log_usage(self, user_id, model_name, usage_details):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'model_name': model_name,
            'usage_details': usage_details
        }
        self.logger.info(f"Logging usage: {log_entry}")
        self.db_handler.store_log(log_entry)

def setup_logger():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('AIModelUsage')
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    # Example usage
    db_handler = DBHandler()  # Assuming DBHandler is defined in db.py
    logger = AIModelUsageLogger(db_handler)
    logger.log_usage('user123', 'modelX', {'input': 'example input', 'output': 'example output'})