import unittest
from app import app, db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        response = self.app.post('/register', json={'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully!', response.data)

    def test_login(self):
        self.app.post('/register', json={'email': 'test@example.com', 'password': 'password123'})
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_login_invalid(self):
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials!', response.data)

if __name__ == '__main__':
    unittest.main()