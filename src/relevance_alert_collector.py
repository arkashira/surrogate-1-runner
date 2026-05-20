import os
import json
import logging
from axentx_common.models import RelevanceAlert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def collect_alerts():
    alerts_path = '/path/to/relevance_alerts.json'
    if not os.path.exists(alerts_path):
        logger.info('No relevance alerts found.')
        return []

    with open(alerts_path, 'r') as f:
        alerts = json.load(f)

    # Process each alert and store relevant data
    for alert in alerts:
        # Extract shard_id and request_id from the alert data
        shard_id = alert['shard_id']
        request_id = alert['request_id']

        # Store the extracted data for drill-down
        RelevanceAlert.store_shard_request(shard_id, request_id)

    logger.info("Relevance alert collection completed")

if __name__ == "__main__":
    logger.info("Starting relevance alert collection")
    collect_alerts()