from sqlalchemy import Column, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # <-- your project's shared Base class

class UserPrefs(Base):
    """
    Per‑user UI preferences.

    Currently only the ``gaming_mode`` toggle is stored, but the table is
    deliberately extensible – just add more columns later.
    """
    __tablename__ = "user_prefs"

    # One row per user – use the user PK as the PK for this table.
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # Preference fields
    gaming_mode = Column(Boolean, nullable=False, default=False)

    # Optional back‑reference (only needed if you want ``user.prefs``)
    user = relationship("User", back_populates="prefs", uselist=False)

    def __repr__(self) -> str:  # helpful when debugging in the shell
        return f"<UserPrefs user_id={self.user_id} gaming_mode={self.gaming_mode}>"