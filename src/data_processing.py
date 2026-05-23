import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_db_connection

def calculate_pl(start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(revenue) - SUM(expenses) AS pl
        FROM financial_data
        WHERE date BETWEEN %s AND %s
    """, (start_date, end_date))

    pl = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return pl