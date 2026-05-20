import os

class Config:
    def __init__(self):
        self.dataset_repo = 'https://huggingface.co/datasets/axentx/surrogate-1-training-pairs'
        self.dataset_script = 'bin/dataset-enrich.sh'
        self.upload_interval_minutes = 30
        self.num_runners = 16

    def get_dataset_list(self):
        return os.popen(f'bash {self.dataset_script}').read().strip()

    def get_dataset_slice(self, shard_id):
        dataset_list = self.get_dataset_list()
        start_index = shard_id * len(dataset_list) // self.num_runners
        end_index = (shard_id + 1) * len(dataset_list) // self.num_runners
        return dataset_list[start_index:end_index]

# tests/test_config.py
import unittest
from unittest.mock import patch
from config import Config

class TestConfig(unittest.TestCase):
    def test_get_dataset_list(self):
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value.stdout.read.return_value = 'dataset1\ndataset2'
            config = Config()
            self.assertEqual(config.get_dataset_list(), 'dataset1\ndataset2')

    def test_get_dataset_slice(self):
        config = Config()
        dataset_list = ['dataset1', 'dataset2', 'dataset3']
        self.assertEqual(config.get_dataset_slice(0), ['dataset1'])
        self.assertEqual(config.get_dataset_slice(1), ['dataset2'])
        self.assertEqual(config.get_dataset_slice(2), ['dataset3'])

if __name__ == '__main__':
    unittest.main()

## Summary
- Simplified configuration process by introducing a Config class.
- Implemented get_dataset_list and get_dataset_slice methods.
- Added unit tests for the Config class.