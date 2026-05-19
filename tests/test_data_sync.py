import unittest
from unittest.mock import patch
from src.models.data_sync import sync_invoice_data, fetch_latest_invoices
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestDataSync(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        from src.models.data_sync import Base
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @patch('src.models.data_sync.fetch_latest_invoices')
    def test_sync_invoice_data(self, mock_fetch_latest_invoices):
        mock_fetch_latest_invoices.return_value = [
            {'invoice_number': 'INV001', 'amount': 100, 'date': '2023-01-01', 'customer_id': 1},
            {'invoice_number': 'INV002', 'amount': 200, 'date': '2023-01-02', 'customer_id': 2}
        ]
        
        sync_invoice_data(self.engine)
        
        session = self.Session()
        invoices = session.query(Invoice).all()
        
        self.assertEqual(len(invoices), 2)
        self.assertEqual(invoices[0].amount, 100)
        self.assertEqual(invoices[1].amount, 200)

if __name__ == '__main__':
    unittest.main()