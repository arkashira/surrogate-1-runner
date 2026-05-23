from .streaming import StreamBuffer

class Parser:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def parse(self):
        stream_buffer = StreamBuffer()
        for chunk in self.input_stream:
            for sub_chunk in stream_buffer.write(chunk):
                # Process each sub_chunk here
                print(f"Parsing chunk: {sub_chunk}")
        stream_buffer.close()
        for remaining in stream_buffer:
            print(f"Parsing remaining: {remaining}")

# Example usage
if __name__ == "__main__":
    # Simulate a large input stream
    large_input = io.BytesIO(b'x' * 10 * 1024 * 1024 * 1024)  # 10GB of 'x'
    parser = Parser(large_input)
    parser.parse()