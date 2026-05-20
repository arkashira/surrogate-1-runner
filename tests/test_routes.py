import pytest
from app import create_app
from models import db, User, Term

@pytest.fixture
def client():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test user
            user = User(username='testuser')
            db.session.add(user)
            db.session.commit()
            # Create test term
            term = Term(word='Cloud Computing', definition='Distributed computing over network', category='Cloud')
            db.session.add(term)
            db.session.commit()
        yield client

def test_mark_term_learned(client):
    # Get auth token
    response = client.post('/login', json={'username': 'testuser'})
    assert response.status_code == 200
    token = response.json['access_token']
    
    # Mark term as learned
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/terms/1/learned', headers=headers)
    assert response.status_code == 201
    assert response.json['msg'] == 'Term marked as learned'
    
    # Verify it's persisted
    with client.application.app_context():
        user = User.query.first()
        assert len(user.learned_terms) == 1
        assert user.learned_terms[0].word == 'Cloud Computing'