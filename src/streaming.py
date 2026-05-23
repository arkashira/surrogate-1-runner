import io

class StreamBuffer(io.IOBase):
    def __init__(self, chunk_size=1024 * 1024):
        self.chunk_size = chunk_size
        self.buffer = b''
        self.closed = False

    def write(self, data):
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        self.buffer += data
        while len(self.buffer) >= self.chunk_size:
            yield self.buffer[:self.chunk_size]
            self.buffer = self.buffer[self.chunk_size:]

    def close(self):
        self.closed = True
        if self.buffer:
            yield self.buffer
        self.buffer = b''