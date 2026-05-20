"""
Surrogate-1 SDK for embedding manipulation and watermarking pipelines.

This SDK provides:
- Internal embedding access functions
- Watermarking utilities and example pipelines
"""

from .embeddings import EmbeddingStore, EmbeddingVector, get_embedding, list_embeddings, create_embedding
from .watermarking import Watermarker, Watermark, apply_watermark, verify_watermark
from .pipelines import WatermarkPipeline, EmbeddingPipeline

__version__ = "0.1.0"

__all__ = [
    "EmbeddingStore",
    "EmbeddingVector",
    "get_embedding",
    "list_embeddings",
    "create_embedding",
    "Watermarker",
    "Watermark",
    "apply_watermark",
    "verify_watermark",
    "WatermarkPipeline",
    "EmbeddingPipeline",
]