from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Mock data for demonstration purposes
components_data = [
    {"name": "Component A", "fps_gain": 30, "cost": 150},
    {"name": "Component B", "fps_gain": 45, "cost": 250},
    {"name": "Component C", "fps_gain": 60, "cost": 350},
]

@app.route('/')
def index():
    # Get filter and sort parameters from URL query string
    sort_by = request.args.get('sort_by', 'fps_gain')
    order = request.args.get('order', 'asc')
    filter_fps = request.args.get('filter_fps')

    # Apply filters
    filtered_components = components_data
    if filter_fps:
        filtered_components = [c for c in components_data if c['fps_gain'] >= int(filter_fps)]

    # Apply sorting
    if order == 'desc':
        filtered_components = sorted(filtered_components, key=lambda x: x[sort_by], reverse=True)
    else:
        filtered_components = sorted(filtered_components, key=lambda x: x[sort_by])

    return render_template('templates.html', components=filtered_components)

if __name__ == '__main__':
    app.run(debug=True)