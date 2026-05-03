import hashlib

SIBLING_REPOS = [
    "axentx/surrogate-1-training-pairs",
    "axentx/surrogate-1-training-pairs-sib1",
    "axentx/surrogate-1-training-pairs-sib2",
    "axentx/surrogate-1-training-pairs-sib3",
    "axentx/surrogate-1-training-pairs-sib4",
]

def repo_for_slug(slug: str) -> str:
    """Deterministic repo assignment from slug."""
    digest = hashlib.md5(slug.encode()).hexdigest()
    idx = int(digest, 16) % len(SIBLING_REPOS)
    return SIBLING_REPOS[idx]