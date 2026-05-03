import os
import time
import numpy as np
import faiss
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DEFAULT_BATCH = int(os.getenv("EMBED_BATCH", "32"))
DEFAULT_DIM = 384  # all-MiniLM-L6-v2 output dim

class PageEmbedder:
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH,
    ):
        self.device = device or ("cuda" if faiss.get_num_gpus() > 0 else "cpu")
        self.model = SentenceTransformer(model_name, device=self.device)
        self.batch_size = batch_size
        self.dim = DEFAULT_DIM
        self.index = faiss.IndexFlatIP(self.dim)  # In-memory FAISS index

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        start = time.time()
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_tensor=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        embeddings = embeddings.cpu().numpy().astype(np.float32)
        faiss.normalize_L2(embeddings)
        elapsed = (time.time() - start) * 1000
        if elapsed > 600:
            import warnings
            warnings.warn(
                f"Embedding batch took {elapsed:.0f}ms; consider smaller batches or GPU."
            )
        return embeddings

    def embed_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        texts = [p["snippet"] for p in pages]
        embs = self.embed_texts(texts)
        for i, p in enumerate(pages):
            p["embedding"] = embs[i]
        self.index.add(embs)  # Add embeddings to the FAISS index
        return pages

    def search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        query_embedding = self.embed_texts([query])
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for idx in indices[0]:
            if idx != -1:  # Check if the index is valid
                results.append(pages[idx])  # Assuming pages are stored globally
        return results