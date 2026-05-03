from typing import List, Dict, Any
from src.documents.retriever import DocumentRetriever

_retriever = DocumentRetriever()

def search_documents(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    API-facing search. Returns list of result objects:
      {title, snippet, tags, source_url, is_local}
    """
    if not query or not query.strip():
        return []
    return _retriever.search(query=query.strip(), limit=limit)