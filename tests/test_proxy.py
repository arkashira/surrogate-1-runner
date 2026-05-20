import unittest
import socket
import threading
from proxy import TransparentProxy

class TestTransparentProxy(unittest.TestCase):
    def setUp(self):
        self.proxy = TransparentProxy(host='127.0.0.1', port=8081, forward_to='127.0.0.1')
        self.proxy_thread = threading.Thread(target=self.proxy.start)
        self.proxy_thread.daemon = True
        self.proxy_thread.start()

    def test_proxy(self):
        # Create a test server that echoes back the received data
        test_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        test_server.bind(('127.0.0.1', 80))
        test_server.listen(1)

        def handle_test_server():
            conn, addr = test_server.accept()
            data = conn.recv(1024)
            conn.send(data)
            conn.close()

        test_server_thread = threading.Thread(target=handle_test_server)
        test_server_thread.daemon = True
        test_server_thread.start()

        # Connect to the proxy and send a test message
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8081))
        test_message = b"Hello, World!"
        client_socket.send(test_message)
        response = client_socket.recv(1024)
        client_socket.close()

        # Verify the response
        self.assertEqual(response, test_message)

        # Clean up
        test_server.close()

    def tearDown(self):
        self.proxy.server.close()

if __name__ == '__main__':
    unittest.main()