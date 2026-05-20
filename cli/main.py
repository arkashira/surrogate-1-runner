import click
from surrogate1.cli.commands.status import status

@click.group()
def cli():
    """surrogate-1 CLI tool."""
    pass

cli.add_command(status)

if __name__ == "__main__":
    cli()