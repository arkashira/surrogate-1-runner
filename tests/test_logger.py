import unittest
from ingestion.logger import log_ingestion_status

class TestIngestionLogger(unittest.TestCase):
    def setUp(self):
        self.test_log_dir = '/tmp/test_ingestion_logs'
        if not os.path.exists(self.test_log_dir):
            os.makedirs(self.test_log_dir)

    def test_log_success(self):
        log_ingestion_status('TXT', '/path/to/document.txt', success=True)
        log_files = [f for f in os.listdir(self.test_log_dir) if f.startswith('ingestion_')]
        self.assertTrue(len(log_files) > 0)
        with open(os.path.join(self.test_log_dir, log_files[0]), 'r') as f:
            log_content = f.read()
            self.assertIn('Successfully ingested TXT document from /path/to/document.txt', log_content)

    def test_log_error(self):
        log_ingestion_status('PDF', '/path/to/document.pdf', success=False)
        log_files = [f for f in os.listdir(self.test_log_dir) if f.startswith('ingestion_')]
        self.assertTrue(len(log_files) > 0)
        with open(os.path.join(self.test_log_dir, log_files[0]), 'r') as f:
            log_content = f.read()
            self.assertIn('Failed to ingest PDF document from /path/to/document.pdf', log_content)

if __name__ == '__main__':
    unittest.main()