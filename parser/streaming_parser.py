import sys
import io

class StreamingParser:
    def __init__(self):
        self.memory_usage = 0

    def process(self, data_stream):
        # Process the data stream in chunks to avoid OOM crashes
        chunk_size = 1024 * 1024  # 1 MB
        chunk = io.BytesIO()
        for data in data_stream:
            chunk.write(data)
            if chunk.tell() >= chunk_size:
                self._process_chunk(chunk)
                chunk.seek(0)
                chunk.truncate()
        if chunk.tell() > 0:
            self._process_chunk(chunk)

    def _process_chunk(self, chunk):
        # Process the chunk
        chunk.seek(0)
        data = chunk.read()
        # Simulate processing time
        import time
        time.sleep(0.01)
        self.memory_usage += sys.getsizeof(data)

    def get_memory_usage(self):
        return self.memory_usage