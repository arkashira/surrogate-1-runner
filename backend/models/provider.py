from sqlalchemy import Column, UUID, String, Text, ForeignKey, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from typing import Optional

Base = declarative_base()

class FundingStage(str, Enum):
    """Valid funding stages for provider pitches."""
    PRE_SEED = "pre-seed"
    SEED = "seed"
    SERIES_A = "series-a"
    SERIES_B = "series-b"
    SERIES_C = "series-c"
    GROWTH = "growth"

class PitchStatus(str, Enum):
    """Status states for pitch submissions."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class TractionMetrics(JSONB):
    """Traction metrics for the provider's business."""
    pass

@dataclass
class Provider(Base):
    __tablename__ = 'providers'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    pitch_id = Column(String, unique=True, nullable=False)
    company_name = Column(String, nullable=False, length=MAX_COMPANY_NAME_LENGTH)
    tagline = Column(String, nullable=False, length=MAX_TAGLINE_LENGTH)
    market = Column(String, nullable=False, length=MAX_MARKET_LENGTH)
    traction_metrics = Column(TractionMetrics, nullable=False)
    funding_stage = Column(String, nullable=False, length=MAX_FUNDING_STAGE_LENGTH)
    executive_summary = Column(Text, nullable=False)
    deck_file_path = Column(String, nullable=True)
    deck_file_size_bytes = Column(Integer, nullable=True)
    deck_content_type = Column(String, nullable=True)
    contact_email = Column(String, nullable=False, unique_index=True, validator=re.compile(VALID_EMAIL_REGEX).match)
    status = Column(String, nullable=False, default=PitchStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Provider(pitch_id='{self.pitch_id}', company_name='{self.company_name}', tagline='{self.tagline}', market='{self.market}', traction_metrics='{self.traction_metrics}', funding_stage='{self.funding_stage}', executive_summary='{self.executive_summary}', deck_file_path='{self.deck_file_path}', deck_file_size_bytes='{self.deck_file_size_bytes}', deck_content_type='{self.deck_content_type}', contact_email='{self.contact_email}', status='{self.status}', created_at='{self.created_at}', updated_at='{self.updated_at}')"