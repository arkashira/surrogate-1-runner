from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/opt/axentx/surrogate-1/workflows'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def list_workflows():
    """List all workflow files with metadata"""
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.json'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            stat = os.stat(filepath)
            with open(filepath, 'r') as f:
                content = json.load(f)
            files.append({
                'name': filename,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'status': content.get('status', 'draft'),
                'tags': content.get('tags', []),
                'path': filepath
            })
    return sorted(files, key=lambda x: x['modified'], reverse=True)

@app.route('/')
def dashboard():
    """Main dashboard view"""
    workflows = list_workflows()
    return render_template('dashboard.html', workflows=workflows)

@app.route('/workflow/<filename>')
def view_workflow(filename):
    """View specific workflow file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    with open(filepath, 'r') as f:
        content = json.load(f)
    
    return render_template('workflow_editor.html', 
                          filename=filename,
                          content=json.dumps(content, indent=2))

@app.route('/api/workflows', methods=['GET', 'POST'])
def manage_workflows():
    """API endpoint for workflow management"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not file.filename.endswith('.json'):
            return jsonify({'error': 'Only JSON files allowed'}), 400
            
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'Workflow saved',
            'filename': filename,
            'path': filepath
        }), 201

    return jsonify({'workflows': list_workflows()})

@app.route('/api/workflow/<filename>', methods=['PUT', 'DELETE'])
def edit_workflow(filename):
    """Edit or delete a workflow"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
        
    if request.method == 'DELETE':
        os.remove(filepath)
        return jsonify({'message': 'Workflow deleted'}), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({'message': 'Workflow updated'}), 200

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)