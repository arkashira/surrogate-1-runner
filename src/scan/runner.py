import os
import subprocess
from github import Github

# Configuration (should be moved to environment variables in production)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_github_token")
REPO_OWNER = os.getenv("REPO_OWNER", "axentx")
REPO_NAME = os.getenv("REPO_NAME", "surrogate-1")
RULE_SETS = ["HIPAA", "SOC2"]  # Supported compliance rule sets

def run_compliance_scan(rule_sets=None):
    """Run compliance scan with specified rule sets.

    Args:
        rule_sets: List of rule sets to scan (default: RULE_SETS)

    Returns:
        tuple: (stdout, returncode)
    """
    if rule_sets is None:
        rule_sets = RULE_SETS

    command = ["compliance-scan", "--rules"] + rule_sets
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout, result.returncode

def post_comment(pr_number, comment):
    """Post a comment to a GitHub pull request.

    Args:
        pr_number: Pull request number
        comment: Text to post as comment
    """
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)

def scan_and_post_comment(pr_number):
    """Run compliance scans and post results to PR.

    Args:
        pr_number: Pull request number to comment on
    """
    results = []
    return_codes = []

    # Run scans for all rule sets
    for rule_set in RULE_SETS:
        output, return_code = run_compliance_scan([rule_set])
        results.append(f"### {rule_set} Results:\n