from flask import Flask, jsonify
from .data_store import get_data_provenance

app = Flask(__name__)

@app.route('/api/provenance/<data_id>', methods=['GET'])
def get_provenance(data_id):
    provenance_data = get_data_provenance(data_id)
    return jsonify(provenance_data)

if __name__ == '__main__':
    app.run(debug=True)