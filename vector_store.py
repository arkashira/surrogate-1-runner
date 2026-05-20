import numpy as np
from typing import List, Tuple, Optional
import faiss
import os
import pickle

class VectorStore:
    def __init__(self, dimension: int, index_path: Optional[str] = None):
        """
        Initialize the vector store with a given dimension.
        
        Args:
            dimension: The dimension of the vectors to be stored
            index_path: Optional path to load/save the FAISS index
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.id_to_vector_id = {}  # Maps document IDs to FAISS internal IDs
        self.vector_id_to_doc_id = {}  # Maps FAISS internal IDs to document IDs
        self.next_vector_id = 0
        self.index_path = index_path
        
        # Load existing index if path provided
        if index_path and os.path.exists(index_path + ".faiss"):
            self.load_index()

    def add_documents(self, doc_ids: List[str], vectors: np.ndarray) -> None:
        """
        Add documents and their embeddings to the vector store.
        
        Args:
            doc_ids: List of document IDs
            vectors: NumPy array of shape (n_docs, dimension)
        """
        if len(doc_ids) != len(vectors):
            raise ValueError("Number of document IDs must match number of vectors")
            
        # Normalize vectors for cosine similarity
        normalized_vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        
        # Add vectors to FAISS index
        self.index.add(normalized_vectors.astype(np.float32))
        
        # Update mapping dictionaries
        for i, doc_id in enumerate(doc_ids):
            self.id_to_vector_id[doc_id] = self.next_vector_id
            self.vector_id_to_doc_id[self.next_vector_id] = doc_id
            self.next_vector_id += 1
            
        # Save index after adding
        if self.index_path:
            self.save_index()

    def search(self, query_vector: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """
        Search for most similar documents to the query vector.
        
        Args:
            query_vector: Query vector of shape (dimension,)
            k: Number of results to return
            
        Returns:
            List of tuples (document_id, similarity_score)
        """
        # Normalize query vector
        normalized_query = query_vector / np.linalg.norm(query_vector)
        
        # Perform search
        similarities, indices = self.index.search(
            normalized_query.reshape(1, -1).astype(np.float32), 
            k
        )
        
        # Convert to list of (doc_id, similarity) tuples
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid result
                doc_id = self.vector_id_to_doc_id[idx]
                similarity = similarities[0][i]
                results.append((doc_id, similarity))
                
        return results

    def save_index(self) -> None:
        """Save the FAISS index and metadata to disk."""
        # Save FAISS index
        faiss.write_index(self.index, self.index_path + ".faiss")
        
        # Save metadata
        metadata = {
            'id_to_vector_id': self.id_to_vector_id,
            'vector_id_to_doc_id': self.vector_id_to_doc_id,
            'next_vector_id': self.next_vector_id
        }
        
        with open(self.index_path + ".metadata", 'wb') as f:
            pickle.dump(metadata, f)

    def load_index(self) -> None:
        """Load the FAISS index and metadata from disk."""
        # Load FAISS index
        self.index = faiss.read_index(self.index_path + ".faiss")
        
        # Load metadata
        with open(self.index_path + ".metadata", 'rb') as f:
            metadata = pickle.load(f)
            
        self.id_to_vector_id = metadata['id_to_vector_id']
        self.vector_id_to_doc_id = metadata['vector_id_to_doc_id']
        self.next_vector_id = metadata['next_vector_id']

    def get_document_count(self) -> int:
        """Get the number of documents currently stored."""
        return len(self.id_to_vector_id)

    def clear(self) -> None:
        """Clear all documents and reset the vector store."""
        self.index.reset()
        self.id_to_vector_id.clear()
        self.vector_id_to_doc_id.clear()
        self.next_vector_id = 0