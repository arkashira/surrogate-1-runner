import io

CHUNK_SIZE = 64 * 1024  # 64 KB

class StreamParser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        result = []
        while True:
            chunk = self.stream.read(CHUNK_SIZE)
            if not chunk:
                break
            # Process the chunk here (for simplicity, just append it to the result)
            result.append(chunk)
        return b''.join(result)

def parse_stream(stream):
    parser = StreamParser(stream)
    return parser.parse()

def parse_string(data):
    stream = io.BytesIO(data.encode('utf-8'))
    return parse_stream(stream)