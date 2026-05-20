from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/terraform/recommendations', methods=['GET'])
def get_recommendations():
    # Placeholder logic for generating recommendations
    recommendations = [
        {
            "description": "Resize VM instances",
            "expected_savings_percentage": 20,
            "implementation_steps": ["Apply Terraform configuration"]
        },
        {
            "description": "Optimize storage usage",
            "expected_savings_percentage": 15,
            "implementation_steps": ["Remove unused data", "Compress data"]
        }
    ]
    return jsonify(recommendations)

@app.route('/api/terraform/resize', methods=['POST'])
def resize_resources():
    data = request.json
    terraform_config_path = data.get('terraform_config_path')
    
    try:
        result = subprocess.run(['terraform', 'apply', '-auto-approve', terraform_config_path], capture_output=True, text=True, check=True)
        return jsonify({"status": "success", "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.stderr}), 500

if __name__ == '__main__':
    app.run(debug=True)