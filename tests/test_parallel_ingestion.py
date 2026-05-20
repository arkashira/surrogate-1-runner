import unittest
from unittest.mock import patch, Mock
from multiprocessing import Process
from queue import Queue
from time import sleep

# Assuming these imports exist in the actual project
from surrogate_1.runner import start_worker, report_completion
from surrogate_1.queue import MessageQueue

class TestParallelIngestion(unittest.TestCase):

    def setUp(self):
        self.dataset_size = 1000
        self.num_workers = 4
        self.message_queue = Queue()
        self.workers = []

    @patch('surrogate_1.runner.MessageQueue')
    def test_spawn_workers(self, mock_queue):
        mock_queue_instance = mock_queue.return_value
        mock_queue_instance.get.side_effect = [i for i in range(self.dataset_size)] + [None]

        for _ in range(self.num_workers):
            worker = Process(target=start_worker, args=(mock_queue_instance,))
            worker.start()
            self.workers.append(worker)

        for worker in self.workers:
            worker.join()

        # Check if all items were processed
        self.assertEqual(mock_queue_instance.get.call_count, self.dataset_size)

    @patch('surrogate_1.runner.MessageQueue')
    def test_worker_coordination(self, mock_queue):
        mock_queue_instance = mock_queue.return_value
        mock_queue_instance.get.side_effect = [i for i in range(self.dataset_size)] + [None]

        worker_processes = []
        for _ in range(self.num_workers):
            worker = Process(target=start_worker, args=(mock_queue_instance,))
            worker.start()
            worker_processes.append(worker)

        for worker in worker_processes:
            worker.join()

        # Ensure there are no duplicated tasks
        calls = mock_queue_instance.put.call_args_list
        unique_tasks = set(call[0][0] for call in calls)
        self.assertEqual(len(unique_tasks), self.dataset_size)

    @patch('surrogate_1.runner.MessageQueue')
    def test_completion_reporting(self, mock_queue):
        mock_queue_instance = mock_queue.return_value
        mock_queue_instance.get.side_effect = [i for i in range(self.dataset_size)] + [None]

        worker_processes = []
        for _ in range(self.num_workers):
            worker = Process(target=start_worker, args=(mock_queue_instance,))
            worker.start()
            worker_processes.append(worker)

        for worker in worker_processes:
            worker.join()

        # Check if all workers reported completion
        self.assertEqual(report_completion.call_count, self.num_workers)

if __name__ == '__main__':
    unittest.main()