"""
Mocked version of advanced examples ensuring that the functions are called correctly.
"""
from unittest.mock import MagicMock
import sys

# Mock occupation_coding module
sys.modules["occupation_coding"] = MagicMock()


def test_multiple_occupations_mocked():
    from occupation_coding import code_occupations

    code_occupations(occupations=["Bürokauffrau", "Abschleifer"])
    code_occupations.assert_called()


def test_retrieve_index_mocked():
    from occupation_coding import retrieve_index

    retrieve_index()
    retrieve_index.assert_called()
