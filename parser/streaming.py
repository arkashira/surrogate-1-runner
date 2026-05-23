"""
Streaming parser utilities for surrogate-1.

This module provides lightweight, memory-efficient parsing helpers that
operate on file-like objects or file paths.  The functions are designed
to process arbitrarily large data streams without loading the entire
payload into memory, thereby preventing OOM crashes even for >500 MB
inputs.

The API is intentionally minimal and generic:

* :func:`parse_stream` – dispatcher that selects the appropriate parser
  based on the ``parser_type`` argument.

All functions return generators; the caller can iterate over them
directly or convert to a list if the data set is small.
"""

import asyncio
import json
import csv
from pathlib import Path
from typing import Iterable, Dict, Generator, Union, TextIO, Optional

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _open_file(file: Union[str, Path, TextIO]) -> TextIO:
    """
    Return a text file object.

    Parameters
    ----------
    file
        Either a file path (str/Path) or an already opened file object.

    Returns
    -------
    TextIO
        Text mode file object ready for reading.
    """
    if isinstance(file, (str, Path)):
        return open(file, mode="r", encoding="utf-8")
    # Assume file-like object
    return file

# --------------------------------------------------------------------------- #
# Streaming parsers
# --------------------------------------------------------------------------- #

class StreamingParser:
    def __init__(self, chunk_size: int = 8192):
        self.chunk_size = chunk_size

    async def parse_stream(self, stream: Iterable[bytes], parser_type: str) -> Generator[Dict, None, None]:
        """
        Stream a data file.

        Parameters
        ----------
        stream
            An iterable of bytes.
        parser_type
            One of ``"jsonl"`` or ``"csv"``.

        Yields
        ------
        dict
            Parsed record for each chunk.
        """
        if parser_type == "jsonl":
            return self._parse_json_lines(stream, chunk_size=self.chunk_size)
        elif parser_type == "csv":
            return self._parse_csv(stream, chunk_size=self.chunk_size)
        else:
            raise ValueError(f"Unsupported parser_type: {parser_type!r}")

    def _parse_json_lines(self, stream: Iterable[bytes], chunk_size: int) -> Generator[Dict, None, None]:
        """
        Stream a JSON Lines (JSONL) file.

        Parameters
        ----------
        stream
            An iterable of bytes.
        chunk_size
            Number of bytes to read per ``read`` call.

        Yields
        ------
        dict
            Parsed JSON object for each line.
        """
        buffer = ""
        for chunk in stream:
            buffer += chunk
            # Split on newline boundaries
            lines = buffer.splitlines(True)  # keepends=True to preserve last incomplete line
            # All complete lines except the last (which may be incomplete)
            for line in lines[:-1]:
                yield json.loads(line.strip())
            # Keep the last incomplete line in buffer
            buffer = lines[-1]

    def _parse_csv(self, stream: Iterable[bytes], chunk_size: int) -> Generator[Dict, None, None]:
        """
        Stream a CSV file.

        Parameters
        ----------
        stream
            An iterable of bytes.
        chunk_size
            Number of bytes to read per ``read`` call.

        Yields
        ------
        dict
            Mapping of column names to values for each row.
        """
        buffer = ""
        for chunk in stream:
            buffer += chunk
            # Split on newline boundaries
            lines = buffer.splitlines(True)  # keepends=True to preserve last incomplete line
            # All complete lines except the last (which may be incomplete)
            for line in lines[:-1]:
                yield dict(csv.DictReader([line.strip().split(",")]))
            # Keep the last incomplete line in buffer
            buffer = lines[-1]

# --------------------------------------------------------------------------- #
# Dispatcher
# --------------------------------------------------------------------------- #

async def parse_stream_async(
    file: Union[str, Path, TextIO],
    *,
    parser_type: str = "jsonl",
    **kwargs,
) -> Generator[Dict, None, None]:
    """
    Dispatch to the appropriate streaming parser.

    Parameters
    ----------
    file
        Path or file-like object.
    parser_type
        One of ``"jsonl"`` or ``"csv"``.
    **kwargs
        Additional keyword arguments forwarded to the underlying parser.

    Returns
    -------
    Generator[Dict, None, None]
        Generator yielding parsed records.
    """
    parser_type = parser_type.lower()
    if parser_type == "jsonl":
        return StreamingParser().parse_stream(file, parser_type, **kwargs)
    elif parser_type == "csv":
        return StreamingParser().parse_stream(file, parser_type, **kwargs)
    raise ValueError(f"Unsupported parser_type: {parser_type!r}")

# --------------------------------------------------------------------------- #
# Example usage (uncomment to run as a script)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python -m parser.streaming <file> <parser_type>")
        sys.exit(1)

    file_path = sys.argv[1]
    parser_type = sys.argv[2]

    async def main():
        async with open(file_path, mode="rb") as file:
            async for result in parse_stream_async(file, parser_type=parser_type):
                print(result)

    asyncio.run(main())