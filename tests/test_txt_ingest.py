import os
import unittest
from ingestion.txt_ingest import ingest_txt

class TestTXTIngest(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "test_sample.txt"
        self.output_dir = "test_output"
        with open(self.test_file_path, 'w') as f:
            f.write("Test content")
    
    def tearDown(self):
        os.remove(self.test_file_path)
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
        os.rmdir(self.output_dir)
    
    def test_ingest_txt(self):
        ingest_txt(self.test_file_path, self.output_dir)
        output_file_path = os.path.join(self.output_dir, os.path.basename(self.test_file_path))
        self.assertTrue(os.path.exists(output_file_path))
        with open(output_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "Test content")

if __name__ == '__main__':
    unittest.main()