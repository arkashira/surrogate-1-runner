import os
from typing import List, Dict, Any
import json
from pathlib import Path

class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, output_dir: str = "chunked_documents"):
        self.chunk_size = chunk_size
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk a document into smaller pieces while preserving structure and context.

        Args:
            document: A dictionary representing the document to be chunked.

        Returns:
            A list of dictionaries, each representing a chunk of the original document.
        """
        chunks = []
        text = document.get("text", "")
        metadata = {k: v for k, v in document.items() if k != "text"}

        for i in range(0, len(text), self.chunk_size):
            chunk_text = text[i:i + self.chunk_size]
            chunk = {
                "text": chunk_text,
                "metadata": metadata,
                "chunk_index": i // self.chunk_size,
                "total_chunks": (len(text) + self.chunk_size - 1) // self.chunk_size
            }
            chunks.append(chunk)

        return chunks

    def save_chunks(self, chunks: List[Dict[str, Any]], document_id: str):
        """
        Save chunks to the specified output directory.

        Args:
            chunks: A list of dictionaries, each representing a chunk of a document.
            document_id: A unique identifier for the document.
        """
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(self.output_dir, f"{document_id}_chunk_{i}.json")
            with open(chunk_path, "w") as f:
                json.dump(chunk, f, indent=2)

    def process_document(self, document: Dict[str, Any], document_id: str):
        """
        Process a document by chunking it and saving the chunks.

        Args:
            document: A dictionary representing the document to be processed.
            document_id: A unique identifier for the document.
        """
        chunks = self.chunk_document(document)
        self.save_chunks(chunks, document_id)