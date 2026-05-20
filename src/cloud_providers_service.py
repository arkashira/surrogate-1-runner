import schedule
import time
from src.cloud_providers import CloudProvider

def get_cloud_provider(provider_name):
    return CloudProvider(provider_name)

def update_cost_data(provider_name):
    cloud_provider = get_cloud_provider(provider_name)
    cost_data = cloud_provider.get_cost_data()
    # This is a placeholder for the actual logic to update the cost data.
    # It should be implemented based on the requirements.
    pass

schedule.every(5).minutes.do(update_cost_data, 'aws')

while True:
    schedule.run_pending()
    time.sleep(1)