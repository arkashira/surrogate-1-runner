import bcrypt
from typing import Dict, Optional

class User:
    def __init__(self, username: str):
        self.username = username
        self.password_hash = None
    
    def set_password(self, password: str):
        """Hash and store password using bcrypt"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

class UserDB:
    def __init__(self):
        self.users: Dict[str, User] = {}
    
    def create_user(self, username: str, password: str) -> User:
        """Create new user with hashed password"""
        if username in self.users:
            raise ValueError("User already exists")
        
        user = User(username)
        user.set_password(password)
        self.users[username] = user
        return user
    
    def get_user(self, username: str) -> Optional[User]:
        """Retrieve user by username"""
        return self.users.get(username)