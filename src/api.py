from flask import Flask, request, jsonify
from .ai_models.Claude import ClaudeAIModel

app = Flask(__name__)

claude_ai = ClaudeAIModel(api_key="your_api_key_here")

@app.route('/query-claude', methods=['POST'])
def query_claude():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = claude_ai.query_model(prompt)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/model-capabilities', methods=['GET'])
def model_capabilities():
    try:
        capabilities = claude_ai.get_model_capabilities()
        return jsonify(capabilities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)