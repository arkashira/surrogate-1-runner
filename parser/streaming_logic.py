import io
import json
from typing import Generator

class StreamingParser:
    def __init__(self, chunk_size: int = 1024):
        self.chunk_size = chunk_size

    def parse_stream(self, stream: io.IOBase) -> Generator[dict, None, None]:
        buffer = b''
        while True:
            chunk = stream.read(self.chunk_size)
            if not chunk:
                if buffer:
                    yield self.parse_buffer(buffer)
                break
            buffer += chunk
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                yield self.parse_line(line)

    def parse_line(self, line: bytes) -> dict:
        try:
            return json.loads(line.decode('utf-8'))
        except json.JSONDecodeError:
            return {}

    def parse_buffer(self, buffer: bytes) -> dict:
        try:
            return json.loads(buffer.decode('utf-8'))
        except json.JSONDecodeError:
            return {}