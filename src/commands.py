import click
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configuration
DATA_DIR = Path('/opt/axentx/surrogate-1/data')
DATA_FILE = DATA_DIR / 'accounts.json'

def load_accounts() -> dict:
    """Load accounts from JSON file, returning empty dict if file doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_accounts(accounts: dict) -> None:
    """Persist accounts to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)

def initialize_account(account_id: str, accounts: dict) -> dict:
    """Create new account record if it doesn't exist."""
    if account_id not in accounts:
        accounts[account_id] = {
            'id': account_id,
            'status': 'pending',
            'steps': {},
            'history': []
        }
    return accounts[account_id]

def log_history(account: dict, action: str, **details) -> None:
    """Add timestamped entry to account history."""
    account['history'].append({
        'timestamp': datetime.now().isoformat(),
        'action': action,
        **details,
        'updated_by': 'cli'
    })

@click.group()
def cli():
    """Account verification management CLI."""
    pass

@cli.command()
@click.option('--account-id', required=True, help='Account ID to update')
@click.option('--status', type=click.Choice(['in_progress', 'verified', 'failed']), help='New verification status')
@click.option('--step', help='Specific step to mark complete')
def update_status(account_id: str, status: Optional[str], step: Optional[str]):
    """Update verification status for an account."""
    accounts = load_accounts()
    account = initialize_account(account_id, accounts)
    
    if status:
        old_status = account['status']
        account['status'] = status
        log_history(account, 'status_change', old_status=old_status, new_status=status)
        click.echo(f"Status changed from '{old_status}' to '{status}'")
    
    if step:
        account['steps'][step] = {'completed': True, 'timestamp': datetime.now().isoformat()}
        log_history(account, 'step_complete', step=step)
        click.echo(f"Step '{step}' marked complete")
    
    save_accounts(accounts)
    click.echo(f"Updated account {account_id}")

@cli.command()
@click.option('--account-id', required=True, help='Account ID to display')
def status(account_id: str):
    """Display current verification status for an account."""
    accounts = load_accounts()
    
    if account_id not in accounts:
        click.echo(f"Account '{account_id}' not found. Use update_status to create it.")
        return
    
    account = accounts[account_id]
    
    click.echo(f"\n=== Account: {account_id} ===")
    click.echo(f"Status: {account['status'].upper()}")
    
    if account['steps']:
        click.echo("\nCompleted Steps:")
        for step, info in account['steps'].items():
            click.echo(f"  - {step}: {info['timestamp']}")
    
    if account['history']:
        click.echo("\nHistory:")
        for entry in account['history'][-5:]:  # Show last 5 entries
            click.echo(f"  [{entry['timestamp']}] {entry['action']}")

if __name__ == '__main__':
    cli()