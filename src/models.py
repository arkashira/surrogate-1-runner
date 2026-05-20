from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SQLEnum,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserRole(Enum):
    """Enumeration of user roles used for access control."""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """User model with role‑based access control."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Store the role as a PostgreSQL ENUM.  The server_default guarantees
    # that new rows default to USER even if the application layer omits it.
    role = Column(
        SQLEnum(UserRole, name="user_role_enum", native_enum=False),
        nullable=False,
        server_default="user",
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def is_admin(self) -> bool:
        """Return True if the user has the ADMIN role."""
        return self.role == UserRole.ADMIN

    def __repr__(self) -> str:
        return f"<User {self.username!r} ({self.role.value})>"