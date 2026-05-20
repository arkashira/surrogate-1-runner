import socket
import threading
import queue
import time

class LoadBalancer:
    def __init__(self, host='localhost', port=8080, max_connections=1000):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_connections)
        self.session_queue = queue.Queue()
        self.active_sessions = set()

    def start(self):
        print(f"Load balancer started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()
        threading.Thread(target=self.handle_sessions, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            self.session_queue.put(client_socket)

    def handle_sessions(self):
        while True:
            client_socket = self.session_queue.get()
            session_thread = threading.Thread(target=self.handle_session, args=(client_socket,))
            session_thread.start()
            self.active_sessions.add(session_thread)

    def handle_session(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)
        except Exception as e:
            print(f"Error handling session: {e}")
        finally:
            client_socket.close()
            self.active_sessions.discard(threading.current_thread())

    def stop(self):
        self.server_socket.close()
        for session_thread in self.active_sessions:
            session_thread.join()
        print("Load balancer stopped")

if __name__ == "__main__":
    load_balancer = LoadBalancer()
    load_balancer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        load_balancer.stop()