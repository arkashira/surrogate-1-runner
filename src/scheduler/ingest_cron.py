import os
import schedule
import time
from src.aws_ingest import ingest_aws_resources

def job():
    ingest_aws_resources()
    print("Inventory ingested at", time.ctime())

schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)