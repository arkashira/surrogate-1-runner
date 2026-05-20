import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.create_logs_table()

    def create_logs_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS user_usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    model_name TEXT NOT NULL,
                    usage_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    action TEXT NOT NULL
                )
            ''')

    def log_usage(self, user_id, model_name, action):
        with self.connection:
            self.connection.execute('''
                INSERT INTO user_usage_logs (user_id, model_name, action)
                VALUES (?, ?, ?)
            ''', (user_id, model_name, action))

    def get_logs(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM user_usage_logs')
        return cursor.fetchall()

    def close(self):
        self.connection.close()