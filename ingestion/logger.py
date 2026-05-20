import logging
import os
from datetime import datetime

class IngestionLogger:
    def __init__(self, log_dir='/tmp/ingestion_logs'):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_file = os.path.join(self.log_dir, f'ingestion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def log_success(self, message):
        logging.info(message)

    def log_error(self, message):
        logging.error(message)

def log_ingestion_status(doc_format, doc_path, success=True):
    logger = IngestionLogger()
    if success:
        logger.log_success(f'Successfully ingested {doc_format} document from {doc_path}')
    else:
        logger.log_error(f'Failed to ingest {doc_format} document from {doc_path}')

# Example usage:
# log_ingestion_status('PDF', '/path/to/document.pdf', success=True)
# log_ingestion_status('DOCX', '/path/to/document.docx', success=False)