import subprocess
import argparse
from rollback import generate_rollback_command

def send_alert(deployment_id, alert_channel):
    """
    Send an alert to the specified channel with rollback instructions.

    Args:
        deployment_id (str): The ID of the deployment that introduced breaking changes.
        alert_channel (str): The channel to send the alert to (e.g., 'slack', 'email').
    """
    rollback_command = generate_rollback_command(deployment_id)
    alert_message = f"Breaking changes detected in deployment {deployment_id}. Rollback command: {rollback_command}"

    if alert_channel == 'slack':
        subprocess.run(['slack-notify', alert_message])
    elif alert_channel == 'email':
        subprocess.run(['send-email', '--subject', 'Breaking Changes Detected', '--body', alert_message])
    else:
        print(f"Unsupported alert channel: {alert_channel}")

def main():
    parser = argparse.ArgumentParser(description='Send an alert with rollback instructions.')
    parser.add_argument('deployment_id', type=str, help='The ID of the deployment that introduced breaking changes')
    parser.add_argument('alert_channel', type=str, help='The channel to send the alert to (e.g., "slack", "email")')
    args = parser.parse_args()

    send_alert(args.deployment_id, args.alert_channel)

if __name__ == "__main__":
    main()