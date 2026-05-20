from sqlalchemy import Column, UUID, BigInteger, String, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class FileMetadata(Base):
    __tablename__ = 'file_metadata'
    
    # Use UUID as primary key for distributed systems
    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(255), nullable=False)
    sha256_checksum = Column(String(64), nullable=False, unique=True)
    ingestion_timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('sha256_checksum', name='unique_sha256_checksum'),
        Index('idx_file_metadata_ingestion_timestamp', 'ingestion_timestamp'),
        Index('idx_file_metadata_mime_type', 'mime_type'),
        Index('idx_file_metadata_file_size', 'file_size'),
    )

    def to_dict(self):
        return {
            "file_id": str(self.file_id),
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "sha256_checksum": self.sha256_checksum,
            "ingestion_timestamp": self.ingestion_timestamp.isoformat() if self.ingestion_timestamp else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }