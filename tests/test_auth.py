import pytest
from src.user_management import UserDB, User
from src.auth import authenticate_user

def test_valid_authentication():
    db = UserDB()
    user = db.create_user("testuser", "SecurePass123!")
    assert authenticate_user("testuser", "SecurePass123!") is True

def test_invalid_password():
    db = UserDB()
    db.create_user("testuser", "SecurePass123!")
    assert authenticate_user("testuser", "wrongpassword") is False

def test_nonexistent_user():
    assert authenticate_user("nonexistent", "any password") is False

def test_password_hashing():
    db = UserDB()
    user = db.create_user("hashuser", "HashPass123!")
    assert user.password_hash.startswith("$2b$")  # Bcrypt hash prefix
    assert user.check_password("HashPass123!") is True
    assert user.check_password("wrong") is False