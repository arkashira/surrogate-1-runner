import re
import requests
from dataclasses import dataclass
from typing import Tuple, Optional
from urllib.parse import urlparse

@dataclass
class ValidationResult:
    """Standardized validation result format."""
    valid: bool
    message: str
    field: Optional[str] = None

class URLValidator:
    """Comprehensive URL validation utilities."""

    # Allowed schemes for production URLs
    ALLOWED_SCHEMES = ('https', 'http')

    # Strict URL pattern matching
    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )

    @classmethod
    def validate_url_format(cls, url: str, field_name: str = "URL") -> ValidationResult:
        """Validate URL format only (without reachability check)."""
        if not url or not isinstance(url, str):
            return ValidationResult(
                valid=False,
                message=f"{field_name} is empty or invalid type",
                field=field_name
            )

        if not cls.URL_PATTERN.match(url):
            return ValidationResult(
                valid=False,
                message=f"{field_name} has invalid format",
                field=field_name
            )

        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return ValidationResult(
                valid=False,
                message=f"{field_name} is missing scheme or domain",
                field=field_name
            )

        if parsed.scheme not in cls.ALLOWED_SCHEMES:
            return ValidationResult(
                valid=False,
                message=f"{field_name} must use http or https scheme",
                field=field_name
            )

        return ValidationResult(valid=True, message=f"{field_name} format is valid", field=field_name)

    @classmethod
    def check_url_reachability(cls, url: str, timeout: int = 5) -> ValidationResult:
        """Check if URL is reachable (returns 2xx or 3xx)."""
        try:
            # First try HEAD request (more efficient)
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            if 200 <= response.status_code < 400:
                return ValidationResult(valid=True, message="URL is reachable", field="URL")

            # If HEAD fails, try GET
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            if 200 <= response.status_code < 400:
                return ValidationResult(valid=True, message="URL is reachable", field="URL")

            return ValidationResult(
                valid=False,
                message=f"URL returned status code {response.status_code}",
                field="URL"
            )

        except requests.RequestException as e:
            return ValidationResult(
                valid=False,
                message=f"URL is not reachable: {str(e)}",
                field="URL"
            )

    @classmethod
    def validate_url(cls, url: str, check_reachability: bool = True, field_name: str = "URL") -> ValidationResult:
        """Comprehensive URL validation (format + reachability)."""
        format_result = cls.validate_url_format(url, field_name)
        if not format_result.valid:
            return format_result

        if check_reachability:
            reachability_result = cls.check_url_reachability(url)
            if not reachability_result.valid:
                return reachability_result

        return ValidationResult(valid=True, message=f"{field_name} is valid", field=field_name)

class EmailValidator:
    """Email address validation utilities."""

    # Comprehensive email regex pattern
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    @classmethod
    def validate_email(cls, email: str, field_name: str = "Email") -> ValidationResult:
        """Validate email address format."""
        if not email or not isinstance(email, str):
            return ValidationResult(
                valid=False,
                message=f"{field_name} is empty or invalid type",
                field=field_name
            )

        if not cls.EMAIL_PATTERN.match(email):
            return ValidationResult(
                valid=False,
                message=f"{field_name} has invalid format",
                field=field_name
            )

        return ValidationResult(valid=True, message=f"{field_name} is valid", field=field_name)

# Convenience functions for backward compatibility
def validate_url(url: str) -> Tuple[bool, str]:
    """Legacy function for URL validation (returns tuple)."""
    result = URLValidator.validate_url(url)
    return (result.valid, result.message)

def validate_email(email: str) -> Tuple[bool, str]:
    """Legacy function for email validation (returns tuple)."""
    result = EmailValidator.validate_email(email)
    return (result.valid, result.message)

def validate_support_url(url: str) -> Tuple[bool, str]:
    """Legacy function for support URL validation (returns tuple)."""
    result = URLValidator.validate_url_format(url, "Support URL")
    return (result.valid, result.message)