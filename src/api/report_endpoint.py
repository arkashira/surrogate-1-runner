from flask import Flask, send_file, make_response
from io import StringIO
import csv
import pandas as pd

app = Flask(__name__)

@app.route('/reports/<tenant_id>/latest.csv')
def latest_csv(tenant_id):
    # Assuming data is fetched from a DataFrame df
    df = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar'],
        'total_spend_usd': [100, 200, 300],
        'spend_change_pct': [10, 20, 30],
        'service': ['A', 'B', 'C'],
        'service_spend_usd': [50, 100, 150],
        'recommendation': ['D', 'E', 'F'],
        'recommendation_savings_usd': [20, 40, 60]
    })

    # Ensure file size is <= 200KB
    if df.memory_usage(index=False).sum() <= 200 * 1024:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_NONNUMERIC)
        csv_buffer.seek(0)

        response = make_response(send_file(csv_buffer, as_attachment=True, attachment_filename='latest.csv', mimetype='text/csv'))
        response.headers['Content-Disposition'] = 'attachment; filename=latest.csv'
        return response
    else:
        return 'File size exceeds 200KB', 500

if __name__ == '__main__':
    app.run(debug=True)