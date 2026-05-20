import os
import pytest
import requests
from testcontainers.postgres import PostgresContainer
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="module")
def testcontainers_postgres():
    with PostgresContainer("postgres:14.5") as postgres:
        # Seed benchmark data
        os.environ["DATABASE_URL"] = postgres.get_connection_url()
        os.system("python3 /opt/axentx/surrogate-1/bin/seed_benchmark_data.py")
        yield postgres

def test_recommendation_flow(testcontainers_postgres):
    # Override database URL for test
    os.environ["DATABASE_URL"] = testcontainers_postgres.get_connection_url()
    
    # Test payload with current rig and $500 budget
    payload = {
        "current_rig": {
            "cpu": "Intel i5-12600K",
            "gpu": "NVIDIA RTX 3060",
            "ram": "16GB DDR4"
        },
        "budget": 500
    }
    
    # Send request to API endpoint
    response = requests.post(
        "http://localhost:8000/api/recommend",
        json=payload,
        timeout=10
    )
    
    # Assert response status and content
    assert response.status_code == 200
    data = response.json()
    assert len(data["bundles"]) > 0
    
    # Verify all bundles stay within budget
    for bundle in data["bundles"]:
        total_price = sum(item["price"] for item in bundle["components"])
        assert total_price <= 500, f"Bundle {bundle['id']} exceeds budget: ${total_price}"