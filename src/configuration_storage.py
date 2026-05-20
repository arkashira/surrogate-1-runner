import sqlite3
from typing import Dict, Any

class ConfigurationStorage:
    def __init__(self, db_path: str = 'configurations.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configurations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_type TEXT NOT NULL,
                    data_volume INTEGER NOT NULL,
                    start_timestamp TEXT NOT NULL,
                    end_timestamp TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_configuration(self, config: Dict[str, Any]) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO configurations (data_type, data_volume, start_timestamp, end_timestamp)
                VALUES (?, ?, ?, ?)
            ''', (config['data_type'], config['data_volume'], config['start_timestamp'], config['end_timestamp']))
            conn.commit()
            return cursor.lastrowid

    def get_configuration(self, config_id: int) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM configurations WHERE id = ?', (config_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'data_type': row[1],
                    'data_volume': row[2],
                    'start_timestamp': row[3],
                    'end_timestamp': row[4],
                    'created_at': row[5]
                }
            return None

    def get_all_configurations(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM configurations')
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'data_type': row[1],
                'data_volume': row[2],
                'start_timestamp': row[3],
                'end_timestamp': row[4],
                'created_at': row[5]
            } for row in rows]