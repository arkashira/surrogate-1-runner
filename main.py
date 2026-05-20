import schedule
import time
from alerts import AlertManager
from config import Config

def main():
    alert_manager = AlertManager(Config.ALERT_THRESHOLD)
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()