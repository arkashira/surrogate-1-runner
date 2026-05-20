from typing import List, Dict, Any
import logging
from uuid import uuid4
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

@dataclass
class EmbeddingRecord:
    """Represents a single embedding record"""
    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]

class VectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def store_embedding(self, record: EmbeddingRecord) -> bool:
        """Store a single embedding record"""
        pass
    
    @abstractmethod
    def store_embeddings(self, records: List[EmbeddingRecord]) -> bool:
        """Store multiple embedding records"""
        pass
    
    @abstractmethod
    def get_embedding(self, id: str) -> EmbeddingRecord:
        """Retrieve a single embedding by ID"""
        pass
    
    @abstractmethod
    def search_similar(self, query_embedding: List[float], 
                      limit: int = 10) -> List[EmbeddingRecord]:
        """Search for similar embeddings"""
        pass

class InMemoryVectorStore(VectorStore):
    """In-memory implementation of vector store for testing purposes"""
    
    def __init__(self):
        self._store = {}
        self._ids = set()
    
    def store_embedding(self, record: EmbeddingRecord) -> bool:
        try:
            if record.id in self._ids:
                logger.warning(f"Overwriting existing embedding with ID: {record.id}")
            
            self._store[record.id] = record
            self._ids.add(record.id)
            logger.info(f"Successfully stored embedding with ID: {record.id}")
            return True
        except Exception as e:
            logger.error(f"Failed to store embedding with ID {record.id}: {str(e)}")
            return False
    
    def store_embeddings(self, records: List[EmbeddingRecord]) -> bool:
        success_count = 0
        for record in records:
            if self.store_embedding(record):
                success_count += 1
        
        logger.info(f"Stored {success_count}/{len(records)} embeddings successfully")
        return success_count == len(records)
    
    def get_embedding(self, id: str) -> EmbeddingRecord:
        try:
            return self._store.get(id)
        except Exception as e:
            logger.error(f"Failed to retrieve embedding with ID {id}: {str(e)}")
            return None
    
    def search_similar(self, query_embedding: List[float], 
                      limit: int = 10) -> List[EmbeddingRecord]:
        # Simple Euclidean distance calculation for demonstration
        try:
            results = []
            for record in self._store.values():
                # Calculate squared Euclidean distance
                distance = sum((a - b) ** 2 for a, b in zip(query_embedding, record.embedding))
                results.append((distance, record))
            
            # Sort by distance and return top results
            results.sort(key=lambda x: x[0])
            return [record for _, record in results[:limit]]
        except Exception as e:
            logger.error(f"Failed to search similar embeddings: {str(e)}")
            return []

def create_vector_store(store_type: str = "memory") -> VectorStore:
    """Factory function to create vector store instances"""
    if store_type == "memory":
        return InMemoryVectorStore()
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")