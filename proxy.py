import socket
import threading

class TransparentProxy:
    def __init__(self, host='0.0.0.0', port=8080, forward_to='127.0.0.1'):
        self.host = host
        self.port = port
        self.forward_to = forward_to
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def handle_client(self, client_socket):
        request = client_socket.recv(4096)
        if not request:
            client_socket.close()
            return

        # Forward the request to the internal VM
        forward_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        forward_socket.connect((self.forward_to, 80))
        forward_socket.send(request)

        # Receive the response from the internal VM
        response = forward_socket.recv(4096)

        # Send the response back to the client
        client_socket.send(response)

        # Close the sockets
        client_socket.close()
        forward_socket.close()

    def start(self):
        print(f"Transparent proxy server started on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == '__main__':
    proxy = TransparentProxy()
    proxy.start()