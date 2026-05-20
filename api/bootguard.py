import csv
from flask import Flask, request, jsonify, send_file
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample data for collision incidents
collision_incidents = [
    {"device": "Device A", "service_name": "Service 1", "severity": "high", "resolution_status": "resolved", "timestamp": datetime.now() - timedelta(days=1)},
    {"device": "Device B", "service_name": "Service 2", "severity": "medium", "resolution_status": "unresolved", "timestamp": datetime.now() - timedelta(days=5)},
    # Add more sample data as needed
]

@app.route('/api/collision-incidents/csv', methods=['GET'])
def export_csv():
    # Filter parameters
    service_name = request.args.get('service_name')
    severity = request.args.get('severity')
    resolution_status = request.args.get('resolution_status')
    
    # Filter incidents based on query parameters
    filtered_incidents = [
        incident for incident in collision_incidents
        if (service_name is None or incident['service_name'] == service_name) and
           (severity is None or incident['severity'] == severity) and
           (resolution_status is None or incident['resolution_status'] == resolution_status)
    ]
    
    # Create CSV response using csv module for better handling
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["device", "service_name", "severity", "resolution_status", "timestamp"])
    for incident in filtered_incidents:
        cw.writerow([incident['device'], incident['service_name'], incident['severity'], incident['resolution_status'], incident['timestamp'].isoformat()])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=collision_incidents.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True)