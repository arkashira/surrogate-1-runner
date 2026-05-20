import logging

def log_ingestion(source, review_id, timestamp):
    logging.info(f"Ingested review from {source} with ID {review_id} at {timestamp}")

def save_review_to_db(review):
    # Placeholder for database saving logic
    print(f"Saving review to DB: {review}")