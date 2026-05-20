import os
from sqlalchemy import create_engine, text

def main():
    engine = create_engine(os.getenv("DATABASE_URL"))
    with engine.connect() as conn:
        # Execute benchmark data seeding SQL
        with open("/opt/axentx/surrogate-1/sql/seed_benchmark.sql", "r") as f:
            conn.execute(text(f.read()))

if __name__ == "__main__":
    main()