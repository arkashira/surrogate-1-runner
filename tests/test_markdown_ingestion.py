import os
import unittest
import sqlite3
from bin.markdown_ingestion import parse_markdown, store_qa_pairs

class TestMarkdownIngestion(unittest.TestCase):
    def setUp(self):
        self.test_markdown_path = 'tests/test_markdown.md'
        self.test_db_path = 'tests/test_database.db'
        with open(self.test_markdown_path, 'w') as file:
            file.write('# Question 1\n\nAnswer 1\n\n# Question 2\n\nAnswer 2')

    def tearDown(self):
        if os.path.exists(self.test_markdown_path):
            os.remove(self.test_markdown_path)
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_parse_markdown(self):
        qa_pairs = parse_markdown(self.test_markdown_path)
        self.assertEqual(len(qa_pairs), 2)
        self.assertEqual(qa_pairs[0], ('Question 1', 'Answer 1'))
        self.assertEqual(qa_pairs[1], ('Question 2', 'Answer 2'))

    def test_store_qa_pairs(self):
        qa_pairs = [('Question 1', 'Answer 1'), ('Question 2', 'Answer 2')]
        store_qa_pairs(qa_pairs, self.test_db_path)
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM qa_pairs')
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], 'Question 1')
        self.assertEqual(rows[0][2], 'Answer 1')
        self.assertEqual(rows[1][1], 'Question 2')
        self.assertEqual(rows[1][2], 'Answer 2')
        conn.close()

if __name__ == '__main__':
    unittest.main()