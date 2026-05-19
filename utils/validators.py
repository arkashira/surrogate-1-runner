import re
from typing import Tuple, List


def validate_password(password: str) -> Tuple[bool, List[str]]:
    """
    Validate password strength with detailed feedback.

    Args:
        password (str): Password to validate.

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_violations)
    """
    violations = []
    
    # Check minimum length (8 characters)
    if len(password) < 8:
        violations.append("Password must be at least 8 characters long")
    elif len(password) > 128:
        violations.append("Password must be less than 128 characters")
    
    # Check for uppercase letter
    if not re.search(r"[A-Z]", password):
        violations.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase letter
    if not re.search(r"[a-z]", password):
        violations.append("Password must contain at least one lowercase letter")
    
    # Check for number
    if not re.search(r"\d", password):
        violations.append("Password must contain at least one number")
    
    # Check for special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        violations.append("Password must contain at least one special character")
    
    # Check for common weak passwords
    common_passwords = {"password", "12345678", "qwerty", "admin", "letmein"}
    if password.lower() in common_passwords:
        violations.append("Password is too common")
    
    return (len(violations) == 0, violations)


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format with detailed feedback.

    Args:
        email (str): Email to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not email:
        return (False, "Email cannot be empty")
    
    # More robust email regex
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if not re.match(email_pattern, email):
        return (False, "Invalid email format")
    
    # Check for valid domain (has at least one dot in domain)
    parts = email.split("@")
    if len(parts) != 2:
        return (False, "Invalid email format")
    
    domain = parts[1]
    if "." not in domain:
        return (False, "Email domain must contain a TLD")
    
    return (True, "")