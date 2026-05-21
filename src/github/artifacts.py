import os
import json
import requests
from github import Github

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
REPO_NAME = os.getenv("GITHUB_REPO_NAME")
ARTIFACT_NAME = "compliance-report.sarif"

def upload_artifact(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/artifacts",
            headers={
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            },
            files={"file": (ARTIFACT_NAME, f)}
        )
    response.raise_for_status()
    return response.json()

def create_sarif_report(scan_results, tool_name, tool_version):
    sarif_report = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": tool_name,
                    "version": tool_version
                }
            },
            "results": scan_results
        }]
    }
    return sarif_report

def save_sarif_file(report, file_path):
    with open(file_path, 'w') as f:
        json.dump(report, f, indent=2)

def upload_sarif_artifact(scan_results, tool_name, tool_version, workflow_run_id):
    sarif_report = create_sarif_report(scan_results, tool_name, tool_version)
    sarif_file_path = '/tmp/compliance-report.sarif'
    save_sarif_file(sarif_report, sarif_file_path)
    upload_artifact(sarif_file_path)

    # Upload the SARIF file as a GitHub artifact using the ArtifactUploader class
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    uploader = ArtifactUploader(GITHUB_TOKEN, REPO_NAME)
    download_link = uploader.upload_sarif_artifact(sarif_report, workflow_run_id)

    return download_link

# Example usage
# scan_results = [...]  # Your scan results here
# tool_name = "AxentX Scanner"
# tool_version = "1.0.0"
# workflow_run_id = 12345  # Your workflow run ID here
# download_link = upload_sarif_artifact(scan_results, tool_name, tool_version, workflow_run_id)
# print(download_link)