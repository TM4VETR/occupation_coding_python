import os
import requests

from dotenv import load_dotenv

from utils.logging_util import logger, PROJECT_DIR


load_dotenv()


FILES = {
    "Gesamtberufsliste_der_BA.xlsx": "https://rest.arbeitsagentur.de/infosysbub/download-portal-rest/ct/dkz-downloads/Gesamtberufsliste_der_BA.xlsx"
}



def get_data_dir() -> str:
    """
    Returns the absolute path to the data directory.
    """

    default_dir = os.path.join(PROJECT_DIR, "data")
    return get_dir("DATA_DIR", default_dir)



def get_model_dir() -> str:
    """
    Returns the absolute path to the model directory.
    """
    default_dir = os.path.join(PROJECT_DIR, "model")
    return get_dir("MODEL_DIR", default_dir)





def get_dir(env_variable: str, default_dir: str) -> str:
    """
    Tries to get a directory path from an environment variable; returns a default path otherwise.

    :param env_variable: The environment variable.
    :param default_dir: The default directory.
    :return: Absolute path to the directory.
    """
    dir_name = os.getenv(env_variable)

    if dir_name is None:
        logger.debug(f"Environment variable {env_variable} is not set. Using default directory: '{default_dir}'")
        dir_name = default_dir

    os.makedirs(dir_name, exist_ok=True)
    return str(dir_name).replace("\\", "/")


def download_data() -> list[str]:
    """
    Downloads all files defined in FILES if they do not yet exist.

    Returns:
        list[str]: List of absolute paths to the downloaded files.
    """
    data_dir = get_data_dir()
    logger.info(f"Downloading required files to {data_dir}...")

    downloaded_paths = []

    for filename, url in FILES.items():
        target_path = os.path.join(data_dir, filename)

        if os.path.exists(target_path):
            logger.debug(f"File already exists: {target_path}")
            downloaded_paths.append(os.path.abspath(target_path))
            continue

        logger.info(f"Downloading {filename} ...")
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to download {filename} (HTTP {response.status_code})")

        with open(target_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Download complete: {target_path}")
        downloaded_paths.append(os.path.abspath(target_path))

    logger.info("Successfully downloaded all files.")
    return downloaded_paths


if __name__ == "__main__":
    download_data()
