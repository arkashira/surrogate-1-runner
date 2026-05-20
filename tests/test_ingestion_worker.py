import unittest
from unittest.mock import patch
from ingestion_worker import fetch_dataset_from_huggingface

class TestIngestionWorker(unittest.TestCase):
    @patch('ingestion_worker.HfApi.dataset_download_files')
    @patch('ingestion_worker.boto3.client')
    def test_fetch_dataset_from_huggingface(self, mock_s3, mock_hf_api):
        mock_hf_api.return_value = 'dataset_path'
        mock_s3.return_value.upload_file.return_value = None

        config = {
            'dataset_name': 'axentx/surrogate-1-training-pairs',
            'dataset_version': 'main',
            's3_bucket': 'axentx-surrogate-1-datasets',
            's3_key': 'surrogate-1-training-pairs.tar.gz'
        }

        fetch_dataset_from_huggingface(config)

        mock_hf_api.assert_called_once_with(
            repo_id='axentx/surrogate-1-training-pairs',
            revision='main',
            path='surrogate-1-training-pairs.tar.gz'
        )
        mock_s3.assert_called_once_with('s3')
        mock_s3.return_value.upload_file.assert_called_once_with('dataset_path', 'axentx-surrogate-1-datasets', 'surrogate-1-training-pairs.tar.gz')

if __name__ == '__main__':
    unittest.main()