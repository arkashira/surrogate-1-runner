import time
import logging
from functools import wraps
from typing import Callable, Iterable, Tuple, Type

# Configure a module level logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

def retry(
    max_attempts: int = 5,
    backoff_factor: float = 1.0,
    retry_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    on_failure: Callable[[Callable, Exception, int], None] | None = None,
) -> Callable:
    """
    Decorator that retries a function call with exponential backoff.

    Parameters
    ----------
    max_attempts : int
        Maximum number of attempts (including the first try). Default is 5.
    backoff_factor : float
        Initial delay in seconds. Each subsequent retry doubles the delay.
        Default is 1.0.
    retry_exceptions : tuple[Type[BaseException], ...]
        Exceptions that trigger a retry. Default is all Exceptions.
    on_failure : Callable[[Callable, Exception, int], None] | None
        Optional callback invoked after the final failure. It receives the
        original function, the exception raised, and the attempt count.
        If not provided, the failure is simply logged.

    Returns
    -------
    Callable
        Wrapped function with retry logic.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = backoff_factor
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as exc:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(
                            f"Function {func.__name__!r} failed after {attempts} attempts: {exc}"
                        )
                        if on_failure:
                            on_failure(func, exc, attempts)
                        raise
                    logger.warning(
                        f"Attempt {attempts} failed for {func.__name__!r}: {exc}. "
                        f"Retrying in {delay}s (attempt {attempts + 1}/{max_attempts})"
                    )
                    time.sleep(delay)
                    delay *= 2
        return wrapper
    return decorator