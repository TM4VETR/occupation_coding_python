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


def test_cli_single_occupation():
    """Ensure the CLI example in the README executes without errors."""
    result = subprocess.run(
        [sys.executable, "run.py", "--occupation", "Bürokauffrau"],
        capture_output=True,
        text=True,
        timeout=60
    )

    print(result)

    assert result.returncode == 0, f"CLI failed: {result.stderr or result.stdout}"
    assert "Buerokauffrau" in result.stdout