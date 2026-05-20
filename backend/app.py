from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load price stub data
with open('data/price_stub.json') as f:
    price_stub = json.load(f)

# Define a route for the ROI calculation
@app.route('/api/v1/roi', methods=['POST'])
def calculate_roi():
    # Get the current rig and candidate components from the request
    data = request.get_json()
    current_rig = data['current_rig']
    candidate_components = data['candidate_components']

    # Initialize the response
    response = []

    # Iterate over the candidate components
    for component in candidate_components:
        # Get the price of the component from the price stub data
        component_price = next((c['price_usd'] for c in price_stub['components'] if c['component_id'] == component['component_id']), None)

        # If the price is missing, skip this component
        if component_price is None:
            continue

        # Calculate the projected FPS gain per dollar (this is a placeholder, the actual calculation will depend on the benchmark data)
        projected_fps = 10.0  # Replace with actual calculation
        fps_per_usd = projected_fps / component_price

        # Add the component to the response
        response.append({
            'component_id': component['component_id'],
            'projected_fps': projected_fps,
            'price_usd': component_price,
            'fps_per_usd': fps_per_usd
        })

    # Return the response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)