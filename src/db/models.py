import sqlite3

class SchemaChange:
    def __init__(self, commit_hash, diff):
        self.commit_hash = commit_hash
        self.diff = diff

    @staticmethod
    def save_change(db_path, commit_hash, diff):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            # Check if the change already exists
            cursor.execute('''
                SELECT id FROM schema_changes WHERE commit_hash = ?
            ''', (commit_hash,))
            existing_change = cursor.fetchone()
            
            if existing_change:
                print(f"Change with commit_hash {commit_hash} already exists.")
                return
            
            cursor.execute('''
                INSERT INTO schema_changes (commit_hash, diff)
                VALUES (?, ?)
            ''', (commit_hash, diff))
            
            connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_history(db_path, limit):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            cursor.execute('''
                SELECT commit_hash, timestamp, diff
                FROM schema_changes
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            changes = cursor.fetchall()
            return changes
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def change_exists(db_path, commit_hash):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            cursor.execute('''
                SELECT id FROM schema_changes WHERE commit_hash = ?
            ''', (commit_hash,))
            
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if connection:
                connection.close()

    @staticmethod
    def delete_change(db_path, commit_hash):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            cursor.execute('''
                DELETE FROM schema_changes WHERE commit_hash = ?
            ''', (commit_hash,))
            
            connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if connection:
                connection.close()