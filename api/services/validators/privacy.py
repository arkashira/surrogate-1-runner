
import re
import socket
from urllib.parse import urlparse
from typing import Dict, List, Optional

import requests

# Comprehensive email regex for validation
_EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+"
    r"(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r'|^".+")@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$'
)

# Required metadata fields for Apple App Store compliance
_REQUIRED_FIELDS: set = {
    "bundle_id",
    "privacy_policy_url",
    "contact_email",
    "support_url",
}


class PrivacyPolicyValidationError(Exception):
    """Raised when privacy policy metadata fails validation."""

    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(f"Privacy policy validation failed: {'; '.join(errors)}")


def validate_url_format(url: str) -> bool:
    """
    Validate that a URL has a proper scheme and netloc.
    
    Args:
        url: The URL string to validate.
        
    Returns:
        True if URL format is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return result.scheme in {"http", "https"} and bool(result.netloc)
    except Exception:
        return False


def validate_url_reachable(url: str, timeout: int = 5) -> bool:
    """
    Perform a lightweight HEAD request to verify the URL is reachable.
    Falls back to GET if HEAD is not allowed by the server.
    
    Args:
        url: The URL to check for reachability.
        timeout:Request timeout in seconds.
        
    Returns:
        True if URL returns status < 400, False otherwise.
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code >= 400:
            # Some servers reject HEAD; try GET as a fallback
            response = requests.get(url, timeout=timeout, stream=True)
        return response.status_code < 400
    except (requests.RequestException, socket.error, TimeoutError):
        return False


def validate_email(email: str) -> bool:
    """
    Validate email address using a comprehensive regular expression.
    
    Args:
        email: The email address to validate.
        
    Returns:
        True if email format is valid, False otherwise.
    """
    return bool(_EMAIL_REGEX.fullmatch(email))


def validate_privacy_metadata(metadata: Dict) -> bool:
    """
    Validate the supplied metadata dictionary for Apple App Store privacy
    compliance.

    Args:
        metadata: Dictionary containing at least the required fields:
            - bundle_id: App bundle identifier (e.g., 'com.example.app')
            - privacy_policy_url: URL to the privacy policy
            - contact_email: Contact email address
            - support_url: URL to support page

    Returns:
        True if all validations pass.

    Raises:
        PrivacyPolicyValidationError: If any validation rule fails. 
            The exception contains a list of human-readable error messages.
    """
    errors: List[str] = []

    # 1. Check required fields presence
    missing = _REQUIRED_FIELDS - set(metadata.keys())
    if missing:
        errors.append(f"Missing required fields: {', '.join(sorted(missing))}")

    # 2. Validate privacy policy URL format and reachability
    privacy_url = metadata.get("privacy_policy_url")
    if privacy_url:
        if not validate_url_format(privacy_url):
            errors.append("privacy_policy_url is not a valid URL")
        elif not validate_url_reachable(privacy_url):
            errors.append("privacy_policy_url is not reachable")

    # 3. Validate contact email format
    contact_email = metadata.get("contact_email")
    if contact_email and not validate_email(contact_email):
        errors.append("contact_email is not a valid email address")

    # 4. Validate support URL format and reachability
    support_url = metadata.get("support_url")
    if support_url:
        if not validate_url_format(support_url):
            errors.append("support_url is not a valid URL")
        elif not validate_url_reachable(support_url):
            errors.append("support_url is not reachable")

    if errors:
        raise PrivacyPolicyValidationError(errors)

    return True


# Convenience functions for individual validations (for backward compatibility)
def validate_privacy_policy(app_metadata: Dict) -> bool:
    """Validate privacy policy URL only."""
    url = app_metadata.get("privacy_policy_url")
    if not url:
        return False
    return validate_url_format(url) and validate_url_reachable(url)


def validate_contact_info(app_metadata: Dict) -> bool:
    """Validate contact email only."""
    email = app_metadata.get("contact_email")
    if not email:
        return False
    return validate_email(email)


def validate_support_url(app_metadata: Dict) -> bool:
    """Validate support URL only."""
    url = app_metadata.get("support_url")
    if not url:
        return False
    return validate_url_format(url) and validate_url_reachable(url)


def check_required_metadata_fields(app_metadata: Dict) -> bool:
    """Check if all required metadata fields are present."""
    missing = _REQUIRED_FIELDS - set(app_metadata.keys())
    if missing:
        print(f"Missing required metadata fields: {', '.join(sorted(missing))}")
        return False
    return True