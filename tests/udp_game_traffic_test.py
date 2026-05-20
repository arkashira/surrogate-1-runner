import socket
import threading
import unittest
import time

class UDPMultiplexer:
    def __init__(self, external_ip='0.0.0.0', external_port=5000):
        self.external_ip = external_ip
        self.external_port = external_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.external_ip, self.external_port))
        self.clients = {}

    def handle_client(self, client_address):
        while True:
            data, addr = self.server_socket.recvfrom(1024)
            if addr == client_address:
                print(f"Received data from {client_address}: {data}")
                self.server_socket.sendto(data, client_address)

    def start(self):
        print("UDP Multiplexer Started")
        try:
            while True:
                data, addr = self.server_socket.recvfrom(1024)
                if addr not in self.clients:
                    print(f"New client connected: {addr}")
                    self.clients[addr] = threading.Thread(target=self.handle_client, args=(addr,))
                    self.clients[addr].start()
                else:
                    print(f"Received data from existing client {addr}: {data}")
                    self.server_socket.sendto(data, addr)
        except KeyboardInterrupt:
            print("Stopping UDP Multiplexer")
            self.server_socket.close()

class TestUDPMultiplexer(unittest.TestCase):
    def setUp(self):
        self.server = UDPMultiplexer('localhost', 12345)
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)  # Allow server to start

    def test_client_connection(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(b'Hello, server!', ('localhost', 12345))
        data, _ = client_socket.recvfrom(1024)
        self.assertEqual(data, b'Hello, server!')
        client_socket.close()

    def test_multiple_clients(self):
        clients = []
        for i in range(3):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(f'Client {i} message'.encode(), ('localhost', 12345))
            data, _ = client_socket.recvfrom(1024)
            self.assertEqual(data, f'Client {i} message'.encode())
            clients.append(client_socket)
        
        for client in clients:
            client.close()

    def tearDown(self):
        self.server.server_socket.close()
        self.server_thread.join(timeout=1)

if __name__ == '__main__':
    unittest.main()