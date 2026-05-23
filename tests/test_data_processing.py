import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.data_processing import calculate_pl

class TestDataProcessing(unittest.TestCase):
    @patch('src.data_processing.get_db_connection')
    def test_calculate_pl(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock the database query result
        mock_cursor.fetchone.return_value = (1000.0,)

        # Calculate the date range for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        # Call the function
        pl = calculate_pl(start_date, end_date)

        # Assert that the database connection and cursor were used correctly
        mock_get_db_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            """
            SELECT SUM(revenue) - SUM(expenses) AS pl
            FROM financial_data
            WHERE date BETWEEN %s AND %s
            """,
            (start_date, end_date)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

        # Assert that the P&L is calculated correctly
        self.assertEqual(pl, 1000.0)

if __name__ == '__main__':
    unittest.main()