import json
import logging
from pathlib import Path
from typing import Dict, List

import boto3
import yaml

from collector import MetricsCollector
from recommender import RecommendationEngine
from writer import RecommendationWriter

log = logging.getLogger(__name__)


class EC2RightsizingEngine:
    def __init__(self, cfg_path: str = "config.yaml"):
        self.cfg = yaml.safe_load(Path(cfg_path).read_text())
        self.region = self.cfg["region"]
        self.profile = self.cfg.get("profile")
        self.session = boto3.Session(profile_name=self.profile) if self.profile else boto3.Session()
        self.ec2 = self.session.client("ec2", region_name=self.region)

        # Load instance database
        self.instance_db = yaml.safe_load(Path("instance_db.yaml").read_text())

        # Initialise sub‑components
        self.collector = MetricsCollector(self.session, self.region, self.cfg)
        self.recommender = RecommendationEngine(
            self.instance_db,
            low_util=self.cfg["low_utilization"],
            high_util=self.cfg["high_utilization"],
        )
        self.writer = RecommendationWriter(
            self.session,
            bucket=self.cfg["output_bucket"],
            prefix=self.cfg["output_prefix"],
        )

    def analyze_instance(self, instance_id: str) -> Dict:
        """Return a recommendation dict for a single instance."""
        metrics = self.collector.get_instance_utilization(instance_id)
        rec = self.recommender.recommend(instance_id, metrics)
        return rec.to_dict()

    def analyze_all(self) -> List[Dict]:
        """Analyze all running instances in the region."""
        recs = []
        for instance in self.ec2.describe_instances()["Reservations"]:
            for inst in instance["Instances"]:
                if inst["State"]["Name"] != "running":
                    continue
                rec = self.analyze_instance(inst["InstanceId"])
                recs.append(rec)
                self.writer.write(rec)
        return recs