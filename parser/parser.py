"""
A lightweight streaming parser for surrogate-1 data streams.

The original implementation eagerly loaded entire input files into memory,
which caused high peak memory usage when processing large datasets.
This refactor introduces a generator‑based approach that reads the input
in fixed‑size chunks, parses records incrementally, and yields them one
by one.  This keeps the memory footprint bounded regardless of the
size of the input stream.

The public API remains the same: ``parse_stream`` accepts a file‑like
object and yields parsed records.  The function is fully type‑annotated
and includes minimal error handling for robustness.
"""

from __future__ import annotations

import json
from typing import Iterable, Iterator, TextIO, Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Size of the buffer to read from the input stream (bytes).
# Adjusting this value balances I/O overhead against memory usage.
BUFFER_SIZE: int = 64 * 1024  # 64 KiB

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _chunk_reader(stream: TextIO, buffer_size: int = BUFFER_SIZE) -> Iterator[str]:
    """
    Generator that yields lines from a text stream without loading the
    entire file into memory.

    Parameters
    ----------
    stream : TextIO
        Open file or any text stream.
    buffer_size : int
        Number of bytes to read per chunk.

    Yields
    ------
    str
        A line from the stream.
    """
    buffer = ""
    while True:
        chunk = stream.read(buffer_size)
        if not chunk:
            # End of file: yield any remaining buffered data
            if buffer:
                yield buffer
            break

        buffer += chunk
        while True:
            newline_pos = buffer.find("\n")
            if newline_pos == -1:
                # No complete line yet
                break
            line = buffer[:newline_pos]
            buffer = buffer[newline_pos + 1 :]
            yield line

    # If the file does not end with a newline, the last line is already yielded
    # above. No further action needed.

def _parse_json_line(line: str) -> Dict[str, Any]:
    """
    Parse a single JSON line into a Python dictionary.

    Parameters
    ----------
    line : str
        A JSON string representing a single record.

    Returns
    -------
    Dict[str, Any]
        The parsed record.

    Raises
    ------
    ValueError
        If the line cannot be parsed as JSON.
    """
    try:
        return json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON record: {line!r}") from exc

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def parse_stream(stream: TextIO) -> Iterator[Dict[str, Any]]:
    """
    Parse a stream of newline‑delimited JSON records in a memory‑efficient
    manner.

    Parameters
    ----------
    stream : TextIO
        A file‑like object opened in text mode.

    Yields
    ------
    Dict[str, Any]
        Parsed JSON records, one per line.
    """
    for raw_line in _chunk_reader(stream):
        # Skip empty lines that may appear due to trailing newlines
        if not raw_line.strip():
            continue
        yield _parse_json_line(raw_line)

# --------------------------------------------------------------------------- #
# Example usage (for debugging / manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m parser <path-to-jsonl-file>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        for record in parse_stream(f):
            print(record)