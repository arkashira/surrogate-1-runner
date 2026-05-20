import datetime
from typing import List

from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///billing.db"  # Replace with actual database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

sessions_table = Table(
    'sessions', metadata,
    Column('id', Integer, primary_key=True),
    Column('organization_id', String),
    Column('duration_seconds', Integer),
)

billing_table = Table(
    'billing', metadata,
    Column('id', Integer, primary_key=True),
    Column('organization_id', String),
    Column('minutes_used', Integer),
    Column('cost', Float),
)

def aggregate_minutes_per_organization(session_durations: List[int], organization_id: str) -> int:
    total_minutes = sum([max(0, duration // 60) for duration in session_durations])
    return total_minutes

def calculate_cost(minutes_used: int) -> float:
    return minutes_used * 0.01  # Assuming cost is $0.01 per minute

def run_nightly_aggregation():
    session = SessionLocal()
    
    query = sessions_table.select().where(sessions_table.c.organization_id == 'example_org')
    result = session.execute(query)
    session_durations = [row.duration_seconds for row in result]
    
    minutes_used = aggregate_minutes_per_organization(session_durations, 'example_org')
    cost = calculate_cost(minutes_used)
    
    insert_query = billing_table.insert().values(
        organization_id='example_org',
        minutes_used=minutes_used,
        cost=cost
    )
    session.execute(insert_query)
    session.commit()

if __name__ == "__main__":
    run_nightly_aggregation()