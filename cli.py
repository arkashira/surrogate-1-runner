import click

@click.command()
@click.option('--url', required=True, help='The URL to trigger the workflow.')
@click.option('--alert-id', required=True, help='The alert ID to diagnose.')
def diagnose(url, alert_id):
    """
    Simulates triggering a workflow for diagnosing an alert.
    
    Args:
        url (str): The URL to trigger the workflow.
        alert_id (str): The alert ID to diagnose.
    
    Outputs:
        Prints the incident ID and a download URL for the incident report.
    """
    # Simulate triggering the workflow
    incident_id = "incident-12345"  # Placeholder for actual incident ID generation
    download_url = f"{url}/download/{incident_id}"  # Placeholder for actual download URL
    print(f"Incident ID: {incident_id}")
    print(f"Download URL: {download_url}")

if __name__ == '__main__':
    diagnose()