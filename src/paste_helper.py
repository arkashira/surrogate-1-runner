"""
paste_helper.py

Utility helpers for performing clipboard-paste operations during CI runs.

The module provides a thin wrapper around `subprocess.run` that:
  * Executes the supplied paste command (e.g. `pbpaste` on macOS).
  * Logs a warning if the command fails due to a timeout or a non-zero
    exit status.
  * Sets the environment variable `PASTE_CASCADE_DETECTED` to `"1"`
    when such a failure is observed, allowing downstream steps to react.

The implementation is deliberately lightweight and has no external
dependencies beyond the Python standard library.
"""

from __future__ import annotations

import logging
import os
import platform
import subprocess
from typing import List, Optional

# --------------------------------------------------------------------------- #
# Logging configuration – the caller (CI runner) is expected to configure the
# root logger.  We obtain a module-level logger for fine-grained control.
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
__all__ = ["run_paste", "PASTE_CASCADE_DETECTED"]


# The name of the environment flag that downstream steps watch.
PASTE_CASCADE_DETECTED = "PASTE_CASCADE_DETECTED"


def _set_cascade_flag() -> None:
    """
    Set the cascade-detected environment flag.

    The flag is set to the string `"1"` (truthy) and is added to the
    current process environment as well as `os.environ` so that any
    subsequently spawned subprocesses inherit it.
    """
    os.environ[PASTE_CASCADE_DETECTED] = "1"
    logger.debug("Environment flag %s set to '1'", PASTE_CASCADE_DETECTED)

def run_paste(
    command: List[str],
    *,
    timeout: Optional[int] = 30,
    capture_output: bool = True,
    check: bool = False,
) -> subprocess.CompletedProcess:
    """
    Execute a paste-related command and handle cascade errors.

    Parameters
    ----------
    command:
        The command to execute, expressed as a list of strings (e.g.
        `["pbpaste"]` on macOS).
    timeout:
        Maximum number of seconds to allow the command to run. `None` means
        no timeout. The default of 30 s matches the CI expectations.
    capture_output:
        If `True` (default), `stdout` and `stderr` are captured.
    check:
        If `True`, a non-zero return code raises `CalledProcessError`.
        The wrapper catches the exception to emit the cascade flag.

    Returns
    -------
    subprocess.CompletedProcess
        The result object from `subprocess.run`.  When a cascade error is
        detected, the `returncode` will be non-zero (or `-9` for a timeout).

    Side Effects
    ------------
    * Logs a warning when a timeout or error code is observed.
    * Sets the `PASTE_CASCADE_DETECTED` environment flag.
    """
    # Guard against running on unsupported platforms – the feature is only
    # required on macOS 12+ but we fail gracefully elsewhere.
    current_system = platform.system()
    if current_system != "Darwin":
        logger.debug(
            "paste_helper.run_paste called on non-macOS platform (%s); proceeding without cascade detection.",
            current_system,
        )
        # Still run the command; cascade detection is a macOS-specific concern.
        return subprocess.run(
            command,
            timeout=timeout,
            capture_output=capture_output,
            check=check,
            text=True,
        )

    try:
        logger.debug("Executing paste command: %s with timeout=%s", command, timeout)
        result = subprocess.run(
            command,
            timeout=timeout,
            capture_output=capture_output,
            check=check,
            text=True,
        )
        # If `check` is False we still need to treat non-zero exit codes as
        # cascade errors per the acceptance criteria.
        if result.returncode != 0:
            logger.warning(
                "Paste operation failed with exit code %s. Command: %s",
                result.returncode,
                command,
            )
            _set_cascade_flag()
        else:
            logger.debug("Paste operation succeeded. Command: %s", command)
        return result

    except subprocess.TimeoutExpired as exc:
        logger.warning(
            "Paste operation timed out after %s seconds. Command: %s",
            exc.timeout,
            command,
        )
        _set_cascade_flag()
        # Re-raise a CompletedProcess-like object for callers that expect it.
        return subprocess.CompletedProcess(
            args=exc.cmd,
            returncode=-9,  # Conventional code for timeout.
            stdout=exc.stdout,
            stderr=exc.stderr,
        )
    except subprocess.CalledProcessError as exc:
        # This block is only hit when `check=True`.
        logger.warning(
            "Paste operation raised CalledProcessError (exit %s). Command: %s",
            exc.returncode,
            command,
        )
        _set_cascade_flag()
        raise  # Preserve original semantics for callers that rely on the exception.