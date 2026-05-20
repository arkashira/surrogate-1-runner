import unittest
import socket
import threading
import time
from src.load_balancer import LoadBalancer

class TestLoadBalancer(unittest.TestCase):
    def setUp(self):
        self.load_balancer = LoadBalancer(host='localhost', port=8081)
        self.load_balancer.start()
        time.sleep(1)  # Give the load balancer time to start

    def tearDown(self):
        self.load_balancer.stop()

    def test_connection_establishment(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_time = time.time()
        client_socket.connect(('localhost', 8081))
        end_time = time.time()
        self.assertLess(end_time - start_time, 2, "Connection establishment took too long")
        client_socket.close()

    def test_concurrent_connections(self):
        def connect_to_server():
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 8081))
            client_socket.close()

        threads = []
        for _ in range(1000):
            thread = threading.Thread(target=connect_to_server)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(len(self.load_balancer.active_sessions), 0, "Not all sessions were handled")

if __name__ == "__main__":
    unittest.main()