"""Optimized streaming JSON parser for large files and infinite streams.

Features:
- Incremental parsing with minimal memory overhead
- Reusable decoder and buffer for efficient processing
- Support for top-level JSON arrays and line-delimited JSON
- Memory-safe operation for files ≥1 GB
- Performance-optimized with tuned chunk sizes
"""

import json
from typing import Iterator, Dict, Any, TextIO, Callable

# Constants
CHUNK_SIZE = 64 * 1024  # 64 KiB per read (tuned for typical SSD I/O)

class StreamingJSONParser:
    """Streaming JSON parser with support for both array and line-delimited formats."""

    def __init__(self, decoder: json.JSONDecoder | None = None):
        """Initialize parser with optional custom decoder."""
        self.decoder = decoder or json.JSONDecoder()
        self._buffer = ""

    def _feed(self, data: str) -> None:
        """Append new data to the internal buffer."""
        self._buffer += data

    def _skip_whitespace(self) -> None:
        """Remove leading whitespace from the buffer."""
        self._buffer = self._buffer.lstrip()

    def _consume(self, n: int) -> None:
        """Remove the first `n` characters from the buffer."""
        self._buffer = self._buffer[n:]

    def _parse_next(self) -> Any | None:
        """Attempt to parse the next JSON value from the buffer."""
        self._skip_whitespace()
        if not self._buffer:
            return None

        try:
            obj, idx = self.decoder.raw_decode(self._buffer)
            self._consume(idx)
            return obj
        except json.JSONDecodeError:
            return None

    def parse_array(self, stream: TextIO) -> Iterator[Any]:
        """Parse a top-level JSON array from the stream."""
        # Read the opening '['
        while True:
            chunk = stream.read(CHUNK_SIZE)
            if not chunk:
                raise ValueError("Unexpected EOF while searching for '['")
            self._feed(chunk)
            self._skip_whitespace()
            if self._buffer.startswith('['):
                self._consume(1)
                break

        # Parse array elements
        while True:
            self._skip_whitespace()
            if self._buffer.startswith(']'):
                self._consume(1)
                break

            if not self._buffer:
                chunk = stream.read(CHUNK_SIZE)
                if not chunk:
                    raise ValueError("Unexpected EOF while parsing array")
                self._feed(chunk)

            obj = self._parse_next()
            if obj is None:
                continue
            yield obj

    def parse_lines(self, stream: TextIO) -> Iterator[Dict[str, Any]]:
        """Parse line-delimited JSON from the stream."""
        for line in stream:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

    def parse(self, stream: TextIO, format: str = 'array') -> Iterator[Any]:
        """Parse JSON stream in specified format.

        Args:
            stream: File-like object opened in text mode
            format: 'array' for JSON arrays or 'lines' for line-delimited JSON

        Yields:
            Parsed JSON objects one at a time
        """
        if format == 'array':
            yield from self.parse_array(stream)
        elif format == 'lines':
            yield from self.parse_lines(stream)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def for_each(self, stream: TextIO, callback: Callable[[Any], None], format: str = 'array') -> None:
        """Convenience method to apply callback to each parsed object."""
        for obj in self.parse(stream, format):
            callback(obj)