import paramiko
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SSHAuthenticator:
    def __init__(self, host, port=22, username="admin"):
        self.host = host
        self.port = port
        self.username = username
        self.client = None

    def connect(self, private_key_path):
        """
        Connects to the SSH server using a private key.
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            self.client.connect(self.host, port=self.port, username=self.username, pkey=private_key)
            logger.info(f"Successfully connected to {self.host}:{self.port} as {self.username}")
            return True
        except FileNotFoundError:
            logger.error(f"Private key file not found at: {private_key_path}")
            return False
        except paramiko.AuthenticationException:
            logger.error(f"Authentication failed for {self.username}@{self.host}:{self.port}. Check your private key.")
            return False
        except Exception as e:
            logger.error(f"An error occurred during SSH connection: {e}")
            return False

    def authenticate_with_key(self, private_key_path):
        """
        Authenticates the user using their SSH private key.
        This method is a wrapper around connect for clarity in the context of authentication.
        """
        return self.connect(private_key_path)

    def close(self):
        """
        Closes the SSH connection.
        """
        if self.client:
            self.client.close()
            logger.info(f"SSH connection to {self.host}:{self.port} closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Example Usage (for demonstration, not part of the final deployable code)
if __name__ == "__main__":
    # This is a placeholder for actual key management and host details.
    # In a real scenario, these would be securely managed.
    TEST_HOST = "your_server_ip"  # Replace with your server IP
    TEST_PRIVATE_KEY_PATH = "/path/to/your/private/key" # Replace with your private key path

    authenticator = SSHAuthenticator(TEST_HOST)

    if authenticator.authenticate_with_key(TEST_PRIVATE_KEY_PATH):
        print("SSH authentication successful!")
        # You can now execute commands or open a shell session
        # For example:
        # stdin, stdout, stderr = authenticator.client.exec_command("ls -l")
        # print(stdout.read().decode())
    else:
        print("SSH authentication failed.")

    authenticator.close()