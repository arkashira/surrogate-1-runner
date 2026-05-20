import time
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_with_exponential_backoff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 5
        base_delay = 1
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt + 1 < max_retries:
                    delay = base_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retries reached. Marking dataset as failed.")
                    # Logic to mark dataset as failed and log it
                    raise
    return wrapper

@retry_with_exponential_backoff
def download_dataset(dataset_url):
    # Simulate a download process that might fail
    import random
    if random.random() < 0.5:
        raise Exception("Download failed")
    logger.info("Dataset downloaded successfully")

# Example usage
if __name__ == "__main__":
    download_dataset("http://example.com/dataset")