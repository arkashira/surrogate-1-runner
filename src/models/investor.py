from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import re

@dataclass
class Investor:
    """Represents an investor profile in the network.

    Attributes:
        id: Unique identifier for the investor
        name: Full name of the investor (required)
        email: Email address (required, validated)
        firm: Company/firm name (optional)
        title: Job title (optional)
        linkedin_url: LinkedIn profile URL (optional, validated)
        bio: Short biography (optional)
        investment_focus: Areas of investment focus (optional)
        investment_stage: Preferred investment stage (optional)
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    firm: Optional[str] = None
    title: Optional[str] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    investment_focus: Optional[str] = None
    investment_stage: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def __post_init__(self) -> None:
        """Validate investor data after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Investor name is required")

        if self.email and "@" not in self.email:
            raise ValueError(f"Invalid email format: {self.email}")

        if self.linkedin_url and not re.match(r'^https?://(www\.)?linkedin\.com/', self.linkedin_url):
            raise ValueError(f"LinkedIn URL must be a valid LinkedIn URL: {self.linkedin_url}")

        # Trim whitespace from string fields
        self.name = self.name.strip()
        self.email = self.email.strip() if self.email else ""
        if self.firm:
            self.firm = self.firm.strip()
        if self.title:
            self.title = self.title.strip()
        if self.linkedin_url:
            self.linkedin_url = self.linkedin_url.strip()
        if self.bio:
            self.bio = self.bio.strip()
        if self.investment_focus:
            self.investment_focus = self.investment_focus.strip()
        if self.investment_stage:
            self.investment_stage = self.investment_stage.strip()

    def to_dict(self) -> dict:
        """Convert investor to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "firm": self.firm,
            "title": self.title,
            "linkedin_url": self.linkedin_url,
            "bio": self.bio,
            "investment_focus": self.investment_focus,
            "investment_stage": self.investment_stage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Investor":
        """Create Investor instance from dictionary."""
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        updated_at = data.get("updated_at")
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        return cls(
            id=data.get("id"),
            name=data.get("name", "").strip(),
            email=data.get("email", "").strip(),
            firm=data.get("firm", "").strip() or None,
            title=data.get("title", "").strip() or None,
            linkedin_url=data.get("linkedin_url", "").strip() or None,
            bio=data.get("bio", "").strip() or None,
            investment_focus=data.get("investment_focus", "").strip() or None,
            investment_stage=data.get("investment_stage", "").strip() or None,
            created_at=created_at or datetime.utcnow(),
            updated_at=updated_at or datetime.utcnow(),
        )

    @classmethod
    def from_csv_row(cls, row: dict) -> "Investor":
        """Create Investor instance from CSV row."""
        return cls(
            name=row.get("name", "").strip(),
            email=row.get("email", "").strip(),
            firm=row.get("firm", "").strip() or None,
            title=row.get("title", "").strip() or None,
            linkedin_url=row.get("linkedin_url", "").strip() or None,
            bio=row.get("bio", "").strip() or None,
            investment_focus=row.get("investment_focus", "").strip() or None,
            investment_stage=row.get("investment_stage", "").strip() or None,
        )