import logging
import os
import shutil
from pathlib import Path
from typing import Set

# Configure a module‑level logger. The application may configure logging globally;
# this ensures a logger is always available.
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class DocumentValidator:
    """
    Validates document formats (PDF, DOCX, TXT) and stores them in a temporary
    processing directory.

    Usage:
        validator = DocumentValidator()
        success = validator.validate_and_store(source_path, temp_dir)
    """

    _ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".txt"}

    @classmethod
    def is_supported(cls, file_path: Path) -> bool:
        """Return True if the file has a supported extension."""
        ext = file_path.suffix.lower()
        return ext in cls._ALLOWED_EXTENSIONS

    @classmethod
    def validate(cls, file_path: Path) -> bool:
        """
        Validate that the file exists and has a supported extension.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not file_path.is_file():
            logger.error("File does not exist: %s", file_path)
            return False

        if not cls.is_supported(file_path):
            logger.error(
                "Unsupported file format for %s. Allowed: %s",
                file_path,
                ", ".join(sorted(cls._ALLOWED_EXTENSIONS)),
            )
            return False

        logger.info("File %s passed format validation.", file_path)
        return True

    @classmethod
    def store(cls, file_path: Path, temp_dir: Path) -> Path:
        """
        Copy the validated file into the temporary directory.

        Returns:
            Path: Destination path of the copied file.
        """
        temp_dir.mkdir(parents=True, exist_ok=True)
        destination = temp_dir / file_path.name
        shutil.copy2(file_path, destination)
        logger.info("Stored %s in temporary directory %s.", file_path, temp_dir)
        return destination

    @classmethod
    def validate_and_store(cls, source_path: str, temp_dir: str) -> bool:
        """
        Full pipeline: validate the document and, if valid, copy it to the
        temporary processing directory.

        Args:
            source_path (str): Path to the source document.
            temp_dir (str): Path to the temporary directory.

        Returns:
            bool: True if the document was validated and stored successfully,
                  False otherwise.
        """
        src = Path(source_path)
        dst_dir = Path(temp_dir)

        if not cls.validate(src):
            return False

        try:
            cls.store(src, dst_dir)
            return True
        except Exception as exc:  # pragma: no cover – defensive logging
            logger.error("Failed to store %s in %s: %s", src, dst_dir, exc)
            return False


__all__ = ["DocumentValidator"]