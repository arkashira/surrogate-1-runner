import os
import tempfile
import unittest
from src.ingest.docx_ingestor import DocxIngestor

class TestDocxIngestor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.ingestor = DocxIngestor(self.temp_dir)

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_ingest(self):
        test_file = os.path.join(self.temp_dir, "test.docx")
        doc = docx.Document()
        doc.add_paragraph("Test paragraph 1")
        doc.add_paragraph("Test paragraph 2")
        doc.save(test_file)

        output_path = self.ingestor.ingest(test_file)
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, "r") as f:
            content = f.read()
        self.assertEqual(content, "Test paragraph 1\nTest paragraph 2")

if __name__ == "__main__":
    unittest.main()