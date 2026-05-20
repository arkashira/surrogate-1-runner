from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

router = APIRouter()

class Term(BaseModel):
    word: str
    definition: str
    example_sentence: str
    category: str

class VocabList(BaseModel):
    terms: List[Term]

vocab_data = [
    {
        "word": "Cloud",
        "definition": "A model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources.",
        "example_sentence": "We moved our infrastructure to the cloud to improve scalability.",
        "category": "Cloud"
    },
    # ... more terms ...
]

@router.get("/vocab", response_model=VocabList)
def get_vocab_list():
    selected_terms = random.sample(vocab_data, 10)
    return {"terms": selected_terms}

@router.post("/vocab/mark_learned")
def mark_term_as_learned(term: Term):
    # Logic to persist learned term in user profile
    pass