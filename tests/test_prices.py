import unittest
from datetime import datetime
from app import create_app, db
from app.models import Component, Price

class PriceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.component = Component(name='Test Component', description='Test Description')
            db.session.add(self.component)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_component_prices(self):
        with self.app.app_context():
            price1 = Price(component_id=self.component.id, vendor='Vendor1', price=100.0)
            price2 = Price(component_id=self.component.id, vendor='Vendor2', price=90.0)
            db.session.add_all([price1, price2])
            db.session.commit()

        response = self.client.get(f'/api/components/{self.component.id}/prices')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['vendor'], 'Vendor2')
        self.assertEqual(data[1]['vendor'], 'Vendor1')

    def test_get_component_current_price(self):
        with self.app.app_context():
            price = Price(component_id=self.component.id, vendor='Vendor1', price=100.0)
            db.session.add(price)
            db.session.commit()

        response = self.client.get(f'/api/components/{self.component.id}/price')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['current_price'], 100.0)
        self.assertEqual(data['vendor'], 'Vendor1')

    def test_get_component_current_price_no_data(self):
        response = self.client.get(f'/api/components/{self.component.id}/price')
        self.assertEqual(response.status_code, 404)