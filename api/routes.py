from flask import Flask, request, jsonify
from ingestion import ingest_dataset

app = Flask(__name__)

@app.route('/ingest', methods=['POST'])
def ingest():
    dataset_name = request.json['dataset_name']
    dataset_data = request.json['dataset_data']
    
    # Start the ingestion job within 5 seconds of API request
    import threading
    def start_ingestion():
        ingest_dataset(dataset_name, dataset_data)
    threading.Thread(target=start_ingestion).start()
    
    return jsonify({'message': 'Ingestion job started successfully'}), 200