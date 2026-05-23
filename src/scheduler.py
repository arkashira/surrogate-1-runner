import schedule
import time
from src.cost_forecast.cost_forecast import generate_cost_forecast

def update_model():
    generate_cost_forecast()

schedule.every().day.at("00:00").do(update_model)

while True:
    schedule.run_pending()
    time.sleep(1)