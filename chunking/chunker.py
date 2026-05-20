import logging
from typing import List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentChunker:
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def chunk_document(self, document: str) -> List[str]:
        """
        Splits the document into chunks of configurable size.
        
        :param document: The document to be chunked.
        :return: A list of document chunks.
        """
        return [document[i:i + self.chunk_size] for i in range(0, len(document), self.chunk_size)]

    def store_chunks(self, chunks: List[str], storage_path: str) -> None:
        """
        Stores the chunks in a structured format at the specified storage path.
        
        :param chunks: The list of document chunks.
        :param storage_path: The path where chunks should be stored.
        """
        try:
            with open(storage_path, 'w') as f:
                for chunk in chunks:
                    f.write(f"{chunk}\n")
            logger.info(f"Chunks successfully stored at {storage_path}")
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")

    def process_document(self, document: str, storage_path: str) -> Tuple[List[str], bool]:
        """
        Processes the document by chunking it and storing the chunks.
        
        :param document: The document to be processed.
        :param storage_path: The path where chunks should be stored.
        :return: A tuple containing the list of chunks and a boolean indicating success.
        """
        chunks = self.chunk_document(document)
        try:
            self.store_chunks(chunks, storage_path)
            return chunks, True
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return [], False


# /opt/axentx/surrogate-1/chunking/tests/test_chunker.py
import unittest
from chunking.chunker import DocumentChunker

class TestDocumentChunker(unittest.TestCase):
    def setUp(self):
        self.chunker = DocumentChunker(chunk_size=10)

    def test_chunk_document(self):
        document = "This is a sample document to be chunked."
        expected_chunks = ["This is a ", "sample do", "cument t", "o be chu", "nked."]
        chunks = self.chunker.chunk_document(document)
        self.assertEqual(chunks, expected_chunks)

    def test_store_chunks(self):
        chunks = ["chunk1", "chunk2", "chunk3"]
        storage_path = "/tmp/test_chunks.txt"
        self.chunker.store_chunks(chunks, storage_path)
        with open(storage_path, 'r') as f:
            stored_chunks = f.readlines()
        self.assertEqual(stored_chunks, ["chunk1\n", "chunk2\n", "chunk3\n"])

    def test_process_document(self):
        document = "Another sample document."
        storage_path = "/tmp/test_processed_chunks.txt"
        chunks, success = self.chunker.process_document(document, storage_path)
        self.assertTrue(success)
        with open(storage_path, 'r') as f:
            stored_chunks = f.readlines()
        expected_chunks = ["Another s", "ample do", "cument.\n"]
        self.assertEqual(stored_chunks, expected_chunks)

if __name__ == '__main__':
    unittest.main()