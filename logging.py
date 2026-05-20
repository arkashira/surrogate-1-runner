# Add to imports
import sys

# In launch_freerouter, add exit code capture:
def launch_freerouter(command: list[str]) -> subprocess.CompletedProcess:
    java_version = _get_java_version()
    try:
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=300  # Add 5-minute timeout to prevent hangs
        )
        return result
    except subprocess.TimeoutExpired as exc:
        _log_error(
            exc,
            error_code="FREEROUTER_TIMEOUT",
            java_version=java_version,
            extra={"command": command, "timeout": 300}
        )
        raise
    except Exception as exc:
        exit_code = exc.returncode if hasattr(exc, 'returncode') else -1
        _log_error(
            exc,
            error_code="FREEROUTER_LAUNCH_FAILED",
            java_version=java_version,
            extra={"command": command, "exit_code": exit_code}
        )
        raise

# Add log rotation to prevent disk full issues:
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    LOG_FILE, 
    maxBytes=10_000_000,  # 10MB
    backupCount=5,
    encoding="utf-8"
)