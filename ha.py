import time
import json
from deployment import deploy_workflow
from utils import load_config, check_node_health

class HighAvailabilityManager:
    def __init__(self, workflow_id, config_file):
        self.workflow_id = workflow_id
        self.config = load_config(config_file)
        self.backup_nodes = self.config["backup_nodes"]
        self.primary_node = self.config["primary_node"]

    def monitor_and_switch(self):
        while True:
            if not check_node_health(self.primary_node):
                print(f"Primary node {self.primary_node} is down. Switching to backup.")
                for backup in self.backup_nodes:
                    if check_node_health(backup):
                        self.switch_to_backup(backup)
                        break
            time.sleep(5)

    def check_node_health(self, node):
        return check_node_health(node)

    def switch_to_backup(self, backup_node):
        print(f"Switching to backup node {backup_node}.")
        deploy_workflow(self.workflow_id, backup_node)

if __name__ == "__main__":
    workflow_id = "workflow123"
    config_file = "config.json"
    ha_manager = HighAvailabilityManager(workflow_id, config_file)
    ha_manager.monitor_and_switch()