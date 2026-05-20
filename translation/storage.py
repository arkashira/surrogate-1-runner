"""
Simple storage abstraction.

In production you would replace the `store` function with a database
insert, a message‑queue publish, or any other persistence mechanism.
"""

import logging
from typing import Dict, Callable

logger = logging.getLogger(__name__)

def store_translation(data: Dict, store_fn: Callable[[Dict], None]) -> None:
    """
    Persist a translation record.

    Parameters
    ----------
    data : dict
        Dictionary containing at least:
        - original_text
        - translated_text
        - language
    store_fn : Callable[[dict], None]
        Function that actually writes the data somewhere.
    """
    try:
        store_fn(data)
    except Exception as exc:
        logger.exception("Failed to store translation: %s", exc)