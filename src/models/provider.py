"""
Provider model for the surrogate-1 service.

This dataclass represents a service provider that registers via the API.
It includes comprehensive validation to ensure required fields are present and non-empty.
The model can be easily extended with additional fields or validation logic as the project evolves.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
import re


def _validate_email(email: str) -> None:
    """
    Very lightweight email validation.
    Raises ValueError if the email is not in a basic RFC‑5322 compliant format.
    """
    email_regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    if not email_regex.match(email):
        raise ValueError(f"Invalid email address: {email}")


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non‑empty string")


@dataclass
class Provider:
    """
    Represents a provider that registers with the surrogate‑1 API.

    Attributes
    ----------
    company_name : str
        The legal name of the provider's company.
    email : str
        Contact email address for the provider.
    phone : Optional[str]
        Optional phone number. If provided, must be a non‑empty string.
    website : Optional[str]
        Optional company website URL.
    industry : Optional[str]
        Optional industry sector.
    description : Optional[str]
        Optional company description.
    created_at : datetime
        Timestamp when the provider was created. Defaults to UTC now.
    is_confirmed : bool
        Flag indicating whether the provider has been confirmed.
    confirmation_token : Optional[str]
        Optional confirmation token for email verification.
    """

    company_name: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_confirmed: bool = False
    confirmation_token: Optional[str] = None

    REQUIRED_FIELDS = ["company_name", "email"]

    def __post_init__(self) -> None:
        # Validate required fields
        self._validate_required_fields()
        self._validate_email()

        # Optional fields validation
        if self.phone is not None:
            _validate_non_empty("phone", self.phone)
        if self.website is not None:
            _validate_non_empty("website", self.website)
        if self.industry is not None:
            _validate_non_empty("industry", self.industry)
        if self.description is not None:
            _validate_non_empty("description", self.description)

    def _validate_required_fields(self) -> None:
        """Ensure all required fields are present and non-empty."""
        for field_name in self.REQUIRED_FIELDS:
            value = getattr(self, field_name, None)
            if not value or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"Required field '{field_name}' cannot be empty")

    def _validate_email(self) -> None:
        """Validate email format."""
        if self.email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                raise ValueError(f"Invalid email format: {self.email}")

    def confirm(self, token: str) -> bool:
        """
        Confirm provider registration using the confirmation token.

        Args:
            token: The confirmation token to validate.

        Returns:
            True if confirmation successful, False otherwise.
        """
        if self.confirmation_token and self.confirmation_token == token:
            self.is_confirmed = True
            self.confirmation_token = None  # Invalidate token after use
            return True
        return False

    def to_dict(self) -> dict:
        """
        Convert the Provider instance into a plain dictionary suitable for
        JSON serialization or database insertion.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Provider":
        """
        Create a Provider instance from a dictionary, performing the same
        validation as the constructor.
        """
        return cls(**data)

    @classmethod
    def create_provider(
        cls,
        company_name: str,
        email: str,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "Provider":
        """
        Factory function to create a new Provider instance.

        Args:
            company_name: Name of the company (required).
            email: Contact email address (required).
            phone: Contact phone number (optional).
            website: Company website URL (optional).
            industry: Industry sector (optional).
            description: Company description (optional).

        Returns:
            A new Provider instance.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        return cls(
            company_name=company_name,
            email=email,
            phone=phone,
            website=website,
            industry=industry,
            description=description,
        )