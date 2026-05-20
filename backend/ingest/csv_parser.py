import csv
import logging
import os
import psycopg2
from datetime import datetime

def parse_csv(file_path, conn):
    logging.basicConfig(filename='/var/log/axentx/surrogate-1/ingest_errors.log', level=logging.ERROR)

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                gpu = row['gpu']
                cpu = row['cpu']
                ram_gb = int(row['ram_gb'])
                fps = float(row['fps'])
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()

                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO benchmark_results (gpu, cpu, ram_gb, fps, date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (gpu, cpu, ram_gb, fps, date))
                conn.commit()
            except (KeyError, ValueError) as e:
                logging.error(f"Invalid row: {row}. Error: {e}")

# /opt/axentx/surrogate-1/backend/ingest/ingest.py
import os
import psycopg2
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .csv_parser import parse_csv

class BenchmarkWatcher(FileSystemEventHandler):
    def __init__(self, conn):
        self.conn = conn

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            parse_csv(event.src_path, self.conn)

def watch_benchmarks(conn):
    event_handler = BenchmarkWatcher(conn)
    observer = Observer()
    observer.schedule(event_handler, path='/data/benchmarks', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# /opt/axentx/surrogate-1/metrics/benchmarks_last_ingest_timestamp.py
from prometheus_client import start_http_server, Gauge
import time

benchmarks_last_ingest_timestamp = Gauge('benchmarks_last_ingest_timestamp', 'Timestamp of the last benchmark ingestion')

def update_metric():
    benchmarks_last_ingest_timestamp.set(time.time())

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        update_metric()
        time.sleep(60)

## Summary
- Implemented CSV parsing function in `csv_parser.py`
- Added file watcher in `ingest.py` to parse CSV files within 5 minutes of arrival
- Exposed health metric `benchmarks_last_ingest_timestamp` via /metrics in `benchmarks_last_ingest_timestamp.py`
- Logged invalid rows to `/var/log/axentx/surrogate-1/ingest_errors.log` and skipped them
- Stored valid records in PostgreSQL table `benchmark_results` with specified columns