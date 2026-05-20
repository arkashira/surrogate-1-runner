from typing import Dict
import boto3
from botocore.exceptions import ClientError
from src.utils.logger import log_error

class TaggingService:
    """
    Service that talks to AWS EC2 to apply tags.
    """

    def __init__(self, ec2_client=None):
        """
        Parameters
        ----------
        ec2_client : boto3.client, optional
            Allows injection of a mock client for testing.
        """
        self.ec2_client = ec2_client or boto3.client("ec2")

    def apply_tags(self, resource_id: str, tags: Dict[str, str]) -> bool:
        """
        Apply the given tags to the specified EC2 resource.

        Returns
        -------
        bool
            True if the tags were applied successfully, False otherwise.
        """
        try:
            tag_list = [{"Key": k, "Value": v} for k, v in tags.items()]
            self.ec2_client.create_tags(Resources=[resource_id], Tags=tag_list)
            return True
        except ClientError as exc:
            log_error(f"Failed to apply tags to {resource_id}: {exc}")
            return False