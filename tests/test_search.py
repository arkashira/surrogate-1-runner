import unittest
from search import Search

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.search = Search()

    def test_search_tools(self):
        results = self.search.search_tools('ingestion')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Data Ingestion')

    def test_search_features(self):
        results = self.search.search_features('visualization')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['tool_name'], 'Data Analysis')
        self.assertEqual(results[0]['feature'], 'visualization')

if __name__ == '__main__':
    unittest.main()