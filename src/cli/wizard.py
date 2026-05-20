import click
import webbrowser
from pathlib import Path
import json
from datetime import datetime

@click.command()
@click.option('--ui', is_flag=True, help='Launch web-based configuration UI')
@click.option('--resume', type=click.Path(), help='Resume from existing state file')
def wizard(ui, resume):
    """Interactive pipeline configuration wizard"""
    state = {}
    
    if resume:
        with open(resume, 'r') as f:
            state = json.load(f)
    
    if ui:
        # Generate temporary state file with timestamp
        temp_state = Path(f"/tmp/surrogate-wizard-{datetime.now().timestamp()}.json")
        with open(temp_state, 'w') as f:
            json.dump(state, f)
        
        # Launch web UI with state file as query param
        webbrowser.open(f"http://localhost:3000/wizard?state={temp_state.name}")
        click.echo("Web UI launched at http://localhost:3000/wizard")
        return
    
    # CLI-only flow (placeholder)
    click.echo("Wizard CLI flow (basic implementation):")
    source = click.prompt('Source URL', default='https://example.com/data')
    format = click.prompt('Format', default='json')
    dest = click_prompt('Destination path', default='./pipeline.yaml')
    
    # Write minimal pipeline config
    with open(dest, 'w') as f:
        f.write(f"""pipeline:
  source: {source}
  format: {format}
  destination: {dest}
""")
    
    click.echo(f"Pipeline config written to {dest}")