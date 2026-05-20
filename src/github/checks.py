import os
import requests

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/check-runs"

def create_check_run(owner, repo, name, conclusion, output):
    url = GITHUB_API_URL.format(owner=owner, repo=repo)
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": name,
        "head_sha": os.getenv('GITHUB_SHA'),
        "status": "completed",
        "conclusion": conclusion,
        "output": {
            "title": "Scan Results",
            "summary": output['summary'],
            "text": output['text'],
            "annotations": output.get('annotations', [])
        }
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

def handle_scan_results(violations):
    if violations:
        conclusion = "failure"
        output = {
            "summary": "Violations detected in the scan.",
            "text": "Please refer to the detailed findings.",
            "annotations": [{"path": "path/to/artifact", "message": "Detailed findings available here."}]
        }
        create_check_run(os.getenv('GITHUB_REPOSITORY_OWNER'), os.getenv('GITHUB_REPOSITORY'), "Security Scan", conclusion, output)
        if os.getenv('COMPLIANCE_ENFORCE') == 'true':
            raise SystemExit("Scan failed due to violations.")
    else:
        conclusion = "success"
        output = {
            "summary": "No violations detected.",
            "text": "All checks passed."
        }
        create_check_run(os.getenv('GITHUB_REPOSITORY_OWNER'), os.getenv('GITHUB_REPOSITORY'), "Security Scan", conclusion, output)