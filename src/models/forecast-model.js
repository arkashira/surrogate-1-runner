import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def forecast_model(data):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data.drop('cost', axis=1), data['cost'], test_size=0.2, random_state=42)

    # Create and train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the testing set
    predictions = model.predict(X_test)

    # Calculate the mean squared error
    mse = mean_squared_error(y_test, predictions)

    return model, mse

def predict_costs(model, data):
    return model.predict(data)

# Example usage
data = pd.DataFrame({
    'cost': [100, 200, 300, 400, 500],
    'category': ['A', 'B', 'C', 'D', 'E']
})

model, mse = forecast_model(data)
print(f'Mean squared error: {mse}')

predictions = predict_costs(model, data)
print(f'Predicted costs: {predictions}')