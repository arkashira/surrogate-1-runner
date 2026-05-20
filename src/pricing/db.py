import os
import logging
from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2.extras import execute_values

LOGGER = logging.getLogger(__name__)

# In a real deployment these would come from a secret manager / env vars.
DB_DSN = os.getenv(
    "PRICING_DB_DSN",
    "dbname=pricing user=pricing password=pricing host=localhost port=5432",
)


@contextmanager
def get_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """Yield a live PostgreSQL connection and guarantee it is closed."""
    conn = psycopg2.connect(DB_DSN)
    try:
        yield conn
    finally:
        conn.close()


def bulk_insert_pricing_data(conn, rows: list[dict]) -> int:
    """
    Insert many rows in a single statement.
    Returns the number of rows inserted.
    """
    if not rows:
        return 0

    sql = """
        INSERT INTO pricing (
            product_id,
            market,
            competitor,
            price,
            currency,
            timestamp
        ) VALUES %s
    """
    values = [
        (
            r["product_id"],
            r["market"],
            r["competitor"],
            r["price"],
            r["currency"],
            r["timestamp"],
        )
        for r in rows
    ]

    with conn.cursor() as cur:
        execute_values(cur, sql, values)
        conn.commit()
    LOGGER.info("Inserted %s pricing rows", len(rows))
    return len(rows)