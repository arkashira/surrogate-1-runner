import unittest
from unittest.mock import patch, MagicMock
from queue import RabbitMQQueue
import yaml
import os

class TestRabbitMQQueue(unittest.TestCase):
    def setUp(self):
        self.config_path = 'test_rabbitmq.yaml'
        with open(self.config_path, 'w') as f:
            yaml.dump({
                'host': 'test_host',
                'port': 1234,
                'vhost': 'test_vhost',
                'username': 'test_user',
                'password': 'test_pass',
                'queue_name': 'test_queue'
            }, f)

    def tearDown(self):
        os.remove(self.config_path)

    @patch('pika.BlockingConnection')
    def test_initialization(self, mock_connection):
        with RabbitMQQueue(self.config_path) as queue:
            self.assertIsNotNone(queue.connection)
            self.assertIsNotNone(queue.channel)
            mock_connection.assert_called_once()

    @patch('pika.BlockingConnection')
    def test_publish_task(self, mock_connection):
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        with RabbitMQQueue(self.config_path) as queue:
            test_task = {'task_id': 1, 'data': 'test_data'}
            queue.publish_task(test_task)
            mock_channel.basic_publish.assert_called_once()

    @patch('pika.BlockingConnection')
    def test_consume_tasks(self, mock_connection):
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        with RabbitMQQueue(self.config_path) as queue:
            test_callback = MagicMock()
            queue.consume_tasks(test_callback)
            mock_channel.basic_consume.assert_called_once_with(
                queue='test_queue',
                on_message_callback=test_callback,
                auto_ack=True
            )

    @patch('pika.BlockingConnection')
    def test_close(self, mock_connection):
        with RabbitMQQueue(self.config_path) as queue:
            queue.close()
            mock_connection.return_value.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()