import unittest
from config.chunk_config import create_chunk_config

class TestChunkConfig(unittest.TestCase):
    def test_create_chunk_config(self):
        chunk_size = 1024
        chunk_config = create_chunk_config(chunk_size)
        self.assertEqual(chunk_config.get_chunk_size(), chunk_size)

    def test_default_chunk_size(self):
        chunk_config = create_chunk_config(1024)
        self.assertEqual(chunk_config.get_chunk_size(), 1024)

if __name__ == "__main__":
    unittest.main()