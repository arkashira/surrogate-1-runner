from surrogate.parser import Parser

# Initialize the parser
parser = Parser()

# Configure the parser
parser.config = {
    'streaming_enabled': True,
    'batch_size': 1000,
    'fallback_to_batch': True
}

# Process data
data = parser.process('path/to/data/file')