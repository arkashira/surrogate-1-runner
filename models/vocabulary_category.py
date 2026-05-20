from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class VocabularyCategory(Base):
    __tablename__ = 'vocabulary_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(500))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # Relationship to vocabulary terms
    terms = relationship("VocabularyTerm", back_populates="category")

    def __repr__(self):
        return f"<VocabularyCategory(name='{self.name}', description='{self.description}')>"