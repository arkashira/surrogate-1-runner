from retry_strategy import RetryStrategy
from error_classifier import ErrorClassifier
import time

def process_batch(batch):
    # Simulate processing a batch
    if batch % 2 == 0:
        raise Exception("Batch processing failed")
    return f"Processed batch {batch}"

def main():
    retry_strategy = RetryStrategy(max_retries=3, initial_delay=1.0, backoff_factor=2.0)
    error_classifier = ErrorClassifier()

    for batch in range(1, 11):
        try:
            result = retry_strategy.execute_with_retry(process_batch, batch)
            print(result)
        except Exception as e:
            error_type = error_classifier.classify_error(str(e))
            print(f"Failed to process batch {batch}: {error_type} error")

if __name__ == "__main__":
    main()