from .error_handler import ErrorHandler

class StreamingBuffer:
    def __init__(self):
        self.error_handler = ErrorHandler()

    def process_chunk(self, chunk_data, chunk_index):
        try:
            # Simulate chunk processing
            self._process(chunk_data)
        except Exception as e:
            self.error_handler.handle_error(e, chunk_data, chunk_index)

    def _process(self, chunk_data):
        # Placeholder for actual chunk processing logic
        pass