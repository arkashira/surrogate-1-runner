import os
import subprocess
from datetime import datetime

class WorkflowManager:
    def __init__(self, shard_id):
        self.shard_id = shard_id
        self.dataset_repo = "axentx/surrogate-1-dataset"
        self.dataset_enrich_script = "bin/dataset-enrich.sh"

    def generate_design_files(self):
        # Generate design files using the dataset enrich script
        command = f"{self.dataset_enrich_script} {self.shard_id}"
        subprocess.run(command, shell=True, check=True)

    def manage_design_files(self):
        # Manage design files by uploading to the dataset repo
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = f"output/shard_{self.shard_id}/{timestamp}"
        command = f"git clone https://github.com/{self.dataset_repo}.git && cd {self.dataset_repo} && mkdir -p {output_path} && cp -r ../../output/* {output_path}/ && git add {output_path} && git commit -m 'Add design files for shard {self.shard_id}' && git push"
        subprocess.run(command, shell=True, check=True)

    def run_workflow(self):
        self.generate_design_files()
        self.manage_design_files()

if __name__ == "__main__":
    shard_id = os.getenv("SHARD_ID")
    if shard_id is not None:
        workflow_manager = WorkflowManager(shard_id)
        workflow_manager.run_workflow()