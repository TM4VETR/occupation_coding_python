"""
Helper functions to parse the results to a pandas DataFrame.
"""

import pandas as pd
from rpy2.robjects import pandas2ri

# Activate automatic R -> pandas DataFrame conversion
pandas2ri.activate()


def parse_results(results) -> pd.DataFrame:
    """
    Parses the R results into a pandas DataFrame.

    Args:
        results: R object containing the results.

    Returns:
        pd.DataFrame: Parsed results as a pandas DataFrame.
    """
    df = pandas2ri.rpy2py(results)
    return df
