import pytest
import requests
import json

BASE_URL = "http://localhost:8000/api/components"

def test_filter_by_brand():
    response = requests.get(f"{BASE_URL}?brand=brand1")
    assert response.status_code == 200
    data = json.loads(response.text)
    assert all(component['brand'] == 'brand1' for component in data['results'])

def test_filter_by_price_range():
    response = requests.get(f"{BASE_URL}?min_price=100&max_price=500")
    assert response.status_code == 200
    data = json.loads(response.text)
    assert all(100 <= component['price'] <= 500 for component in data['results'])

def test_filter_by_performance():
    response = requests.get(f"{BASE_URL}?min_score=80")
    assert response.status_code == 200
    data = json.loads(response.text)
    assert all(component['benchmark_score'] >= 80 for component in data['results'])

def test_invalid_query_params():
    response = requests.get(f"{BASE_URL}?invalid_param=test")
    assert response.status_code == 400
    data = json.loads(response.text)
    assert 'error' in data

def test_pagination():
    response = requests.get(f"{BASE_URL}?page=2")
    assert response.status_code == 200
    data = json.loads(response.text)
    assert data['page'] == 2

## Summary
- Added tests for filtering by brand, price range, and performance.
- Added tests for invalid query parameters and pagination.