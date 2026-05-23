import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from cron_jobs.daily_pl_refresh import refresh_daily_pl

class TestDailyPLRefresh(unittest.TestCase):
    @patch('cron_jobs.daily_pl_refresh.calculate_pl')
    @patch('cron_jobs.daily_pl_refresh.get_db_connection')
    def test_refresh_daily_pl(self, mock_get_db_connection, mock_calculate_pl):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock the calculate_pl function
        mock_calculate_pl.return_value = 1000.0

        # Call the function
        refresh_daily_pl()

        # Assert that calculate_pl was called with the correct date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        mock_calculate_pl.assert_called_once_with(start_date, end_date)

        # Assert that the database connection and cursor were used correctly
        mock_get_db_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO daily_pl (date, pl)
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE SET pl = EXCLUDED.pl
            """,
            (end_date.date(), 1000.0)
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()