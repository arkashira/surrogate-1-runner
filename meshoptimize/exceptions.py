class MeshOptimizeError(Exception):
    """Base exception for all SDK errors."""


class InvalidAPIKeyError(MeshOptimizeError):
    """Raised when the provided API key is invalid."""


class MeshOptimizationError(MeshOptimizeError):
    """Raised when the optimizer fails to process the mesh."""