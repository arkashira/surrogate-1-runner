import pika
import yaml
import logging
from typing import Dict, Any

class RabbitMQQueue:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.connection = None
        self.channel = None
        self._setup_connection()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _setup_connection(self):
        credentials = pika.PlainCredentials(
            self.config['username'],
            self.config['password']
        )
        parameters = pika.ConnectionParameters(
            host=self.config['host'],
            port=self.config['port'],
            virtual_host=self.config['vhost'],
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config['queue_name'], durable=True)

    def publish_task(self, task: Dict[str, Any]):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.config['queue_name'],
            body=str(task),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

    def consume_tasks(self, callback):
        self.channel.basic_consume(
            queue=self.config['queue_name'],
            on_message_callback=callback,
            auto_ack=True
        )
        self.channel.start_consuming()

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()