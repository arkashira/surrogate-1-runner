import os
import tempfile
import unittest
from src.parser.chunk_loader import ChunkLoader

class TestChunkLoader(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'a' * 1024 * 1024 * 10)  # 10MB文件
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_chunk_loader(self):
        loader = ChunkLoader(self.temp_file.name, chunk_size=1024*1024)
        chunks = list(loader.load_chunks())
        self.assertEqual(len(chunks), 10)
        self.assertEqual(len(chunks[0]), 1024*1024)
        self.assertEqual(len(chunks[-1]), 1024*1024)

    def test_get_chunk_count(self):
        loader = ChunkLoader(self.temp_file.name, chunk_size=1024*1024)
        self.assertEqual(loader.get_chunk_count(), 10)