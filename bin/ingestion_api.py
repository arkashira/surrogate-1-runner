from flask import Flask, request, jsonify
import os
from markdown_ingestion import parse_markdown, store_qa_pairs

app = Flask(__name__)

@app.route('/ingest', methods=['POST'])
def ingest_markdown():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.md'):
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        qa_pairs = parse_markdown(file_path)
        store_qa_pairs(qa_pairs, 'path/to/surrogate-1/database.db')
        os.remove(file_path)
        return jsonify({'message': 'File ingested successfully', 'qa_pairs': qa_pairs}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)