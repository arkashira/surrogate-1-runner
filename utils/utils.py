import random
import string

def generate_large_data_stream(size):
    # Generate a large data stream
    for _ in range(size):
        yield random.choice(string.ascii_letters).encode('utf-8')