import subprocess
import sys


def test_cli_help():
    """Test that the --help option prints usage info."""
    result = subprocess.run(
        [sys.executable, "run.py", "--help"],
        capture_output=True, text=True
    )
    assert "usage" in result.stdout.lower()


def test_cli_missing_argument():
    """Test that missing --occupation returns an error."""
    result = subprocess.run(
        [sys.executable, "run.py"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "usage" in result.stderr.lower() or "error" in result.stderr.lower()
