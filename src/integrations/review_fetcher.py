"""
ReviewFetcher Service

This service fetches component reviews from an external review API,
aggregates the ratings, and extracts the top 3 most helpful comments.
It is designed to be used by the surrogate-1 ingestion pipeline
to enrich component metadata with real‑world satisfaction data.

The external API is expected to return a JSON payload in the following
shape:

{
    "component_id": "<id>",
    "reviews": [
        {
            "rating": 4,                 # integer 1-5
            "comment": "Great component!",
            "helpful_votes": 12          # integer
        },
        ...
    ]
}

If the API returns an empty list or the request fails, the service
returns a placeholder indicating that no reviews are available.
"""

import os
import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import requests

log = logging.getLogger(__name__)

# Default API endpoint; can be overridden by REVIEW_API_URL env var
API_BASE_URL = os.getenv("REVIEW_API_URL", "https://api.example.com/reviews")

# Timeout for HTTP requests in seconds
REQUEST_TIMEOUT = 5


@dataclass
class Review:
    rating: int
    comment: str
    helpful_votes: int


class ReviewFetcher:
    """
    Service responsible for retrieving and processing reviews for a component.
    """

    def __init__(self, api_base_url: str = API_BASE_URL, timeout: int = REQUEST_TIMEOUT):
        self.api_base_url = api_base_url.rstrip("/")
        self.timeout = timeout

    def _fetch_from_api(self, component_id: str) -> Optional[Dict[str, Any]]:
        """
        Internal helper to perform the HTTP GET request.
        Returns the parsed JSON or None on failure.
        """
        url = f"{self.api_base_url}/{component_id}"
        try:
            log.debug("Fetching reviews from %s", url)
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            log.warning("Failed to fetch reviews for %s: %s", component_id, exc)
            return None

    def _parse_reviews(self, data: Dict[str, Any]) -> List[Review]:
        """
        Convert raw JSON into a list of Review objects.
        """
        reviews_raw = data.get("reviews", [])
        reviews = []
        for r in reviews_raw:
            try:
                review = Review(
                    rating=int(r.get("rating", 0)),
                    comment=str(r.get("comment", "")),
                    helpful_votes=int(r.get("helpful_votes", 0)),
                )
                reviews.append(review)
            except (ValueError, TypeError) as exc:
                log.debug("Skipping malformed review entry %s: %s", r, exc)
        return reviews

    def _aggregate_rating(self, reviews: List[Review]) -> Dict[str, Any]:
        """
        Compute the average rating and total count.
        """
        if not reviews:
            return {"average": None, "count": 0}
        total = sum(r.rating for r in reviews)
        avg = round(total / len(reviews), 2)
        return {"average": avg, "count": len(reviews)}

    def _top_comments(self, reviews: List[Review], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Return the top `limit` comments sorted by helpful_votes descending.
        """
        sorted_reviews = sorted(reviews, key=lambda r: r.helpful_votes, reverse=True)
        top = sorted_reviews[:limit]
        return [
            {"comment": r.comment, "helpful_votes": r.helpful_votes}
            for r in top
        ]

    def get_component_reviews(self, component_id: str) -> Dict[str, Any]:
        """
        Public API: fetches reviews, aggregates rating, and extracts top comments.

        Returns a dictionary with keys:
            - average_rating: float or None
            - rating_count: int
            - top_comments: list of dicts
            - placeholder: bool (True if no reviews were found)
        """
        data = self._fetch_from_api(component_id)
        if not data:
            return {
                "average_rating": None,
                "rating_count": 0,
                "top_comments": [],
                "placeholder": True,
            }

        reviews = self._parse_reviews(data)
        rating_info = self._aggregate_rating(reviews)
        top_comments = self._top_comments(reviews)

        return {
            "average_rating": rating_info["average"],
            "rating_count": rating_info["count"],
            "top_comments": top_comments,
            "placeholder": rating_info["count"] == 0,
        }