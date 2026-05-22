import subprocess
import json
import requests
from datetime import datetime
from .utils.notifier import send_alert

def listen_for_git_hooks():
    while True:
        result = subprocess.run(['git', 'log', '-1', '--pretty=format:%H'], capture_output=True, text=True)
        latest_commit_hash = result.stdout.strip()

        if is_vulnerable_commit(latest_commit_hash):
            alert_data = {
                'timestamp': datetime.now().isoformat(),
                'commit_hash': latest_commit_hash,
                'remediation_steps': get_remediation_steps(latest_commit_hash)
            }
            send_alert('Git Hook Listener', json.dumps(alert_data))

def is_vulnerable_commit(commit_hash):
    # Real scenario: Use a vulnerability scanner or API to check for known vulnerabilities
    # For now, using a placeholder condition
    return 'vulnerable_code' in subprocess.run(['git', 'show', commit_hash], capture_output=True, text=True).stdout

def get_remediation_steps(commit_hash):
    return [
        f'Revert commit {commit_hash}',
        'Review changes for security issues',
        'Update dependencies to patched versions'
    ]

if __name__ == "__main__":
    listen_for_git_hooks()