import click
from surrogate1.core.upgrade import get_upgrade_status
from surrogate1.utils.formatting import format_status

@click.command()
def status():
    """Query the current upgrade status."""
    status_data = get_upgrade_status()
    formatted_status = format_status(status_data)
    click.echo(formatted_status)