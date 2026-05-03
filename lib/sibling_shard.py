import hashlib
from typing import List

SIBLINGS = [
    "axentx/surrogate-1-training-pairs",
    "axentx/surrogate-1-shard-1",
    "axentx/surrogate-1-shard-2",
    "axentx/surrogate-1-shard-3",
    "axentx/surrogate-1-shard-4",
]

def repo_for_slug(slug: str, siblings: List[str] = SIBLINGS) -> str:
    """
    Deterministic shard assignment: hash slug -> sibling repo.
    5 siblings = 640 commits/hr aggregate.
    """
    digest = hashlib.sha256(slug.encode()).hexdigest()
    idx = int(digest, 16) % len(siblings)
    return siblings[idx]