import psycopg2
from psycopg2.extras import DictCursor
from utils.config import get_db_config

class HistoricalUsageDB:
    def __init__(self):
        self.conn = psycopg2.connect(**get_db_config())
        
    def query_usage_by_date_range(self, start_date, end_date):
        """Retrieve historical usage records between dates"""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT usage_date, SUM(cost) as cost
                FROM cloud_usage
                WHERE usage_date BETWEEN %s AND %s
                GROUP BY usage_date
                ORDER BY usage_date
            """, (start_date, end_date))
            return [dict(row) for row in cur.fetchall()]
            
    def save_forecast(self, forecast_df):
        """Store generated forecasts in database"""
        with self.conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO cost_forecasts (forecast_date, predicted_cost)
                VALUES (%s, %s)
                ON CONFLICT (forecast_date) DO UPDATE
                SET predicted_cost = EXCLUDED.predicted_cost
            """, list(forecast_df.itertuples(index=False, name=None)))
        self.conn.commit()