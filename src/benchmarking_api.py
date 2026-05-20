import csv
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load performance data from CSV
def load_performance_data():
    with open('/opt/axentx/surrogate-1/src/performance_data.csv', mode='r') as file:
        reader = csv.DictReader(file)
        data = {row['rig_config']: row for row in reader}
    return data

performance_data = load_performance_data()

@app.route('/api/benchmark', methods=['GET'])
def benchmark():
    current_rig = request.args.get('current_rig')
    proposed_upgrades = request.args.get('proposed_upgrades')

    if not current_rig or not proposed_upgrades:
        return jsonify({'error': 'Missing current_rig or proposed_upgrades parameters'}), 400

    current_performance = performance_data.get(current_rig, {})
    proposed_performance = performance_data.get(proposed_upgrades, {})

    comparison = {
        'current_rig': current_rig,
        'proposed_upgrades': proposed_upgrades,
        'current_performance': current_performance,
        'proposed_performance': proposed_performance,
        'comparison_metrics': {
            'fps_improvement': float(proposed_performance.get('fps', 0)) - float(current_performance.get('fps', 0)),
            'latency_improvement': float(current_performance.get('latency', 0)) - float(proposed_performance.get('latency', 0))
        }
    }

    return jsonify(comparison)

if __name__ == '__main__':
    app.run(debug=True)