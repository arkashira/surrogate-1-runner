import json
import os
from pathlib import Path
from typing import List

from fastapi import UploadFile

class FileValidator:
    """
    Validates uploaded files for the Surrogate service.

    Rules
    -----
    * Extension must be in the allowed list.
    * File must not be empty.
    * `.tf.json` and `.json` files must contain valid JSON.
    """

    # Allowed extensions – case‑insensitive
    _ALLOWED_EXTENSIONS: set[str] = {
        ".tf",
        ".tf.json",
        ".yaml",
        ".yml",
        ".log",
        ".txt",
        ".json",
    }

    @classmethod
    def validate(cls, upload_file: UploadFile) -> None:
        """
        Raise ValueError if the file fails any rule.
        """
        filename = upload_file.filename
        _, ext = os.path.splitext(filename.lower())

        if ext not in cls._ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {ext}")

        # Read a small chunk to make sure the file is not empty.
        # We rewind afterwards so that the caller can read the file again.
        chunk = upload_file.file.read(1024)
        if not chunk:
            raise ValueError("File is empty")
        upload_file.file.seek(0)

        # JSON validation for .tf.json and .json files
        if ext in {".tf.json", ".json"}:
            try:
                json.load(upload_file.file)
                upload_file.file.seek(0)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON content: {exc}") from exc