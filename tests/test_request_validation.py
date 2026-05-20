import pytest
from flask import Flask, request, jsonify
from src.middleware.request_validation import validate_component_filters

@pytest.fixture
def app():
    app = Flask(__name__)
    @app.route('/api/components', methods=['GET'])
    @validate_component_filters
    def get_components():
        return jsonify({'status': 'success'})
    return app

def test_valid_filters(app):
    with app.test_client() as client:
        response = client.get('/api/components?brand=BrandA&min_price=100&max_price=200&min_benchmark=50')
        assert response.status_code == 200

def test_invalid_brand(app):
    with app.test_client() as client:
        response = client.get('/api/components?brand=123')
        assert response.status_code == 400
        assert b'Brand must be a string' in response.data

def test_invalid_min_price(app):
    with app.test_client() as client:
        response = client.get('/api/components?min_price=abc')
        assert response.status_code == 400
        assert b'Minimum price must be a number' in response.data

def test_invalid_max_price(app):
    with app.test_client() as client:
        response = client.get('/api/components?max_price=abc')
        assert response.status_code == 400
        assert b'Maximum price must be a number' in response.data

def test_invalid_min_benchmark(app):
    with app.test_client() as client:
        response = client.get('/api/components?min_benchmark=abc')
        assert response.status_code == 400
        assert b'Minimum benchmark score must be a number' in response.data

def test_min_price_greater_than_max_price(app):
    with app.test_client() as client:
        response = client.get('/api/components?min_price=200&max_price=100')
        assert response.status_code == 400
        assert b'Minimum price cannot be greater than maximum price' in response.data