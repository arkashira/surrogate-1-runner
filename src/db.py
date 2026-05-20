from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/pricing_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    future=True,               # use 2.0 style API
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
    future=True,
)


def get_db() -> Session:
    """
    FastAPI dependency that yields a DB session and guarantees it is closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()