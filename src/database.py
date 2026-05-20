"""
Database operations for cost tracking and budget management.
"""
import os
import sqlite3
from datetime import date
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


def get_db_path() -> str:
    """Get the database path from environment or default."""
    return os.environ.get('DATABASE_PATH', '/opt/axentx/surrogate-1/data/costs.db')


@contextmanager
def get_connection():
    """Context manager for database connections."""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the database with required tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Cost entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cost_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                service TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Budget configuration table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period TEXT NOT NULL,
                limit_amount REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Alert log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
                budget_id INTEGER,
                cumulative_cost REAL,
                threshold_amount REAL,
                FOREIGN KEY (budget_id) REFERENCES budgets(id)
            )
        ''')
        
        conn.commit()


def add_cost_entry(amount: float, service: str, cost_date: Optional[str] = None):
    """Add a cost entry for a specific date."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cost_date = cost_date or date.today().isoformat()
        cursor.execute(
            'INSERT INTO cost_entries (date, amount, service) VALUES (?, ?, ?)',
            (cost_date, amount, service)
        )
        conn.commit()


def get_costs_for_date(cost_date: Optional[str] = None) -> float:
    """Get cumulative costs for a specific date."""
    cost_date = cost_date or date.today().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COALESCE(SUM(amount), 0) FROM cost_entries WHERE date = ?',
            (cost_date,)
        )
        return cursor.fetchone()[0]


def get_current_budget() -> Optional[Dict[str, Any]]:
    """Get the current active budget configuration."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, period, limit_amount FROM budgets 
            ORDER BY created_at DESC LIMIT 1
        ''')
        row = cursor.fetchone()
        if row:
            return {'id': row['id'], 'period': row['period'], 'limit_amount': row['limit_amount']}
        return None


def set_budget(period: str, limit_amount: float):
    """Set a new budget limit."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO budgets (period, limit_amount) VALUES (?, ?)',
            (period, limit_amount)
        )
        conn.commit()


def log_alert(alert_type: str, message: str, budget_id: Optional[int] = None, 
             cumulative_cost: Optional[float] = None, threshold_amount: Optional[float] = None):
    """Log an alert event to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alert_logs (alert_type, message, budget_id, cumulative_cost, threshold_amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (alert_type, message, budget_id, cumulative_cost, threshold_amount))
        conn.commit()


def get_alert_history(limit: int = 100) -> List[Dict[str, Any]]:
    """Get recent alert history."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM alert_logs ORDER BY sent_at DESC LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]