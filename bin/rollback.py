import subprocess
import argparse

def generate_rollback_command(deployment_id):
    """
    Generate a rollback command for a given deployment ID.

    Args:
        deployment_id (str): The ID of the deployment to rollback.

    Returns:
        str: The rollback command.
    """
    return f"kubectl rollout undo deployment/{deployment_id}"

def main():
    parser = argparse.ArgumentParser(description='Generate rollback command for a deployment.')
    parser.add_argument('deployment_id', type=str, help='The ID of the deployment to rollback')
    args = parser.parse_args()

    rollback_command = generate_rollback_command(args.deployment_id)
    print(f"Rollback command: {rollback_command}")

if __name__ == "__main__":
    main()