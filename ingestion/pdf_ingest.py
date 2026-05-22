"""
PDF ingestion module for surrogate-1.

This module provides a single public function :func:`ingest_pdf` which
extracts the textual content from a PDF file and writes it to a
`.txt` file in a user‑specified output directory.  The function
returns the path to the created text file.

The implementation uses :mod:`pdfminer.six` which is available in the
surrogate-1 runtime.  If the extraction fails for any reason, a
``PDFIngestError`` is raised with a helpful message.

Example
-------
>>> ingest_pdf("sample.pdf", "/tmp/output")
'/tmp/output/sample.txt'
"""

from __future__ import annotations

import os
import pathlib
from typing import Union

# pdfminer is a heavy dependency; import lazily to keep import time low.
try:
    from pdfminer.high_level import extract_text
except Exception as exc:  # pragma: no cover
    # If pdfminer is not available, we raise a clear error when the
    # function is called.
    extract_text = None  # type: ignore


class PDFIngestError(RuntimeError):
    """Raised when PDF ingestion fails."""


def ingest_pdf(
    pdf_path: Union[str, pathlib.Path],
    output_dir: Union[str, pathlib.Path],
    *,
    encoding: str = "utf-8",
) -> pathlib.Path:
    """
    Extract text from a PDF file and write it to a `.txt` file.

    Parameters
    ----------
    pdf_path : str | pathlib.Path
        Path to the source PDF file.
    output_dir : str | pathlib.Path
        Directory where the extracted text file will be written.
    encoding : str, optional
        Text encoding used when writing the output file.  Defaults to
        ``"utf-8"``.

    Returns
    -------
    pathlib.Path
        Absolute path to the created text file.

    Raises
    ------
    PDFIngestError
        If the PDF cannot be read or the output cannot be written.
    FileNotFoundError
        If ``pdf_path`` does not exist.
    ValueError
        If ``pdf_path`` is not a file or does not have a ``.pdf`` extension.
    """
    pdf_path = pathlib.Path(pdf_path).expanduser().resolve()
    output_dir = pathlib.Path(output_dir).expanduser().resolve()

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {pdf_path.suffix}")

    if extract_text is None:
        raise PDFIngestError(
            "pdfminer.six is not available in the environment. "
            "Please install it with `pip install pdfminer.six`."
        )

    try:
        text = extract_text(str(pdf_path))
    except Exception as exc:  # pragma: no cover
        raise PDFIngestError(f"Failed to extract text from {pdf_path}: {exc}") from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    txt_path = output_dir / f"{pdf_path.stem}.txt"

    try:
        txt_path.write_text(text, encoding=encoding)
    except Exception as exc:  # pragma: no cover
        raise PDFIngestError(f"Failed to write text file {txt_path}: {exc}") from exc

    return txt_path


if __name__ == "__main__":  # pragma: no cover
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Ingest a PDF to text.")
    parser.add_argument("pdf", help="Path to the PDF file.")
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        help="Directory to write the extracted text file.",
    )
    parser.add_argument(
        "-e",
        "--encoding",
        default="utf-8",
        help="Encoding for the output text file.",
    )
    args = parser.parse_args()

    try:
        txt_file = ingest_pdf(args.pdf, args.output, encoding=args.encoding)
        print(f"Extracted text written to: {txt_file}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)