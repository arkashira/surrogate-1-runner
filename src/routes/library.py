
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import sqlite3  # Assuming SQLite is used for demonstration

app = Flask(__name__)

# Sample database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Replace with actual DB connection
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/library', methods=['GET'])
def get_library():
    conn = get_db_connection()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Query to fetch documents with sorting
    query = """
    SELECT title, source, last_opened_at, open_count
    FROM documents
    WHERE last_opened_at >= ?
    ORDER BY last_opened_at DESC, open_count DESC
    LIMIT 1000
    """
    
    documents = conn.execute(query, (thirty_days_ago,)).fetchall()
    conn.close()
    
    # Format the response
    response = [
        {
            'title': doc['title'],
            'source': doc['source'],
            'last_opened_at': doc['last_opened_at']
        }
        for doc in documents
    ]
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)