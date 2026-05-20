from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Load historical cost data
historical_data = pd.read_csv('path/to/historical_cost_data.csv')

# Train forecasting model
X = historical_data[['feature1', 'feature2']]  # Replace with actual features
y = historical_data['cost']
model = LinearRegression()
model.fit(X, y)

@app.route('/forecast', methods=['GET'])
def forecast():
    # Get filter parameters from request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by')

    # Apply filters and sorting
    filtered_data = historical_data[(historical_data['date'] >= start_date) & (historical_data['date'] <= end_date)]
    sorted_data = filtered_data.sort_values(by=sort_by)

    # Generate forecasts
    forecasts = model.predict(sorted_data[['feature1', 'feature2']])

    return render_template('forecast.html', forecasts=forecasts, data=sorted_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)