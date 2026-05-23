from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Dummy data structure to simulate budget limits storage
budget_limits = {}

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        service = request.form['service']
        limit = float(request.form['limit'])
        budget_limits[service] = limit
        return jsonify({'status': 'success', 'message': f'Budget limit set for {service} to {limit}'})
    else:
        return render_template('settings.html', budget_limits=budget_limits)

if __name__ == '__main__':
    app.run(debug=True)