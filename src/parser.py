import gc

class Parser:
    def __init__(self):
        self.buffer = []

    def parse_stream(self, stream):
        for chunk in self._generate_chunks(stream):
            # Process each chunk here
            print(f"Processing chunk: {chunk}")
        
        # Ensure garbage collection is triggered promptly
        gc.collect()

    def _generate_chunks(self, stream):
        chunk_size = 1024 * 1024  # 1 MB chunks
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            yield chunk
            del chunk  # Explicitly delete reference to chunk

# Test cases
def test_parser():
    import io
    test_data = b'a' * (1024 * 1024 * 1024)  # 1 GB data
    stream = io.BytesIO(test_data)
    
    parser = Parser()
    parser.parse_stream(stream)

    # Check memory usage and ensure it's below 200 MB
    import psutil
    process = psutil.Process()
    mem_info = process.memory_info()
    assert mem_info.rss < 200 * 1024 * 1024, "Memory usage exceeds 200 MB"

test_parser()