import os
import pickle
import time
from typing import List, Dict, Any, Tuple

_MODEL_PATH = "/opt/axentx/surrogate-1/models/ranker.pkl"
_DEFAULT_TOP_N = 3


class DummyModel:
    """A very lightweight fallback model used when the real model file is missing."""

    def predict(self, features: List[float]) -> float:
        # Simulate a cheap linear scoring function.
        return sum(features)


def _load_model() -> Any:
    """Load the ranking model from disk, falling back to a dummy model if unavailable."""
    if os.path.exists(_MODEL_PATH):
        try:
            with open(_MODEL_PATH, "rb") as f:
                model = pickle.load(f)
                return model
        except Exception:
            # Corrupted file – fall back to dummy.
            pass
    return DummyModel()


# Load once at import time – cheap and thread‑safe for our use‑case.
_MODEL = _load_model()


def _extract_features(build: Dict[str, Any]) -> List[float]:
    """
    Convert a build dict into a flat list of numeric features for the model.
    This implementation is intentionally simple; real logic would be more elaborate.
    """
    # Example: assume each build has numeric fields 'cpu', 'gpu', 'ram'.
    # Missing keys default to 0.
    return [
        float(build.get("cpu", 0)),
        float(build.get("gpu", 0)),
        float(build.get("ram", 0)),
    ]


def score_builds(
    builds: List[Dict[str, Any]],
    top_n: int = _DEFAULT_TOP_N,
) -> List[Tuple[Dict[str, Any], float]]:
    """
    Score each candidate build using the loaded model and return the top N builds.

    Returns:
        List of tuples (build, score) sorted descending by score.
    """
    scored: List[Tuple[Dict[str, Any], float]] = []
    for build in builds:
        features = _extract_features(build)
        score = _MODEL.predict(features)  # type: ignore[attr-defined]
        scored.append((build, score))

    # Sort by score descending and keep the best `top_n`.
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_n]