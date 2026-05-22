import pathlib
import tempfile
import sys

import pytest

# Import the CLI entry point and the format command's run function.
from src.cli import main as cli_main
from src.cli.format import run as format_run, build_parser as format_build_parser


def test_format_success(tmp_path: pathlib.Path, capsys):
    # Create a dummy Python file.
    repo = tmp_path / "repo"
    repo.mkdir()
    dummy_file = repo / "example.py"
    dummy_file.write_text("print('hello')\n")

    # Build a minimal parser that only knows the `format` command.
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    format_build_parser(subparsers)

    # Simulate CLI arguments.
    args = parser.parse_args(["format", "--repo", str(repo)])
    # Run the command.
    exit_code = format_run(args)

    # Verify exit code and output.
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Formatted 1 file(s)." in captured.out

    # Ensure the file still exists and content is unchanged.
    assert dummy_file.read_text() == "print('hello')\n"


def test_format_invalid_repo(tmp_path: pathlib.Path, capsys):
    # Provide a non‑existent path.
    non_existent = tmp_path / "does_not_exist"

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    format_build_parser(subparsers)

    args = parser.parse_args(["format", "--repo", str(non_existent)])
    exit_code = format_run(args)

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "does not exist or is not a directory" in captured.err