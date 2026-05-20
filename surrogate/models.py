from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    author = Column(String(255), nullable=False)
    action = Column(Text, nullable=False)

    def __repr__(self) -> str:  # handy for debugging
        return (
            f"<AuditLog id={self.id} article_id={self.article_id} "
            f"author={self.author} action={self.action[:20]}>"
        )