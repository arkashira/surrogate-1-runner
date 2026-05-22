import unittest
from api.progress import progress_blueprint, db, Progress
from flask import Flask
import json

class TestProgressAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(self.app)
        self.app.register_blueprint(progress_blueprint)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_get_progress(self):
        with self.app.app_context():
            session = db.session
            new_progress = Progress(user_id=1, quiz_score=0.5)
            session.add(new_progress)
            session.commit()
        response = self.client.get('/progress')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1)

    def test_create_progress(self):
        data = {'user_id': 1, 'quiz_score': 0.5}
        response = self.client.post('/progress', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['user_id'], 1)

    def test_reset_progress(self):
        with self.app.app_context():
            session = db.session
            new_progress = Progress(user_id=1, quiz_score=0.5)
            session.add(new_progress)
            session.commit()
        data = {'user_id': 1, 'confirm': True}
        response = self.client.post('/progress/reset', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Progress reset successfully')

if __name__ == '__main__':
    unittest.main()