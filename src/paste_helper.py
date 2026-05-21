import os
import logging
import threading
import time
from typing import Callable, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment flag used by downstream CI steps
PASTE_CASCADE_ENV_VAR = "PASTE_CASCADE_DETECTED"

class PasteTimeoutError(RuntimeError):
    """Raised when a paste operation exceeds the allowed time."""

def _run_with_timeout(func: Callable, timeout: float, *args, **kwargs) -> Any:
    """
    Executes ``func`` in a separate thread and raises :class:`PasteTimeoutError`
    if it does not complete within ``timeout`` seconds.

    This helper works on macOS 12+ where the GIL does not block native
    ``CGEvent``/``AX`` calls.
    """
    result = {}
    exc = {}

    def target():
        try:
            result["value"] = func(*args, **kwargs)
        except Exception as e:
            exc["error"] = e

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise PasteTimeoutError(f"Paste operation timed out after {timeout}s")
    if "error" in exc:
        raise exc["error"]
    return result.get("value")

def detect_paste_cascade_error(ax_call_result, cg_event_result):
    """
    Detects paste cascade errors based on the results of AX and CGEvent calls.
    
    Args:
    ax_call_result (dict): The result of the AX call.
    cg_event_result (dict): The result of the CGEvent call.
    
    Returns:
    bool: True if a paste cascade error is detected, False otherwise.
    """
    if ax_call_result.get('error_code') or cg_event_result.get('error_code'):
        return True
    if ax_call_result.get('timeout') or cg_event_result.get('timeout'):
        return True
    return False

def log_warning_and_set_flag(error_message):
    """
    Logs a warning message and sets the PASTE_CASCADE_DETECTED flag in the environment.
    
    Args:
    error_message (str): The error message to log.
    """
    logger.warning(error_message)
    os.environ[PASTE_CASCADE_ENV_VAR] = '1'

def detect_paste_cascade(func: Callable, timeout: float = 5.0, *args, **kwargs) -> Any:
    """
    Wrapper for AX or CGEvent paste calls.

    - Executes ``func`` with a timeout.
    - On timeout or any exception, logs a warning and sets the
      ``PASTE_CASCADE_DETECTED`` environment variable.
    - Returns the original function's result on success.

    This function is intended to be used in CI pipelines where a paste
    cascade (e.g., repeated failures) should abort further steps.
    """
    try:
        return _run_with_timeout(func, timeout, *args, **kwargs)
    except (PasteTimeoutError, Exception) as e:
        logger.warning("Paste cascade detected: %s", e)
        os.environ[PASTE_CASCADE_ENV_VAR] = '1'
        # Re-raise to allow callers to handle the failure if they wish
        raise

def ax_paste(*args, **kwargs):
    """
    Perform a paste using the Accessibility (AX) API.
    This function is wrapped with ``detect_paste_cascade`` to provide
    robust error handling.
    """
    from .ax_interface import perform_ax_paste  # local module providing the real call
    return detect_paste_cascade(perform_ax_paste, *args, **kwargs)

def cg_event_paste(*args, **kwargs):
    """
    Perform a paste using the CoreGraphics (CGEvent) API.
    Wrapped with ``detect_paste_cascade``.
    """
    from .cg_event_interface import perform_cg_event_paste
    return detect_paste_cascade(perform_cg_event_paste, *args, **kwargs)

def wrap_paste_call(ax_call, cg_event_call):
    """
    Wraps the paste call with error detection and logging.
    
    Args:
    ax_call (function): The AX call function.
    cg_event_call (function): The CGEvent call function.
    
    Returns:
    tuple: The results of the AX and CGEvent calls.
    """
    ax_call_result = ax_call()
    cg_event_result = cg_event_call()
    if detect_paste_cascade_error(ax_call_result, cg_event_result):
        log_warning_and_set_flag('Paste cascade error detected')
    return ax_call_result, cg_event_result