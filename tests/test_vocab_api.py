import pytest
from fastapi.testclient import TestClient
from src.api.vocab import router

client = TestClient(router)

def test_get_vocab_list():
    response = client.get("/vocab")
    assert response.status_code == 200
    data = response.json()
    assert len(data["terms"]) == 10
    for term in data["terms"]:
        assert "word" in term
        assert "definition" in term
        assert "example_sentence" in term
        assert "category" in term

def test_mark_term_as_learned():
    term = {
        "word": "Cloud",
        "definition": "A model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources.",
        "example_sentence": "We moved our infrastructure to the cloud to improve scalability.",
        "category": "Cloud"
    }
    response = client.post("/vocab/mark_learned", json=term)
    assert response.status_code == 200