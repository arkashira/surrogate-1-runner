from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./requests.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    sla_target = Column(DateTime, nullable=True)  # ISO-8601 parsed to datetime
    status = Column(String, default="open")  # open, in_progress, closed, etc.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "owner": self.owner,
            "sla_target": self.sla_target.isoformat() if self.sla_target else None,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_request(
    db: Session,
    *,
    type: str,
    title: str,
    owner: str,
    sla_target: datetime | None = None,
) -> RequestModel:
    db_obj = RequestModel(
        type=type,
        title=title,
        owner=owner,
        sla_target=sla_target,
        status="open",
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def list_requests(db: Session, *, limit: int = 100) -> list[RequestModel]:
    return db.query(RequestModel).order_by(RequestModel.created_at.desc()).limit(limit).all()