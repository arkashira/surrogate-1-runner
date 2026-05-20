from flask import Flask, Response, request
import csv
from io import StringIO
from datetime import datetime
from .datastore import get_data_for_export
from surrogate_1.models import db, Usage  # Assuming Usage model exists

app = Flask(__name__)

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    # Query parameters for filtering (optional)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Create CSV generator for streaming
    def generate_csv():
        # Create CSV writer
        output = StringIO()
        writer = csv.writer(output)

        # Write headers
        writer.writerow(['date', 'model', 'endpoint', 'tokens', 'cost', 'team'])

        # Get data (either from datastore or direct query)
        if hasattr(get_data_for_export, '__call__'):
            # Use provided data source
            data = get_data_for_export()
        else:
            # Direct database query with efficient streaming
            query = db.session.query(
                Usage.timestamp.label('date'),
                Usage.model_name.label('model'),
                Usage.endpoint.label('endpoint'),
                Usage.tokens.label('tokens'),
                Usage.cost.label('cost'),
                Usage.team_id.label('team')
            )

            if start_date and end_date:
                query = query.filter(
                    Usage.timestamp.between(start_date, end_date)
                )

            # Stream results in batches
            for chunk in query.yield_per(1000):
                for row in chunk:
                    formatted_date = row.date.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([
                        formatted_date,
                        row.model,
                        row.endpoint,
                        row.tokens,
                        f'{row.cost:.4f}',
                        row.team
                    ])
                    yield output.getvalue().encode('utf-8')
                    output.seek(0)
                    output.truncate()
        else:
            # Fallback to provided data
            for row in data:
                writer.writerow(row)
                yield output.getvalue().encode('utf-8')
                output.seek(0)
                output.truncate()

    return Response(
        generate_csv(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=export.csv'
        }
    )

if __name__ == '__main__':
    app.run(debug=True)