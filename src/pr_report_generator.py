import requests
import json
from slack_notifier import send_report_to_slack
from config import load_config, get_slack_enabled, get_github_token

def generate_pr_report(selected_tests, coverage_gaps):
    report = f"### Selected Tests\n"
    report += "| Test | Status |\n"
    report += "| --- | --- |\n"
    for test in selected_tests:
        report += f"| {test['name']} | {test['status']} |\n"
    report += "\n### Coverage Gaps\n"
    report += "| File | Coverage |\n"
    report += "| --- | --- |\n"
    for gap in coverage_gaps:
        report += f"| {gap['file']} | {gap['coverage']} |\n"
    return report

def post_report_to_pr(report, pr_number):
    github_token = get_github_token()
    headers = {'Authorization': f'token {github_token}', 'Content-Type': 'application/json'}
    data = {'body': report}
    response = requests.post(f'https://api.github.com/repos/axentx/surrogate-1/issues/{pr_number}/comments', headers=headers, data=json.dumps(data))
    if response.status_code != 201:
        print(f"Failed to post report to PR: {response.text}")

def send_report(config, selected_tests, coverage_gaps, pr_number):
    report = generate_pr_report(selected_tests, coverage_gaps)
    post_report_to_pr(report, pr_number)
    if get_slack_enabled(config):
        send_report_to_slack(config, report)