import unittest
from unittest.mock import patch
from src.pipeline.pipeline import DocumentPipeline

class TestDocumentPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = DocumentPipeline()

    @patch('src.pipeline.pipeline.PerformanceMonitor')
    def test_process_documents(self, mock_monitor):
        documents = [{'id': 1, 'text': 'test'}, {'id': 2, 'text': 'test2'}]
        processed_docs = self.pipeline.process_documents(documents)
        self.assertEqual(len(processed_docs), 2)
        mock_monitor.return_value.start_timer.assert_called_with('process_documents')
        mock_monitor.return_value.end_timer.assert_called_with('process_documents')

    @patch('src.pipeline.pipeline.PerformanceMonitor')
    def test_process_single_document(self, mock_monitor):
        document = {'id': 1, 'text': 'test'}
        processed_doc = self.pipeline._process_single_document(document)
        self.assertEqual(processed_doc, document)
        mock_monitor.return_value.start_timer.assert_called_with('process_single_document')
        mock_monitor.return_value.end_timer.assert_called_with('process_single_document')

    def test_get_performance_metrics(self):
        metrics = self.pipeline.get_performance_metrics()
        self.assertIsInstance(metrics, dict)

if __name__ == '__main__':
    unittest.main()