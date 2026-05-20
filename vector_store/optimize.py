import numpy as np
from typing import List, Optional
from .base import VectorStore
from .config import VectorStoreConfig

class OptimizedVectorStore(VectorStore):
    def __init__(self, config: VectorStoreConfig):
        super().__init__(config)
        self._dimension = config.dimension
        self._metric = config.metric
        self._quantize = config.quantize
        self._index = None

    def add_vectors(self, vectors: List[np.ndarray], ids: Optional[List[str]] = None):
        """Add vectors to the optimized vector store.

        Args:
            vectors: List of vectors to add.
            ids: Optional list of IDs corresponding to the vectors.
        """
        if self._index is None:
            self._initialize_index()

        if ids is None:
            ids = [str(i) for i in range(len(vectors))]

        self._index.add_items(vectors, ids)

    def search(self, query_vector: np.ndarray, k: int = 10) -> List[tuple]:
        """Search for similar vectors in the optimized vector store.

        Args:
            query_vector: The query vector.
            k: Number of nearest neighbors to return.

        Returns:
            List of tuples containing (id, distance) for the nearest neighbors.
        """
        if self._index is None:
            raise ValueError("Index has not been initialized. Call add_vectors first.")

        return self._index.search(query_vector, k)

    def _initialize_index(self):
        """Initialize the optimized index based on the configuration."""
        if self._quantize:
            from pynndescent import NNDescent
            self._index = NNDescent(
                metric=self._metric,
                algorithm='hnsw',
                n_neighbors=10,
                low_memory=True
            )
        else:
            from pynndescent import NNDescent
            self._index = NNDescent(
                metric=self._metric,
                algorithm='hnsw',
                n_neighbors=10,
                low_memory=False
            )

    def optimize(self):
        """Optimize the vector store for performance."""
        if self._index is not None:
            self._index.prepare()

    def save(self, path: str):
        """Save the optimized vector store to disk.

        Args:
            path: Path to save the vector store.
        """
        if self._index is not None:
            self._index.save(path)

    def load(self, path: str):
        """Load the optimized vector store from disk.

        Args:
            path: Path to load the vector store from.
        """
        from pynndescent import NNDescent
        self._index = NNDescent.load(path)