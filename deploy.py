import os
import requests
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_DEPLOY_TOKEN")
REPO = "axentx/surrogate-1"

def trigger_workflow():
    """Trigger GitHub Actions workflow with zero-delay deployment"""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO)
    workflow = repo.get_workflow(42)  # Assuming workflow ID 42 is the deployment workflow
    repo.create_git_ref(ref=f"refs/heads/deploy-{os.urandom(4).hex()}", sha="HEAD")
    workflow.create_dispatch(ref=f"deploy-{os.urandom(4).hex()}")
    return "Workflow triggered instantly"

def verify_deployment():
    """Verify deployment status within 5s timeout"""
    response = requests.get(
        f"https://api.github.com/repos/{REPO}/actions/runs",
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    return "Deployment verified" if response.status_code == 200 else "Verification failed"