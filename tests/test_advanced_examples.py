"""
Test to ensure that all advances examples from the README.md can be executed without errors.
"""
import os
import pytest
import subprocess
import sys

from occupation_coding import code_occupations


@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS", "").lower() == "true",
    reason="Skipped in CI because it requires an R installation and local data."
)
def test_single_occupation_subprocess():
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


@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS", "").lower() == "true",
    reason="Skipped in CI because it requires an R installation and local data."
)
def test_single_occupation():
    """Ensure the CLI example in the README executes without errors."""
    df_results = code_occupations(occupations=["Bürokauffrau"])

    assert "Buerokauffrau" in df_results["ans"].values
    assert "71402" in df_results["pred.code"].values


@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS", "").lower() == "true",
    reason="Skipped in CI because it requires an R installation and local data."
)
def test_multiple_occupations():
    from occupation_coding import code_occupations # pylint: disable=import-outside-toplevel

    """Ensure code_occupations() example runs."""
    occupations = [
        "Bürokauffrau",
        "Stadtjugendpfleger",
        "Erzieherhelfer im Lehrlingswohnheim.",
        "Mitarbeit bei einer Filmproduktion",
        "Abschleifer",
    ]

    try:
        results = code_occupations(occupations=occupations)
    except Exception as e:
        pytest.fail(f"code_occupations() example failed: {e}")

    print(results)

    assert results is not None
    assert isinstance(results, (list, dict, object))


@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS", "").lower() == "true",
    reason="Skipped in CI because it requires an R installation and local data."
)
def test_retrieve_index():
    """Ensure retrieve_index() example runs."""
    from occupation_coding import retrieve_index # pylint: disable=import-outside-toplevel

    try:
        index = retrieve_index()
    except Exception as e:
        pytest.fail(f"retrieve_index() example failed: {e}")

    print(index)

    assert index is not None
