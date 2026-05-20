import pandas as pd
from sklearn.model_selection import train_test_split

class CostDataLoader:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_data(self):
        return pd.read_csv(self.data_path)

    def preprocess_data(self, data):
        # Perform necessary preprocessing steps such as handling missing values, encoding categorical variables, etc.
        return data.fillna(0)  # Example: Fill missing values with 0

    def split_data(self, data):
        X = data.drop('cost', axis=1)
        y = data['cost']
        return train_test_split(X, y, test_size=0.2, random_state=42)


def get_prepared_data(data_path):
    loader = CostDataLoader(data_path)
    raw_data = loader.load_data()
    processed_data = loader.preprocess_data(raw_data)
    X_train, X_test, y_train, y_test = loader.split_data(processed_data)
    return X_train, X_test, y_train, y_test