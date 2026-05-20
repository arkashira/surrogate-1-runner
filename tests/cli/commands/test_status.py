import pytest
from click.testing import CliRunner
from surrogate1.cli.commands.status import status

def test_status_command():
    runner = CliRunner()
    result = runner.invoke(status)
    assert result.exit_code == 0
    assert "status" in result.output
    assert "shift_percentage" in result.output
    assert "health" in result.output