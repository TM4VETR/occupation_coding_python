import os.path
from typing import Dict

from rpy2.robjects import r, globalenv

from utils.data_util import download_data, get_data_dir
from utils.logging_util import logger


def prepare_r_environment() -> None:
    """
    Prepares the R environment.
    """
    r('options(encoding = "UTF-8")')
    r('options(warn = -1)')  # suppress warnings

    ## Install packages
    install_r_packages([
        {"name": "remotes"},
        {"name": "readxl"},
        {"name": "occupationCoding", "github": "malsch/occupationCoding"},
    ])

    # Download required data files
    download_data()

    # Set path to Berufsliste
    data_dir = get_data_dir()
    path_berufsliste = str(os.path.join(data_dir, "Gesamtberufsliste_der_BA.xlsx")).replace("\\", "/")
    globalenv["path_berufsliste"] = path_berufsliste
    r('coding_index_w_codes <- prepare_German_coding_index_Gesamtberufsliste_der_BA(path_berufsliste, count.categories = FALSE)')


def install_r_packages(packages: Dict) -> None:
    """
    Installs the specified R packages (if they are not installed yet).
    """
    for package in packages:
        name = package["name"]
        github = package.get("github")

        if github:
            # install from GitHub only if needed
            r(f'''
            suppressMessages(suppressWarnings({{
                if (!require("{name}", quietly = TRUE)) {{
                    if (!require("remotes", quietly = TRUE))
                        install.packages("remotes", repos="https://cloud.r-project.org")
                    remotes::install_github("{github}", quiet = TRUE, upgrade = "never")
                }}
            }}))
            ''')
        else:
            # install from CRAN only
            r(f'''
            suppressMessages(suppressWarnings({{
                if (!require("{name}", quietly = TRUE))
                    install.packages("{name}", repos="https://cloud.r-project.org")
            }}))
            ''')

    logger.info("Successfully installed R packages!")
