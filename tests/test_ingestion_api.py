import os
import unittest
import sqlite3
from flask import json
from bin.ingestion_api import app

class TestIngestionAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.test_markdown_path = 'tests/test_markdown.md'
        self.test_db_path = 'tests/test_database.db'
        with open(self.test_markdown_path, 'w') as file:
            file.write('# Question 1\n\nAnswer 1\n\n# Question 2\n\nAnswer 2')

    def tearDown(self):
        if os.path.exists(self.test_markdown_path):
            os.remove(self.test_markdown_path)
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_ingest_markdown(self):
        with open(self.test_markdown_path, 'rb') as file:
            response = self.app.post('/ingest', data={'file': (file, 'test_markdown.md')})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'File ingested successfully')
        self.assertEqual(len(data['qa_pairs']), 2)

if __name__ == '__main__':
    unittest.main()