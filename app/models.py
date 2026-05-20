from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CostActual(Base):
    __tablename__ = "cost_actuals"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CostForecast(Base):
    __tablename__ = "cost_forecasts"
    id = Column(Integer, primary_key=True, index=True)
    forecast_date = Column(Date, nullable=False, index=True)
    target_date = Column(Date, nullable=False, index=True)
    predicted_amount = Column(Float, nullable=False)
    model_version = Column(String, default="v1")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ForecastMetric(Base):
    __tablename__ = "forecast_metrics"
    id = Column(Integer, primary_key=True, index=True)
    evaluation_date = Column(Date, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    mae = Column(Float, nullable=False)
    mape = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())