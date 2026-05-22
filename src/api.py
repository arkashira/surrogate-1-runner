from flask import Flask, request, jsonify
from deployer import SurrogateDeployer

app = Flask(__name__)
deployer = SurrogateDeployer()

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.json
    template_url = data.get('template_url')
    stack_name = data.get('stack_name')
    parameters = data.get('parameters', [])

    if not template_url or not stack_name:
        return jsonify({'error': 'template_url and stack_name are required'}), 400

    try:
        response = deployer.deploy_environment(template_url, stack_name, parameters)
        return jsonify({'message': 'Deployment started', 'stack_id': response['StackId']}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    data = request.json
    stack_name = data.get('stack_name')

    if not stack_name:
        return jsonify({'error': 'stack_name is required'}), 400

    try:
        response = deployer.cleanup_environment(stack_name)
        return jsonify({'message': 'Cleanup started', 'stack_id': response['StackId']}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)