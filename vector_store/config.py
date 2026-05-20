from dataclasses import dataclass
from typing import Optional

@dataclass
class VectorStoreConfig:
    dimension: int
    metric: str = "cosine"
    quantize: bool = False
    index_path: Optional[str] = None