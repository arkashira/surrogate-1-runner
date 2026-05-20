from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def init_db():
    engine = create_engine('sqlite:///surrogate-1.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# Example usage
if __name__ == "__main__":
    session = init_db()
    print("Database schema initialized.")