import socket
from encryption import secure_shell_session, generate_key

def main():
    key = generate_key()
    cert = 'path/to/cert.pem'
    secure_shell_session(key, cert)

if __name__ == '__main__':
    main()