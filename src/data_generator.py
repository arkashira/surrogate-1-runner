
import random
import string
import numpy as np
import pandas as pd

def generate_synthetic_data(num_rows=1000):
    data = {
        'timestamp': pd.date_range(start='1/1/2022', periods=num_rows, freq='H'),
        'metric_name': np.random.choice(['cpu_usage', 'memory_usage', 'disk_usage'], num_rows),
        'value': np.random.rand(num_rows) * 100,
        'host': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) for _ in range(num_rows)
    }
    return pd.DataFrame(data)

# /opt/axentx/surrogate-1/tests/test_data_generator.py

import unittest
import pandas as pd
from src.data_generator import generate_synthetic_data

class TestDataGenerator(unittest.TestCase):

    def test_generate_synthetic_data(self):
        df = generate_synthetic_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1000)
        self.assertIn('timestamp', df.columns)
        self.assertIn('metric_name', df.columns)
        self.assertIn('value', df.columns)
        self.assertIn('host', df.columns)

if __name__ == '__main__':
    unittest.main()

## Summary
- Implemented synthetic data generation function in `data_generator.py`
- Added unit test for `generate_synthetic_data` function in `test_data_generator.py`
- Synthetic data includes columns: 'timestamp', 'metric_name', 'value', 'host'
- Data generation function creates 1000 rows of data by default