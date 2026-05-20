import requests
import json
from datetime import datetime
from .utils import log_ingestion, save_review_to_db

class AmazonReviewFetcher:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.amazon.com/reviews"

    def fetch_reviews(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}:{self.api_secret}'
        }
        response = requests.get(self.base_url, headers=headers)
        if response.status_code == 200:
            reviews = response.json()
            for review in reviews:
                self.process_review(review)
        else:
            print(f"Failed to fetch reviews: {response.status_code}")

    def process_review(self, review):
        unified_schema_review = {
            'source': 'Amazon',
            'review_id': review['id'],
            'content': review['content'],
            'rating': review['rating'],
            'timestamp': datetime.fromisoformat(review['timestamp'])
        }
        save_review_to_db(unified_schema_review)
        log_ingestion('Amazon', review['id'], datetime.now())

def start_amazon_ingestion():
    fetcher = AmazonReviewFetcher('your_api_key', 'your_api_secret')
    fetcher.fetch_reviews()

if __name__ == "__main__":
    start_amazon_ingestion()