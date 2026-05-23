import gc
import contextlib
from typing import Iterator, Any, Optional

class Parser:
    def __init__(self):
        self.buffer = None
        self.temp_data = None
        self.parsed_result = None

    def parse_stream(self, stream) -> Any:
        """Parse a stream and ensure intermediate buffers are released."""
        try:
            # Initialize buffers
            self.buffer = bytearray(1024 * 1024)  # 1MB buffer
            self.temp_data = []
            
            # Process stream
            for chunk in stream:
                self.temp_data.append(chunk)
                # Simulate processing
                if len(self.temp_data) > 1000:
                    self._process_batch()
            
            # Finalize parsing
            self.parsed_result = self._finalize()
            
            return self.parsed_result
            
        finally:
            # Explicitly release resources
            self._cleanup()

    def _process_batch(self):
        """Process a batch of data."""
        # Simulate processing logic
        processed = [item.upper() for item in self.temp_data]
        self.temp_data.clear()
        del processed  # Explicit cleanup

    def _finalize(self) -> Any:
        """Finalize parsing and return result."""
        # Combine all data
        result = ''.join(self.temp_data)
        self.temp_data.clear()
        return result

    def _cleanup(self):
        """Explicitly clean up all intermediate buffers."""
        # Clear references to intermediate data
        if hasattr(self, 'buffer') and self.buffer is not None:
            self.buffer.clear()
            del self.buffer
            self.buffer = None
            
        if hasattr(self, 'temp_data') and self.temp_data is not None:
            self.temp_data.clear()
            del self.temp_data
            self.temp_data = None
            
        if hasattr(self, 'parsed_result'):
            del self.parsed_result
            self.parsed_result = None
            
        # Force garbage collection
        gc.collect()

@contextlib.contextmanager
def managed_parser() -> Iterator[Parser]:
    """Context manager for parser to ensure cleanup."""
    parser = Parser()
    try:
        yield parser
    finally:
        parser._cleanup()

def parse_with_context(stream) -> Any:
    """Parse using context manager for automatic cleanup."""
    with managed_parser() as parser:
        return parser.parse_stream(stream)