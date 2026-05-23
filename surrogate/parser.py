class StreamingParser:
    def parse_stream(self, stream):
        """
        Parse a stream of data.

        Args:
            stream: A file-like object representing the stream to parse.

        Returns:
            The parsed data.
        """
        data = stream.read()
        return self.parse(data)

    def parse(self, data):
        """
        Parse the given data.

        Args:
            data: The data to parse.

        Returns:
            The parsed data.

        Raises:
            ValueError: If the data is empty.
        """
        if not data:
            raise ValueError("Data cannot be empty")

        # Simulate parsing by converting bytes to string and adding a prefix
        parsed_data = 'parsed_' + data.decode('utf-8')
        return parsed_data