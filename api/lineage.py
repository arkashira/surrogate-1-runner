from flask import Flask, jsonify
from .data_store import get_model_lineage

app = Flask(__name__)

@app.route('/api/lineage/<model_id>', methods=['GET'])
def get_lineage(model_id):
    lineage_data = get_model_lineage(model_id)
    return jsonify(lineage_data)

if __name__ == '__main__':
    app.run(debug=True)