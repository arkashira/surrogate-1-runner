class MemoryManager:
    def __init__(self):
        self.buffer_size = 1024 * 1024  # 1MB buffer size

    def stream_chunks(self, data_stream):
        while True:
            chunk = data_stream.read(self.buffer_size)
            if not chunk:
                break
            yield chunk