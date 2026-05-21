import sqlite3

def init_db():
    conn = sqlite3.connect("surrogate_1.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS surrogate_1_data (
            id INTEGER PRIMARY KEY,
            data TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()