import pytest
import os
from click.testing import CliRunner
from surrogate_1.cli.wizard import wizard

def test_wizard_cli_flow():
    runner = CliRunner()
    result = runner.invoke(wizard, [])
    
    assert result.exit_code == 0
    assert "Wizard CLI flow" in result.output
    assert os.path.exists("pipeline.yaml")
    
    # Clean up
    os.remove("pipeline.yaml")

def test_wizard_ui_flag():
    runner = CliRunner()
    result = runner.invoke(wizard, ["--ui"])
    
    assert result.exit_code == 0
    assert "Web UI launched" in result.output

def test_wizard_resume():
    test_state = {"source": "http://test.com"}
    temp_file = "test_state.json"
    
    with open(temp_file, 'w') as f:
        json.dump(test_state, f)
    
    runner = CliRunner()
    result = runner.invoke(wizard, ["--resume", temp_file])
    
    assert result.exit_code == 0
    assert "Resuming from" in result.output
    
    # Clean up
    os.remove(temp_file)