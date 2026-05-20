class ChunkConfig:
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def get_chunk_size(self):
        return self.chunk_size

def create_chunk_config(chunk_size):
    return ChunkConfig(chunk_size)

def main():
    chunk_size = 1024  # default chunk size
    chunk_config = create_chunk_config(chunk_size)
    print(f"Chunk size: {chunk_config.get_chunk_size()}")

if __name__ == "__main__":
    main()