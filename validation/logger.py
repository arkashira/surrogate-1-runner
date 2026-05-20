import logging

def setup_logger(log_file):
    logger = logging.getLogger('validation_logger')
    logger.setLevel(logging.ERROR)
    
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

def log_error(logger, message):
    logger.error(message)