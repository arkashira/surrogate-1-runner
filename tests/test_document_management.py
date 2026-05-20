import unittest
from document_management import DocumentManager

class TestDocumentManager(unittest.TestCase):
    def setUp(self):
        self.manager = DocumentManager()

    def test_create_document(self):
        self.manager.create_document('doc1', 'Initial content')
        self.assertEqual(self.manager.documents['doc1']['content'], 'Initial content')

    def test_edit_document(self):
        self.manager.create_document('doc1', 'Initial content')
        self.manager.edit_document('doc1', 'Updated content')
        self.assertEqual(self.manager.documents['doc1']['content'], 'Updated content')

    def test_delete_document(self):
        self.manager.create_document('doc1', 'Initial content')
        self.manager.delete_document('doc1')
        self.assertNotIn('doc1', self.manager.documents)

    def test_get_version_history(self):
        self.manager.create_document('doc1', 'Initial content')
        self.manager.edit_document('doc1', 'Updated content')
        history = self.manager.get_version_history('doc1')
        self.assertEqual(history, ['Initial content', 'Updated content'])

    def test_revert_to_previous_version(self):
        self.manager.create_document('doc1', 'Initial content')
        self.manager.edit_document('doc1', 'Updated content')
        self.manager.revert_to_previous_version('doc1', 0)
        self.assertEqual(self.manager.documents['doc1']['content'], 'Initial content')

if __name__ == '__main__':
    unittest.main()