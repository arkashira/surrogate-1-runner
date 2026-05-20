import pytest
from surrogate_1.models import ExampleModel

def test_example_model():
    model = ExampleModel(items=[])
    model.add_item("test")
    assert len(model.items) == 1
    assert model.items[0] == "test"

def test_model_serialization():
    model = ExampleModel(items=["test1", "test2"])
    data = model.dict()
    assert data["items"] == ["test1", "test2"]

    json_data = model.json()
    assert "test1" in json_data
    assert "test2" in json_data