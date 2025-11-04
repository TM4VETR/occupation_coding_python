"""
Test to ensure that all advances examples from the README.md can be executed without errors.
"""
import pytest

from occupation_coding import code_occupations, retrieve_index


def test_multiple_occupations():
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


def test_retrieve_index():
    """Ensure retrieve_index() example runs."""
    try:
        index = retrieve_index()
    except Exception as e:
        pytest.fail(f"retrieve_index() example failed: {e}")

    print(index)

    assert index is not None
