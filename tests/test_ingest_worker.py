import unittest
from ingest_worker import IngestWorker

class TestIngestWorker(unittest.TestCase):
    def setUp(self):
        self.worker = IngestWorker(num_workers=4)

    def test_spawn_workers(self):
        datasets = ["dataset1", "dataset2", "dataset3", "dataset4", "dataset5"]
        self.worker.spawn_workers(datasets)

if __name__ == '__main__':
    unittest.main()