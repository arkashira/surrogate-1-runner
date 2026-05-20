import logging
from typing import List, Dict, Any
from .monitor import PerformanceMonitor

class DocumentPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.monitor = PerformanceMonitor()

    def process_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.monitor.start_timer('process_documents')
        processed_documents = []
        for doc in documents:
            processed_doc = self._process_single_document(doc)
            processed_documents.append(processed_doc)
        self.monitor.end_timer('process_documents')
        return processed_documents

    def _process_single_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        self.monitor.start_timer('process_single_document')
        # Add document processing logic here
        processed_document = document.copy()
        self.monitor.end_timer('process_single_document')
        return processed_document

    def get_performance_metrics(self) -> Dict[str, Any]:
        return self.monitor.get_metrics()