"""
A minimal guide resolution module that demonstrates how to use the
`guide_logger` to record usage events.

In a real system this module would contain the logic for resolving
guides.  For the purposes of this PR we provide a simple
`resolve_guide` function that randomly succeeds or fails and logs the
event using `guide_logger.log_guide_usage`.
"""

import random
from typing import Dict, Any

from .guide_logger import log_guide_usage


def resolve_guide(guide_id: str, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulate the resolution of a guide.

    Parameters
    ----------
    guide_id : str
        Identifier of the guide to resolve.
    user_id : str
        Identifier of the user invoking the guide.
    payload : dict
        Arbitrary data passed to the guide.

    Returns
    -------
    dict
        Result of the resolution.  On success the dict contains a
        ``result`` key; on failure it contains an ``error`` key.
    """
    # Simulate a 80% success rate
    success = random.random() < 0.8

    if success:
        result = {"result": f"Guide {guide_id} resolved successfully."}
        log_guide_usage(
            guide_id=guide_id,
            user_id=user_id,
            outcome="success",
            details={"payload": payload},
        )
        return result
    else:
        error = {"error": f"Guide {guide_id} failed to resolve."}
        log_guide_usage(
            guide_id=guide_id,
            user_id=user_id,
            outcome="failure",
            details={"payload": payload, "error": error},
        )
        return error