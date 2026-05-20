import unittest
from embedding import EmbeddingGenerator

class TestEmbeddingGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = EmbeddingGenerator(model_name="test-model", vector_store_path="test_vector_store.txt")

    def tearDown(self):
        import os
        if os.path.exists("test_vector_store.txt"):
            os.remove("test_vector_store.txt")

    def test_generate_embeddings(self):
        document_chunks = ["chunk1", "chunk2"]
        embeddings = self.generator.generate_embeddings(document_chunks)
        self.assertEqual(len(embeddings), len(document_chunks))
        with open("test_vector_store.txt", 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), len(document_chunks))

if __name__ == "__main__":
    unittest.main()