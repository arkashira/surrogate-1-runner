import os
import shutil
import logging
from datetime import datetime
from pathlib import Path

# Configure logging to write to a specific file with timestamp format
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_FILE = "/var/log/axentx/filesystem.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Define custom exceptions
class SourceNotFoundError(Exception):
    """Raised when the source file does not exist."""
    pass

class DestinationNotWritableError(Exception):
    """Raised when the destination directory is not writable."""
    pass

class PermissionError(Exception):
    """Raised when a permission issue occurs."""
    pass


def _validate_source_and_destination(source_path: Path, dest_path: Path) -> None:
    """Validate source existence and destination writability."""
    if not source_path.exists():
        raise SourceNotFoundError(f"Source path does not exist: {source_path.resolve()}")
    
    dest_dir = dest_path.parent
    if not dest_dir.exists():
        try:
            os.makedirs(dest_dir, exist_ok=True)
            logging.info(f"Created destination directory: {dest_dir.resolve()}")
        except PermissionError as e:
            raise PermissionError(f"Cannot create destination directory {dest_dir.resolve()}: {str(e)}")
    
    if not os.access(dest_dir, os.W_OK):
        raise DestinationNotWritableError(f"Destination directory not writable: {dest_dir.resolve()}")


def copy_file(source_path: Path, dest_path: Path, mode: int = 0o644) -> None:
    """Copy file with validation, permissions, and logging."""
    try:
        _validate_source_and_destination(source_path, dest_path)
        
        shutil.copy2(source_path.resolve(), dest_path.resolve())
        os.chmod(dest_path.resolve(), mode)
        
        logging.info(
            f"Copied {source_path.resolve()} -> {dest_path.resolve()} (mode: {oct(mode)})"
        )
    except Exception as e:
        logging.error(f"Copy failed {source_path.resolve()} -> {dest_path.resolve()}: {str(e)}")
        raise


def move_file(source_path: Path, dest_path: Path, mode: int = 0o644) -> None:
    """Move file with validation, permissions, and logging."""
    try:
        _validate_source_and_destination(source_path, dest_path)
        
        shutil.move(source_path.resolve(), dest_path.resolve())
        os.chmod(dest_path.resolve(), mode)
        
        logging.info(
            f"Moved {source_path.resolve()} -> {dest_path.resolve()} (mode: {oct(mode)})"
        )
    except Exception as e:
        logging.error(f"Move failed {source_path.resolve()} -> {dest_path.resolve()}: {str(e)}")
        raise