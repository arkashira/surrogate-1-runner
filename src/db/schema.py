import sqlite3

def create_schema(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schema_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commit_hash TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            diff TEXT NOT NULL
        )
    ''')
    
    connection.commit()
    connection.close()