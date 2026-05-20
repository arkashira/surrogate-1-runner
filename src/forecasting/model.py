from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from .data import get_prepared_data

class CostForecastModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = LinearRegression()

    def train(self):
        X_train, X_test, y_train, y_test = get_prepared_data(self.data_path)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f'Training completed. Mean Squared Error: {mse}')

    def predict(self, input_data):
        return self.model.predict(input_data)


def train_and_forecast(data_path):
    model = CostForecastModel(data_path)
    model.train()
    return model