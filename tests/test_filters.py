
import pytest
from src.filters import app, TimeRangeFilter, ServiceFilter

@pytest.fixture(scope="module")
def test_data():
    # Assuming you have some test data in the database
    pass

def test_get_filtered_cost_data():
    # Test with valid data
    app.dependency_overrides({"Depends(get_db)": None})
    with app.test_client() as client:
        response = client.get(
            "/cost_data/filter/",
            params={
                "start_date": "2022-01-01",
                "end_date": "2022-01-31",
                "service": "service1",
            },
        )
        assert response.status_code == 200
        assert len(response.json()) > 0

    # Test with invalid data
    with pytest.raises(HTTPException):
        app.dependency_overrides({"Depends(get_db)": None})
        with app.test_client() as client:
            client.get(
                "/cost_data/filter/",
                params={
                    "start_date": "invalid_date",
                    "end_date": "invalid_date",
                    "service": "service1",
                },
            )