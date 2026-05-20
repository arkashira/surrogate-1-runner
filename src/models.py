from sqlalchemy import Column, Integer, JSON, String, Float, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PricingRawData(Base):
    __tablename__ = "pricing_raw_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, nullable=False, index=True)
    market = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    raw_json = Column(JSON, nullable=False)