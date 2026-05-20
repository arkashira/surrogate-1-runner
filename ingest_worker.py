import time
from .metrics import initialize_metrics

metrics = initialize_metrics()

def ingest_data(data):
    try:
        start_time = time.time()
        
        # Simulate data ingestion process
        time.sleep(2)  # Simulating ingestion delay
        
        end_time = time.time()
        duration = end_time - start_time
        metrics.observe_duration(duration)
        
        # Simulate successful ingestion
        print("Data ingested successfully")
        
    except Exception as e:
        print(f"Ingestion failed: {str(e)}")
        metrics.increment_failure()

if __name__ == "__main__":
    # Example data ingestion call
    ingest_data("example_data")