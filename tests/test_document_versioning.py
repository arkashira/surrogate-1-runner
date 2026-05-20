import unittest
from document_versioning import DocumentVersioning

class TestDocumentVersioning(unittest.TestCase):
    def setUp(self):
        self.doc_versioning = DocumentVersioning('test_doc')

    def test_create_version(self):
        version_id = self.doc_versioning.create_version('Test content')
        self.assertEqual(version_id, 1)
        self.assertEqual(len(self.doc_versioning.get_version_history()), 1)

    def test_get_version_history(self):
        self.doc_versioning.create_version('Version 1')
        self.doc_versioning.create_version('Version 2')
        history = self.doc_versioning.get_version_history()
        self.assertEqual(len(history), 2)

    def test_revert_to_version(self):
        self.doc_versioning.create_version('Version 1')
        self.doc_versioning.create_version('Version 2')
        self.assertTrue(self.doc_versioning.revert_to_version(1))
        latest_version = self.doc_versioning.get_version_history()[-1]
        self.assertEqual(latest_version['content'], 'Version 1')


if __name__ == '__main__':
    unittest.main()