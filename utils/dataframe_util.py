"""
Helper functions to parse the results to a pandas DataFrame.
"""

import pandas as pd

from rpy2.robjects import conversion, default_converter
from rpy2.robjects import pandas2ri


# Build a pandas-aware converter once
_PANDAS_CONVERTER = default_converter + pandas2ri.converter


def parse_results(results) -> pd.DataFrame:
    """
    Parses the R results into a pandas DataFrame.

    Args:
        results: R object containing the results.

    Returns:
        pd.DataFrame: Parsed results as a pandas DataFrame.
    """
    with conversion.localconverter(_PANDAS_CONVERTER):
        df = conversion.rpy2py(results)

    # Safety: ensure we really return a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    return df
