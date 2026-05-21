import unittest
from unittest.mock import patch, MagicMock
from src.main import Worker

class TestMain(unittest.TestCase):
    @patch('src.main.Worker')
    def test_main(self, mock_worker):
        mock_worker_instance = MagicMock()
        mock_worker.return_value = mock_worker_instance
        import src.main
        mock_worker_instance.start.assert_called_once()
        mock_worker_instance.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()