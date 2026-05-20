
from fastapi import Depends, FastAPI
from surrogate_1.database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    global models
    models = [DecisionAudit]
    database_url = "postgresql://user:password@localhost/surrogate_1"
    engine.connect(database_url)
    models = [mapper.configure("surrogate_1")(cls) for cls in models]
    Base.metadata.create_all(bind=engine)