import hashlib
import hmac
import secrets
from typing import Dict

class Authenticator:
    def __init__(self):
        self.users: Dict[str, str] = {}

    def register_user(self, username: str, password: str):
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password

    def authenticate(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        hashed_password = self._hash_password(password)
        return hmac.compare_digest(hashed_password, self.users[username])

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = secrets.token_hex(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return salt + ':' + hashed_password.hex()

    def get_user(self, username: str) -> str:
        return self.users.get(username, None)

class AccessController:
    def __init__(self):
        self.permissions: Dict[str, Dict[str, bool]] = {}

    def grant_permission(self, username: str, permission: str):
        if username not in self.permissions:
            self.permissions[username] = {}
        self.permissions[username][permission] = True

    def revoke_permission(self, username: str, permission: str):
        if username in self.permissions and permission in self.permissions[username]:
            del self.permissions[username][permission]

    def has_permission(self, username: str, permission: str) -> bool:
        return username in self.permissions and permission in self.permissions[username] and self.permissions[username][permission]

def main():
    authenticator = Authenticator()
    access_controller = AccessController()

    # Register a user
    authenticator.register_user('admin', 'password123')

    # Grant permission
    access_controller.grant_permission('admin', 'read')

    # Authenticate and check permission
    if authenticator.authenticate('admin', 'password123') and access_controller.has_permission('admin', 'read'):
        print('Access granted')
    else:
        print('Access denied')

if __name__ == '__main__':
    main()