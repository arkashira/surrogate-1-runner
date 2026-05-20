import os
import time
from flask import Flask, render_template, request
from gcp_billing_client import GCPBillingClient

app = Flask(__name__)
billing_client = GCPBillingClient()

@app.route('/')
def dashboard():
    project_id = request.args.get('project_id')
    resource_type = request.args.get('resource_type')
    cost_data = billing_client.fetch_cost_data(project_id, resource_type)
    return render_template('dashboard.html', cost_data=cost_data)

def update_cost_data():
    while True:
        time.sleep(300)  # Update every 5 minutes

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))