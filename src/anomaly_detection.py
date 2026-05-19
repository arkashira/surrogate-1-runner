import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

class AnomalyDetector:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

    def detect_anomalies(self):
        # Get the last 30 days of data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        query = text("""
            SELECT date, SUM(daily_spend) as total_spend
            FROM cost_data
            WHERE date BETWEEN :start_date AND :end_date
            GROUP BY date
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {'start_date': start_date, 'end_date': end_date})
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        # Calculate mean and standard deviation
        mean_spend = df['total_spend'].mean()
        std_spend = df['total_spend'].std()

        # Identify anomalies
        anomalies = df[df['total_spend'] > mean_spend + 3 * std_spend]

        # Store anomalies in the database
        if not anomalies.empty:
            anomalies['is_anomaly'] = True
            anomalies.to_sql('cost_anomalies', self.engine, if_exists='append', index=False)

        return anomalies