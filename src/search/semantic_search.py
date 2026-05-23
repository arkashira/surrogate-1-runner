"""
Semantic search engine for markdown documents.

This module provides a `SemanticSearchEngine` class that:
* Loads a pre-built FAISS index and associated metadata.
* Executes a semantic query and returns results ranked by cosine similarity.
* Supports optional filtering by tags, dates, and content types.

The index is expected to be built by `src/indexer/indexer.py`.
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticSearchEngine:
    """
    Semantic search engine for markdown documents.

    Parameters
    ----------
    index_path : str | Path
        Path to the FAISS index file (.index).
    metadata_path : str | Path
        Path to the JSON file mapping vector IDs to metadata.
    model_name : str, optional
        SentenceTransformer model name to use for query embeddings.
    """

    def __init__(
        self,
        index_path: str | Path,
        metadata_path: str | Path,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

        if not self.index_path.is_file():
            raise FileNotFoundError(f"FAISS index not found: {self.index_path}")
        if not self.metadata_path.is_file():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")

        # Load FAISS index
        self.index = faiss.read_index(str(self.index_path))
        # Load metadata mapping
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            self.id_to_meta: Dict[int, Dict[str, Any]] = json.load(f)

        # Load sentence transformer model for query embeddings
        self.model = SentenceTransformer(model_name)

        # Determine dimensionality
        self.dim = self.index.d

    def _filter_ids(
        self,
        ids: List[int],
        tags: Optional[List[str]] = None,
        dates: Optional[List[str]] = None,
        content_types: Optional[List[str]] = None,
    ) -> List[int]:
        """
        Filter a list of vector IDs based on metadata.

        Parameters
        ----------
        ids : List[int]
            Candidate vector IDs.
        tags : Optional[List[str]]
            Tags to filter by (OR semantics).
        dates : Optional[List[str]]
            Dates to filter by (exact match).
        content_types : Optional[List[str]]
            Content types to filter by (OR semantics).

        Returns
        -------
        List[int]
            Filtered list of vector IDs.
        """
        if not any([tags, dates, content_types]):
            return ids

        filtered = []
        for idx in ids:
            meta = self.id_to_meta.get(str(idx), {})
            if tags and not set(tags).intersection(set(meta.get("tags", []))):
                continue
            if dates and meta.get("date") not in dates:
                continue
            if content_types and meta.get("content_type") not in content_types:
                continue
            filtered.append(idx)
        return filtered

    def search(
        self,
        query: str,
        top_k: int = 10,
        tags: Optional[List[str]] = None,
        dates: Optional[List[str]] = None,
        content_types: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute a semantic search query.

        Parameters
        ----------
        query : str
            Natural language query.
        top_k : int, default 10
            Number of results to return before filtering.
        tags : Optional[List[str]]
            Tags to filter by.
        dates : Optional[List[str]]
            Dates to filter by.
        content_types : Optional[List[str]]
            Content types to filter by.

        Returns
        -------
        List[Dict[str, Any]]
            List of result dictionaries sorted by relevance.
            Each dict contains:
                - path: file path
                - score: cosine similarity score
                - metadata: dict of metadata fields
        """
        # Encode query
        query_vec = self.model.encode([query], normalize_embeddings=True)
        query_vec = np.asarray(query_vec, dtype="float32")

        # Search FAISS index
        distances, indices = self.index.search(query_vec, top_k * 2)  # overshoot for filtering
        # FAISS returns L2 distances; convert to cosine similarity
        # Since vectors are normalized, cosine = 1 - 0.5 * L2^2
        sims = 1 - 0.5 * distances[0] ** 2
        candidate_ids = indices[0].tolist()

        # Apply metadata filters
        filtered_ids = self._filter_ids(candidate_ids, tags, dates, content_types)

        # Build result list
        results = []
        for idx, score in zip(filtered_ids, sims):
            meta = self.id_to_meta.get(str(idx), {})
            results.append(
                {
                    "path": meta.get("path"),
                    "score": float(score),
                    "metadata": meta,
                }
            )
            if len(results) >= top_k:
                break

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results