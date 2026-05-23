
import sys
import itertools
import threading
import time
import gc

BUFFER_SIZE = 50 * (1024 * 1024)  # 50MB

class StreamingParser:
    def __init__(self, data_stream):
        self.data_stream = data_stream
        self.buffer = b''
        self.lock = threading.Lock()

    def read_chunk(self):
        with self.lock:
            while len(self.buffer) < BUFFER_SIZE:
                chunk = self.data_stream.read(BUFFER_SIZE)
                if not chunk:
                    break
                self.buffer += chunk
            return self.buffer

    def process_chunk(self, chunk):
        # Process the chunk here
        pass

    def run(self):
        while True:
            chunk = self.read_chunk()
            if not chunk:
                break
            self.process_chunk(chunk)
            del chunk  # Free memory
            gc.collect()
            time.sleep(0.1)  # Throttle processing to avoid CPU spikes