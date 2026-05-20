import logging
from axentx_common.models import ShardTrace, CostGovernanceAction
from src.relevance_alert_collector import collect_alerts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_drill_down(shard_id, request_id):
    # Fetch shard-level query trace visualization for the given shard_id and request_id
    trace = ShardTrace.get_trace(shard_id, request_id)

    if not trace:
        logger.info(f'No trace found for shard {shard_id} and request {request_id}.')
        return

    # Highlight the exact request causing the issue in the trace visualization
    trace.highlight_request(request_id)

    # Fetch recent cost-governance actions related to the selected shard
    actions = CostGovernanceAction.get_recent_actions(shard_id)

    # Display the fetched trace visualization and cost-governance actions
    display_trace(trace)
    display_actions(actions)

    logger.info("Drill-down handling completed")

if __name__ == "__main__":
    # Example usage: handle_drill_down('shard123', 'request456')
    logger.info("Handling drill-down for shard 'shard123' and request 'request456'")
    handle_drill_down('shard123', 'request456')