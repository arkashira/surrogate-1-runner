import paramiko
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from .security_alerts import trigger_security_alert

class TerminalSession:
    def __init__(self, host, port=22):
        self.host = host
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def register_ssh_key(self, public_key_str):
        # Simulate admin approval process
        approved = self._admin_approval(public_key_str)
        if not approved:
            raise Exception("SSH key registration failed due to lack of admin approval.")
        
        # Store the approved public key
        self.public_key = serialization.load_ssh_public_key(
            public_key_str.encode(),
            backend=default_backend()
        )

    def _admin_approval(self, public_key_str):
        # Placeholder for actual admin approval logic
        return True  # Assume admin always approves for demo purposes

    def create_encrypted_tunnel(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        self.client.connect(self.host, self.port, pkey=private_key)

    def validate_ssh_tunnel(self):
        try:
            stdin, stdout, stderr = self.client.exec_command('whoami')
            response = stdout.read().decode()
            if 'root' in response:
                return True
            else:
                trigger_security_alert("Failed login attempt detected.")
                return False
        except Exception as e:
            trigger_security_alert(f"Exception during SSH tunnel validation: {str(e)}")
            return False

    def close(self):
        self.client.close()

# Example usage
if __name__ == "__main__":
    session = TerminalSession('example.com')
    public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD...'
    session.register_ssh_key(public_key)
    session.create_encrypted_tunnel()
    if session.validate_ssh_tunnel():
        print("SSH tunnel validated successfully.")
    else:
        print("SSH tunnel validation failed.")
    session.close()