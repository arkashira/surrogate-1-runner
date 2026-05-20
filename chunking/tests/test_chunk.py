import unittest
import os
import json
from chunking.chunk import DocumentChunker

class TestDocumentChunker(unittest.TestCase):
    def setUp(self):
        self.chunker = DocumentChunker(chunk_size=10, output_dir="test_chunks")
        self.document = {
            "text": "This is a sample document to be chunked into smaller pieces.",
            "title": "Sample Document",
            "author": "John Doe"
        }
        self.document_id = "test_doc_123"

    def tearDown(self):
        if os.path.exists("test_chunks"):
            for file in os.listdir("test_chunks"):
                os.remove(os.path.join("test_chunks", file))
            os.rmdir("test_chunks")

    def test_chunk_document(self):
        chunks = self.chunker.chunk_document(self.document)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0]["text"], "This is a ")
        self.assertEqual(chunks[1]["text"], "sample docu")
        self.assertEqual(chunks[2]["text"], "ment to be c")
        self.assertEqual(chunks[0]["metadata"], {"title": "Sample Document", "author": "John Doe"})
        self.assertEqual(chunks[0]["chunk_index"], 0)
        self.assertEqual(chunks[0]["total_chunks"], 3)

    def test_save_chunks(self):
        chunks = self.chunker.chunk_document(self.document)
        self.chunker.save_chunks(chunks, self.document_id)
        for i in range(3):
            chunk_path = os.path.join("test_chunks", f"{self.document_id}_chunk_{i}.json")
            self.assertTrue(os.path.exists(chunk_path))
            with open(chunk_path, "r") as f:
                chunk = json.load(f)
                self.assertEqual(chunk["text"], chunks[i]["text"])
                self.assertEqual(chunk["metadata"], chunks[i]["metadata"])

    def test_process_document(self):
        self.chunker.process_document(self.document, self.document_id)
        for i in range(3):
            chunk_path = os.path.join("test_chunks", f"{self.document_id}_chunk_{i}.json")
            self.assertTrue(os.path.exists(chunk_path))
            with open(chunk_path, "r") as f:
                chunk = json.load(f)
                self.assertEqual(chunk["text"], self.document["text"][i*10:(i+1)*10])
                self.assertEqual(chunk["metadata"], {"title": "Sample Document", "author": "John Doe"})

if __name__ == "__main__":
    unittest.main()