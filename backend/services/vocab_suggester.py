"""
Vocabulary suggestion engine for the surrogate-1 backend.

Features
--------
* Load a curated list of 500 IT terms at startup.
* Detect terms in a given text and return tooltip data.
* Track user mastery of each term in an in-memory store.
"""

import json
import os
import re
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Path to the curated terms file (JSON array of objects with `term`, `definition`, `example`).
# The file should contain exactly 500 entries as per the PRD.
TERMS_FILE = os.path.join(os.path.dirname(__file__), "terms.json")

# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #

class Term:
    """Represents a single vocabulary term."""
    def __init__(self, term: str, definition: str, example: str):
        self.term = term
        self.definition = definition
        self.example = example

    def to_dict(self) -> Dict[str, str]:
        return {
            "term": self.term,
            "definition": self.definition,
            "example": self.example,
        }

class VocabSuggester:
    """
    Core engine that loads terms, provides suggestions, and tracks mastery.
    """
    def __init__(self, terms_file: str = TERMS_FILE):
        self.terms_file = terms_file
        self._terms: Dict[str, Term] = {}
        self._mastery: Dict[str, Dict[str, bool]] = {}  # user_id -> {term: mastered}
        self._load_terms()

    # ----------------------------------------------------------------------- #
    # Term loading
    # ----------------------------------------------------------------------- #
    def _load_terms(self) -> None:
        """Load terms from the JSON file into the internal dictionary."""
        if not os.path.exists(self.terms_file):
            raise FileNotFoundError(f"Terms file not found: {self.terms_file}")

        with open(self.terms_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Terms file must contain a JSON array")

        for entry in data:
            if not all(k in entry for k in ("term", "definition", "example")):
                raise ValueError(f"Invalid term entry: {entry}")
            term_obj = Term(entry["term"], entry["definition"], entry["example"])
            self._terms[term_obj.term.lower()] = term_obj

        # Verify we have 500 terms
        if len(self._terms) != 500:
            raise ValueError(f"Expected 500 terms, found {len(self._terms)}")

    # ----------------------------------------------------------------------- #
    # Suggestion logic
    # ----------------------------------------------------------------------- #
    def get_suggestions(self, text: str) -> List[Dict[str, str]]:
        """
        Return a list of tooltip data for terms found in the input text.

        Parameters
        ----------
        text : str
            The AI response or user input to scan for terms.

        Returns
        -------
        List[Dict[str, str]]
            Each dict contains `term`, `definition`, and `example`.
        """
        if not text:
            return []

        # Build a regex that matches any of the terms as whole words, case-insensitive
        # Escape terms to avoid regex meta characters
        escaped_terms = [re.escape(t) for t in self._terms.keys()]
        pattern = r"\b(" + "|".join(escaped_terms) + r")\b"
        regex = re.compile(pattern, flags=re.IGNORECASE)

        found_terms = set()
        for match in regex.finditer(text):
            found_terms.add(match.group(0).lower())

        suggestions = [self._terms[t].to_dict() for t in found_terms]
        return suggestions

    # ----------------------------------------------------------------------- #
    # Mastery tracking
    # ----------------------------------------------------------------------- #
    def record_mastery(self, user_id: str, term: str, mastered: bool = True) -> None:
        """
        Record that a user has mastered (or not) a term.

        Parameters
        ----------
        user_id : str
            Unique identifier for the user.
        term : str
            The term being mastered.
        mastered : bool
            True if mastered, False otherwise.
        """
        term_key = term.lower()
        if term_key not in self._terms:
            raise ValueError(f"Term '{term}' not recognized")

        user_store = self._mastery.setdefault(user_id, {})
        user_store[term_key] = mastered

    def get_mastery(self, user_id: str) -> Dict[str, bool]:
        """
        Retrieve mastery status for all terms for a given user.

        Parameters
        ----------
        user_id : str

        Returns
        -------
        Dict[str, bool]
            Mapping of term -> mastered status.
        """
        return self._mastery.get(user_id, {}).copy()

    # ----------------------------------------------------------------------- #
    # Utility
    # ----------------------------------------------------------------------- #
    def list_terms(self) -> List[str]:
        """Return a list of all terms."""
        return list(self._terms.keys())

# --------------------------------------------------------------------------- #
# Singleton instance for use across the application
# --------------------------------------------------------------------------- #
vocab_suggester = VocabSuggester()