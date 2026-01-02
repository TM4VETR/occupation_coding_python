import sys
from typing import List

import pandas as pd
from rpy2.robjects import r

from utils.dataframe_util import parse_results
from utils.logging_util import logger
from utils.r_util import prepare_r_environment
from utils.text_util import replace_umlauts


prepare_r_environment()


def code_occupations(occupations: List[str]) -> pd.DataFrame:
    """
    Matches all occupations and returns the corresponding codes.

    Args:
        occupations (List[str]): List of job titles to match.

    Returns:
        pandas.DataFrame: DataFrame with matching results.
    """

    # Replace umlauts in job titles
    occupations = [replace_umlauts(o) for o in occupations]

    r('text_input <- c({})'.format(", ".join(f'"{o}"' for o in occupations)))
    r('results <- occupationCoding::predictWithCodingIndex(text_input, coding_index = coding_index_w_codes)')
    results = r('results')

    df_results = parse_results(results)

    return df_results


def retrieve_index():
    """
    Returns the entire coding index including all occupations.

    Returns:
        List[str]: Complete occupation index.
    """
    coding_index_w_codes = r('coding_index_w_codes')
    return coding_index_w_codes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("No input text provided.")
        sys.exit(1)

    input_text = sys.argv[1]

    # Split at spaces, line breaks, commas
    occupations = [o.strip() for o in input_text.replace(",", " ").split() if o.strip()]

    result_df = code_occupations(occupations)

    assert 'pred.code' in result_df.columns, "Expected column 'pred.code' not found in results."
    result_values = result_df['pred.code'].tolist()
    print("\n".join(result_values))
