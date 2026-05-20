import unittest
from embedding.optimizer import EmbeddingOptimizer

class TestEmbeddingOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = EmbeddingOptimizer()

    def test_optimize_embeddings(self):
        documents = ["Document 1", "Document 2", "Document 3"] * 10
        optimized_embeddings = self.optimizer.optimize_embeddings(documents)
        self.assertEqual(len(optimized_embeddings), len(documents))

    def test_performance_logging(self):
        documents = ["Document 1", "Document 2", "Document 3"] * 10
        optimized_embeddings = self.optimizer.optimize_embeddings(documents)
        self.optimizer.log_performance_metrics(documents, optimized_embeddings)
        # Assuming logging is successful if no exceptions are raised

if __name__ == '__main__':
    unittest.main()