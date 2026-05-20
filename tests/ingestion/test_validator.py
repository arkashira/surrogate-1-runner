import os
import tempfile
from pathlib import Path

import pytest

from ingestion.validator import DocumentValidator


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def create_file():
    def _make(suffix: str, content: str = "test"):
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return Path(path)

    return _make


def test_valid_pdf_is_stored(create_file, temp_dir):
    src = create_file(".pdf")
    result = DocumentValidator.validate_and_store(str(src), str(temp_dir))
    assert result is True
    assert (temp_dir / src.name).exists()


def test_valid_docx_is_stored(create_file, temp_dir):
    src = create_file(".docx")
    result = DocumentValidator.validate_and_store(str(src), str(temp_dir))
    assert result is True
    assert (temp_dir / src.name).exists()


def test_valid_txt_is_stored(create_file, temp_dir):
    src = create_file(".txt")
    result = DocumentValidator.validate_and_store(str(src), str(temp_dir))
    assert result is True
    assert (temp_dir / src.name).exists()


def test_unsupported_extension_is_rejected(create_file, temp_dir):
    src = create_file(".png")
    result = DocumentValidator.validate_and_store(str(src), str(temp_dir))
    assert result is False
    assert not (temp_dir / src.name).exists()


def test_nonexistent_file_is_rejected(temp_dir):
    src = Path("/nonexistent/file.pdf")
    result = DocumentValidator.validate_and_store(str(src), str(temp_dir))
    assert result is False