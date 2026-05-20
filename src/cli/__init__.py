import click
from .wizard import wizard_cmd

@click.group()
def main():
    """Surrogate-1 CLI"""
    pass

main.add_command(wizard_cmd)