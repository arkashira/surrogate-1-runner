from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    rating_average = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    top_comments = Column(Text)  # JSON string storing top 3 comments

    def __repr__(self):
        return f"<Component(name='{self.name}', rating_average={self.rating_average}, rating_count={self.rating_count})>"