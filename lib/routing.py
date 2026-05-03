import hashlib

SIBLINGS = [
    "axentx/surrogate-1-training-pairs",
    "axentx/surrogate-1-training-pairs-sib1",
    "axentx/surrogate-1-training-pairs-sib2",
    "axentx/surrogate-1-training-pairs-sib3",
    "axentx/surrogate-1-training-pairs-sib4",
]

def pick_repo(slug: str) -> str:
    """Deterministic repo assignment from slug."""
    digest = hashlib.md5(slug.encode()).hexdigest()
    idx = int(digest, 16) % len(SIBLINGS)
    return SIBLINGS[idx]

def pick_repo_by_shard(shard_id: int, total_shards: int = 16) -> str:
    """Map N shards into 5 siblings deterministically."""
    idx = shard_id % len(SIBLINGS)
    return SIBLINGS[idx]