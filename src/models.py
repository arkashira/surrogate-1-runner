from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///alerts.db')
Base = declarative_base()

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    message = Column(String)

    @classmethod
    def get_latest(cls):
        Session = sessionmaker(bind=engine)
        session = Session()
        latest_alert = session.query(cls).order_by(cls.id.desc()).first()
        session.close()
        return latest_alert

Base.metadata.create_all(engine)