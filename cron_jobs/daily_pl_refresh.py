import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import calculate_pl
from src.database import get_db_connection

def refresh_daily_pl():
    # Calculate the date range for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Calculate the P&L
    pl = calculate_pl(start_date, end_date)

    # Store the P&L in the database
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO daily_pl (date, pl)
        VALUES (%s, %s)
        ON CONFLICT (date) DO UPDATE SET pl = EXCLUDED.pl
    """, (end_date.date(), pl))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    refresh_daily_pl()