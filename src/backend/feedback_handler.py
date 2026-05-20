import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create a connection to the SQLite database
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS feedback
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             name TEXT, 
             email TEXT, 
             feedback TEXT)''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

# Define a route for the feedback form
@app.route('/feedback', methods=['POST'])
def collect_feedback():
    data = request.get_json()
    name = data['name']
    email = data['email']
    feedback = data['feedback']

    # Connect to the database
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()

    # Insert the feedback into the database
    c.execute("INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)", (name, email, feedback))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    return jsonify({'message': 'Feedback collected successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)