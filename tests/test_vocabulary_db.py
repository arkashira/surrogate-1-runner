import unittest
from src.vocabulary_db import VocabularyDB

class TestVocabularyDB(unittest.TestCase):
    def setUp(self):
        self.db = VocabularyDB(':memory:')
        self.db.add_vocabulary('Network Switch', 'Device that connects multiple computers together', 'Networking')
        self.db.add_vocabulary('Router', 'Device that directs traffic between networks', 'Networking')

    def test_get_vocabulary_by_topic(self):
        vocabulary = self.db.get_vocabulary_by_topic('Networking')
        self.assertEqual(len(vocabulary), 2)

    def tearDown(self):
        self.db.close()

if __name__ == '__main__':
    unittest.main()