import csv
from io import StringIO
from flask import make_response
from .models import Difference  # Assuming a model named Difference exists

def generate_csv(differences):
    """Generate CSV content from a list of differences."""
    fieldnames = ['id', 'severity', 'script_name', 'database', 'details']
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    for diff in differences:
        writer.writerow({
            'id': diff.id,
            'severity': diff.severity,
            'script_name': diff.script_name,
            'database': diff.database,
            'details': diff.details
        })
    return csv_buffer.getvalue()

def export_differences_to_csv():
    """Export all differences to a CSV file."""
    differences = Difference.query.all()  # Adjust query based on actual data retrieval method
    csv_content = generate_csv(differences)
    
    response = make_response(csv_content)
    response.headers['Content-Disposition'] = 'attachment; filename=differences.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

# Example usage in a Flask route
# @app.route('/api/export/csv')
# def export_csv():
#     return export_differences_to_csv()