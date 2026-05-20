import json
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class ChunkStorage:
    """Handles storage of document chunks in a structured format."""
    
    def __init__(self, storage_path: str):
        """
        Initialize chunk storage.
        
        Args:
            storage_path: Path where chunks will be stored
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
    def save_chunks(self, document_id: str, chunks: List[Dict[str, Any]]) -> bool:
        """
        Save chunks for a document in structured JSON format.
        
        Args:
            document_id: Unique identifier for the document
            chunks: List of chunk dictionaries
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create filename based on document ID
            filename = f"{document_id}.json"
            file_path = self.storage_path / filename
            
            # Prepare data structure
            data = {
                "document_id": document_id,
                "chunks": chunks,
                "chunk_count": len(chunks)
            }
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Successfully saved {len(chunks)} chunks for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save chunks for document {document_id}: {str(e)}")
            return False
    
    def load_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Load chunks for a document.
        
        Args:
            document_id: Unique identifier for the document
            
        Returns:
            List of chunk dictionaries or empty list if not found
        """
        try:
            filename = f"{document_id}.json"
            file_path = self.storage_path / filename
            
            if not file_path.exists():
                logger.warning(f"No chunks found for document {document_id}")
                return []
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            logger.info(f"Successfully loaded {data['chunk_count']} chunks for document {document_id}")
            return data.get('chunks', [])
            
        except Exception as e:
            logger.error(f"Failed to load chunks for document {document_id}: {str(e)}")
            return []