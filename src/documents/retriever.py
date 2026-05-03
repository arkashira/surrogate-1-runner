from typing import List, Dict, Any

class DocumentRetriever:
    def __init__(self, index_path: str = None):
        # lightweight in-memory or disk index placeholder
        self.index_path = index_path

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Return search results with:
          - title
          - snippet
          - tags (list[str])
          - source_url
          - is_local (bool)
        """
        # Placeholder implementation — replace with real retrieval (BM25/embedding).
        # This ensures API/frontend contract is stable.
        results: List[Dict[str, Any]] = []

        # Example mock results to satisfy frontend contract during dev:
        mock = [
            {
                "title": "Getting Started with Surrogate-1",
                "snippet": "This document describes the surrogate-1 architecture and how to run ingestion workers.",
                "tags": ["architecture", "ingest", "guide"],
                "source_url": "/documents/guide-surrogate-1.pdf",
                "is_local": True,
            },
            {
                "title": "Dataset Enrichment Script",
                "snippet": "The bin/dataset-enrich.sh script normalizes and deduplicates public datasets.",
                "tags": ["scripts", "dedup", "datasets"],
                "source_url": "https://github.com/axentx/surrogate-1/blob/main/bin/dataset-enrich.sh",
                "is_local": False,
            },
        ]

        # Simple keyword filter on title/snippet for mock behavior
        lowered = query.lower()
        for item in mock:
            if lowered in item["title"].lower() or lowered in item["snippet"].lower():
                results.append(item)

        # If real index exists, replace mock with:
        # results = self._query_index(query, limit)

        return results[:limit]

    # Optional: real index query stub
    def _query_index(self, query: str, limit: int) -> List[Dict[str, Any]]:
        # TODO: integrate BM25/vector index
        return []