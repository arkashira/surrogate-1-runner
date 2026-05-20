import subprocess

def test_cli_flags():
    # Test specifying diff source, coverage file, and output paths
    result = subprocess.run(
        [
            "python",
            "main.py",
            "--diff-source=source.txt",
            "--coverage-file=coverage.txt",
            "--output-path=output.txt"
        ],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Processed diff source: source.txt" in result.stdout
    assert "Used coverage file: coverage.txt" in result.stdout
    assert "Output written to: output.txt" in result.stdout