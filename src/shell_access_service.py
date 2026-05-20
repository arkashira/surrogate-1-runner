import socket
import threading
from load_balancer import LoadBalancer

class ShellAccessService:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.load_balancer = LoadBalancer(host=self.host, port=self.port)

    def start(self):
        self.load_balancer.start()
        print(f"Shell access service started on {self.host}:{self.port}")

    def stop(self):
        self.load_balancer.stop()
        print("Shell access service stopped")

if __name__ == "__main__":
    shell_access_service = ShellAccessService()
    shell_access_service.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shell_access_service.stop()