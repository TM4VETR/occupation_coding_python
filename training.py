import os

from rpy2.robjects import r

from utils.data_util import get_model_dir
from utils.logging_util import logger
from utils.r_util import prepare_r_environment
from utils.text_util import replace_umlauts


prepare_r_environment()


def train_model(
        model_type: str,
        num_allowed_codes: int = 1291,
        n_draws: int = 250,
        check_normality: bool = False,
):
    """
    Train a similarity-based using the occupationCoding R package.

    For details see:
    https://github.com/malsch/occupationCoding/blob/master/README.md

    Args:
        model_type (str): Model to train: "wordwise" or "substring".
        num_allowed_codes (int): Number of allowed codes.
        n_draws (int): Number of draws for the simulation.
        check_normality (bool): Check normality during simulation or not.

    Returns:
        R object: The trained model.
    """
    if not model_type or model_type not in ("wordwise", "substring"):
        raise ValueError("model_type must be either 'wordwise' or 'substring'!")

    # Variable and dataset names in R
    var_name = f"simBasedModel{model_type.capitalize()}"
    data_var = f"surveyCounts{model_type.capitalize()}Similarity"

    # Type-specific parameters
    if model_type == "wordwise":
        dist_control = 'list(method = "osa", weight = c(d = 1, i = 1, s = 1, t = 1))'
        threshold = 'c(max = NA, use = 1)'
    else:  # substring
        dist_control = 'NA'
        threshold = 'NA'

    # Boolean to R literal
    r_check_normality = "TRUE" if check_normality else "FALSE"

    # Construct R command
    r_code = f'''
    {var_name} <- trainSimilarityBasedReasoning2(
        anonymized_data = {data_var},
        num.allowed.codes = {num_allowed_codes},
        coding_index_w_codes = coding_index_w_codes,
        preprocessing = list(stopwords = NULL, stemming = NULL, strPreprocessing = TRUE, removePunct = FALSE),
        dist.type = "{model_type}",
        dist.control = {dist_control},
        threshold = {threshold},
        simulation.control = list(n.draws = {n_draws}, check.normality = {r_check_normality})
    )
    '''

    logger.info(f"Training model '{model_type}'... (This can take some time.)\n Parameters: {num_allowed_codes=}, {n_draws=}, {check_normality=}")

    # Execute R command
    r(r_code)

    logger.info(f"Model '{model_type}' trained successfully.")

    return r(var_name)


def save_model(model, filename: str):
    """
    Save a trained R model object to an .RDS file.

    Args:
        model: R model object
        filename (str): Target filename.

    Returns:
        str: Absolute path to the saved .RDS file.
    """
    model_dir = get_model_dir()

    target_path = os.path.join(model_dir, filename)
    target_path_r = target_path.replace("\\", "/")  # ensure R-compatible path

    # Assign model to R variable and save
    r.assign("model", model)
    r(f'saveRDS(model, file = "{target_path_r}")')

    logger.info(f"Model saved to: {target_path}")
    return os.path.abspath(target_path)


def load_model(filename: str):
    """
    Load a previously saved R model (.RDS file).

    Args:
        filename (str): The filename of the .RDS file (relative or absolute).

    Returns:
        R object: The loaded R model.
    """
    model_dir = get_model_dir()
    full_path = os.path.join(model_dir, filename)
    logger.info(f"Loading model from from: {full_path}")

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Model file not found: {full_path}")

    full_path_r = full_path.replace("\\", "/")  # R-compatible path
    r(f'model <- readRDS("{full_path_r}")')

    return r("model")


def predict(model, occupations):
    """
    Predict occupation codes using a previously trained model.

    Args:
        model: R model object.
        occupations: List[str]: List of job titles.

    Returns:
        R object: Predicted occupational codes.
    """
    if not occupations or len(occupations) == 0:
        logger.info("No occupations provided for prediction.")
        return None

    # Replace umlauts in job titles
    occupations = [replace_umlauts(o) for o in occupations]

    text_input = ", ".join(f'"{o}"' for o in occupations)
    r(f'text_input <- c({text_input})')

    r.assign("model", model)

    # Run prediction
    r('res <- predictSimilarityBasedReasoning(model, text_input)')

    # Retrieve R result
    res = r('res')

    logger.info(f"Successfully predicted {len(occupations)} occupations.")
    return res


if __name__ == "__main__":
    # Example usage:
    wordwise_model = train_model("wordwise")
    substring_model = train_model("substring")

    save_model(wordwise_model, "model_wordwise.RDS")

    model = load_model("model_wordwise.RDS")

    results = predict(model, ["Bürokauffrau", "Maschinenbauingenieur", "Krankenpfleger"])
    print(results)
