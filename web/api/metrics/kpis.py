
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/metrics/kpis')
def kpis():
    # Fetch KPIs from the database or another data source
    kpis = [
        {'name': 'Active Users', 'value': 12345},
        {'name': 'Daily Revenue', 'value': 54321},
        {'name': 'Conversion Rate', 'value': 0.05}
    ]
    return jsonify(kpis)

if __name__ == '__main__':
    app.run(debug=True)