from flask import Flask, request, jsonify, send_file
import csv
import io
import time
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Mock data generator for demonstration
def generate_mock_differences(count=200):
    severities = ["Critical", "Warning", "Info"]
    databases = ["production", "staging", "analytics"]
    scripts = ["user_migration.sql", "data_cleanup.sql", "schema_update.sql"]
    
    differences = []
    for i in range(count):
        diff = {
            "id": i + 1,
            "severity": random.choice(severities),
            "database": random.choice(databases),
            "script_name": random.choice(scripts),
            "sql_script_link": f"/scripts/{random.choice(scripts)}",
            "database_logs_link": f"/logs/{random.choice(databases)}_{random.choice(scripts)}.log",
            "detected_at": (datetime.utcnow() - timedelta(minutes=random.randint(0, 60))).isoformat()
        }
        differences.append(diff)
    return differences

# In-memory storage for demo (replace with real database in production)
DIFFERENCES = generate_mock_differences()

@app.route('/api/diffs', methods=['GET'])
def get_differences():
    # Get query parameters
    severity = request.args.get('severity')
    database = request.args.get('database')
    script_name = request.args.get('script_name')
    format_type = request.args.get('format', 'json')
    
    # Filter differences
    filtered_diffs = DIFFERENCES.copy()
    if severity:
        filtered_diffs = [d for d in filtered_diffs if d['severity'] == severity]
    if database:
        filtered_diffs = [d for d in filtered_diffs if d['database'] == database]
    if script_name:
        filtered_diffs = [d for d in filtered_diffs if d['script_name'] == script_name]
    
    # Return CSV if requested
    if format_type == 'csv':
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'id', 'severity', 'database', 'script_name', 
            'sql_script_link', 'database_logs_link', 'detected_at'
        ])
        writer.writeheader()
        writer.writerows(filtered_diffs)
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            attachment_filename='differences.csv'
        )
    
    # Return JSON response
    return jsonify({
        "differences": filtered_diffs,
        "total": len(filtered_diffs),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/diffs/refresh', methods=['POST'])
def refresh_differences():
    # Simulate data refresh (replace with actual refresh logic)
    global DIFFERENCES
    DIFFERENCES = generate_mock_differences()
    return jsonify({"status": "refreshed", "count": len(DIFFERENCES)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)