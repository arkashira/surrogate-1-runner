"""
PDF ingestion helper.

* Extracts plain‑text from a PDF using **pdfminer.six**.
* Returns a self‑contained payload that can be sent downstream
  (e.g. to a vector‑store, a message queue, …).
* Guarantees that the caller never receives an uncaught exception –
  failures are logged and reported in the ``error`` field.
* Provides a tiny CLI so the module can be exercised directly from the
  command line (useful for debugging, ad‑hoc runs, or CI checks).

The implementation merges the strongest ideas from the two proposals:

* **Robust metadata** – ``ingestion_id``, ``filename``, ``path`` (absolute),
  ``filetype`` (derived from the actual suffix, lower‑cased) and the extracted
  ``text``.
* **Explicit error reporting** – an ``error`` key that is ``None`` on success
  and contains the exception string on failure.
* **Consistent logging** – a module‑level logger that records the full traceback
  at *ERROR* level.
* **Typed public API** – ``ingest_pdf`` returns ``Dict[str, Any]`` with clear
  type hints.
* **CLI entry point** – ``python -m ingestion.pdf_parser <path>`` prints a
  pretty‑printed JSON payload.
"""

from __future__ import annotations

import argparse
import json
import logging
import uuid
from pathlib import Path
from typing import Any, Dict

from pdfminer.high_level import extract_text

# --------------------------------------------------------------------------- #
# Logger configuration (the application that imports this module can
# re‑configure the root logger – we only set a sensible default handler).
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)
if not logger.handlers:                     # avoid duplicate handlers on reload
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s – %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def ingest_pdf(file_path: str) -> Dict[str, Any]:
    """
    Ingest a single PDF file.

    Parameters
    ----------
    file_path: str
        Path to the PDF file to be processed.

    Returns
    -------
    dict
        ``{
            "ingestion_id": <uuid str>,
            "filename":     <basename>,
            "path":         <absolute path>,
            "filetype":     <lower‑cased suffix, e.g. ".pdf">,
            "text":         <extracted plain‑text or empty string>,
            "error":        <None on success, otherwise error message>
        }``

    The function never raises – any exception raised by *pdfminer* or by the
    filesystem is caught, logged, and reflected in the ``error`` field.
    """
    # ------------------------------------------------------------------- #
    # Build the static part of the payload first – this guarantees that
    # callers always receive a dictionary with the same keys.
    # ------------------------------------------------------------------- #
    path_obj = Path(file_path).expanduser().resolve()
    ingestion_id = str(uuid.uuid4())

    result: Dict[str, Any] = {
        "ingestion_id": ingestion_id,
        "filename": path_obj.name,
        "path": str(path_obj),
        "filetype": path_obj.suffix.lower(),
        "text": "",
        "error": None,
    }

    # ------------------------------------------------------------------- #
    # Validate the input early – a missing file is a common user error.
    # ------------------------------------------------------------------- #
    if not path_obj.is_file():
        msg = f"File not found: {file_path}"
        logger.error(msg)
        result["error"] = msg
        return result

    # ------------------------------------------------------------------- #
    # Extract the text.  pdfminer may raise many different exceptions
    # (corrupt PDF, permission errors, etc.).  We swallow them so the
    # ingestion pipeline can continue processing other files.
    # ------------------------------------------------------------------- #
    try:
        extracted = extract_text(str(path_obj))
        result["text"] = extracted if extracted is not None else ""
    except Exception as exc:  # pylint: disable=broad-except
        logger.error(
            "Failed to ingest PDF %s (ingestion_id=%s): %s",
            file_path,
            ingestion_id,
            exc,
            exc_info=True,
        )
        result["error"] = str(exc)

    return result


# --------------------------------------------------------------------------- #
# Simple command‑line interface – useful for manual runs and CI smoke tests.
# --------------------------------------------------------------------------- #
def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF and emit a JSON payload."
    )
    parser.add_argument(
        "file",
        metavar="PDF_PATH",
        help="Path to the PDF file to ingest",
    )
    args = parser.parse_args()

    payload = ingest_pdf(args.file)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()