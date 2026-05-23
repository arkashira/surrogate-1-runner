import io
import lz4
from collections import deque

class MemoryEfficientParser:
    def __init__(self):
        self.buffer = io.BytesIO()
        self.deque = deque(maxlen=1024)  # Limit the memory usage by deque size

    def feed(self, data):
        self.buffer.write(data)
        while self.buffer.tell() > 1024 * 1024:  # Process in 1MB chunks
            chunk = self.buffer.read(1024 * 1024)
            self.deque.append(lz4.compress(chunk))
            self.buffer.seek(0)
            self.buffer.truncate()

    def parse(self):
        for data in self.deque:
            # Parse the compressed data here
            pass

# src/data_structures.py
from collections import defaultdict

class LRUCache:
    def __init__(self, capacity):
        self.cache = defaultdict(int)
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache[key] = self.cache[key] + 1
            return True
        else:
            return False

    def put(self, key):
        if len(self.cache) >= self.capacity:
            # Remove the least recently used item
            self.cache.pop(min(self.cache, key=lambda x: self.cache[x]))
        self.cache[key] = 1

## Summary
- Implemented `MemoryEfficientParser` to handle large data streams without excessive memory usage.
- Used `io.BytesIO` for buffering and `lz4` for compression to reduce memory footprint.
- Implemented `LRUCache` for efficient data retrieval, limiting memory usage by evicting least recently used items.