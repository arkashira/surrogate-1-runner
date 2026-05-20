import sqlite3

class DBHandler:
    def __init__(self, db_path='usage_logs.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_model_usage (
                timestamp TEXT,
                user_id TEXT,
                model_name TEXT,
                usage_details TEXT
            )
        ''')
        self.conn.commit()

    def store_log(self, log_entry):
        self.cursor.execute('''
            INSERT INTO ai_model_usage (timestamp, user_id, model_name, usage_details)
            VALUES (?, ?, ?, ?)
        ''', (log_entry['timestamp'], log_entry['user_id'], log_entry['model_name'], str(log_entry['usage_details'])))
        self.conn.commit()

    def get_logs(self):
        self.cursor.execute('SELECT * FROM ai_model_usage')
        return self.cursor.fetchall()

if __name__ == "__main__":
    # Example usage
    db_handler = DBHandler()
    print(db_handler.get_logs())