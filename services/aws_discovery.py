import boto3
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

# Define the resource types we want to scan
RESOURCE_TYPES = ["ec2", "s3", "rds"]

def list_regions() -> List[str]:
    """Return a list of all available AWS regions."""
    ec2 = boto3.client("ec2")
    return [r["RegionName"] for r in ec2.describe_regions()["Regions"]]

def discover_resources(account_id: str, region: str) -> List[Dict[str, Any]]:
    """
    Discover resources in a given account and region.
    Returns a list of dicts with resource metadata.
    """
    session = boto3.Session(profile_name=account_id, region_name=region)
    resources = []

    # EC2 instances
    ec2 = session.client("ec2")
    try:
        for reservation in ec2.describe_instances()["Reservations"]:
            for instance in reservation["Instances"]:
                resources.append(
                    {
                        "account": account_id,
                        "region": region,
                        "type": "ec2",
                        "id": instance["InstanceId"],
                        "tags": instance.get("Tags", []),
                        "created_at": instance["LaunchTime"],
                    }
                )
    except Exception as e:
        logger.error(f"Error discovering EC2 instances: {e}")

    # S3 buckets (global, but we include region for consistency)
    s3 = session.client("s3")
    try:
        for bucket in s3.list_buckets()["Buckets"]:
            try:
                tag_set = s3.get_bucket_tagging(Bucket=bucket["Name"]).get("TagSet", [])
            except Exception:
                tag_set = []  # Handle cases where tagging is not enabled
            resources.append(
                {
                    "account": account_id,
                    "region": region,
                    "type": "s3",
                    "id": bucket["Name"],
                    "tags": tag_set,
                    "created_at": bucket["CreationDate"],
                }
            )
    except Exception as e:
        logger.error(f"Error discovering S3 buckets: {e}")

    # RDS instances
    rds = session.client("rds")
    try:
        for db in rds.describe_db_instances()["DBInstances"]:
            resources.append(
                {
                    "account": account_id,
                    "region": region,
                    "type": "rds",
                    "id": db["DBInstanceIdentifier"],
                    "tags": rds.list_tags_for_resource(ResourceName=db["DBInstanceArn"]).get(
                        "TagList", []
                    ),
                    "created_at": db["InstanceCreateTime"],
                }
            )
    except Exception as e:
        logger.error(f"Error discovering RDS instances: {e}")

    return resources

def find_orphans(resources: List[Dict[str, Any]], age_threshold_days: int = 7) -> List[Dict[str, Any]]:
    """
    Flag resources that have no tags and are older than the threshold.
    """
    threshold = datetime.now(timezone.utc) - timedelta(days=age_threshold_days)
    orphans = []
    for res in resources:
        if not res["tags"] and res["created_at"] < threshold:
            orphans.append(res)
    return orphans

# /opt/axentx/surrogate-1/tasks/resource_scanner.py
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any
from celery import Celery

from services.aws_discovery import list_regions, discover_resources, find_orphans

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("resource_scanner")

# Placeholder for connected accounts; in real usage this would come from a config or DB
CONNECTED_ACCOUNTS = ["default"]  # using default AWS profile for demo

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def scan_all_accounts() -> List[Dict[str, Any]]:
    """
    Scan all connected accounts and regions for orphaned resources.
    Returns a list of orphaned resource dicts.
    """
    all_orphans: List[Dict[str, Any]] = []
    regions = list_regions()
    logger.info(f"Discovered regions: {regions}")

    for account in CONNECTED_ACCOUNTS:
        logger.info(f"Scanning account: {account}")
        for region in regions:
            logger.info(f"  Region: {region}")
            resources = discover_resources(account, region)
            orphans = find_orphans(resources, age_threshold_days=7)
            if orphans:
                logger.info(f"    Found {len(orphans)} orphaned resources")
                all_orphans.extend(orphans)
    return all_orphans

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls scan_all_accounts every 24 hours.
    sender.add_periodic_task(86400.0, scan_all_accounts.s(), name='scan-all-accounts')

def main():
    orphans = scan_all_accounts()
    if orphans:
        logger.info(f"Total orphaned resources found: {len(orphans)}")
        for orphan in orphans:
            logger.info(
                f"{orphan['type']} {orphan['id']} in {orphan['region']} (account {orphan['account']})"
            )
    else:
        logger.info("No orphaned resources found.")

if __name__ == "__main__":
    main()