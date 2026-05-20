import schedule
import time
from datetime import datetime
from catalog import Catalog
from benchmark_sources import fetch_benchmarks

def normalize_and_store_benchmarks():
    """
    Fetches benchmark data from various sources, normalizes it, and stores it in the catalog.
    """
    sources = ['PassMark', 'UserBenchmark', 'Geekbench']
    all_benchmarks = {}

    for source in sources:
        benchmarks = fetch_benchmarks(source)
        for component_id, score in benchmarks.items():
            if component_id not in all_benchmarks:
                all_benchmarks[component_id] = []
            all_benchmarks[component_id].append(score)

    # Normalize and calculate composite scores
    normalized_scores = {}
    for component_id, scores in all_benchmarks.items():
        avg_score = sum(scores) / len(scores)
        normalized_scores[component_id] = avg_score

    # Store in catalog
    catalog = Catalog()
    catalog.update_benchmarks(normalized_scores)

def refresh_benchmarks_job():
    print(f"Refreshing benchmarks at {datetime.now()}")
    normalize_and_store_benchmarks()

# Schedule the job to run weekly
schedule.every().monday.at("00:00").do(refresh_benchmarks_job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)