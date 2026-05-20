from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.aws_inventory import Base

DATABASE_URL = "postgresql://user:password@localhost:5432/axentx"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create the database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)